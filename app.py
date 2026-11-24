from pathlib import Path

import joblib
import base64

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)

model = joblib.load(BASE_DIR / 'model' / 'diabetes_tree.joblib')
feature_names = joblib.load(BASE_DIR / 'model' / 'feature_names.json')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    # 1x1 transparent GIF — keeps the browser quiet without a real icon file
    gif = base64.b64decode('R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7')
    return app.response_class(gif, mimetype='image/gif')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(silent=True) or {}

    try:
        row = {
            'age': float(data['age']),
            'hypertension': int(data['hypertension']),
            'heart_disease': int(data['heart_disease']),
            'bmi': float(data['bmi']),
            'HbA1c_level': float(data['hba1c']),
            'blood_glucose_level': float(data['glucose']),
        }
    except (KeyError, TypeError, ValueError):
        return jsonify({'error': 'Please fill in every field with a valid number.'}), 400

    gender = str(data.get('gender', '')).lower()
    smoking = str(data.get('smoking', ''))

    # smoking_history_* come from pd.get_dummies(drop_first=True),
    # so 'ever', 'No Info' and 'Female' are the reference categories (all flags zero).
    gender_flags = {
        'gender_Male': 1 if gender == 'male' else 0,
        'gender_Other': 1 if gender == 'other' else 0,
    }
    smoking_flags = {
        'smoking_history_current': 1 if smoking == 'current' else 0,
        'smoking_history_ever': 1 if smoking == 'ever' else 0,
        'smoking_history_former': 1 if smoking == 'former' else 0,
        'smoking_history_never': 1 if smoking == 'never' else 0,
        'smoking_history_not current': 1 if smoking == 'not current' else 0,
    }

    features = {**row, **gender_flags, **smoking_flags}
    try:
        X = [[features[name] for name in feature_names]]
    except KeyError as missing:
        return jsonify({'error': f'Unknown feature: {missing}'}), 500

    pred = int(model.predict(X)[0])
    proba = float(model.predict_proba(X)[0][1])

    return jsonify({
        'prediction': 'Diabetic' if pred == 1 else 'Not Diabetic',
        'is_diabetic': pred,
        'probability': round(proba, 4),
    })


if __name__ == '__main__':
    app.run(debug=True)
