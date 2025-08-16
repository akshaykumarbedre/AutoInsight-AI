/**
 * Visualization Studio Interface
 * Handles data visualization creation and management
 */
class VisualizationStudio {
    constructor() {
        this.currentData = null;
        this.selectedDataType = 'text';
        this.selectedChartType = '';
        this.isProcessing = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.checkUrlParams();
    }
    
    initializeElements() {
        this.dataTextArea = document.getElementById('data-text');
        this.fileInput = document.getElementById('file-input');
        this.fileStatus = document.getElementById('file-status');
        this.dataUrlInput = document.getElementById('data-url-input');
        this.vizQuery = document.getElementById('viz-query');
        this.createVizBtn = document.getElementById('create-viz-btn');
        this.clearBtn = document.getElementById('clear-btn');
        this.previewContainer = document.getElementById('preview-container');
        this.loading = document.getElementById('loading');
        this.messageLog = document.getElementById('message-log');
        this.statusText = document.getElementById('status-text');
        this.toast = document.getElementById('toast');
        this.fileUploadArea = document.querySelector('.file-upload-area');
    }
    
    setupEventListeners() {
        // Data input event listeners
        this.dataTextArea.addEventListener('input', () => this.validateInputs());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.dataUrlInput.addEventListener('input', () => this.validateInputs());
        this.vizQuery.addEventListener('input', () => this.validateInputs());
        
        // File upload drag and drop
        this.fileUploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.fileUploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.fileUploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        
        // Chart type selection
        document.querySelectorAll('.chart-option').forEach(option => {
            option.addEventListener('click', (e) => this.selectChartType(e));
        });
        
        // Action buttons
        this.createVizBtn.addEventListener('click', () => this.createVisualization());
        this.clearBtn.addEventListener('click', () => this.clearAll());
        
        // Initial validation
        this.validateInputs();
    }
    
    checkUrlParams() {
        const urlParams = new URLSearchParams(window.location.search);
        const dataParam = urlParams.get('data');
        
        if (dataParam) {
            try {
                const data = JSON.parse(decodeURIComponent(dataParam));
                this.dataTextArea.value = JSON.stringify(data, null, 2);
                this.currentData = data;
                this.validateInputs();
                this.showToast('Data loaded from database query result');
            } catch (error) {
                console.error('Error parsing URL data:', error);
                this.showToast('Error loading data from URL', 'error');
            }
        }
    }
    
    switchDataTab(tabType) {
        this.selectedDataType = tabType;
        
        // Update tab appearance
        document.querySelectorAll('.data-tab').forEach(tab => tab.classList.remove('active'));
        document.querySelector(`[onclick*="${tabType}"]`).classList.add('active');
        
        // Show/hide panels
        document.querySelectorAll('.data-input-panel').forEach(panel => {
            panel.style.display = 'none';
        });
        document.getElementById(`data-${tabType}`).style.display = 'block';
        
        this.validateInputs();
    }
    
    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.readFile(file);
        }
    }
    
    handleDragOver(event) {
        event.preventDefault();
        this.fileUploadArea.classList.add('dragover');
    }
    
    handleDragLeave(event) {
        event.preventDefault();
        this.fileUploadArea.classList.remove('dragover');
    }
    
    handleDrop(event) {
        event.preventDefault();
        this.fileUploadArea.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            this.readFile(files[0]);
        }
    }
    
    async readFile(file) {
        try {
            this.fileStatus.textContent = `Loading ${file.name}...`;
            const text = await this.fileToText(file);
            
            this.dataTextArea.value = text;
            this.currentData = text;
            this.fileStatus.textContent = `Loaded: ${file.name} (${file.size} bytes)`;
            this.fileStatus.style.color = '#27ae60';
            
            this.validateInputs();
            this.showToast(`File "${file.name}" loaded successfully`);
        } catch (error) {
            this.fileStatus.textContent = `Error loading file: ${error.message}`;
            this.fileStatus.style.color = '#e74c3c';
            this.showToast('Error loading file: ' + error.message, 'error');
        }
    }
    
    fileToText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(new Error('File reading failed'));
            reader.readAsText(file);
        });
    }
    
    async loadDataFromUrl() {
        const url = this.dataUrlInput.value.trim();
        if (!url) return;
        
        try {
            this.statusText.textContent = 'Loading data from URL...';
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const text = await response.text();
            this.dataTextArea.value = text;
            this.currentData = text;
            
            this.statusText.textContent = 'Ready to create visualizations';
            this.validateInputs();
            this.showToast('Data loaded from URL successfully');
        } catch (error) {
            this.statusText.textContent = 'Ready to create visualizations';
            this.showToast('Error loading data from URL: ' + error.message, 'error');
        }
    }
    
    selectChartType(event) {
        // Remove previous selection
        document.querySelectorAll('.chart-option').forEach(option => {
            option.classList.remove('selected');
        });
        
        // Add selection to clicked option
        const option = event.currentTarget;
        option.classList.add('selected');
        this.selectedChartType = option.dataset.type || '';
        
        this.validateInputs();
    }
    
    validateInputs() {
        let hasData = false;
        let hasQuery = false;
        
        // Check data input
        if (this.selectedDataType === 'text') {
            hasData = this.dataTextArea.value.trim().length > 0;
        } else if (this.selectedDataType === 'file') {
            hasData = this.currentData !== null;
        } else if (this.selectedDataType === 'url') {
            hasData = this.dataUrlInput.value.trim().length > 0;
        }
        
        // Check query input
        hasQuery = this.vizQuery.value.trim().length > 0;
        
        // Enable/disable create button
        this.createVizBtn.disabled = !(hasData && hasQuery) || this.isProcessing;
    }
    
    async createVisualization() {
        if (this.isProcessing) return;
        
        const query = this.vizQuery.value.trim();
        let data = '';
        
        // Get data based on selected type
        if (this.selectedDataType === 'text') {
            data = this.dataTextArea.value.trim();
        } else if (this.selectedDataType === 'file') {
            data = this.currentData;
        } else if (this.selectedDataType === 'url') {
            await this.loadDataFromUrl();
            data = this.dataTextArea.value.trim();
        }
        
        if (!data || !query) {
            this.showToast('Please provide both data and visualization request', 'error');
            return;
        }
        
        this.isProcessing = true;
        this.createVizBtn.disabled = true;
        this.loading.classList.add('show');
        this.statusText.textContent = 'Creating visualization...';
        this.showMessageLog();
        this.addLogMessage('info', 'Starting visualization creation...');
        
        try {
            const payload = {
                data: data,
                query: query,
                chart_type: this.selectedChartType
            };
            
            const response = await fetch('/create_visualization', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            this.handleVisualizationResponse(result);
            
        } catch (error) {
            console.error('Error creating visualization:', error);
            this.addLogMessage('error', `Visualization creation failed: ${error.message}`);
            this.showToast('Visualization creation failed: ' + error.message, 'error');
        } finally {
            this.isProcessing = false;
            this.createVizBtn.disabled = false;
            this.loading.classList.remove('show');
            this.statusText.textContent = 'Ready to create visualizations';
            this.validateInputs();
        }
    }
    
    handleVisualizationResponse(result) {
        if (result.status === 'success' && result.plot_path) {
            this.addLogMessage('success', 'Visualization created successfully!');
            this.displayVisualization(result.plot_path);
            this.showToast('Visualization created successfully!');
        } else if (result.status === 'error') {
            this.addLogMessage('error', result.message || 'Unknown error occurred');
            this.showToast('Visualization failed: ' + (result.message || 'Unknown error'), 'error');
        } else {
            this.addLogMessage('error', 'Unexpected response format');
            this.showToast('Unexpected response format', 'error');
        }
    }
    
    displayVisualization(plotPath) {
        const plotUrl = `/static/${plotPath}`;
        
        this.previewContainer.innerHTML = `
            <div class="viz-result">
                <img src="${plotUrl}" alt="Generated Visualization" />
                <div class="viz-actions">
                    <button class="btn btn-secondary btn-small" onclick="downloadVisualization('${plotPath}')">
                        <i class="fas fa-download"></i> Download
                    </button>
                    <button class="btn btn-secondary btn-small" onclick="shareVisualization('${plotPath}')">
                        <i class="fas fa-share"></i> Share
                    </button>
                </div>
            </div>
        `;
    }
    
    showMessageLog() {
        this.messageLog.style.display = 'block';
    }
    
    addLogMessage(type, message) {
        const logDiv = document.createElement('div');
        logDiv.className = `log-message ${type}`;
        logDiv.textContent = `${new Date().toLocaleTimeString()} - ${message}`;
        
        this.messageLog.appendChild(logDiv);
        this.messageLog.scrollTop = this.messageLog.scrollHeight;
    }
    
    clearAll() {
        // Clear all inputs
        this.dataTextArea.value = '';
        this.dataUrlInput.value = '';
        this.vizQuery.value = '';
        this.fileInput.value = '';
        this.fileStatus.textContent = '';
        this.currentData = null;
        
        // Clear chart selection
        document.querySelectorAll('.chart-option').forEach(option => {
            option.classList.remove('selected');
        });
        this.selectedChartType = '';
        
        // Clear preview
        this.previewContainer.innerHTML = `
            <div class="preview-placeholder">
                <i class="fas fa-chart-bar"></i>
                <div>
                    <h3>Your visualization will appear here</h3>
                    <p>Upload data and describe what you want to visualize</p>
                </div>
            </div>
        `;
        
        // Hide message log
        this.messageLog.style.display = 'none';
        this.messageLog.innerHTML = `
            <div class="section-title" style="padding: 10px 15px; margin: 0; border-bottom: 1px solid #e9ecef;">
                <i class="fas fa-list"></i>
                Processing Log
            </div>
        `;
        
        this.validateInputs();
        this.showToast('All fields cleared');
    }
    
    showToast(message, type = 'success') {
        this.toast.textContent = message;
        this.toast.className = `toast ${type} show`;
        
        setTimeout(() => {
            this.toast.classList.remove('show');
        }, 3000);
    }
}

// Global functions
function switchDataTab(tabType) {
    if (window.vizStudio) {
        window.vizStudio.switchDataTab(tabType);
    }
}

function downloadVisualization(plotPath) {
    const link = document.createElement('a');
    link.href = `/static/${plotPath}`;
    link.download = plotPath;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function shareVisualization(plotPath) {
    const url = `${window.location.origin}/static/${plotPath}`;
    
    if (navigator.share) {
        navigator.share({
            title: 'Data Visualization',
            text: 'Check out this visualization created with AutoInsight AI',
            url: url
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(url).then(() => {
            if (window.vizStudio) {
                window.vizStudio.showToast('Visualization URL copied to clipboard');
            }
        });
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.vizStudio = new VisualizationStudio();
});
