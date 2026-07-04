import re

import joblib
from django.conf import settings
from django.shortcuts import render

# --- Load the trained model + vectorizer once, when the server starts ---
# (not on every request, since loading from disk is relatively slow)
_MODEL_PATH = settings.MODELS_DIR / "spam_classifier.joblib"
_VECTORIZER_PATH = settings.MODELS_DIR / "tfidf_vectorizer.joblib"

model = joblib.load(_MODEL_PATH)
vectorizer = joblib.load(_VECTORIZER_PATH)


# --- Same cleaning function used in the notebook ---
def clean_text(text):
    text = text.lower()
    text = re.sub(r"(https?://\S+|www\.\S+)", " ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def predict_message(text):
    cleaned = clean_text(text)
    vectorized = vectorizer.transform([cleaned])
    pred = model.predict(vectorized)[0]

    confidence = None
    if hasattr(model, "decision_function"):
        score = model.decision_function(vectorized)[0]
        confidence = round(float(score), 2)

    return ("SPAM" if pred == 1 else "HAM"), confidence


def index(request):
    label = None
    confidence = None
    message = ""

    if request.method == "POST":
        message = request.POST.get("message", "")
        if message.strip():
            label, confidence = predict_message(message)

    return render(request, "detector/index.html", {
        "label": label,
        "confidence": confidence,
        "message": message,
    })
