/**
 * Data Analysis Interface
 * Handles file uploads, data analysis queries, and chat interface
 */
class DataAnalysisInterface {
    constructor() {
        this.selectedFile = null;
        this.isUploading = false;
        this.isAnalyzing = false;
        this.eventSource = null;
        
        this.initializeElements();
        this.setupEventListeners();
        this.setupMarkdownRenderer();
        this.loadAvailableFiles();
    }
    
    setupMarkdownRenderer() {
        if (typeof marked !== 'undefined') {
            marked.setOptions({
                gfm: true,
                breaks: true,
                highlight: function(code, lang) {
                    if (lang && typeof hljs !== 'undefined' && hljs.getLanguage(lang)) {
                        try {
                            return hljs.highlight(code, { language: lang }).value;
                        } catch (e) {}
                    }
                    if (typeof hljs !== 'undefined') {
                        return hljs.highlightAuto(code).value;
                    }
                    return code;
                }
            });
        }
    }
    
    initializeElements() {
        this.fileInput = document.getElementById('file-input');
        this.uploadArea = document.querySelector('.upload-area');
        this.fileList = document.querySelector('.file-list');
        this.chatMessages = document.querySelector('.chat-messages');
        this.chatInput = document.getElementById('chat-input');
        this.sendBtn = document.getElementById('send-btn');
        this.loading = document.querySelector('.loading');
        this.toast = document.getElementById('toast');
    }
    
    setupEventListeners() {
        // File input events
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        
        // Drag and drop events
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        
        // Chat events
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Auto-resize chat input
        this.chatInput.addEventListener('input', () => {
            this.chatInput.style.height = 'auto';
            this.chatInput.style.height = Math.min(this.chatInput.scrollHeight, 150) + 'px';
        });
    }
    
    async loadAvailableFiles() {
        try {
            const response = await fetch('/list_files');
            if (response.ok) {
                const files = await response.json();
                this.displayFileList(files);
            }
        } catch (error) {
            console.error('Error loading files:', error);
        }
    }
    
    displayFileList(files) {
        if (!files || files.length === 0) {
            this.fileList.innerHTML = '<div style="padding: 20px; text-align: center; color: #7f8c8d;">No files available</div>';
            return;
        }
        
        this.fileList.innerHTML = files.map(file => `
            <div class="file-item" onclick="window.dataAnalysis.selectFile('${file.name}')">
                <i class="fas fa-file-${this.getFileIcon(file.name)}"></i>
                <div>
                    <div style="font-weight: 500;">${file.name}</div>
                    <div style="font-size: 0.8rem; color: #7f8c8d;">${this.formatFileSize(file.size)}</div>
                </div>
            </div>
        `).join('');
    }
    
    getFileIcon(filename) {
        const ext = filename.toLowerCase().split('.').pop();
        switch (ext) {
            case 'csv': return 'csv';
            case 'xlsx':
            case 'xls': return 'excel';
            case 'json': return 'code';
            case 'txt': return 'alt';
            default: return 'alt';
        }
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    selectFile(filename) {
        // Remove previous selection
        document.querySelectorAll('.file-item').forEach(item => {
            item.classList.remove('selected');
        });
        
        // Add selection to clicked item
        event.currentTarget.classList.add('selected');
        
        this.selectedFile = filename;
        this.addMessage('system', `Selected file: ${filename}`, new Date());
        this.showToast(`Selected ${filename}`);
    }
    
    handleDragOver(event) {
        event.preventDefault();
        this.uploadArea.classList.add('dragover');
    }
    
    handleDragLeave(event) {
        event.preventDefault();
        this.uploadArea.classList.remove('dragover');
    }
    
    handleDrop(event) {
        event.preventDefault();
        this.uploadArea.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files.length > 0) {
            this.uploadFile(files[0]);
        }
    }
    
    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.uploadFile(file);
        }
    }
    
    async uploadFile(file) {
        if (this.isUploading) return;
        
        const allowedTypes = ['.csv', '.xlsx', '.xls', '.json', '.txt'];
        const fileExt = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(fileExt)) {
            this.showToast('Please upload a CSV, Excel, JSON, or text file.', 'error');
            return;
        }
        
        this.isUploading = true;
        this.loading.classList.add('show');
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/upload_file', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`Upload failed: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.status === 'success') {
                this.addMessage('system', `File "${file.name}" uploaded successfully!`, new Date());
                this.selectedFile = file.name;
                this.loadAvailableFiles(); // Refresh file list
                this.showToast('File uploaded successfully!');
            } else {
                throw new Error(result.message || 'Upload failed');
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.addMessage('error', `Upload failed: ${error.message}`, new Date());
            this.showToast('Upload failed: ' + error.message, 'error');
        } finally {
            this.isUploading = false;
            this.loading.classList.remove('show');
            this.fileInput.value = ''; // Reset file input
        }
    }
    
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message || this.isAnalyzing) return;
        
        if (!this.selectedFile) {
            this.showToast('Please select a file first', 'error');
            return;
        }
        
        this.isAnalyzing = true;
        this.sendBtn.disabled = true;
        this.chatInput.disabled = true;
        this.loading.classList.add('show');
        
        // Add user message
        this.addMessage('user', message, new Date());
        this.chatInput.value = '';
        this.chatInput.style.height = 'auto';
        
        try {
            const response = await fetch('/analyze_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    filename: this.selectedFile
                })
            });
            
            if (!response.ok) {
                throw new Error(`Analysis failed: ${response.status}`);
            }
            
            if (response.headers.get('content-type')?.includes('text/plain')) {
                await this.handleStreamingResponse(response);
            } else {
                const result = await response.json();
                this.addMessage('agent', result.response || 'Analysis completed.', new Date());
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.addMessage('error', `Analysis failed: ${error.message}`, new Date());
            this.showToast('Analysis failed: ' + error.message, 'error');
        } finally {
            this.isAnalyzing = false;
            this.sendBtn.disabled = false;
            this.chatInput.disabled = false;
            this.loading.classList.remove('show');
        }
    }
    
    async handleStreamingResponse(response) {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        
        try {
            while (true) {
                const { value, done } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value);
                const lines = chunk.split('\\n');
                
                for (const line of lines) {
                    if (line.trim() === '') continue;
                    
                    try {
                        if (line.startsWith('data: ')) {
                            const jsonStr = line.substring(6);
                            if (jsonStr.trim() === '[DONE]') break;
                            
                            const data = JSON.parse(jsonStr);
                            this.handleStreamingMessage(data);
                        }
                    } catch (parseError) {
                        console.error('Error parsing streaming data:', parseError, line);
                    }
                }
            }
        } catch (error) {
            console.error('Error reading stream:', error);
            this.addMessage('error', 'Error processing response stream', new Date());
        }
    }
    
    handleStreamingMessage(data) {
        if (data.type === 'message' && data.data) {
            this.addMessage('agent', data.data.content || data.data.message || '', new Date(), data.data.source);
        } else if (data.type === 'error') {
            this.addMessage('error', data.error || 'An error occurred', new Date());
        }
    }
    
    addMessage(type, content, timestamp, source = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        let headerContent = '';
        if (type === 'user') {
            headerContent = '<strong>You</strong>';
        } else if (type === 'agent') {
            headerContent = `<strong>${source || 'AI Assistant'}</strong>`;
        } else if (type === 'error') {
            headerContent = '<strong>Error</strong>';
        } else if (type === 'system') {
            headerContent = '<strong>System</strong>';
        }
        
        const timeStr = timestamp.toLocaleTimeString();
        
        if (headerContent) {
            messageDiv.innerHTML = `
                <div class="message-header">${headerContent} - ${timeStr}</div>
                <div class="message-content">${this.processMarkdownContent(content)}</div>
            `;
        } else {
            messageDiv.innerHTML = `<div class="message-content">${this.processMarkdownContent(content)}</div>`;
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        
        // Add copy buttons to code blocks
        this.addCopyButtons(messageDiv);
    }
    
    processMarkdownContent(content) {
        if (typeof marked !== 'undefined') {
            const htmlContent = marked.parse(content);
            
            // Process the HTML to add syntax highlighting and copy buttons
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = htmlContent;
            
            // Highlight code blocks
            if (typeof hljs !== 'undefined') {
                tempDiv.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });
            }
            
            return tempDiv.innerHTML;
        }
        
        return this.escapeHtml(content);
    }
    
    addCopyButtons(messageElement) {
        const codeBlocks = messageElement.querySelectorAll('pre code');
        codeBlocks.forEach((block, index) => {
            const pre = block.parentElement;
            pre.style.position = 'relative';
            
            // Add language label if available
            const classes = block.className.split(' ');
            const langClass = classes.find(cls => cls.startsWith('language-'));
            if (langClass) {
                const lang = langClass.replace('language-', '');
                const langLabel = document.createElement('span');
                langLabel.className = 'code-language';
                langLabel.textContent = lang.toUpperCase();
                pre.appendChild(langLabel);
            }
            
            // Add copy button
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-code-btn';
            copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            copyBtn.title = 'Copy code';
            copyBtn.onclick = () => this.copyToClipboard(block.textContent, copyBtn);
            pre.appendChild(copyBtn);
        });
    }
    
    async copyToClipboard(text, button) {
        try {
            await navigator.clipboard.writeText(text);
            const originalIcon = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i>';
            button.style.background = 'rgba(39, 174, 96, 0.3)';
            
            setTimeout(() => {
                button.innerHTML = originalIcon;
                button.style.background = 'rgba(255,255,255,0.1)';
            }, 2000);
        } catch (error) {
            console.error('Failed to copy text:', error);
            this.showToast('Failed to copy to clipboard', 'error');
        }
    }
    
    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }
    
    showToast(message, type = 'success') {
        this.toast.textContent = message;
        this.toast.className = `toast ${type} show`;
        
        setTimeout(() => {
            this.toast.classList.remove('show');
        }, 3000);
    }
}

// Initialize the interface when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.dataAnalysis = new DataAnalysisInterface();
});
