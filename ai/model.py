from transformers import pipeline
import torch

class DisasterClassifier:
    def __init__(self):
        # Load pre-trained transformer (can be replaced with fine-tuned model later)
        self.model = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

    def predict(self, text):
        """
        Returns: 
            label (str), confidence (float)
        """
        result = self.model(text)[0]
        label = result['label']  # 'POSITIVE' or 'NEGATIVE' — interpreted as disaster or not
        confidence = result['score']
        return label, confidence

    def predict_batch(self, texts):
        """
        Batch prediction for performance
        """
        return self.model(texts)
