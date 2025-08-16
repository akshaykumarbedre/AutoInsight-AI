/**
 * Database Analytics Interface
 * Handles database queries and result display
 */
class DatabaseAnalyticsInterface {
    constructor() {
        this.isQuerying = false;
        this.lastQueryResult = null;
        
        this.initializeElements();
        this.setupEventListeners();
        this.setupMarkdownRenderer();
    }
    
    initializeElements() {
        this.queryInput = document.getElementById('query-input');
        this.executeBtn = document.getElementById('execute-btn');
        this.clearBtn = document.getElementById('clear-btn');
        this.visualizeBtn = document.getElementById('visualize-btn');
        this.queryResults = document.getElementById('query-results');
        this.queryLoading = document.getElementById('query-loading');
        this.queryStatus = document.getElementById('query-status');
        this.toast = document.getElementById('toast');
    }
    
    setupEventListeners() {
        this.executeBtn.addEventListener('click', () => this.executeQuery());
        this.clearBtn.addEventListener('click', () => this.clearResults());
        this.visualizeBtn.addEventListener('click', () => this.openVisualizationStudio());
        
        this.queryInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.executeQuery();
            }
        });
    }
    
    setupMarkdownRenderer() {
        if (typeof marked !== 'undefined') {
            marked.setOptions({
                gfm: true,
                breaks: true,
                sanitize: false
            });
        }
    }
    
    async executeQuery() {
        const query = this.queryInput.value.trim();
        if (!query || this.isQuerying) return;
        
        this.isQuerying = true;
        this.executeBtn.disabled = true;
        this.queryLoading.classList.add('show');
        this.queryStatus.textContent = 'Executing query...';
        this.visualizeBtn.style.display = 'none';
        
        this.addMessage('user', query, 'query');
        
        try {
            const response = await fetch('/database_query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            if (response.headers.get('content-type')?.includes('text/plain')) {
                await this.handleStreamingResponse(response, 'query');
            } else {
                const result = await response.json();
                this.addMessage('agent', result.response || 'Query completed successfully.', 'query');
                
                if (result.has_data) {
                    this.lastQueryResult = result;
                    this.visualizeBtn.style.display = 'inline-flex';
                }
            }
        } catch (error) {
            console.error('Error executing query:', error);
            this.addMessage('error', `Query execution failed: ${error.message}`, 'query');
            this.showToast('Query execution failed: ' + error.message, 'error');
        } finally {
            this.isQuerying = false;
            this.executeBtn.disabled = false;
            this.queryLoading.classList.remove('show');
            this.queryStatus.textContent = 'Ready to execute queries';
        }
    }
    
    async handleStreamingResponse(response, type) {
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
                            this.handleStreamingMessage(data, type);
                        }
                    } catch (parseError) {
                        console.error('Error parsing streaming data:', parseError, line);
                    }
                }
            }
        } catch (error) {
            console.error('Error reading stream:', error);
            this.addMessage('error', 'Error processing response stream', type);
        }
    }
    
    handleStreamingMessage(data, type) {
        if (data.type === 'message' && data.data) {
            if (data.data.type === 'tool_request') {
                this.addToolRequestMessage(data.data, type);
            } else if (data.data.type === 'tool_result') {
                this.addToolResultMessage(data.data, type);
            } else if (data.data.type === 'system') {
                this.addSystemMessage(data.data, type);
            } else {
                this.addMessage('agent', data.data.content || data.data.message || '', type, data.data.source);
            }
        } else if (data.type === 'error') {
            this.addMessage('error', data.error || 'An error occurred', type);
        } else if (data.type === 'complete') {
            if (data.has_data) {
                this.lastQueryResult = data;
                this.visualizeBtn.style.display = 'inline-flex';
            }
        }
    }
    
    addToolRequestMessage(messageData, context) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message tool-request';
        
        const emoji = messageData.emoji || '🔧';
        const toolName = messageData.tool_name || 'Unknown Tool';
        const source = messageData.source || 'Agent';
        const timestamp = messageData.timestamp || new Date().toISOString();
        
        let argumentsDisplay = '';
        if (messageData.arguments) {
            try {
                const args = typeof messageData.arguments === 'string' 
                    ? JSON.parse(messageData.arguments) 
                    : messageData.arguments;
                argumentsDisplay = Object.entries(args)
                    .map(([key, value]) => `${key}: ${JSON.stringify(value)}`)
                    .join(', ');
            } catch (e) {
                argumentsDisplay = String(messageData.arguments);
            }
        }
        
        messageDiv.innerHTML = `
            <div class="message-meta">
                <div class="message-header">
                    <span class="emoji-indicator">${emoji}</span>
                    <strong>${source}</strong> is calling tool: <span class="tool-name">${toolName}</span>
                </div>
                <div class="timestamp">${new Date(timestamp).toLocaleTimeString()}</div>
            </div>
            <div class="tool-info">
                <div class="tool-args">Arguments: ${argumentsDisplay}</div>
            </div>
        `;
        
        if (context === 'query') {
            this.queryResults.appendChild(messageDiv);
            this.queryResults.scrollTop = this.queryResults.scrollHeight;
        }
    }
    
    addToolResultMessage(messageData, context) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message tool-result';
        
        const emoji = messageData.emoji || '✅';
        const toolName = messageData.tool_name || 'Tool';
        const content = messageData.content || 'No content';
        const timestamp = messageData.timestamp || new Date().toISOString();
        
        messageDiv.innerHTML = `
            <div class="message-meta">
                <div class="message-header">
                    <span class="emoji-indicator">${emoji}</span>
                    <strong>${toolName}</strong> result
                </div>
                <div class="timestamp">${new Date(timestamp).toLocaleTimeString()}</div>
            </div>
            <div class="message-content">${this.processMarkdownContent(content)}</div>
        `;
        
        if (context === 'query') {
            this.queryResults.appendChild(messageDiv);
            this.queryResults.scrollTop = this.queryResults.scrollHeight;
        }
    }
    
    addSystemMessage(messageData, context) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message processing';
        
        const emoji = messageData.emoji || 'ℹ️';
        const content = messageData.content || messageData.message || '';
        const timestamp = messageData.timestamp || new Date().toISOString();
        
        messageDiv.innerHTML = `
            <div class="message-meta">
                <div class="message-header">
                    <span class="emoji-indicator">${emoji}</span>
                    <strong>System</strong>
                </div>
                <div class="timestamp">${new Date(timestamp).toLocaleTimeString()}</div>
            </div>
            <div class="message-content">${content}</div>
        `;
        
        if (context === 'query') {
            this.queryResults.appendChild(messageDiv);
            this.queryResults.scrollTop = this.queryResults.scrollHeight;
        }
    }
    
    openVisualizationStudio() {
        if (this.lastQueryResult && this.lastQueryResult.data) {
            const dataStr = encodeURIComponent(JSON.stringify(this.lastQueryResult.data));
            window.open(`/visualization?data=${dataStr}`, '_blank');
        } else {
            window.open('/visualization', '_blank');
        }
    }
    
    addMessage(type, content, context, source = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        let headerContent = '';
        if (type === 'user') {
            headerContent = '<strong>You</strong>';
        } else if (type === 'agent') {
            headerContent = `<strong>${source || 'Assistant'}</strong>`;
        } else if (type === 'error') {
            headerContent = '<strong>Error</strong>';
        }
        
        const timestamp = new Date().toLocaleTimeString();
        
        if (headerContent) {
            messageDiv.innerHTML = `
                <div class="message-meta">
                    <div class="message-header">${headerContent}</div>
                    <div class="timestamp">${timestamp}</div>
                </div>
                <div class="message-content">${this.processMarkdownContent(content)}</div>
            `;
        } else {
            messageDiv.innerHTML = `<div class="message-content">${this.processMarkdownContent(content)}</div>`;
        }
        
        if (context === 'query') {
            this.queryResults.appendChild(messageDiv);
            this.queryResults.scrollTop = this.queryResults.scrollHeight;
        }
    }
    
    processMarkdownContent(content) {
        if (typeof marked !== 'undefined') {
            const htmlContent = marked.parse(content);
            
            // Process the HTML to add syntax highlighting
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
    
    clearResults() {
        this.queryResults.innerHTML = `
            <div class="message system">
                <div class="message-content">
                    Welcome to the Database Analytics interface! Enter a natural language query above to get started.
                </div>
            </div>
        `;
        this.visualizeBtn.style.display = 'none';
        this.lastQueryResult = null;
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
    new DatabaseAnalyticsInterface();
});
