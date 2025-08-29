from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch

def paraphrase_text(text):
    model_name = "tuner007/pegasus_paraphrase"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    inputs = tokenizer([text], truncation=True, padding="longest", return_tensors="pt")
    outputs = model.generate(**inputs, max_length=60, num_beams=5, num_return_sequences=1, temperature=1.5)
    paraphrased = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return paraphrased