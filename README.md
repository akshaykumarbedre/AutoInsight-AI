# 🚀 AutoInsight AI

> **Enterprise-Grade Intelligent Multi-Agent Data Analytics Platform**  
> A sophisticated AI-powered platform that transforms natural language into actionable data insights through collaborative multi-agent teams and real-time streaming interfaces.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red.svg)](https://streamlit.io)
[![AutoGen](https://img.shields.io/badge/AutoGen-0.6+-orange.svg)](https://github.com/microsoft/autogen)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-purple.svg)](https://openai.com)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://docker.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-yellow.svg)](https://langchain.com)
[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Available-brightgreen.svg)](https://autoinsight-app-302134120130.asia-south1.run.app)



---

## 📌 Project Overview

**AutoInsight AI** is an enterprise-grade multi-agent analytics platform that democratizes data analysis through natural language conversations. Built with modern Python technologies, it features specialized AI agent teams that collaborate seamlessly to transform complex user queries into comprehensive data insights, visualizations, and actionable intelligence.

### 🎯 Core Platform Capabilities

- **🗄️ Database Analytics Agent Team**: Natural language to SQL conversion with intelligent query optimization and data retrieval
- **📊 Data Visualization Agent Team**: Intelligent chart generation with 5+ visualization types and custom styling options  
- **🧠 Data Analysis Agent Team**: Real-time Python code execution with full library support (Pandas, NumPy, Matplotlib, Scikit-learn)
- **🐳 Docker-Isolated Execution**: Secure containerized code execution environment for data processing
- **🔄 Real-Time Streaming**: Live agent communication with asynchronous conversation streaming
- **🌐 Multi-Interface Support**: FastAPI REST APIs, Streamlit web interfaces, and modern HTML5 frontend
- **👥 Human-in-the-Loop**: Interactive approval and verification workflows

---

## 🎬 Platform Demonstrations

### � **Platform Screenshots**

#### 📊 **Data Analysis Agent Interface**
![Data Analysis Interface](notebook/imagean.png)
*Real-time Python code execution with machine learning capabilities, file upload, and comprehensive data analysis workflows*

#### 🗄️ **Database Analytics Interface**  
![Database Analytics Interface](notebook/imagedb.png)
*Natural language SQL queries with smart suggestions, real-time execution, and integrated visualization studio*

### �📹 **Video Demos**

Experience AutoInsight AI in action with these comprehensive demonstrations:

#### 🗄️ **Database Analytics Agent Demo**
[![Database Analytics Demo](https://img.shields.io/badge/▶️_Watch_Demo-Database_Analytics-blue?style=for-the-badge)](https://drive.google.com/file/d/1Ybjt1YOVaMd48aXRc1Lmu25DL9K_uV_J/view?usp=drive_link)

**Features Demonstrated:**
- Natural language to SQL query conversion
- Real-time database querying and results display
- Smart query suggestions and schema exploration
- Integrated visualization studio workflow

#### 📊 **Data Analysis Agent Demo**
[![Data Analysis Demo](https://img.shields.io/badge/▶️_Watch_Demo-Data_Analysis-green?style=for-the-badge)](https://drive.google.com/file/d/188XHB_nlON-SguIxxNAkBFFML-PefuYK/view?usp=sharing)

**Features Demonstrated:**
- Real-time Python code execution in Docker environment
- File upload and comprehensive data analysis
- Machine learning model building and evaluation
- Advanced visualization generation with custom styling

### 🌐 **Live Interactive Demo**
Try the platform yourself with the live deployment:
[![Live Platform](https://img.shields.io/badge/🚀_Try_Live_Platform-Interactive_Demo-brightgreen?style=for-the-badge)](https://autoinsight-fastapi-302134120130.asia-south1.run.app)

---

## ✨ Platform Features

| Feature | Description | Implementation |
|---------|-------------|---------------|
| 🤖 **Multi-Agent Teams** | Specialized agents with RoundRobinGroupChat orchestration | AutoGen 0.6+ with termination conditions |
| 💬 **Natural Language Processing** | Convert plain English to SQL queries and data insights | GPT-4o-mini with LangChain SQL toolkit |
| 📊 **Intelligent Visualizations** | 5+ chart types with custom styling and image export | Matplotlib + Plotly with AI-driven recommendations |
| 🗄️ **Database Integration** | SQLite with extensible SQL toolkit and schema exploration | LangChain SQL tools with auto-adaptation |
| 🐳 **Secure Code Execution** | Containerized Python environment with full library support | Docker 7.1+ with isolated runtime |
| 📁 **Multi-Format File Support** | CSV, Excel, JSON analysis with real-time processing | Pandas 2.3+ with streaming data handlers |
| 🔄 **Real-Time Streaming** | Live conversation flow with async message handling | FastAPI + WebSockets with SSE streaming |
| 👥 **Human Verification** | Interactive approval workflows and feedback loops | Streamlit dialogs + FastAPI endpoints |
| � **Modern Web Interface** | Responsive HTML5 frontend with professional styling | Custom CSS3 + JavaScript with FA icons |
| 🔧 **Enterprise Architecture** | Production-ready with logging, error handling, and monitoring | FastAPI + Uvicorn with health checks |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     AutoInsight AI Platform                         │
├─────────────────────────────────────────────────────────────────────┤
│  Frontend Layer                                                    │
│  ├── 🌐 HTML5/CSS3/JS (index.html, dataanalyst.html, etc.)        │
│  ├── 📱 Streamlit Web Apps (Database & Data Analysis UIs)          │
│  └── 🔗 FastAPI Templates with Jinja2 rendering                    │
├─────────────────────────────────────────────────────────────────────┤
│  API Gateway Layer                                                 │
│  ├── 🚀 FastAPI Server (app_fastapi.py) - REST APIs               │
│  ├── 📡 WebSocket Streaming Endpoints                             │
│  ├── 📁 File Upload/Download Handlers                             │
│  └── 🔍 Health Monitoring & Status APIs                           │
├─────────────────────────────────────────────────────────────────────┤
│  Agent Orchestration Layer                                         │
│  ├── 🎯 TeamManager - Multi-agent coordination                     │
│  ├── 🗄️ Database Agent Team (RoundRobinGroupChat)                 │
│  ├── 📊 Visualization Agent Team (Chart generation)                │
│  └── 🧠 Data Analysis Team (Code execution + Analysis)             │
├─────────────────────────────────────────────────────────────────────┤
│  Agent Implementation Layer                                        │
│  ├── 🤖 Database Agent - SQL query generation                      │
│  ├── 📈 Visualization Agent - Chart creation                       │
│  ├── 🔬 Data Analysis Agent - Python code generation               │
│  ├── ⚙️ Code Executor Agent - Docker runtime                       │
│  └── 👤 Human Agent - Interactive feedback                         │
├─────────────────────────────────────────────────────────────────────┤
│  Tool & Execution Layer                                            │
│  ├── 🛠️ SQL Toolkit (LangChain) - Database operations             │
│  ├── 📊 Plotting Tools - 5+ chart types (Matplotlib/Plotly)       │
│  ├── 🐳 Docker Executor - Isolated Python environment             │
│  └── 📁 File Processing - Multi-format data handlers              │
├─────────────────────────────────────────────────────────────────────┤
│  Infrastructure & AI Layer                                         │
│  ├── 🧠 OpenAI GPT-4o-mini - Language models                      │
│  ├── 🗄️ SQLite Database - E-commerce sample data                  │
│  ├── 🐳 Docker Runtime - Containerized execution                   │
│  ├── 📁 File Storage - Plots, uploads, temp files                 │
│  └── 📝 Logging & Monitoring - Production-ready observability     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

### Core Framework & AI
- **AutoGen** (0.6.1) - Microsoft's multi-agent conversation framework with RoundRobinGroupChat orchestration
- **LangChain** (0.3.25) - LLM application framework with SQL toolkit and tool adapters
- **OpenAI** (1.86.0) - GPT-4o-mini for intelligent agent responses and reasoning
- **FastAPI** (0.115.6) - Modern async web framework for RESTful APIs and real-time streaming

### Web Interfaces & Frontend
- **Streamlit** (1.45.1) - Interactive web applications for data analysis and database querying
- **HTML5/CSS3/JavaScript** - Professional responsive frontend with modern styling
- **Jinja2** (3.1.6) - Template engine for server-side rendering
- **Font Awesome** (6.0.0) - Professional iconography and UI elements

### Data Processing & Visualization
- **Pandas** (2.3.0) - Advanced data manipulation and analysis capabilities
- **Matplotlib** (3.10.3) - Static plotting and high-quality visualizations
- **Plotly** (6.1.2) - Interactive visualizations with export capabilities
- **Seaborn** (0.13.2) - Statistical data visualization and styling
- **NumPy** (2.3.0) - Numerical computing and array operations

### Infrastructure & Deployment
- **Docker** (7.1.0) - Containerized code execution and deployment
- **SQLite & SQLAlchemy** (2.0.41) - Database engine with ORM capabilities
- **Uvicorn** - ASGI server for production deployment
- **Python-multipart** (0.0.20) - File upload handling and processing

### Development & Monitoring
- **Python** (3.12+) - Core programming language with modern features
- **Pydantic** (2.11.7) - Data validation and settings management
- **Python-dotenv** (1.1.0) - Environment variable management
- **Asyncio** - Asynchronous programming for real-time streaming

---

## 🚀 Installation & Deployment

### Prerequisites
- Python 3.12 or higher
- Docker Desktop (required for secure code execution)
- OpenAI API key with GPT-4o-mini access

### 1. Repository Setup
```bash
git clone https://github.com/akshaykumarbedre/AutoInsight-AI.git
cd AutoInsight-AI
```

### 2. Environment Configuration
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
```bash
# Copy environment template
cp .env.example .env    # On Linux/Mac
copy .env.example .env  # On Windows

# Configure your API keys in .env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Database Initialization
The platform includes a pre-configured SQLite database (`database/ecommerce.db`) with comprehensive e-commerce sample data including customers, orders, products, and suppliers. No additional setup required.

### 🌐 **Deployment Options**

#### Option 1: FastAPI Server (Recommended)
```bash
# Start the main FastAPI server with all features
python app_fastapi.py

# Access interfaces:
# 🏠 Homepage: http://localhost:8080
# 📊 Data Analysis: http://localhost:8080/dataanalyst  
# 🗄️ Database Analytics: http://localhost:8080/database
# 📈 Visualization Studio: http://localhost:8080/visualization
# 📖 API Documentation: http://localhost:8080/docs
```



#### Option 2: Docker Deployment (Production)
```bash
# Build and run with Docker
docker build -t autoinsight-ai .
docker run -p 5001:5001 --env-file .env autoinsight-ai

# Access: http://localhost:5001
```

### 🌐 **Live Production Deployment**

The AutoInsight AI platform is deployed and available online:

**🚀 Live Demo**: [https://autoinsight-app-302134120130.asia-south1.run.app](https://autoinsight-app-302134120130.asia-south1.run.app)

**Available Interfaces:**
- 🏠 **Homepage**: [/](https://autoinsight-app-302134120130.asia-south1.run.app/) - Platform overview and navigation
- 📊 **Data Analysis**: [/dataanalyst](https://autoinsight-app-302134120130.asia-south1.run.app/dataanalyst) - Real-time Python code execution
- 🗄️ **Database Analytics**: [/database](https://autoinsight-app-302134120130.asia-south1.run.app/database) - Natural language SQL queries  
- 📈 **Visualization Studio**: [/visualization](https://autoinsight-app-302134120130.asia-south1.run.app/visualization) - Custom chart creation
- 📖 **API Documentation**: [/docs](https://autoinsight-app-302134120130.asia-south1.run.app/docs) - Interactive API docs

**Deployment Details:**
- **Platform**: Google Cloud Run (Asia South 1)
- **Architecture**: Containerized FastAPI application with Docker
- **Scaling**: Auto-scaling based on demand
- **Monitoring**: Health checks and logging enabled

---

## 🎮 Platform Usage Guide

### 🌐 **FastAPI Web Platform** (Primary Interface)
Launch the comprehensive web platform:
```bash
python app_fastapi.py
```

**Platform Features:**
- **Homepage**: Professional portfolio showcase with feature overview
- **Real-time streaming**: Live agent communication with SSE streaming
- **File management**: Upload, download, and manage analysis files
- **API documentation**: Interactive OpenAPI/Swagger documentation

**Access Points:**
- 🏠 **Homepage**: `http://localhost:8080/` - Platform overview and navigation
- 📊 **Data Analysis**: `http://localhost:8080/dataanalyst` - File analysis with real-time Python execution
- 🗄️ **Database Analytics**: `http://localhost:8080/database` - Natural language SQL queries with visualization integration
- 📈 **Visualization Studio**: `http://localhost:8080/visualization` - Custom chart creation with 5+ chart types
- 📖 **API Docs**: `http://localhost:8080/docs` - Interactive API documentation

### 📊 **Data Analysis Agent**
Advanced file analysis with real-time Python code execution:

**Key Capabilities:**
- **Real-time Python execution** in Docker-isolated environment
- **Full library support**: Pandas, NumPy, Matplotlib, Scikit-learn, Seaborn
- **Machine learning workflows**: Model building, hyperparameter tuning, evaluation
- **Multi-format support**: CSV, Excel, JSON file processing
- **Automated visualization**: Graph generation with custom styling

**Example Analysis Tasks:**
```
"Create a correlation matrix and heatmap for all numeric columns"
"Build a machine learning model to predict sales trends"
"Generate statistical summary with outlier detection"
"Perform time series analysis with seasonal decomposition"
"Create interactive dashboard with key performance metrics"
```

### 🗄️ **Database Analytics Agent**
Natural language to SQL conversion with intelligent query optimization:

**Advanced Features:**
- **Smart query suggestions** categorized by complexity (Basic, Intermediate, Advanced)
- **Real-time SQL execution** with formatted result display
- **Schema exploration** and table relationship discovery
- **Direct visualization** integration with chart studio
- **Query optimization** recommendations

**Example Database Queries:**
```
"Show top 10 customers by total order value with year-over-year growth"
"Analyze product performance across different supplier categories"
"Find customers with declining purchase patterns in the last 6 months"
"Compare seasonal sales trends between product categories"
"Identify potential fraud patterns in order data"
```

### 📈 **Visualization Studio**
Professional chart creation with AI-powered recommendations:

**Visualization Capabilities:**
- **5+ Chart Types**: Bar, Line, Scatter, Pie, Histogram with custom styling
- **Full customization**: Colors, themes, legends, annotations
- **High-quality export**: PNG image export with configurable resolution
- **Real-time preview**: Instant chart generation and updates
- **Data integration**: Direct import from database queries or file uploads

**Chart Creation Examples:**
```
"Create a professional sales dashboard with multiple KPIs"
"Generate a correlation scatter plot matrix for feature analysis"  
"Build an interactive time series chart with trend lines"
"Design a comparative bar chart with custom color schemes"
"Create a geographic heat map for regional performance analysis"
```

### 🔄 **Real-Time Streaming Features**
All interfaces support live agent communication:
- **Message streaming**: Real-time conversation flow visualization
- **Progress tracking**: Live execution status and progress indicators
- **Error handling**: Graceful error recovery with detailed diagnostics
- **Result caching**: Efficient data management and retrieval

---

## 📊 Code Examples & API Usage

### FastAPI REST API Examples

#### Database Query API
```python
import requests

# Natural language database query
response = requests.post("http://localhost:8080/api/v1/database/query", 
    json={
        "query": "Show top 5 customers by total order value",
        "reset_context": True
    },
    headers={"Content-Type": "application/json"}
)

# Stream response handling
for line in response.iter_lines():
    if line:
        data = json.loads(line.decode('utf-8').replace('data: ', ''))
        print(f"Type: {data.get('type')}, Content: {data.get('content')}")
```

#### Visualization Creation API
```python
import requests

# Create visualization from data
response = requests.post("http://localhost:8080/api/v1/visualization/create",
    json={
        "data": "Name,Sales,Region\nJohn,1000,North\nJane,1500,South",
        "query": "Create a bar chart showing sales by person",
        "chart_type": "bar"
    }
)

result = response.json()
if result['success']:
    print(f"Visualization created: {result['plot_url']}")
```

#### File Analysis API
```python
import requests

# Upload and analyze file
with open('data.csv', 'rb') as f:
    response = requests.post("http://localhost:8080/api/v1/data-analysis/upload",
        files={"file": f},
        data={"task": "Perform comprehensive statistical analysis"}
    )

# Process streaming analysis results
for line in response.iter_lines():
    if line:
        data = json.loads(line.decode('utf-8').replace('data: ', ''))
        if data.get('type') == 'code_execution':
            print(f"Executed: {data.get('code')}")
        elif data.get('type') == 'analysis_result':
            print(f"Result: {data.get('content')}")
```

### Multi-Agent Team Programming

#### Database Team Usage
```python
from teams import TeamManager
from agent import create_database_agent
from database import DatabaseManager
from config import get_openai_client

# Initialize database team
team_manager = TeamManager()
database_manager = DatabaseManager()
database_manager.connect()

database_team = team_manager.create_db_team(
    create_database_agent(
        get_openai_client(),
        database_manager.get_tools()
    )
)

# Execute natural language query
async def query_database():
    result = database_team.run_stream(
        task="Find customers with orders over $1000 in the last month"
    )
    async for message in result:
        print(f"Agent response: {message}")

asyncio.run(query_database())
```

#### Data Analysis Team Usage
```python
from agent import create_data_analysis_agent, create_code_exuter_agent
from tool import create_docker_cmd_code_excuter
from util.stream_data_anaylisi import run_code_executor_agent_streamlit

# Setup data analysis team
docker = create_docker_cmd_code_excuter()
code_executor = create_code_exuter_agent(docker=docker)
analysis_expert = create_data_analysis_agent(get_openai_client())

data_team = team_manager.create_data_analysis_team(
    openai_client=get_openai_client(),
    DataAnalysisExpert=analysis_expert,
    code_executor_agent=code_executor,
    human_agent=human_agent
)

# Execute analysis task
async def analyze_data():
    async_gen = run_code_executor_agent_streamlit(
        team=data_team,
        docker=docker,
        file_name="sales_data.csv",
        task="Build and evaluate a machine learning model"
    )
    
    async for message_data in async_gen:
        print(f"Analysis step: {message_data}")

asyncio.run(analyze_data())
```

---

## ⚙️ Configuration & Customization

### Environment Variables
| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4o-mini access | Yes | None |
| `PORT` | FastAPI server port | No | 8080 |
| `DEBUG` | Enable debug mode and hot reload | No | False |
| `WORKERS` | Number of Uvicorn workers | No | 1 |

### Model Configuration
Customize AI models in `config/settings.py`:
```python
def get_openai_client(model: str = "gpt-4o-mini", api_key: str = None):
    """Configure OpenAI client with custom model"""
    return OpenAIChatCompletionClient(
        model=model,  # Options: gpt-4o-mini, gpt-4, gpt-3.5-turbo
        api_key=api_key,
        temperature=0.1,  # Adjust for creativity vs accuracy
        max_tokens=2000   # Customize response length
    )
```

### Docker Execution Settings
Modify `tool/docker_executer.py` for custom execution environment:
```python
# Timeout settings
EXECUTION_TIMEOUT = 300  # 5 minutes default

# Pre-installed packages
INITIAL_PACKAGES = [
    "pandas", "numpy", "matplotlib", "seaborn", 
    "scikit-learn", "plotly", "scipy"
]

# Volume mappings for data persistence
VOLUME_MAPPINGS = {
    "./coding": "/workspace/data",
    "./plots": "/workspace/output"
}
```

### Database Configuration
Extend database support in `database/db_manager.py`:
```python
# Support for multiple database types
DATABASE_CONFIGS = {
    "sqlite": "sqlite:///database/ecommerce.db",
    "postgresql": "postgresql://user:pass@localhost/db",
    "mysql": "mysql://user:pass@localhost/db"
}
```

### Custom Agent Creation
Add specialized agents in `agent/` directory:
```python
def create_custom_agent(model_client, specialized_tools):
    """Create domain-specific agent"""
    return AssistantAgent(
        name="CustomAgent",
        model_client=model_client,
        tools=specialized_tools,
        system_message="Your specialized system prompt here",
        description="Agent description for team coordination"
    )
```

---

## 📁 Project Structure & Architecture

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
    └── .gitignore                 # Version control configuration
```

### 🔧 **Key Architecture Components**

#### Agent System (`agent/` + `teams/`)
- **Modular Design**: Each agent has specialized capabilities and tools
- **Team Coordination**: RoundRobinGroupChat manages multi-agent conversations
- **Termination Conditions**: Smart conversation ending with TextMention and MaxMessage limits

#### Tool System (`tool/`)
- **Docker Isolation**: Secure Python code execution with full library support
- **Visualization Engine**: 5+ chart types with custom styling and export
- **Database Toolkit**: LangChain-powered SQL tools with auto-adaptation

#### Streaming Architecture (`util/`)
- **Real-time Communication**: Async streaming for live agent interactions
- **Progress Tracking**: Live execution status and result streaming
- **Error Recovery**: Graceful error handling with diagnostic information

#### Web Platform (`templates/` + `app_fastapi.py`)
- **Multi-Interface Support**: HTML5, Streamlit, and REST APIs
- **Professional UI**: Modern responsive design with CSS3 animations
- **Production Ready**: Health checks, logging, and monitoring endpoints

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

## 👨‍💻 Developer & Author

**Akshay Kumar BM**  
*Senior Software Engineer & AI/ML Specialist*

- 📧 **Email**: [akshaykumarbedre.bm@gmail.com](mailto:akshaykumarbedre.bm@gmail.com)
- 🔗 **LinkedIn**: [linkedin.com/in/akshay-kumar-bm](https://linkedin.com/in/akshay-kumar-bm)
- 🐙 **GitHub**: [github.com/akshaykumarbedre](https://github.com/akshaykumarbedre)

### 🚀 **Technical Expertise**
- **AI/ML Engineering**: Generative AI, OpenAI GPT integration, LLM applications
- **Multi-Agent Systems**: AutoGen framework, agent orchestration, collaborative AI
- **Full-Stack Development**: FastAPI, Streamlit, HTML5/CSS3/JavaScript
- **Data Engineering**: Python, Pandas, NumPy, real-time data processing
- **DevOps & Infrastructure**: Docker containerization, cloud deployment, API design

### 🏆 **Professional Highlights**
- **Enterprise-Grade Architecture**: Production-ready multi-agent platform with real-time streaming
- **Advanced AI Integration**: Seamless OpenAI GPT-4o-mini integration with custom agent workflows
- **Modern Web Development**: Responsive interfaces with professional UI/UX design
- **Security & Isolation**: Docker-based secure code execution environment
- **Scalable Design**: Modular architecture supporting multiple deployment strategies

---


## ⭐ Star this repository if you find it useful!

*Built with ❤️ for the data science and AI community*