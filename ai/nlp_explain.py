from transformers import pipeline
from lime.lime_text import LimeTextExplainer

# Load model
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

def classify(text):
    return classifier(text)[0]

def explain_prediction(text):
    explainer = LimeTextExplainer(class_names=["disaster", "non-disaster"])
    explanation = explainer.explain_instance(text, lambda x: [i['score'] for i in classifier(x)], num_features=5)
    words_weights = explanation.as_list()
    pred = classify(text)
    return words_weights, pred
