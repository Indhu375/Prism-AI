<p align="center">
  <img src="https://img.shields.io/badge/Prism-AI-blueviolet?style=for-the-badge&logo=prisma&logoColor=white" alt="Prism AI" />
</p>

<h1 align="center">🔮 Prism AI</h1>

<p align="center">
  <b>One Product Name. Infinite Content.</b><br/>
  AI-powered content generation platform for creators — blogs, social media images & video scripts, all from a single input.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-LLaMA_3.1-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" />
</p>

---

## 🚀 What is Prism AI?

**Prism AI** is an all-in-one AI content generation platform built for **content creators, marketers, and indie hackers**. Just enter your **product name**, and Prism AI instantly generates:

| Content Type | Description |
|---|---|
| 📝 **SEO Blog** | A fully structured, SEO-optimized blog article with title, meta description, headings, and CTA |
| 🎬 **Video Script** | A professional video script with hook, intro, main content, engagement prompt, and outro |
| 🖼️ **Social Media Image** | Eye-catching visuals tailored for platforms like Instagram, LinkedIn & Twitter *(coming soon)* |

> **One input. Three powerful outputs.** Save hours of content creation time.

---

## ✨ Features

- 🎯 **Single Input Workflow** — Enter a product name and let AI handle the rest
- 📝 **SEO Blog Generation** — Structured articles with proper headings, meta descriptions & CTAs
- 🎬 **Video Script Generation** — Platform-ready scripts with hooks, pacing & engagement prompts
- 🖼️ **Social Media Image Generation** — AI-generated visuals for social platforms *(coming soon)*
- ⚡ **Powered by Groq + LLaMA 3.1** — Ultra-fast inference for instant content
- 🔌 **RESTful API** — Clean FastAPI backend with interactive Swagger docs
- 🌐 **CORS Enabled** — Ready to connect with any frontend

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python, FastAPI |
| **AI Model** | Groq API (LLaMA 3.1) |
| **API Docs** | Swagger UI (auto-generated) |
| **Frontend** | *Coming Soon* |

---

## 📁 Project Structure

```
Prism-AI/
├── backend/
│   ├── main.py               # FastAPI app — routes & entry point
│   ├── blog_generation.py    # Blog generation logic (Groq API)
│   ├── video_script.py       # Video script generation logic (Groq API)
│   └── .gitignore
├── .env                      # Environment variables (API keys)
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.10+
- A [Groq API Key](https://console.groq.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Prism-AI.git
cd Prism-AI
```

### 2. Install Dependencies

```bash
pip install fastapi uvicorn groq python-dotenv
```

### 3. Set Up Environment Variables

Create a `.env` file in the `backend/` directory:

```env
API_KEY=your_groq_api_key_here
```

### 4. Run the Server

```bash
cd backend
python -m uvicorn main:app --reload
```

The API will be live at **http://localhost:8000**

📖 Interactive API docs at **http://localhost:8000/docs**

---

## 📡 API Endpoints

### `GET /`
Health check & endpoint listing.

### `POST /generate-blog`
Generate an SEO-optimized blog article.

**Request Body:**
```json
{
  "product_name": "Prism AI",
  "tone": "Professional",
  "word_count": 800
}
```

**Response:**
```json
{
  "status": "success",
  "product_name": "Prism AI",
  "tone": "Professional",
  "word_count": 800,
  "generated_blog": "..."
}
```

### `POST /generate-video-script`
Generate a structured video script.

**Request Body:**
```json
{
  "product_name": "Prism AI",
  "tone": "Energetic",
  "duration": "5"
}
```

**Response:**
```json
{
  "status": "success",
  "product_name": "Prism AI",
  "tone": "Energetic",
  "duration_mins": 5,
  "generated_script": "..."
}
```

---

## 🗺️ Roadmap

- [x] Blog Generation API
- [x] Video Script Generation API
- [ ] Social Media Image Generation
- [ ] Frontend Website (React / Next.js)
- [ ] User Authentication
- [ ] Content History & Dashboard
- [ ] Multi-language Support
- [ ] Export to PDF / Markdown

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with 💜 by <b>Prism AI Team</b>
</p>
