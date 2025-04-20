# vahan.ai

📽️ [Click here to watch the demo video](https://drive.google.com/file/d/19MtBxa8fN1Wtgjlbnz4qm3ezvOGbi8Kl/view?usp=sharing)

# 📚 AI-Powered Interactive Learning Assistant

An **AI-driven educational backend system** designed to generate dynamic, personalized learning reports by leveraging **Large Language Models (LLMs)**, multiple research sources (web, academic, and video), and user feedback. Built with **FastAPI** and fully containerized using **Docker**.

---

## 🚀 Key Features

### 🧠 Interactive Questionnaire  
- Understands user preferences and learning styles through dynamic question generation and analysis.

### 🔍 Multi-Source Research Engine  
- Aggregates information from **simulated web, academic, and video sources** to ensure comprehensive insights.

### 📝 Smart Report Generation  
- Synthesizes research into **well-structured, markdown-formatted reports** using LLMs.

### 🔁 Feedback-Driven Refinement  
- Enhances and adapts reports based on user-provided feedback.

### 🧾 Topic Submission Endpoint  
- Enables easy submission of topics with learning objectives for processing.

### ⚙ Modular & Extensible Design  
- Clean, plug-and-play architecture for future integration of sources and services.

---

## 🧩 Project Structure  

```
├── src/
│   ├── core/
│   │   ├── interactive_questionnaire.py
│   │   ├── report_generator.py
│   │   ├── research_engine.py
│   │   └── __init__.py
│   ├── data/
│   │   └── sources/
│   │       ├── web_source.py
│   │       ├── academic_source.py
│   │       ├── video_source.py
│   │       └── __init__.py
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── citation_service.py
│   │   └── __init__.py
│   └── main.py
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🛠 Setup Instructions  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/yourusername/interactive-learning-assistant.git
cd interactive-learning-assistant
```

### 2️⃣ Add Environment Variables  
Create a `.env` file in the root directory and add the following:
```ini
GROQ_API_KEY=your_groq_api_key
```

### 3️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the FastAPI Server  
```bash
uvicorn src.main:app --reload
```

### 5️⃣ Using Docker  
```bash
docker-compose up --build
```

---

## 📬 API Endpoints  

| **Endpoint**              | **Method** | **Description**                                      |
|---------------------------|------------|----------------------------------------------------|
| `/api/topics`             | `POST`     | Submit a topic and learning objectives to start the process. |
| `/api/reports`            | `POST`     | Generate a personalized educational report.        |
| `/api/reports/{report_id}/modify` | `POST`     | Modify a previously generated report using feedback. |

---

## 💡 Example Workflow  

1. User submits a topic + learning objectives to `/api/topics`.  
2. System returns **clarifying questions**.  
3. User sends responses to `/api/reports`.  
4. System conducts research and generates a **customized report**.  
5. User provides feedback to `/api/reports/{report_id}/modify`.  
6. A refined version of the report is returned.

---

## 🤖 Tech Stack  

- **FastAPI** — Backend framework  
- **Python 3.11+**  
- **Groq API (Mixtral)** — LLM inference  
- **Docker & Docker Compose** — Containerization  
- **Markdown** — Report formatting  

---

## 📘 Future Enhancements  

- Real-time data extraction from **actual web, video, and academic sources**.  
- Frontend UI and user authentication.  
- Export reports as **PDFs**.  
- Support for **multilingual content**.  

---
![Image 1](ASSETS_IMAGES/WhatsApp%20Image%202025-04-20%20at%2020.32.29_0e14e018.jpg)

![Image 2](ASSETS_IMAGES/WhatsApp%20Image%202025-04-20%20at%2020.32.29_67adcb73.jpg)

![Image 3](ASSETS_IMAGES/WhatsApp%20Image%202025-04-20%20at%2020.32.30_0f99b636.jpg)

![Image 4](ASSETS_IMAGES/WhatsApp%20Image%202025-04-20%20at%2020.32.30_4a79cadb.jpg)

![Screenshot](ASSETS_IMAGES/WhatsApp%20Image%202025-04-20%20at%2020.28.14_b8c6fac3.jpg)


