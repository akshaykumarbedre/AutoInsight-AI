# 🚀 AutoInsight AI

> **Intelligent Conversational Analytics Platform with Multi-Agent Teams**  
> A full-stack AI agent platform that transforms natural language into actionable data insights through advanced agent collaboration.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red.svg)](https://streamlit.io)
[![AutoGen](https://img.shields.io/badge/AutoGen-0.6+-green.svg)](https://github.com/microsoft/autogen)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://docker.com)

---

## 📌 Project Overview

**AutoInsight AI** is a sophisticated multi-agent platform that democratizes data analysis through natural language conversations. It features specialized AI agent teams that work collaboratively to transform user queries into comprehensive data insights and visualizations.

### 🎯 Core Capabilities

- **🗄️ Database Agent Team**: Converts natural language to SQL queries with intelligent data retrieval
- **📊 Data Visualization Team**: Creates intelligent charts and visualizations from query results  
- **🧠 Data Analysis Agent Team**: Performs complex data analysis on CSV/Excel files with Docker isolation
- **👥 Human-in-the-Loop**: Interactive feedback and verification system
- **🔄 Streaming Conversations**: Real-time agent communication and result streaming

---

## 🎬 Demo

### Screenshots
![Database Agent Interface](https://github.com/user-attachments/assets/5397151e-bc19-4e1e-a7e0-8813fc76805b)

![Data Analysis Interface](https://github.com/user-attachments/assets/aa893388-8d13-4ae9-94a2-eeb8d26cd634)

### Demo Videos
- 🎥 [Database Agent Demo](https://drive.google.com/file/d/11pplCQI1jrP8usHWf_VWDhoDR_pjud38/view?usp=sharing)
- 🎥 [Data Analysis Agent Demo](https://dl.dropboxusercontent.com/scl/fi/780sf6p8x7htrhclw1pdl/opera_1l7FBf5KlR.mp4?rlkey=vo3cgh3xcrznpfoqtmo4wheuc&dl=0)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-Agent Teams** | Specialized agents working collaboratively for complex tasks |
| 💬 **Natural Language Queries** | Ask questions in plain English, get SQL results and insights |
| 📊 **Intelligent Visualizations** | Automatic chart generation with matplotlib, plotly integration |
| 🗄️ **Database Integration** | Native SQLite support with extensible SQL toolkit |
| 🐳 **Docker Isolation** | Secure code execution in containerized environments |
| 📁 **File Analysis** | Upload and analyze CSV, Excel, JSON files |
| 🔄 **Real-time Streaming** | Live conversation flow with agent interactions |
| 👥 **Human Verification** | Interactive approval and feedback mechanisms |
| 🎨 **Modern UI** | Clean Streamlit interface with dual-pane design |
| 🔧 **Extensible Architecture** | Modular design for easy feature additions |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AutoInsight AI Platform                  │
├─────────────────────────────────────────────────────────────┤
│  Frontend Layer (Streamlit)                                │
│  ├── Database Agent UI                                     │
│  └── Data Analysis Agent UI                                │
├─────────────────────────────────────────────────────────────┤
│  Agent Orchestration Layer                                 │
│  ├── TeamManager (Agent Coordination)                      │
│  ├── Database Agent Team                                   │
│  ├── Visualization Agent Team                              │
│  └── Data Analysis Agent Team                              │
├─────────────────────────────────────────────────────────────┤
│  Tool & Execution Layer                                    │
│  ├── SQL Toolkit (LangChain)                              │
│  ├── Plotting Tools (Matplotlib/Plotly)                   │
│  ├── Docker Code Executor                                  │
│  └── File Processing Tools                                 │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure Layer                                      │
│  ├── OpenAI GPT-4 (Language Models)                       │
│  ├── SQLite Database                                       │
│  ├── Docker Runtime                                        │
│  └── File System Storage                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technologies Used

### Core Framework
- **AutoGen** (0.6+) - Multi-agent conversation framework
- **LangChain** (0.3+) - LLM application framework and SQL toolkit
- **Streamlit** (1.45+) - Web application framework

### AI & ML
- **OpenAI GPT-4** - Large language models for agent intelligence
- **OpenAI Embeddings** - For future RAG implementations

### Data & Visualization
- **Pandas** (2.3+) - Data manipulation and analysis
- **Matplotlib** (3.10+) - Static plotting and visualizations
- **Plotly** (6.1+) - Interactive visualizations
- **Seaborn** (0.13+) - Statistical data visualization

### Infrastructure
- **Docker** (7.1+) - Containerized code execution
- **SQLite** - Embedded database engine
- **SQLAlchemy** (2.0+) - Database toolkit and ORM

### Development
- **Python** (3.8+) - Core programming language
- **asyncio** - Asynchronous programming support
- **python-dotenv** - Environment variable management

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Docker Desktop (for code execution features)
- OpenAI API key

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/AutoInsight-AI.git
cd AutoInsight-AI
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
```bash
# Copy environment template
copy .env.example .env  # On Windows
cp .env.example .env    # On Linux/Mac

# Edit .env file with your API keys
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here  # Optional for web search
```

### 5. Database Setup
The application includes a pre-configured SQLite database (`ecommerce.db`) with sample e-commerce data. No additional setup required.

---

## 🎮 Usage

### Database Agent Interface
Launch the database analysis interface:
```bash
streamlit run Dataabase_agent_streamlit.py
```

Features:
- Natural language database queries
- SQL generation and execution
- Automatic visualization creation
- Dual-pane conversation interface

**Example Queries:**
- "Show me the top 10 customers by total order amount"
- "What are the most popular products by quantity sold?"
- "Compare supplier performance scores"

### Data Analysis Agent Interface
Launch the file analysis interface:
```bash
streamlit run Data_anaylis_agent_streamlit.py
```

Features:
- Upload CSV/Excel/JSON files
- Natural language analysis requests
- Docker-isolated code execution
- Graph generation and export

**Example Tasks:**
- "Create a correlation matrix for all numeric columns"
- "Show distribution of sales by region"
- "Generate a time series analysis"

### Command Line Interface
For programmatic usage:
```bash
python main.py
```

### Core Application
For direct API usage:
```bash
python app.py
```

---

## 📊 Examples

### Database Query Example
```python
from main import initialize_teams

# Initialize teams
database_team, visualization_team = initialize_teams()

# Query database
query = "Show top 5 products by sales volume"
result = await database_team.run_stream(task=query)

# Create visualization
viz_result = await visualization_team.run_stream(task=result)
```

### Data Analysis Example
```python
from Data_anaylis_agent_streamlit import data_analysis_team

# Analyze uploaded file
task = "Create a scatter plot showing correlation between price and sales"
result = await data_analysis_team.run_stream(task=task)
```

---

## ⚙️ Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT models | Yes |
| `SERPER_API_KEY` | Serper API key for web search | No |

### Model Configuration
Edit `config/settings.py` to customize:
- Model selection (GPT-4, GPT-4-mini)
- Temperature and other LLM parameters
- Database connection strings

### Docker Configuration
Modify `tool/docker_executer.py` for:
- Timeout settings
- Volume mappings
- Initial package installations

---

## 📁 Project Structure

```
AutoInsight-AI/
├── agent/                      # Agent implementations
│   ├── database_agent.py      # SQL query agent
│   ├── visualization_agent.py # Chart creation agent
│   ├── dataanalsys_agent.py   # Data analysis expert
│   ├── code_excuter_agent.py  # Code execution agent
│   └── human_agent.py         # Human interaction agent
├── config/                     # Configuration management
│   └── settings.py            # Environment and model config
├── database/                   # Database management
│   └── db_manager.py          # Database connection handler
├── teams/                      # Agent team orchestration
│   └── team_manager.py        # Multi-agent coordination
├── tool/                       # Tool implementations
│   ├── plotting.py            # Visualization tools
│   ├── docker_executer.py     # Docker code execution
│   └── sql_tool_kit.py        # SQL database tools
├── util/                       # Utility functions
│   ├── stream_handler.py      # Conversation streaming
│   ├── display_helper.py      # UI display utilities
│   └── stream_data_anaylisi.py # Data analysis streaming
├── notebook/                   # Jupyter notebooks and experiments
├── plots/                      # Generated visualization outputs
├── tmp/                        # Temporary file storage
├── app.py                      # Core application logic
├── main.py                     # CLI interface
├── Dataabase_agent_streamlit.py # Database UI
├── Data_anaylis_agent_streamlit.py # Analysis UI
├── requirements.txt            # Python dependencies
├── ecommerce.db               # Sample SQLite database
└── titanic.csv                # Sample dataset
```

---

## 🧪 Development

### Running Tests
```bash
# Run individual components
python -m pytest tests/

# Test agent functionality
python agent/test_agents.py

# Test database connections
python database/test_db.py
```

### Adding New Agents
1. Create agent in `agent/` directory
2. Register in `agent/__init__.py`
3. Add to team configuration in `teams/team_manager.py`
4. Update UI interfaces as needed

### Adding New Tools
1. Implement tool in `tool/` directory
2. Register in `tool/__init__.py`
3. Add to agent tool lists
4. Update documentation

---

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open pull request**

### Contribution Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include tests for new features
- Update README for significant changes

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Microsoft AutoGen** - Multi-agent framework
- **LangChain** - LLM application framework
- **OpenAI** - GPT models and API
- **Streamlit** - Web application framework
- **Docker** - Containerization platform

---

## 👨‍💻 Author

**Akshay Kumar BM**
- 📧 Email: [akshaykumarbedre.bm@gmail.com](mailto:akshaykumarbedre.bm@gmail.com)
- 🔗 LinkedIn: [linkedin.com/in/akshaykumarbm](https://linkedin.com/in/akshaykumarbm)
- 🐙 GitHub: [github.com/akshaykumarbm](https://github.com/akshaykumarbm)

---

## 🌟 Future Roadmap

- [ ] **AutoML Agent Integration** - Automated machine learning pipelines
- [ ] **RAG Implementation** - Retrieval-augmented generation for better context
- [ ] **Multi-Database Support** - PostgreSQL, MySQL, MongoDB integration
- [ ] **Advanced Visualization** - Interactive dashboards and reports
- [ ] **API Endpoints** - REST API for external integrations
- [ ] **Cloud Deployment** - AWS/Azure/GCP deployment configurations

---

## ⭐ Star this repository if you find it useful!

*Built with ❤️ for the data science and AI community*