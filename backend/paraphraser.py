import re
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

def remove_first_person(text):
    return re.sub(r"\b(I|we|me|my|mine|our|us|ours)\b", "", text, flags=re.IGNORECASE)

def simulate_academic_style(text):
    replacements = {
        "get": "obtain",
        "a lot": "a significant amount",
        "really": "truly",
        "very": "highly",
        "help": "assist",
        "show": "demonstrate"
    }
    for informal, formal in replacements.items():
        text = re.sub(rf"\b{informal}\b", formal, text, flags=re.IGNORECASE)
    return text

def convert_voice(text, to_voice="passive"):
    if to_voice == "active":
        # Very basic active voice conversion
        return re.sub(r"(\b\w+\b) was (\w+) by (\b\w+\b)", r"\3 \2 \1", text)
    elif to_voice == "passive":
        # Very basic passive voice conversion
        return re.sub(r"(\b\w+\b) (\w+) (\b\w+\b)", r"\3 was \2 by \1", text)
    return text

def paraphrase_text(text, option="normal", voice_type="passive"):
    model_name = "tuner007/pegasus_paraphrase"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)

    # Handle options
    if option == "first_person_removal":
        text = remove_first_person(text)

    inputs = tokenizer([text], truncation=True, padding="longest", return_tensors="pt")

    input_length = inputs['input_ids'].shape[1]
    max_length = input_length + 10  # buffer
    min_length = max(input_length - 10, 20)

    outputs = model.generate(
        **inputs,
        max_length=max_length,
        min_length=min_length,
        num_beams=5,
        num_return_sequences=1,
        temperature=1.0,
        early_stopping=True
    )
    paraphrased = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Apply academic filter
    if option == "academic_filter":
        paraphrased = simulate_academic_style(paraphrased)

    # Apply voice conversion
    if option == "active_passive":
        paraphrased = convert_voice(paraphrased, to_voice=voice_type)

    return paraphrased