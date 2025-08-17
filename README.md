# 🚀 AutoInsight AI

> **Enterprise-Grade Intelligent Multi-Agent Data Analytics Platform**
> Transform natural language into actionable data insights with collaborative AI agents, real-time streaming, and interactive visualizations.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red.svg)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://docker.com)
[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Available-brightgreen.svg)](https://autoinsight-app-302134120130.asia-south1.run.app)

---

## 📑 Table of Contents

* [Overview](#-overview)
* [Live Demo & Screenshots](#-live-demo--screenshots)
* [Quick Start](#-quick-start)
* [Core Features](#-core-features)
* [Architecture](#-architecture)
* [Technology Stack](#-technology-stack)
* [Usage](#-usage)
* [Contributing](#-contributing)
* [License](#-license)
* [Author](#-author)

---

## 📌 Overview

**AutoInsight AI** democratizes data analytics by enabling anyone to query databases, analyze datasets, and generate visualizations with **natural language conversations**.

* Multi-agent orchestration with **AutoGen**
* Real-time **Python execution in Docker**
* Natural language → **SQL conversion**
* **Interactive visualizations** with AI-driven charting
* FastAPI REST API + Streamlit web apps + HTML5 frontend

---

## 🎬 Live Demo & Screenshots

### 🌐 Try It Live

[🚀 **Interactive Demo**](https://autoinsight-app-302134120130.asia-south1.run.app)

* 📊 [Data Analysis](https://autoinsight-app-302134120130.asia-south1.run.app/dataanalyst)
* 🗄️ [Database Analytics](https://autoinsight-app-302134120130.asia-south1.run.app/database)
* 📈 [Visualization Studio](https://autoinsight-app-302134120130.asia-south1.run.app/visualization)
* 📖 [API Docs](https://autoinsight-app-302134120130.asia-south1.run.app/docs)

### 📸 Screenshots

#### Data Analysis Agent

![Data Analysis Interface](notebook/imagean.png)

#### Database Analytics Agent

![Database Analytics Interface](notebook/imagedb.png)


#### 📹 **Video Demonstrations**
- **🗄️ Database Analytics**: [![Demo](https://img.shields.io/badge/▶️_Watch-Database_Demo-blue)](https://drive.google.com/file/d/1Ybjt1YOVaMd48aXRc1Lmu25DL9K_uV_J/view?usp=drive_link)
- **📊 Data Analysis**: [![Demo](https://img.shields.io/badge/▶️_Watch-Analysis_Demo-green)](https://drive.google.com/file/d/188XHB_nlON-SguIxxNAkBFFML-PefuYK/view?usp=sharing)


---

## ⚡ Quick Start

### 🔹 Local Setup

```bash
git clone https://github.com/akshaykumarbedre/AutoInsight-AI.git
cd AutoInsight-AI
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
cp .env.example .env
```

Update `.env` with your OpenAI API key.

Run:

```bash
python app_fastapi.py
```

Visit: [http://localhost:8080](http://localhost:8080)

### 🔹 Docker Setup

```bash
docker build -t autoinsight-ai .
docker run -p 5001:5001 --env-file .env autoinsight-ai
```

Visit: [http://localhost:5001](http://localhost:5001)

---

## ✨ Core Features

* 🤖 **Multi-Agent Teams** – SQL, visualization, code execution, and human-in-the-loop agents
* 💬 **Natural Language Queries** – Convert plain English into SQL and insights
* 📊 **Intelligent Visualizations** – Auto-generate bar, line, scatter, pie, and histogram charts
* 🐳 **Secure Execution** – Docker-isolated Python runtime for safe code execution
* 🔄 **Real-Time Streaming** – Asynchronous communication with progress tracking
* 🌐 **Multiple Interfaces** – FastAPI APIs, Streamlit apps, modern web UI

---

## 🏗 Architecture

```
AutoInsight-AI/
├── 🌐 Frontend & Templates
│   ├── templates/                   # HTML5 web interfaces
│   │   ├── index.html              # Professional homepage & portfolio
│   │   ├── dataanalyst.html        # Data analysis interface
│   │   ├── database.html           # Database analytics interface
│   │   └── visualization.html      # Visualization studio
│   └── streamlit/                  # Streamlit applications
│       ├── Dataabase_agent_streamlit.py    # Database UI
│       └── Data_anaylis_agent_streamlit.py # Analysis UI
├── 🚀 Core Application
│   ├── app_fastapi.py              # Main FastAPI server with all APIs
│   ├── requirements.txt            # Production dependencies
│   ├── Dockerfile                  # Container deployment config
│   └── .env.example               # Environment configuration template
├── 🤖 Agent System
│   ├── agent/                      # Specialized AI agents
│   │   ├── database_agent.py       # SQL query generation agent
│   │   ├── visualization_agent.py  # Chart creation agent  
│   │   ├── dataanalsys_agent.py   # Data analysis expert agent
│   │   ├── code_excuter_agent.py  # Docker code execution agent
│   │   └── human_agent.py         # Human-in-the-loop agent
│   └── teams/                      # Multi-agent orchestration
│       └── team_manager.py        # RoundRobinGroupChat coordination
├── 🛠️ Tools & Execution
│   ├── tool/                       # Specialized tool implementations
│   │   ├── plotting.py            # 5+ visualization tools (Matplotlib/Plotly)
│   │   ├── docker_executer.py     # Secure containerized code execution
│   │   └── sql_tool_kit.py        # LangChain SQL database tools
│   └── util/                       # Utility functions & streaming
│       ├── stream_handler.py       # Real-time conversation streaming
│       ├── display_helper.py       # UI display utilities
│       └── stream_data_anaylisi.py # Data analysis streaming handlers
├── 🗄️ Data & Configuration  
│   ├── config/                     # Environment & model configuration
│   │   └── settings.py            # OpenAI client & model settings
│   ├── database/                   # Database management
│   │   ├── db_manager.py          # SQLite connection & toolkit
│   │   └── ecommerce.db           # Sample e-commerce database
│   ├── coding/                     # User uploaded data files
│   │   ├── *.csv, *.json, *.xlsx  # Analysis datasets
│   │   └── *.pkl                  # Trained ML models
│   └── plots/                      # Generated visualizations
│       └── *.png                  # Chart exports & images
├── 🧪 Development & Notebooks
│   ├── notebook/                   # Jupyter development notebooks
│   │   ├── *.ipynb                # Experimental agent workflows
│   │   └── demo.py                # Interactive demonstrations
│   └── __pycache__/               # Compiled Python modules
└── 📄 Documentation
    ├── README.md                   # Comprehensive documentation
    ├── autoinsight_server.log      # Application logging
    └── .gitignore                 # Version control configuration<!-- Replace ASCII with a diagram image -->
```
---

## 🛠 Technology Stack

* **AI & Agents**: AutoGen, LangChain, OpenAI GPT-4o-mini
* **Backend**: FastAPI, WebSockets, Uvicorn
* **Frontend**: Streamlit, HTML5, CSS3, JS
* **Visualization**: Pandas, Matplotlib, Plotly, Seaborn
* **Infrastructure**: Docker, SQLite, SQLAlchemy

---

## 🎮 Usage

Once running, access the platform at [http://localhost:8080](http://localhost:8080):

* 🗄️ **Database Analytics** → Query databases in natural language
* 📊 **Data Analysis** → Upload CSV/Excel/JSON and run Python analysis
* 📈 **Visualization Studio** → Generate charts and dashboards

Example queries:

```
"Show top 10 customers by total order value"
"Create a correlation matrix heatmap"
"Predict sales trends with a regression model"
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -m 'Add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

👉 Follow PEP 8, add docstrings, and include tests.

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE).

---

## 👨‍💻 Author

**Akshay Kumar BM**
Senior Software Engineer & AI/ML Specialist

* 📧 [akshaykumarbedre.bm@gmail.com](mailto:akshaykumarbedre.bm@gmail.com)
* 🔗 [LinkedIn](https://linkedin.com/in/akshay-kumar-bm)
* 🐙 [GitHub](https://github.com/akshaykumarbedre)

---

⭐ If you find this project useful, don’t forget to **star the repo**!

*Built with ❤️ for the data science & AI community*

