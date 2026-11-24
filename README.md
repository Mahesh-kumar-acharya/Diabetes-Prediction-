# Diabetes Risk Assessment

> A decision-tree classifier that predicts diabetes risk from eight clinical features — wrapped in a deliberately quiet, editorial Flask frontend.

Not a dashboard. Not a gradient. A form, a model, and a verdict.

---

## What this is

You enter a patient's vitals — age, BMI, HbA1c, blood glucose, smoking history, and whether they carry hypertension or heart disease. A decision tree, trained on **100,000 patient records**, tells you what it thinks.

The whole stack is three files of frontend, one file of Flask, and one pickled tree. No build step, no JS framework, no chart library pretending to be the product.

---

## The model

|                 |                                                                                   |
| --------------- | --------------------------------------------------------------------------------- |
| Algorithm       | `DecisionTreeClassifier` (scikit-learn)                                           |
| Training data   | 100,000 rows, stratified 80/20 split                                              |
| Class weighting | `balanced` — the dataset is ~91% non-diabetic, so accuracy alone would lie to you |
| Train accuracy  | 99.9%                                                                             |
| Test accuracy   | 95.5%                                                                             |

**A note on honesty:** the gap between train and test accuracy is the tree overfitting — that's what unrestricted decision trees do, and the README won't pretend otherwise. For a production-grade model you'd prune (`max_depth`, `min_samples_leaf`) or reach for a random forest / gradient boosting. This tree is the honest baseline your notebook asked for.

Because of the class imbalance, the frontend reports **probability and class**, not just a binary yes/no.

### Features used

`gender` · `age` · `hypertension` · `heart_disease` · `smoking_history` · `bmi` · `HbA1c_level` · `blood_glucose_level`

Categorical columns are one-hot encoded (`pd.get_dummies` with `drop_first=True`) — the Flask app reconstructs that exact encoding at inference time so the model sees the same shape it was trained on.

---

## The design

Three colors. That's it.

| Role       | Color                  |
| ---------- | ---------------------- |
| Background | `#FAF9F6` — warm paper |
| Text       | `#1C1C1A` — ink        |
| Accent     | `#A3482A` — rust       |

Serif body (Georgia) against sans labels (Helvetica Neue), hairline rules dividing the form into three numbered sections, underline-style inputs, and toggle switches for the yes/no conditions. The verdict page is one large word, a probability, and a footnote reminding you that a statistical model is not a physician.

No gradients. No dark mode. No neon. If it looks like a print journal, that's the point.

---

## Run it

```bash
git clone https://github.com/Mahesh-kumar-acharya/Diabetes-Prediction-
cd Diabetes-Prediction

pip install -r requirements.txt

# (re)train the model — saves to model/diabetes_tree.joblib
python train_save.py

# start the server (Flask dev server)
python wsgi.py

# ...or production (Render, etc.) — gunicorn reads wsgi:app
gunicorn wsgi:app --bind 0.0.0.0:$PORT
```

> **Note for Windows:** `gunicorn` relies on Unix-only modules (`fcntl`) and won't run on Windows locally — use `python wsgi.py` there. On Render (Linux), `gunicorn wsgi:app --bind 0.0.0.0:$PORT` is the way.

---

## Project structure

```
├── app.py                          # Flask server + /predict endpoint
├── train_save.py                   # trains the tree, saves model artifacts
├── diabetes_prediction_dataset.csv # Kaggle dataset (synthetic, no PII)
├── model/
│   ├── diabetes_tree.joblib        # trained classifier
│   └── feature_names.json          # feature order the model expects
├── templates/
│   └── index.html                  # the form
├── static/
│   ├── style.css                   # three colors, hairlines, whitespace
│   └── script.js                   # form logic, fetch call, result render
└── notebook/
    └── EDA-FE.ipynb                # EDA, feature engineering, model training
```

---

## Dataset

Sourced from the Kaggle _Diabetes prediction dataset_ — a synthetic dataset of 100,000 rows built for exactly this kind of demonstration. It contains no real patient identifiers or PHI, so it's safe to distribute. The "No Info" smoking category (~35k rows) is treated as its own category rather than imputed.

---

## Known limitations

- The tree is overfit (99.9% train / 95.5% test) — prune it for production use.
- Leaf probabilities are near-binary (0 or 1) for the same reason; don't read the percentage as calibrated risk.
- No SHAP-style feature explanation in the UI — the model knows _why_, the form doesn't show you yet.
- Not a medical device. Obviously.

---

## License

MIT — do what you want, credit is welcome.
