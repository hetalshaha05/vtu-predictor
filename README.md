\# 📚 VTU Predictor

**Predict likely exam questions from previous year papers using pattern analysis.**

A Streamlit web app that analyses VTU previous year question papers, finds repeated questions across years, and ranks them by how likely they are to appear again — weighted by marks and confidence.

---

## 🎯 The Problem

Every VTU student faces the same question the night before an exam: **what do I study?**

There are 5 modules, 40+ topics, and no way to know which questions actually matter. Students end up reading everything — or nothing. Meanwhile, a huge portion of exam questions repeat every year, and nobody is measuring it.

## 💡 The Solution

**VTU Predictor** quantifies question repetition. Drop in 4 previous year papers, and it shows you:

- **Which questions keep coming back** — ranked by repetition rate
- **How much they're worth** — weighted by marks
- **How confident we are** — based on text similarity within the cluster
- **When they appeared** — year-wise timeline per question

Result: a **prioritized study plan** instead of a panic read.

---

## 🚀 Live Demo

**Deployed on AWS EC2:** `http://YOUR_EC2_PUBLIC_IP:8501`

*(Replace with your actual EC2 URL after deployment.)*

---

## ✨ Features

- **📊 Three-tier categorization**
  - 🔥 Mostly Predictable (appeared in 3–4 papers)
  - ⚡ Moderately Repeated (appeared in 2 papers)
  - 📌 Less Repeated (appeared in 1 paper)

- **🎯 Weighted scoring**
  - Questions are ranked by `repetition_rate × (1 + marks / 25)`
  - High-marks repeated questions rise to the top

- **🧠 Confidence indicator**
  - High / Medium / Low based on how similar clustered questions are
  - Tells students how reliable each prediction is

- **📈 Year-wise analysis**
  - See exactly which papers each question appeared in
  - Spot questions that are "overdue" for a comeback

- **🎨 Clean, calm UI**
  - Green + beige palette designed for late-night study sessions
  - Animated SVG student keeps the vibe warm and academic

- **👤 Guest mode**
  - No signup required — explore as guest
  - Optional sign-in to personalize dashboard

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11 |
| NLP | scikit-learn (TF-IDF + cosine similarity) |
| Clustering | Agglomerative Clustering |
| Frontend | Streamlit |
| Deployment | AWS EC2 (Ubuntu 22.04, t3.micro) |
| Data storage | JSON files (no database needed) |

**No external APIs. No LLM calls. 100% local and free to run.**

---

## 🧠 How It Works

### 1. Parsing
Each TXT file (converted from a PDF) is parsed with regex to extract:
- Question number and sub-part (`1. a)`, `Q2 b)`, etc.)
- Question text
- Marks (from trailing `|N` or `(N marks)`)

### 2. Similarity Detection
All questions are vectorized using **TF-IDF** with bigrams, then compared pairwise using **cosine similarity**.

### 3. Clustering
Questions with ≥ 75% similarity are grouped using **Agglomerative Clustering**. Each cluster represents a "concept" that may have been asked in multiple years with slightly different wording.

### 4. Scoring
For each cluster:

```
repetition_rate = (papers_appeared / total_papers) × 100
weighted_score  = repetition_rate × (1 + marks / 25)
confidence      = High / Medium / Low  (based on avg cluster similarity)
```

### 5. Output
Results are saved to `predictions.json` and rendered in a sortable, scannable HTML table in the UI.

---

## 📁 Project Structure

```
vtu-predictor/
├── app.py                  # Backend: parses papers → clusters → predictions.json
├── ui.py                   # Frontend: 4-page Streamlit app
├── predictions.json        # Generated predictions (auto-created)
├── requirements.txt
├── README.md
├── .gitignore
└── papers/
    ├── jan2024.txt
    ├── june2024.txt
    ├── jan2026.txt
    └── june2025.txt
```

---

## 🚀 Running Locally

### Prerequisites
- Python 3.11 (⚠️ do **not** use 3.12+ — `scikit-learn` breaks)
- pip

### Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/vtu-predictor.git
cd vtu-predictor

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate predictions from papers
python app.py

# Launch the app
streamlit run ui.py
```

The app opens at `http://localhost:8501`.

---

## ☁️ Deploying to AWS EC2

```bash
# On the EC2 instance (Ubuntu 22.04)
sudo apt update
sudo apt install python3-pip python3-venv git -y

git clone https://github.com/YOUR_USERNAME/vtu-predictor.git
cd vtu-predictor

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python app.py

nohup streamlit run ui.py --server.port 8501 --server.address 0.0.0.0 &
```

**Security group must allow:**
- SSH (port 22) — your IP
- Custom TCP (port 8501) — `0.0.0.0/0`

Access at `http://<ec2-public-ip>:8501`.

---

## 📥 Adding Your Own Papers

Want to add a new subject? No code changes needed.

1. Create a new folder: `papers/BCS401/`
2. Drop your TXT files inside (one per paper)
3. Run `python app.py`
4. Add the subject to the dropdown in `ui.py`

The parser auto-detects every `.txt` in the folder.

### Format for TXT files
```
1. a) Discuss the ACID properties of a database transaction. |6
2. b) Explain normalization with examples. (8 marks)
```

Marks can be at the end as `|6` or `(6 marks)` — either works.

---

## 📊 Sample Output

```
🔮 TOP 10 MOST PREDICTABLE QUESTIONS (sorted by weighted score)
======================================================================

[Score 132.0] 100.0% repeat | 8 marks | High confidence | 4/4 papers
  → Explain dynamic programming with an example...

[Score 105.0] 75.0% repeat | 10 marks | High confidence | 3/4 papers
  → Discuss the ACID properties of a database transaction...

[Score 90.0] 75.0% repeat | 6 marks | Medium confidence | 3/4 papers
  → Compare BFS and DFS with examples...
```

---

## 🎯 Roadmap

- [x] Multi-year repetition analysis
- [x] Marks-weighted scoring
- [x] Confidence indicator
- [ ] Multi-subject support
- [ ] Unit/module-wise filtering
- [ ] User-uploaded papers (crowd-sourced)
- [ ] College-wise analytics dashboard

---

## 🤝 Contributing

Built for a hackathon, but the concept has legs. If you're a VTU student and want to help expand this to more subjects, open an issue or PR.

---

## 📄 License

MIT — use it, fork it, improve it.

---

## 👤 Author

**Your Name**
- GitHub: [@hetalshaha05](https://github.com/hetalshaha05)
- USN: 2JI@4CS044
- Branch: CSE, Semester 4

---

*Built with Python, TF-IDF, and late-night coffee.* ☕