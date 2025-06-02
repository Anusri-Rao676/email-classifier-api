
# 📧 Email Classification API with PII Masking

This project implements a backend-only API that classifies support emails into predefined categories — while masking all Personally Identifiable Information (PII) before classification.

It is designed for use by customer support systems to improve ticket triaging while ensuring user data privacy.

---

## 🚀 Deployed API

**POST Endpoint:**  
👉 [`/classify`](https://Anusri666-email-classifier-api.hf.space/classify)

**GET Endpoint (browser-friendly):**  
👉 [`/`](https://Anusri666-email-classifier-api.hf.space) — returns a welcome message

> Deployed on [Hugging Face Spaces](https://huggingface.co/spaces/Anusri666/email-classifier-api)

---

## 📥 Input Format

Send a **POST request** to `/classify` with this JSON body:

```json
{
  "input_email_body": "Hi, my name is John Doe. My email is john@example.com and my Aadhar is 1234 5678 9012."
}
```

---

## 📤 Output Format

You’ll receive a JSON response with:

```json
{
  "input_email_body": "Hi, my name is John Doe. My email is john@example.com and my Aadhar is 1234 5678 9012.",
  "list_of_masked_entities": [
    {
      "position": [26, 43],
      "classification": "email",
      "entity": "john@example.com"
    },
    {
      "position": [61, 76],
      "classification": "aadhar_num",
      "entity": "1234 5678 9012"
    }
  ],
  "masked_email": "Hi, my name is [full_name]. My email is [email] and my Aadhar is [aadhar_num].",
  "category_of_the_email": "Request"
}
```

---

## 🧠 Model Pipeline

### 🔐 PII Masking:
- **Regex patterns** for: `email`, `phone_number`, `dob`, `aadhar_num`, `cvv_no`, `credit_debit_no`, `expiry_no`
- **spaCy NER (`en_core_web_sm`)** for identifying `full_name`

### 🧠 Classification:
- `TfidfVectorizer` to extract text features from the masked email
- `RandomForestClassifier` to predict the category

### 📦 Framework:
- FastAPI (for serving)
- Deployed on Hugging Face Spaces (no frontend, backend-only API)

---

## 📦 Requirements

Install required libraries using:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## 🧪 How to Test the API

### Using Python:

```python
import requests

url = "https://Anusri666-email-classifier-api.hf.space/classify"
data = {
    "input_email_body": "Hi, my name is Rahul. My email is rahul@example.com and my phone is 9876543210."
}
res = requests.post(url, json=data)
print(res.status_code)
print(res.json())
```

### Using Postman:
- Method: `POST`
- URL: `https://Anusri666-email-classifier-api.hf.space/classify`
- Body: raw JSON as shown above
- Headers: `Content-Type: application/json`

---

## 🗂 File Structure

```plaintext
.
├── api.py                # FastAPI backend
├── model.pkl.gz          # Compressed trained classifier
├── vectorizer.pkl.gz     # Compressed TF-IDF vectorizer
├── requirements.txt      # Dependencies
└── README.md             # This file
```

---

## 👩‍💻 Author

- GitHub: [@Anusri-Rao-676](https://github.com/Anusri-Rao676)
- Hugging Face Space: [email-classifier-api](https://huggingface.co/spaces/Anusri666/email-classifier-api)

---

## ✅ Assignment Compliance

✔️ PII masking without LLMs  
✔️ Classification into required labels  
✔️ `/classify` endpoint deployed on Hugging Face  
✔️ `/` GET endpoint added for browser users  
✔️ Input/output format as per spec  
✔️ No frontend (backend-only FastAPI)

--
