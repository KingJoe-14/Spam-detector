# Spam Detector — Django Web App

A simple Django app wrapping the spam classifier you trained in the notebook.
Paste a message into a text box, get an instant SPAM / HAM prediction.

## Project structure
```
spamdetector/
├── manage.py
├── requirements.txt
├── spam_classifier.joblib      ← copy this in from your notebook (see Setup)
├── tfidf_vectorizer.joblib     ← copy this in from your notebook (see Setup)
├── spamdetector/                # project settings
│   ├── settings.py
│   └── urls.py
└── detector/                    # the app
    ├── views.py                 # loads the model, runs predictions
    ├── urls.py
    └── templates/detector/index.html
```

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Copy your two trained model files into this folder (the same folder as
   `manage.py`):
   - `spam_classifier.joblib`
   - `tfidf_vectorizer.joblib`

   These were created back in Step 9 of the notebook. If you don't have
   them anymore, just re-run that cell in the notebook and copy them over.

3. Run the server:
   ```
   python manage.py runserver
   ```

4. Open **http://localhost:8000** in your browser.

## How it works

- `detector/views.py` loads the model and vectorizer once when the server
  starts (not on every request — that would be slow).
- It reuses the exact same `clean_text()` cleaning function from the
  notebook, so predictions match what you saw there.
- The form submits a POST request back to the same page; Django re-renders
  the page with the prediction and a confidence score.

## Notes

- This uses Django's built-in development server — fine for trying things
  out locally, not meant for production/public deployment.
- `DEBUG = True` is left on in `settings.py` for easier local debugging;
  turn it off (and set `ALLOWED_HOSTS`) before deploying anywhere public.
