from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "Hello-SimpleAI/chatgpt-detector-roberta"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def detect_ai_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.softmax(logits, dim=1).numpy()
    human_prob = probs[0][0]
    ai_prob = probs[0][1]
    return {
        "Human Probability": round(human_prob * 100, 2),
        "AI Probability": round(ai_prob * 100, 2)
    }