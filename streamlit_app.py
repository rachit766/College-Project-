
import streamlit as st
import pandas as pd
import os
import pickle
import joblib

st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #142b49, #07111f 55%, #050914);
    color: #eaf2ff;
}
[data-testid="stSidebar"] {
    background: #0b1424;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3, p, label {
    color: #eaf2ff;
}
div[data-testid="stMetric"] {
    background: #101e32;
    border: 1px solid #243a56;
    padding: 18px;
    border-radius: 15px;
}
.stButton > button, .stFormSubmitButton > button {
    border-radius: 12px;
    height: 3rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🛡️ PhishGuard AI")
st.markdown("### Intelligent Phishing Website Detection")
st.caption("Machine Learning powered website security assessment")

st.markdown("""
This dashboard uses your trained machine learning model to
classify website feature patterns as potentially phishing or legitimate.
""")

with st.sidebar:
    st.markdown("# 🛡️ PhishGuard AI")
    st.divider()
    st.markdown("### About")
    st.write("Phishing Website Detection using Machine Learning.")
    st.write("Model: Trained classification model")
    st.divider()
    st.warning(
        "This tool is a machine-learning demonstration. "
        "A prediction does not guarantee website safety."
    )

MODEL_OPTIONS = [
    "phishing_detection_model.pkl",
    "best_model.pkl",
    "phishing_model.pkl",
    "model.pkl"
]

model = None
model_path = None
load_error = None

for path in MODEL_OPTIONS:
    if os.path.isfile(path):
        model_path = path
        break

if model_path:
    try:
        model = joblib.load(model_path)
    except Exception as e1:
        try:
            with open(model_path, "rb") as f:
                model = pickle.load(f)
        except Exception as e2:
            load_error = f"Joblib error: {e1}\nPickle error: {e2}"
else:
    load_error = "No model file found."

if model is None:
    st.error("## Model Loading Failed")

    st.write(
        "The model file was not found or could not be loaded."
    )

    st.markdown("### Required files")
    st.code(
        "streamlit_app.py\n"
        "phishing_detection_model.pkl\n"
        "requirements.txt"
    )

    if model_path:
        st.info(f"Model file detected: {model_path}")
        st.code(str(load_error))

    st.markdown("### How to save your model again")

    st.code(
        "import joblib\n"
        "joblib.dump(best_model, "
        "'phishing_detection_model.pkl')",
        language="python"
    )

    st.stop()

st.success("Model loaded successfully!")

features = list(
    getattr(model, "feature_names_in_", [])
)

feature_count = getattr(
    model, "n_features_in_", None
)

if not features and feature_count:
    features = [
        f"Feature_{i+1}"
        for i in range(feature_count)
    ]

if not features:
    st.error("Could not identify model features.")
    st.stop()

st.divider()

st.markdown("## 🔍 Website Feature Analysis")
st.write(
    "Enter the feature values used by your trained model."
)

with st.form("prediction_form"):

    values = {}
    cols = st.columns(3)

    for i, feature in enumerate(features):

        with cols[i % 3]:

            values[feature] = st.selectbox(
                feature.replace("_", " ").title(),
                options=[-1, 0, 1],
                index=1,
                key=f"feature_{i}",
                help="Choose the feature value according to its dataset definition."
            )

    submitted = st.form_submit_button(
        "🔎 Analyze Website",
        use_container_width=True
    )

if submitted:

    input_df = pd.DataFrame(
        [values],
        columns=features
    )

    try:

        prediction = model.predict(input_df)[0]

        st.divider()
        st.markdown("## 📊 Analysis Result")

        col1, col2 = st.columns(2)

        if prediction == -1:

            with col1:
                st.metric("Security Assessment", "Phishing")

            with col2:
                st.metric("Predicted Class", "-1")

            st.error(
                "🚨 The model classified these feature values "
                "as potentially phishing."
            )

        elif prediction == 1:

            with col1:
                st.metric("Security Assessment", "Legitimate")

            with col2:
                st.metric("Predicted Class", "1")

            st.success(
                "✅ The model classified these feature values "
                "as likely legitimate."
            )

        else:

            st.warning(
                f"Model prediction: {prediction}"
            )

        if hasattr(model, "predict_proba"):

            try:

                probabilities = model.predict_proba(input_df)[0]

                probability_df = pd.DataFrame(
                    {
                        "Class": [
                            str(c)
                            for c in model.classes_
                        ],
                        "Probability": probabilities
                    }
                )

                st.markdown("### 📈 Model Probability")

                st.bar_chart(
                    probability_df.set_index("Class")
                )

                st.dataframe(
                    probability_df,
                    use_container_width=True,
                    hide_index=True
                )

            except Exception:
                st.info(
                    "Probability scores are not available."
                )

        st.caption(
            "Prediction is based on the supplied feature values "
            "and is not a guarantee of website safety."
        )

    except Exception as e:

        st.error(f"Prediction error: {e}")

st.divider()

st.markdown("### ⚠️ Security Disclaimer")

st.write(
    "Do not rely exclusively on this prediction to visit websites. "
    "Never enter sensitive credentials on unfamiliar websites."
)

st.caption("PhishGuard AI | Machine Learning Project")
