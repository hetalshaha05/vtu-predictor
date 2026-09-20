# 📚 VTU Predictor

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
- Question number and sub-part (`1. a)`, `Q2 b)`, etc.
- Question text
- Marks (from trailing `|N` or `(N marks)`)

### 2. Similarity Detection
All questions are vectorized using **TF-IDF** with bigrams, then compared pairwise using **cosine similarity**.

### 3. Clustering
Questions with ≥ 75% similarity are grouped using **Agglomerative Clustering**. Each cluster represents a "concept" that may have been asked in multiple years with slightly different wording.

### 4. Scoring
For each cluster:
