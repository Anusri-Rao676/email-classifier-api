
# 📄 Final Report: Email Classification with PII Masking

## 👩‍💻 Author
**GitHub**: [Anusri666](https://github.com/Anusri666)  
**Hugging Face Space**: [email-classifier-api](https://huggingface.co/spaces/Anusri666/email-classifier-api)  
**API Endpoint**: https://Anusri666-email-classifier-api.hf.space/classify

---

## 📌 1. Problem Statement

The task is to classify customer support emails into one of the following categories:
- Incident
- Request
- Problem
- Change

Before classification, the email content must be passed through a PII masking pipeline to identify and mask sensitive information such as full names, email addresses, phone numbers, Aadhar numbers, credit/debit card numbers, etc.

---

## 🔐 2. PII Masking Strategy

The PII masking pipeline is designed **without using LLMs** and handles both structured and unstructured PII entities:

### Techniques Used:
- **Regex Matching** for:
  - `email`, `phone_number`, `aadhar_num`, `dob`, `cvv_no`, `credit_debit_no`, `expiry_no`
- **spaCy NER (`en_core_web_sm`)** for:
  - Full names (`PERSON` entities)

### Output Format:
```json
{
  "position": [start, end],
  "classification": "entity_type",
  "entity": "original_value"
}
```

---

## 🤖 3. Classification Pipeline

### Preprocessing:
- Emails are lowercased, stripped of whitespace, and passed through the masking function.

### Feature Extraction:
- `TfidfVectorizer` with `max_features=5000` is used to convert masked text into numerical vectors.

### Classifier:
- A `RandomForestClassifier` from scikit-learn is trained on the vectorized data.

### Model Performance:
- **Accuracy**: ~73%
- Best performing classes: **Request**, **Incident**
- Slight class imbalance affected **Problem** class recall

---

## 🛰️ 4. API Development

- **Framework**: FastAPI
- **Routes**:
  - `GET /` → Returns a welcome message for browser users
  - `POST /classify` → Accepts email input and returns classification
- **Hosting**: Hugging Face Spaces (no frontend)
- **Startup Commands**:
  ```bash
  python -m spacy download en_core_web_sm
  uvicorn api:app --host 0.0.0.0 --port 7860
  ```

### POST Input:
```json
{ "input_email_body": "..." }
```

### Output:
```json
{
  "input_email_body": "...",
  "list_of_masked_entities": [...],
  "masked_email": "...",
  "category_of_the_email": "..."
}
```

---

## ✅ 5. Challenges Faced

- Handling overlapping entities and entity replacement without disrupting indexing
- Tuning classifier on imbalanced data while keeping it lightweight
- Ensuring correct API output format as per evaluation spec
- Learning Hugging Face Spaces backend deployment for FastAPI
- Adding GET / root route to make the API browser-friendly

---

## 📦 6. Final Deliverables

- ✅ Deployed API: https://Anusri666-email-classifier-api.hf.space/classify
- ✅ Welcome Route: https://Anusri666-email-classifier-api.hf.space/
- ✅ GitHub Repo: https://github.com/Anusri666/email-classifier-api
- ✅ README with input/output format and root route
- ✅ Report (this document)

---

## 🏁 Conclusion

The project meets all specified requirements:
- PII masking without LLMs
- Accurate classification
- Deployed API with correct JSON format
- User-friendly browser support via GET /

This pipeline is ready for integration into real-world support systems.
