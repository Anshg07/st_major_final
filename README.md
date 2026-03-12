# 📧 AI-Powered Customer Care Assistant

A streamlined **Streamlit** application designed to help customer support teams generate professional, context-aware email responses using Google's **Gemini AI**.

---

## 🚀 Features

* **Secure Authentication**: Simple login system to protect the dashboard and configuration.
* **AI-Generated Responses**: Leverages the `gemini-3.1-flash-lite-preview` model to craft emails based on specific customer queries.
* **Multi-Company Support**: Manage and switch between different company profiles (e.g., TechCorp, MediCare, EduLearn) to maintain brand consistency.
* **Tone Customization**: Choose from various tones—Professional, Friendly, Compassionate, or Formal—to suit the situation.
* **Dynamic Configuration**: Add, update, or delete company profiles and manage your Google AI API key directly within the app.

---

## 🛠️ Tech Stack

* **Frontend**: [Streamlit](https://streamlit.io/)
* **AI Engine**: [Google Generative AI (Gemini)](https://ai.google.dev/)
* **Language**: Python

---

## 📋 Prerequisites

Before running the app, ensure you have:

1. **Python 3.9+** installed.
2. A **Google AI API Key**. You can obtain one from the [Google AI Studio](https://aistudio.google.com/).

---

## 📥 Installation & Setup

1. **Clone the repository:**
```bash
git clone <your-repository-url>
cd <repository-folder>

```


2. **Install dependencies:**
```bash
pip install streamlit google-generativeai

```


3. **Run the application:**
```bash
streamlit run app.py

```



---

## 📖 How to Use

### 1. Login

* **Username**: `admin`
* **Password**: `password`
*(Note: These are hardcoded for demonstration purposes in the current version).*

### 2. Configuration

* Navigate to the **⚙️ Configuration** tab.
* Enter your **Google API Key**.
* (Optional) Add new company profiles or edit the existing ones to provide context for the AI.

### 3. Generate a Response

* Navigate to **✉️ Generate Response**.
* Select the target **Company** and desired **Tone**.
* Paste the customer's message into the **Customer Query** text area.
* Click **Generate Response** to receive a drafted email.

---

## 🔐 Security Note

The current version uses `st.session_state` for API key management and hardcoded credentials. For production environments, it is recommended to use **Environment Variables** or **Streamlit Secrets** for sensitive data.

---

## 👤 Credits

Developed by **Ansh**.
