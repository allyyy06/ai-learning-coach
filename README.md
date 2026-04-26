# 🧠 AI-Powered Personalized Learning Coach / Yapay Zeka Destekli Öğrenme Koçu

[🇹🇷 Türkçe Seçeneği İçin Aşağı Kaydırın (Turkish version below)](#türkçe-tr)

An intelligent, multi-agent platform designed to act as your personal learning companion. It generates tailored study plans, tracks your progress, gamifies your learning experience, and provides dynamic feedback through specialized AI agents.

---

## 🇬🇧 English (EN)

### 🌟 Key Features

*   **Multi-Agent AI Architecture:**
    *   **Planner Agent:** Dynamically creates tailored weekly/daily study plans based on your goals, level, and available time.
    *   **Evaluator Agent:** Objectively analyzes your daily progress reports and calculates a performance score.
    *   **Coach Agent:** Provides motivational, constructive feedback and adjusts your mindset like a real mentor.
*   **🎮 Gamification Engine:** Keeps you motivated by awarding **XP**, increasing your **Level**, and tracking your daily **Streaks (🔥)** for every submitted progress report.
*   **🌳 Interactive Skill Tree:** Visualizes your study plan not just as a list, but as an interactive node graph (powered by `streamlit-agraph`), unlocking the "big picture" of your learning journey.
*   **⏱️ Built-in Pomodoro Timer:** A focus timer (e.g., 25 minutes) integrated directly into the progress page. Once the time is up, it seamlessly prompts you to write your learning report.
*   **🔄 Adaptive Engine:** The system dynamically adjusts the difficulty and content of your future plans based on your daily performance scores.
*   **📊 Visual Performance Dashboard:** Tracks your learning analytics, metrics, and progress distribution using rich `Plotly` charts.
*   **🤖 Multi-LLM Support:** Compatible with various LLM providers (OpenAI GPT, Google Gemini, Groq) to balance cost and performance.

### 📸 Screenshots

| Interactive Skill Tree | Pomodoro Focus Timer | Profile & Gamification |
| :---: | :---: | :---: |
| ![Skill Tree](https://placehold.co/600x400?text=Skill+Tree+Screenshot) | ![Pomodoro](https://placehold.co/600x400?text=Pomodoro+Screenshot) | ![Profile](https://placehold.co/600x400?text=Gamification+Screenshot) |

### 🛠 Technology Stack

*   **Backend:** FastAPI (Python), SQLAlchemy, SQLite
*   **Frontend:** Streamlit, Streamlit-agraph, Plotly, Pandas
*   **AI Integration:** LangChain / Direct API integrations (OpenAI, Gemini, Groq)
*   **Data Models:** Pydantic

### 📂 Project Structure

```text
ai-learning-coach/
├── backend/
│   ├── agents/          # LLM agent logic (Planner, Evaluator, Coach)
│   ├── api/             # FastAPI routes
│   ├── database/        # SQLite models and DB setup
│   ├── models/          # Pydantic schemas
│   ├── services/        # Business logic and agent orchestration
│   └── main.py          # FastAPI application entry point
├── frontend/
│   └── app.py           # Streamlit application UI
├── data/                # SQLite database storage
├── prompts/             # System prompts for AI agents
├── .env.example         # Environment variables template
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

### 🚀 Installation & Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-learning-coach.git
cd ai-learning-coach
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Environment Variables
Copy the example environment file and fill in your API keys (e.g., OpenAI API Key).
```bash
cp .env.example .env
```

#### 4. Run the Application

**Start the Backend (FastAPI):**
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Start the Frontend (Streamlit):**
Open a new terminal window and run:
```bash
python -m streamlit run frontend/app.py
```

Visit `http://localhost:8501` in your browser.

### 📦 Deployment
*   **Backend:** Ready for deployment on Render, Railway, or Heroku.
*   **Frontend:** Can be easily deployed via Streamlit Community Cloud.

---

<div id="türkçe-tr"></div>

## 🇹🇷 Türkçe (TR)

### 🌟 Temel Özellikler

*   **Çoklu Ajan (Multi-Agent) Mimarisi:**
    *   **Planner Agent:** Hedeflerinize, seviyenize ve zamanınıza göre haftalık ve günlük planlar oluşturur.
    *   **Evaluator Agent:** Günlük ilerleme raporlarınızı analiz eder ve nesnel bir performans puanı hesaplar.
    *   **Coach Agent:** Gerçek bir mentor gibi motive edici ve yapıcı geri bildirimler sunar.
*   **🎮 Oyunlaştırma (Gamification):** Yazdığınız her çalışma raporu için size **XP** kazandırır, **Seviye (Level)** atlamanızı sağlar ve **Günlük Seri (🔥 Streak)** takibi yaparak motivasyonunuzu zirvede tutar.
*   **🌳 Etkileşimli Yetenek Ağacı (Skill Tree):** Klasik listelerin ötesine geçerek, `streamlit-agraph` altyapısıyla tüm planınızı birbirine bağlı interaktif düğümler (node) şeklinde haritalandırır.
*   **⏱️ Entegre Pomodoro Sayacı:** İlerleme sayfasına gömülü odaklanma sayacı ile 25 dakikalık periyotlar halinde çalışabilirsiniz. Süre dolduğunda sistem otomatik olarak sizden rapor yazmanızı ister.
*   **🔄 Adaptif Öğrenme Motoru:** Performans puanlarınıza bağlı olarak, planın zorluğunu veya hızını dinamik bir şekilde güncelleyerek size ayak uydurur.
*   **📊 Görsel Performans Paneli:** Gelişiminizi ve analitik verilerinizi `Plotly` kütüphanesi ile hazırlanan interaktif grafiklerle takip etmenizi sağlar.
*   **🤖 Çoklu LLM Desteği:** İhtiyaca göre OpenAI GPT, Google Gemini veya Groq modelleri ile çalışabilme esnekliği sunar.

### 📸 Ekran Görüntüleri

| Etkileşimli Yetenek Ağacı | Pomodoro Odaklanma Sayacı | Profil ve Oyunlaştırma |
| :---: | :---: | :---: |
| ![Skill Tree](https://placehold.co/600x400?text=Yetenek+Agaci) | ![Pomodoro](https://placehold.co/600x400?text=Pomodoro+Sayaci) | ![Profile](https://placehold.co/600x400?text=Oyunlastirma) |

### 🛠 Teknoloji Yığını

*   **Backend:** FastAPI (Python), SQLAlchemy, SQLite
*   **Frontend:** Streamlit, Streamlit-agraph, Plotly, Pandas
*   **Yapay Zeka:** OpenAI, Gemini, Groq Entegrasyonları
*   **Veri Doğrulama:** Pydantic

### 📂 Proje Yapısı

```text
ai-learning-coach/
├── backend/
│   ├── agents/          # Yapay zeka ajanları (Planner, Evaluator, Coach)
│   ├── api/             # FastAPI yönlendirmeleri (routes)
│   ├── database/        # Veritabanı modelleri ve SQLite ayarları
│   ├── models/          # Pydantic şemaları
│   ├── services/        # İş mantığı ve ajan orkestrasyonu
│   └── main.py          # FastAPI ana giriş noktası
├── frontend/
│   └── app.py           # Streamlit kullanıcı arayüzü
├── data/                # SQLite veritabanı dosyası
├── prompts/             # Ajanlar için sistem komutları (prompts)
├── .env.example         # Çevre değişkenleri şablonu
├── requirements.txt     # Python kütüphaneleri
└── README.md            # Proje dokümantasyonu
```

### 🚀 Kurulum ve Çalıştırma

#### 1. Depoyu Klonlayın
```bash
git clone https://github.com/your-username/ai-learning-coach.git
cd ai-learning-coach
```

#### 2. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

#### 3. Ortam Değişkenleri
`.env.example` dosyasını kopyalayarak `.env` isimli yeni bir dosya oluşturun ve gerekli API anahtarlarınızı (örn: `OPENAI_API_KEY`) ekleyin.
```bash
cp .env.example .env
```

#### 4. Uygulamayı Başlatın

**Arka Ucu (Backend) Başlatın:**
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Ön Yüzü (Frontend) Başlatın:**
Yeni bir terminal penceresi açın ve şu komutu çalıştırın:
```bash
python -m streamlit run frontend/app.py
```

Tarayıcınızda `http://localhost:8501` adresine giderek uygulamayı kullanmaya başlayabilirsiniz.

### 📦 Dağıtım (Deployment)
*   **Backend:** Render, Railway veya Heroku gibi bulut platformlarına tek tıkla yüklenebilir.
*   **Frontend:** Streamlit Community Cloud üzerinden saniyeler içinde yayına alınabilir.

---
*Developed by Ali İhsan Çetin*
