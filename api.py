from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import spacy
import re

# Load model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
nlp = spacy.load("en_core_web_sm")

app = FastAPI()

class EmailInput(BaseModel):
    input_email_body: str

def mask_pii(text):
    entities = []
    masked_text = text

    patterns = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone_number": r"\b(?:\+91[- ]?)?[6-9]\d{9}\b",
        "aadhar_num": r"\b\d{4}[- ]?\d{4}[- ]?\d{4}\b",
        "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
        "cvv_no": r"\b\d{3}\b",
        "expiry_no": r"\b(0[1-9]|1[0-2])/?([0-9]{2,4})\b",
        "dob": r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"
    }

    # Regex-based masking
    for label, pattern in patterns.items():
        for match in re.finditer(pattern, masked_text):
            start, end = match.start(), match.end()
            entity_text = match.group()
            replacement = f"[{label}]"

            entities.append({
                "position": [start, end],
                "classification": label,
                "entity": entity_text
            })

            masked_text = masked_text.replace(entity_text, replacement, 1)

    # spaCy NER-based full name masking
    doc = nlp(masked_text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            start, end = ent.start_char, ent.end_char
            entity_text = ent.text
            replacement = "[full_name]"

            entities.append({
                "position": [start, end],
                "classification": "full_name",
                "entity": entity_text
            })

            masked_text = masked_text.replace(entity_text, replacement, 1)

    return masked_text, entities

@app.post("/classify")
def classify_email(email: EmailInput):
    input_text = email.input_email_body
    masked_email, entity_list = mask_pii(input_text)
    features = vectorizer.transform([masked_email])
    predicted_category = model.predict(features)[0]

    return {
        "input_email_body": input_text,
        "list_of_masked_entities": entity_list,
        "masked_email": masked_email,
        "category_of_the_email": predicted_category
    }
