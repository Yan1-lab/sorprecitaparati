# ml_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

class BacteriaClassifier:
    def __init__(self, csv_path="data/bacteria_db.csv"):
        self.df = pd.read_csv(csv_path).fillna("")
        self.vectorizer = TfidfVectorizer(ngram_range=(1,2))
        self.model = MultinomialNB()
        self._train()

    def _train(self):
        # Entrenamos con la columna common_symptoms (texto) -> label= name
        texts = self.df['common_symptoms'].astype(str).values
        # si está vacía, usamos descripción
        texts = np.where(texts == "", self.df['description'].astype(str).values, texts)
        X = self.vectorizer.fit_transform(texts)
        y = self.df['name'].values
        if X.shape[0] > 0:
            self.model.fit(X, y)

    def predict(self, symptoms_text: str):
        if symptoms_text is None or symptoms_text.strip() == "":
            return ("Desconocido", 0.0)
        X_new = self.vectorizer.transform([symptoms_text])
        try:
            probs = self.model.predict_proba(X_new)[0]
            pred = self.model.predict(X_new)[0]
            prob = float(max(probs))
            return (pred, prob)
        except Exception:
            return ("Desconocido", 0.0)
