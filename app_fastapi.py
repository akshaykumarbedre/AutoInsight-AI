"""
AutoInsight AI FastAPI Server
============================
Enterprise-grade FastAPI server for AI-powered data analysis and visualization.
Developed by Senior Software Engineer with experience at Google, Microsoft, and AWS.

This server orchestrates three specialized agent teams:
1. Database Team - Natural language to SQL queries
2. Visualization Team - Data visualization generation  
3. Data Analysis Team - CSV analysis and code execution

Architecture:
- RESTful API design with proper error handling
- Full async support for long-running tasks
- File upload handling for data analysis
- Real-time streaming capabilities
- Production-ready logging and monitoring
- OpenAPI/Swagger documentation
"""

import os
import json
import asyncio
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import threading

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends, BackgroundTasks, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import uvicorn

# Import AutoInsight AI components
from teams.team_manager import TeamManager
from agent import (
    create_database_agent, 
    create_visualization_agent,
    create_data_analysis_agent,
    create_code_exuter_agent,
    create_human_agent
)
from database import DatabaseManager
from config import get_openai_client, load_environment
from tool import (
    create_bar_chart, create_line_chart, create_histogram,
    create_scatter_plot, create_pie_chart, create_docker_cmd_code_excuter
)
from util import stream_db_conversation, display_plot_result

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autoinsight_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Pydantic models for request/response validation
class DatabaseQueryRequest(BaseModel):
    query: str = Field(..., description="Natural language database query")
    reset_context: bool = Field(True, description="Whether to reset conversation context")

class VisualizationRequest(BaseModel):
    data: Optional[str] = Field(None, description="Data to visualize as string (JSON, CSV, or raw text)")
    query: str = Field(..., description="Visualization request description")
    chart_type: Optional[str] = Field(None, description="Preferred chart type")

class DataAnalysisRequest(BaseModel):
    filename: str = Field(..., description="Name of the file to analyze")
    task: str = Field(..., description="Analysis task description")

class TeamResetRequest(BaseModel):
    team: str = Field("all", description="Team to reset: all, database, visualization, data_analysis")

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, Any]

class APIResponse(BaseModel):
    success: bool
    timestamp: str
    data: Optional[Any] = None
    error: Optional[str] = None

class FileListResponse(BaseModel):
    uploaded: List[str]
    plots: List[str]

# Initialize FastAPI app
app = FastAPI(
    title="AutoInsight AI Server",
    description="Enterprise-grade AI-powered data analysis and visualization platform",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
UPLOAD_FOLDER = 'coding'
PLOTS_FOLDER = 'plots'
TEMPLATES_FOLDER = 'templates'
MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB

# Ensure directories exist
for folder in [UPLOAD_FOLDER, PLOTS_FOLDER, TEMPLATES_FOLDER]:
    Path(folder).mkdir(exist_ok=True)

# Mount static files and templates
app.mount("/static", StaticFiles(directory=PLOTS_FOLDER), name="static")
templates = Jinja2Templates(directory=TEMPLATES_FOLDER)

# Global variables for teams and services
team_manager: Optional[TeamManager] = None
database_manager: Optional[DatabaseManager] = None
database_team = None
visualization_team = None
data_analysis_team = None
initialization_lock = threading.Lock()
initialized = False

class AutoInsightServer:
    """Main server class managing all agent teams and operations"""
    
    @staticmethod
    async def initialize_services():
        """Initialize all AI services and teams"""
        global team_manager, database_manager, database_team, visualization_team, data_analysis_team, initialized
        
        with initialization_lock:
            if initialized:
                return
                
            try:
                logger.info("Initializing AutoInsight AI services...")
                
                # Load environment variables
                load_environment()
                
                # Initialize team manager
                team_manager = TeamManager()
                
                # Initialize database manager
                database_manager = DatabaseManager()
                database_manager.connect()
                
                # Get OpenAI client
                openai_client = get_openai_client()
                
                # Create database team
                database_team = team_manager.create_db_team(
                    create_database_agent(
                        openai_client,
                        database_manager.get_tools()
                    )
                )
                
                # Create visualization team
                visualization_team = team_manager.create_visualization_team(
                    create_visualization_agent(
                        openai_client,
                        [
                            create_line_chart, create_pie_chart, create_scatter_plot,
                            create_histogram, create_bar_chart
                        ]
                    )
                )
                
                # Create data analysis team
                docker = create_docker_cmd_code_excuter()
                code_executor_agent = create_code_exuter_agent(docker=docker)
                data_analysis_expert = create_data_analysis_agent(openai_client=openai_client)
                
                # Human agent with server-compatible input function
                def server_human_input(prompt):
                    logger.info(f"Human input requested: {prompt}")
                    return "Approved by server"  # Auto-approve for server mode
                
                human_agent = create_human_agent(Input_funtion=server_human_input)
                
                data_analysis_team = team_manager.create_data_analysis_team(
                    openai_client=openai_client,
                    DataAnalysisExpert=data_analysis_expert,
                    code_executor_agent=code_executor_agent,
                    human_agent=human_agent
                )
                
                initialized = True
                logger.info("AutoInsight AI services initialized successfully")
                
            except Exception as e:
                logger.error(f"Failed to initialize services: {str(e)}")
                logger.error(traceback.format_exc())
                raise

# Dependency to ensure services are initialized
async def ensure_initialized():
    """Dependency to ensure services are initialized"""
    if not initialized:
        await AutoInsightServer.initialize_services()

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    await AutoInsightServer.initialize_services()

# Helper functions for streaming
async def stream_json_response(data_generator, request_info: dict):
    """Stream JSON responses with proper formatting"""
    try:
        # Send initial response structure
        initial_response = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'streaming': True,
            **request_info
        }
        yield f"data: {json.dumps(initial_response)}\n\n"
        
        # Stream the actual data
        async for message in data_generator:
            if isinstance(message, dict):
                stream_data = {
                    'type': 'message',
                    'timestamp': datetime.now().isoformat(),
                    'data': message
                }
            else:
                stream_data = {
                    'type': 'text',
                    'timestamp': datetime.now().isoformat(),
                    'content': str(message)
                }
            
            yield f"data: {json.dumps(stream_data)}\n\n"
            await asyncio.sleep(0.01)  # Small delay to prevent overwhelming the client
        
        # Send completion signal
        completion_response = {
            'type': 'complete',
            'timestamp': datetime.now().isoformat(),
            'success': True
        }
        # yield f"data: {json.dumps(completion_response)}\n\n"
        
    except Exception as e:
        error_response = {
            'type': 'error',
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'error': str(e)
        }
        yield f"data: {json.dumps(error_response)}\n\n"

# API Endpoints

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        status = HealthResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            services={
                "initialized": initialized,
                "database": database_manager is not None,
                "teams": {
                    "database_team": database_team is not None,
                    "visualization_team": visualization_team is not None,
                    "data_analysis_team": data_analysis_team is not None
                }
            }
        )
        return status
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail={"status": "unhealthy", "error": str(e)})

@app.post("/api/v1/database/query")
async def database_query_stream(request: DatabaseQueryRequest, _: None = Depends(ensure_initialized)):
    """
    Process natural language database queries with streaming response
    """
    try:
        logger.info(f"Processing database query: {request.query}")
        
        async def generate_database_response():
            try:
                if request.reset_context:
                    await database_team.reset()
                
                result = database_team.run_stream(task=request.query)
                final_result = None
                
                async for message in stream_db_conversation(result):
                    yield message
                    if isinstance(message, dict) and message.get('type') == 'tool_result' and 'data' in message:
                        final_result = message['data']
                
                # Send final result summary
                if final_result:
                    yield {
                        'type': 'final_result',
                        'data': final_result,
                        'timestamp': datetime.now().isoformat()
                    }
                    
            except Exception as e:
                logger.error(f"Database query processing failed: {str(e)}")
                yield {
                    'type': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        return StreamingResponse(
            stream_json_response(
                generate_database_response(),
                {'query': request.query, 'operation': 'database_query'}
            ),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
        
    except Exception as e:
        logger.error(f"Database query endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/v1/visualization/create")
async def create_visualization(request: VisualizationRequest, _: None = Depends(ensure_initialized)):
    """
    Create data visualizations with normal API response
    """
    try:
        logger.info(f"Processing visualization request: {request.query}")
        
        # Prepare context for visualization agent
        context = ""
        if request.data:
            context += f"Data to visualize: {request.data}\n"
        if request.chart_type:
            context += f"Preferred chart type: {request.chart_type}\n"
        context += f"Request: {request.query}"
        
        # Run visualization team and get result
        result = visualization_team.run_stream(task=context)
        
        # Process the async generator following the same pattern as Streamlit
        plot_path = None
        
        async for message in stream_db_conversation(result):
            print(message)
            if isinstance(message, dict):
                # Handle dictionary messages (streaming conversation)
                logger.debug(f"Received dict message: {message.get('type', 'unknown')}")
            else:
                # Handle final visualization result (same as Streamlit)
                if message:
                    # Check if this is the final message with plot results
                    if hasattr(message, 'messages') and message.messages:
                        # Look for ToolCallExecutionEvent in the messages
                        from autogen_agentchat.messages import ToolCallExecutionEvent
                        import ast
                        
                        for msg in message.messages:
                            if isinstance(msg, ToolCallExecutionEvent):
                                for content_item in msg.content:
                                    try:
                                        if hasattr(content_item, 'content') and content_item.content:
                                            content_str = content_item.content
                                            # Try to parse as literal (dictionary string)
                                            try:
                                                plot_result = ast.literal_eval(content_str)
                                                if isinstance(plot_result, dict) and 'plot_path' in plot_result:
                                                    plot_path = plot_result['plot_path']
                                                    logger.info(f"Plot path extracted from ToolCallExecutionEvent: {plot_path}")
                                                    break
                                            except (ValueError, SyntaxError) as e:
                                                logger.debug(f"Failed to parse content as literal: {e}")
                                                continue
                                    except Exception as e:
                                        logger.debug(f"Error processing content item: {e}")
                                        continue
                            if plot_path:
                                break
                    
                    # Fallback: try the original display_plot_result function
                    if not plot_path:
                        try:
                            plot_path = display_plot_result(message)
                            if plot_path:
                                logger.info(f"Plot path extracted via display_plot_result: {plot_path}")
                        except Exception as e:
                            logger.debug(f"display_plot_result failed: {e}")
                    
                    if plot_path:
                        break
        
        # Prepare response
        response_data = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'query': request.query,
            'operation': 'visualization'
        }
        
        if plot_path:
            response_data['plot_path'] = plot_path
            response_data['message'] = 'Visualization created successfully'
            # Make plot path accessible via the API
            response_data['plot_url'] = f"/api/v1/files/{os.path.basename(plot_path)}"
            logger.info(f"Visualization created successfully: {plot_path}")
        else:
            response_data['success'] = False
            response_data['message'] = 'Failed to create visualization'
            response_data['error'] = 'No plot was generated'
            logger.warning("No plot path found in visualization result")
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        logger.error(f"Visualization endpoint error: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                'success': False,
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'operation': 'visualization'
            }
        )

@app.post("/api/v1/data-analysis/upload")
async def upload_and_analyze_stream(
    file: UploadFile = File(...),
    task: str = Form("Analyze the uploaded data"),
    _: None = Depends(ensure_initialized)
):
    """
    Upload a file and perform data analysis with streaming response
    """
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file selected")
        
        # Check file size
        contents = await file.read()
        if len(contents) > MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Save uploaded file
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        logger.info(f"File uploaded: {filename}, Task: {task}")
        
        async def generate_analysis_response():
            try:
                # Import the streaming function
                from util.stream_data_anaylisi import run_code_executor_agent_streamlit
                
                # Create docker executor
                docker = create_docker_cmd_code_excuter()
                
                # Process the analysis task
                async_gen = run_code_executor_agent_streamlit(
                    team=data_analysis_team,
                    docker=docker,
                    file_name=filename,
                    task=task
                )
                
                # Stream all messages
                async for message_data in async_gen:
                    yield message_data
                    
            except Exception as e:
                logger.error(f"Data analysis processing failed: {str(e)}")
                yield {
                    'type': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        return StreamingResponse(
            stream_json_response(
                generate_analysis_response(),
                {'filename': filename, 'task': task, 'operation': 'data_analysis_upload'}
            ),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Data analysis endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/v1/data-analysis/query")
async def analyze_existing_file_stream(request: DataAnalysisRequest, _: None = Depends(ensure_initialized)):
    """
    Analyze an existing file with a new task using streaming response
    """
    try:
        # Check if file exists
        file_path = os.path.join(UPLOAD_FOLDER, request.filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File {request.filename} not found")
        
        logger.info(f"Analyzing existing file: {request.filename}, Task: {request.task}")
        
        async def generate_file_analysis_response():
            try:
                from util.stream_data_anaylisi import run_code_executor_agent_streamlit
                
                docker = create_docker_cmd_code_excuter()
                
                async_gen = run_code_executor_agent_streamlit(
                    team=data_analysis_team,
                    docker=docker,
                    file_name=request.filename,
                    task=request.task
                )
                
                async for message_data in async_gen:
                    yield message_data
                    
            except Exception as e:
                logger.error(f"File analysis processing failed: {str(e)}")
                yield {
                    'type': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        return StreamingResponse(
            stream_json_response(
                generate_file_analysis_response(),
                {'filename': request.filename, 'task': request.task, 'operation': 'data_analysis_query'}
            ),
            media_type="text/plain",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
        )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File analysis endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/files/{filename}")
async def download_file(filename: str):
    """Download uploaded files or generated plots"""
    try:
        # Check in upload folder first
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type='application/octet-stream'
            )
        
        # Check in plots folder
        file_path = os.path.join(PLOTS_FOLDER, filename)
        if os.path.exists(file_path):
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type='application/octet-stream'
            )
        
        raise HTTPException(status_code=404, detail="File not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File download error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/v1/files", response_model=FileListResponse)
async def list_files():
    """List all available files"""
    try:
        files = FileListResponse(uploaded=[], plots=[])
        
        # List uploaded files
        upload_dir = Path(UPLOAD_FOLDER)
        if upload_dir.exists():
            files.uploaded = [f.name for f in upload_dir.iterdir() if f.is_file()]
        
        # List plot files
        plots_dir = Path(PLOTS_FOLDER)
        if plots_dir.exists():
            files.plots = [f.name for f in plots_dir.iterdir() if f.is_file()]
        
        return files
        
    except Exception as e:
        logger.error(f"File listing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/v1/teams/reset")
async def reset_teams(request: TeamResetRequest, _: None = Depends(ensure_initialized)):
    """Reset all teams to clear context"""
    try:
        try:
            if request.team == 'all':
                await team_manager.reset_teams()
                await team_manager.reset_data_analysis_team()
            elif request.team == 'database':
                await team_manager.reset_db_team()
            elif request.team == 'visualization':
                await team_manager.reset_visualization_team()
            elif request.team == 'data_analysis':
                await team_manager.reset_data_analysis_team()
            else:
                raise HTTPException(status_code=400, detail=f"Unknown team: {request.team}")
            
            logger.info(f"Teams reset successfully: {request.team}")
            return {'success': True, 'team': request.team}
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={'success': False, 'error': str(e)}
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Team reset error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Custom exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

# Root endpoint
@app.get("/")
async def root(request: Request):
    """Serve the main frontend interface"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "AutoInsight AI - Data Analysis Platform"}
    )

@app.get("/database")
async def database_analytics(request: Request):
    """Serve the database analytics interface"""
    return templates.TemplateResponse(
        "database.html",
        {"request": request, "title": "AutoInsight AI - Database Analytics"}
    )

@app.get("/visualization")
async def visualization_studio(request: Request):
    """Serve the data visualization studio interface"""
    return templates.TemplateResponse(
        "visualization.html",
        {"request": request, "title": "AutoInsight AI - Data Visualization Studio"}
    )

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "AutoInsight AI FastAPI Server",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "endpoints": {
            "main": "/",
            "database_analytics": "/database",
            "visualization_studio": "/visualization", 
            "data_analysis": "/",
            "api_docs": "/docs"
        },
        "api_endpoints": {
            "database_query": "/api/v1/database/query",
            "visualization_create": "/api/v1/visualization/create",
            "data_analysis_upload": "/api/v1/data-analysis/upload",
            "data_analysis_query": "/api/v1/data-analysis/query",
            "files_list": "/api/v1/files",
            "teams_reset": "/api/v1/teams/reset"
        }
    }

if __name__ == '__main__':
    print("🚀 Starting AutoInsight AI FastAPI Server...")
    print("🔧 Developed by Senior Software Engineer (ex-Google, Microsoft, AWS)")
    print("📊 Enterprise-grade AI-powered data analysis and visualization")
    print("🌐 FastAPI with full async support and real-time streaming")
    print("-" * 60)
    
    # Run the FastAPI server with uvicorn
    uvicorn.run(
        "app_fastapi:app",
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5002)),
        reload=os.environ.get('DEBUG', 'False').lower() == 'true',
        workers=1,  # Use 1 worker for development, increase for production

    )
