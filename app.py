import re
import glob
import os
import json
from collections import defaultdict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering


QUESTION_START = re.compile(
    r'^\s*(?:Q\.?\s*)?(\d{1,2})\s*[\.\)]?\s*(?:([a-z])\s*[\.\)])?\s*',
    re.IGNORECASE
)
MARKS = re.compile(r'\(?(\d{1,2})\s*marks?\)?', re.IGNORECASE)
PIPE_MARKS = re.compile(r'\|\s*(\d{1,2})\s*$')


def clean_question_text(text):
    text = re.sub(r'^[a-z]\s*[\|\)\.:]\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\|\s*\d{1,2}\s*$', '', text).strip()
    text = text.lstrip('|').strip()
    text = re.sub(r'\s*\|\s*', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def infer_module(qno, text):
    m = re.search(r'\bmodule\s*[-:]?\s*(\d)', text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    try:
        n = int(qno)
        return min(5, (n - 1) // 2 + 1)
    except (ValueError, TypeError):
        return 1


def parse_txt(filepath, label):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    questions = []
    current = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        m = QUESTION_START.match(line)
        if m:
            if current:
                questions.append(current)
            raw_text = line[m.end():].strip()

            detected_marks = None
            pipe_match = PIPE_MARKS.search(raw_text)
            if pipe_match:
                detected_marks = int(pipe_match.group(1))
                raw_text = raw_text[:pipe_match.start()].strip()
            else:
                paren_match = MARKS.search(raw_text)
                if paren_match:
                    detected_marks = int(paren_match.group(1))
                    raw_text = raw_text[:paren_match.start()].strip()

            raw_text = clean_question_text(raw_text)
            current = {
                'paper': label,
                'qno': m.group(1),
                'sub': m.group(2) or '',
                'text': raw_text,
                'marks': detected_marks
            }
        else:
            if current:
                stripped = line.strip()
                pipe_only = re.match(r'^\|\s*(\d{1,2})\s*$', stripped)
                marks_only = re.match(r'^\(?(\d{1,2})\s*marks?\)?$', stripped, re.IGNORECASE)
                if pipe_only and not current.get('marks'):
                    current['marks'] = int(pipe_only.group(1))
                    continue
                if marks_only and not current.get('marks'):
                    current['marks'] = int(marks_only.group(1))
                    continue
                current['text'] += ' ' + line

    if current:
        questions.append(current)

    for q in questions:
        if not q.get('marks'):
            mm = MARKS.search(q['text'])
            if mm:
                q['marks'] = int(mm.group(1))
                q['text'] = MARKS.sub('', q['text']).strip()
            else:
                pm = PIPE_MARKS.search(q['text'])
                if pm:
                    q['marks'] = int(pm.group(1))
                    q['text'] = q['text'][:pm.start()].strip()
        q['text'] = clean_question_text(q['text'])

    questions = [q for q in questions if q['text']]

    for q in questions:
        q['module'] = infer_module(q['qno'], q['text'])

    return questions


def build_predictions(paper_files):
    all_qs = []
    for fp in paper_files:
        label = os.path.splitext(os.path.basename(fp))[0]
        all_qs.extend(parse_txt(fp, label))

    if not all_qs:
        return []

    texts = [q['text'] for q in all_qs]
    vec = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    X = vec.fit_transform(texts)
    sim = cosine_similarity(X)

    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=0.25,
        metric='precomputed',
        linkage='average'
    )
    labels = clustering.fit_predict(1 - sim)

    clusters = defaultdict(list)
    for i, lab in enumerate(labels):
        clusters[lab].append(i)

    total_papers = len(paper_files)

    results = []
    for lab, idxs in clusters.items():
        papers = set(all_qs[i]['paper'] for i in idxs)
        rate = len(papers) / total_papers * 100

        marks_values = [all_qs[i]['marks'] for i in idxs if all_qs[i]['marks']]
        if marks_values:
            common_marks = max(set(marks_values), key=marks_values.count)
            marks_min = min(marks_values)
            marks_max = max(marks_values)
            marks_display = f"{marks_min}-{marks_max}" if marks_min != marks_max else str(common_marks)
            marks_value = common_marks
        else:
            common_marks = None
            marks_display = None
            marks_value = 5

        weighted = round(rate * (1 + marks_value / 25), 1)

        if len(idxs) > 1:
            cluster_sims = [sim[i][j] for i in idxs for j in idxs if i < j]
            avg_sim = sum(cluster_sims) / len(cluster_sims)
        else:
            avg_sim = 1.0

        if avg_sim >= 0.9:
            confidence = "High"
        elif avg_sim >= 0.8:
            confidence = "Medium"
        else:
            confidence = "Low"

        modules = [all_qs[i].get('module', 1) for i in idxs]
        common_module = max(set(modules), key=modules.count) if modules else 1

        results.append({
            'question': all_qs[idxs[0]]['text'],
            'papers': sorted(papers),
            'times_appeared': len(papers),
            'repetition_rate': round(rate, 1),
            'marks': marks_display,
            'marks_common': common_marks,
            'weighted_score': weighted,
            'confidence': confidence,
            'avg_similarity': round(avg_sim, 2),
            'module': common_module
        })

    results.sort(key=lambda x: (x['weighted_score'], x['times_appeared']), reverse=True)
    return results


def main():
    os.makedirs('predictions', exist_ok=True)

    if not os.path.isdir('papers'):
        print("❌ No 'papers/' folder found.")
        return

    paper_files = sorted(glob.glob('papers/*.txt'))
    if not paper_files:
        nested = glob.glob('papers/*/*.txt')
        if nested:
            paper_files = sorted(nested)
        else:
            print("❌ No .txt files in papers/")
            return

    print(f"📄 Found {len(paper_files)} paper(s):")
    for fp in paper_files:
        print(f"   • {os.path.basename(fp)}")

    predictions = build_predictions(paper_files)

    if not predictions:
        print("⚠️  No questions parsed.")
        return

    with open('predictions.json', 'w', encoding='utf-8') as f:
        json.dump(predictions, f, indent=2, ensure_ascii=False)
    with open('predictions/BCS403.json', 'w', encoding='utf-8') as f:
        json.dump(predictions, f, indent=2, ensure_ascii=False)

    total_papers = len(paper_files)
    repeats = [r for r in predictions if r['times_appeared'] >= 2]
    with_marks = [r for r in predictions if r['marks']]

    print(f"\n📊 Total unique questions: {len(predictions)}")
    print(f"🔁 Repeated questions: {len(repeats)}")
    print(f"🏷️  Questions with marks: {len(with_marks)}/{len(predictions)}")
    print(f"💾 Saved to predictions.json AND predictions/BCS403.json")

    print("\n" + "=" * 70)
    print("🔮 TOP 10 MOST PREDICTABLE QUESTIONS")
    print("=" * 70)
    for r in predictions[:10]:
        marks_str = f"{r['marks']} marks" if r['marks'] else "marks N/A"
        print(f"\n[Score {r['weighted_score']}] {r['repetition_rate']}% | "
              f"{marks_str} | M{r['module']} | {r['confidence']} | "
              f"{r['times_appeared']}/{total_papers} papers")
        print(f"  → {r['question'][:90]}...")


if __name__ == "__main__":
    main()