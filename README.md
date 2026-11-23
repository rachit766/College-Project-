# PhishGuard AI — Streamlit App

## Files
- `streamlit_app.py`: App interface
- `requirements.txt`: Required packages
- Put your trained model pickle file in this folder, named `best_model.pkl`, `phishing_model.pkl`, or `model.pkl`.

## Run
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Important
This app expects the model to accept the same feature values and feature order as in training. The UCI phishing dataset commonly uses values -1, 0 and 1. The app exposes the model's feature names automatically when available.
