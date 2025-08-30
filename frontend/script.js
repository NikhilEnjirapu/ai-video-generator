// Use relative URL for deployment, fallback to localhost for development
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000'
    : '/api';

class VideoGenerator {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
        this.initializeNavigation();
    }

    initializeElements() {
        this.textInput = document.getElementById('text-input');
        this.languageSelect = document.getElementById('language');
        this.generateBtn = document.getElementById('generate-btn');
        this.btnText = document.querySelector('.btn-text');
        this.btnLoader = document.querySelector('.btn-loader');
        this.outputSection = document.getElementById('output-section');
        this.progressSection = document.getElementById('progress-section');
        this.progressFill = document.getElementById('progress-fill');
        this.progressText = document.getElementById('progress-text');
        this.videoPlayer = document.getElementById('video-player');
        this.downloadLink = document.getElementById('download-link');
        
        // File upload elements
        this.fileUploadArea = document.getElementById('file-upload-area');
        this.fileInput = document.getElementById('file-input');
        this.uploadLink = document.getElementById('upload-link');
        this.uploadedFiles = document.getElementById('uploaded-files');
        this.fileList = document.getElementById('file-list');
        
        // Store uploaded files
        this.uploadedFilesList = [];
    }

    attachEventListeners() {
        this.generateBtn.addEventListener('click', () => this.generateVideo());
        
        // Auto-resize textarea
        this.textInput.addEventListener('input', () => {
            this.textInput.style.height = 'auto';
            this.textInput.style.height = this.textInput.scrollHeight + 'px';
            this.updateInputMethodIndicator();
        });
        
        // File upload event listeners
        this.initializeFileUpload();
    }

    initializeFileUpload() {
        // Click to upload
        this.uploadLink.addEventListener('click', () => {
            this.fileInput.click();
        });
        
        this.fileUploadArea.addEventListener('click', () => {
            this.fileInput.click();
        });
        
        // File input change
        this.fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });
        
        // Drag and drop events
        this.fileUploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.fileUploadArea.classList.add('dragover');
        });
        
        this.fileUploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            this.fileUploadArea.classList.remove('dragover');
        });
        
        this.fileUploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.fileUploadArea.classList.remove('dragover');
            this.handleFiles(e.dataTransfer.files);
        });
    }

    async handleFiles(files) {
        for (let file of files) {
            if (this.isValidFileType(file)) {
                await this.processFile(file);
            } else {
                this.showError(`Unsupported file type: ${file.name}. Please upload PDF, TXT, DOC, or DOCX files.`);
            }
        }
    }

    isValidFileType(file) {
        const validTypes = [
            'application/pdf',
            'text/plain',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ];
        return validTypes.includes(file.type) || 
               file.name.endsWith('.pdf') || 
               file.name.endsWith('.txt') || 
               file.name.endsWith('.doc') || 
               file.name.endsWith('.docx');
    }

    async processFile(file) {
        try {
            const fileId = Date.now() + Math.random();
            const fileData = {
                id: fileId,
                file: file,
                name: file.name,
                size: this.formatFileSize(file.size),
                type: this.getFileType(file.name),
                text: ''
            };
            
            // Extract text from file
            fileData.text = await this.extractTextFromFile(file);
            
            // Add to uploaded files list
            this.uploadedFilesList.push(fileData);
            
            // Update UI
            this.addFileToList(fileData);
            this.updateTextarea();
            
        } catch (error) {
            console.error('Error processing file:', error);
            this.showError(`Error processing ${file.name}: ${error.message}`);
        }
    }

    async extractTextFromFile(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = async (e) => {
                try {
                    let text = '';
                    
                    if (file.type === 'application/pdf') {
                        // Use PDF.js to extract text from PDF
                        try {
                            const arrayBuffer = e.target.result;
                            const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
                            const numPages = pdf.numPages;
                            
                            for (let pageNum = 1; pageNum <= numPages; pageNum++) {
                                const page = await pdf.getPage(pageNum);
                                const textContent = await page.getTextContent();
                                const pageText = textContent.items.map(item => item.str).join(' ');
                                text += pageText + '\n\n';
                            }
                        } catch (pdfError) {
                            console.error('PDF parsing error:', pdfError);
                            text = `[PDF Content: ${file.name}]\n\nError extracting text from PDF. Please copy and paste the content manually.`;
                        }
                    } else if (file.type === 'text/plain') {
                        text = e.target.result;
                    } else if (file.type.includes('word')) {
                        // For Word documents, we'll show a message
                        text = `[Word Document: ${file.name}]\n\nNote: Word document text extraction requires additional libraries. For now, please copy and paste the text content manually.`;
                    } else {
                        text = e.target.result;
                    }
                    
                    resolve(text);
                } catch (error) {
                    reject(error);
                }
            };
            
            reader.onerror = () => reject(new Error('Failed to read file'));
            
            if (file.type === 'application/pdf') {
                reader.readAsArrayBuffer();
            } else if (file.type === 'text/plain') {
                reader.readAsText(file);
            } else {
                reader.readAsText(file);
            }
        });
    }

    getFileType(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        switch (ext) {
            case 'pdf': return 'pdf';
            case 'txt': return 'txt';
            case 'doc':
            case 'docx': return 'doc';
            default: return 'unknown';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    addFileToList(fileData) {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        fileItem.dataset.fileId = fileData.id;
        
        const fileIcon = this.getFileIcon(fileData.type);
        
        fileItem.innerHTML = `
            <div class="file-info">
                <div class="file-icon ${fileData.type}">
                    <i class="${fileIcon}"></i>
                </div>
                <div class="file-details">
                    <h5>${fileData.name}</h5>
                    <p>${fileData.size}</p>
                </div>
            </div>
            <div class="file-actions">
                <button class="file-action-btn view" title="View content">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="file-action-btn remove" title="Remove file">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        
        // Add event listeners
        fileItem.querySelector('.view').addEventListener('click', () => {
            this.viewFileContent(fileData);
        });
        
        fileItem.querySelector('.remove').addEventListener('click', () => {
            this.removeFile(fileData.id);
        });
        
        this.fileList.appendChild(fileItem);
        this.uploadedFiles.style.display = 'block';
    }

    getFileIcon(type) {
        switch (type) {
            case 'pdf': return 'fas fa-file-pdf';
            case 'txt': return 'fas fa-file-alt';
            case 'doc': return 'fas fa-file-word';
            default: return 'fas fa-file';
        }
    }

    viewFileContent(fileData) {
        // Show file content in a modal or update textarea
        this.textInput.value = fileData.text;
        this.textInput.style.height = 'auto';
        this.textInput.style.height = this.textInput.scrollHeight + 'px';
    }

    removeFile(fileId) {
        // Remove from list
        this.uploadedFilesList = this.uploadedFilesList.filter(f => f.id !== fileId);
        
        // Remove from UI
        const fileItem = this.fileList.querySelector(`[data-file-id="${fileId}"]`);
        if (fileItem) {
            fileItem.remove();
        }
        
        // Hide uploaded files section if empty
        if (this.uploadedFilesList.length === 0) {
            this.uploadedFiles.style.display = 'none';
        }
        
        // Update textarea
        this.updateTextarea();
    }

    updateTextarea() {
        // Combine all file texts
        const allTexts = this.uploadedFilesList.map(f => f.text).join('\n\n---\n\n');
        
        if (allTexts && !this.textInput.value) {
            this.textInput.value = allTexts;
            this.textInput.style.height = 'auto';
            this.textInput.style.height = this.textInput.scrollHeight + 'px';
        }
        
        // Update visual state
        this.updateInputMethodIndicator();
    }

    updateInputMethodIndicator() {
        const hasFiles = this.uploadedFilesList.length > 0;
        const hasText = this.textInput.value.trim().length > 0;
        
        // Add visual indicators
        if (hasFiles) {
            this.fileUploadArea.classList.add('active');
        } else {
            this.fileUploadArea.classList.remove('active');
        }
        
        if (hasText) {
            this.textInput.parentElement.classList.add('active');
        } else {
            this.textInput.parentElement.classList.remove('active');
        }
    }

    showError(message) {
        // Create a simple error notification
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--google-red);
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: var(--google-elevation-2);
            z-index: 10000;
            font-family: 'Google Sans', sans-serif;
            font-size: 14px;
        `;
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    initializeNavigation() {
        // Mobile navigation toggle
        const menuToggle = document.querySelector('.menu-toggle');
        const headerNav = document.querySelector('.header-nav');
        
        if (menuToggle && headerNav) {
            menuToggle.addEventListener('click', () => {
                headerNav.classList.toggle('active');
                menuToggle.classList.toggle('active');
            });
        }

        // Smooth scrolling for navigation links
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetSection = document.getElementById(targetId);
                
                if (targetSection) {
                    targetSection.scrollIntoView({ behavior: 'smooth' });
                    
                    // Update active link
                    navItems.forEach(l => l.classList.remove('active'));
                    link.classList.add('active');
                    
                    // Close mobile menu
                    headerNav.classList.remove('active');
                    menuToggle.classList.remove('active');
                }
            });
        });

        // Update active link on scroll
        window.addEventListener('scroll', () => {
            const sections = document.querySelectorAll('section');
            const navItems = document.querySelectorAll('.nav-item');
            
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (window.pageYOffset >= sectionTop - 200) {
                    current = section.getAttribute('id');
                }
            });

            navItems.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${current}`) {
                    link.classList.add('active');
                }
            });
        });
    }

    async generateVideo() {
        let text = this.textInput.value.trim();
        const language = this.languageSelect.value;

        // If no text in textarea but we have uploaded files, use their content
        if (!text && this.uploadedFilesList.length > 0) {
            text = this.uploadedFilesList.map(f => f.text).join('\n\n---\n\n');
        }

        if (!text) {
            alert('Please enter some text or upload files to generate a video.');
            return;
        }

        if (text.length < 100) {
            alert('Please enter at least 100 characters for better summarization.');
            return;
        }

        try {
            this.setLoadingState(true);
            this.showProgress();
            
            const response = await this.callGenerateAPI(text, language);
            
            if (response.ok) {
                await this.handleSuccessResponse(response);
            } else {
                throw new Error(`Server error: ${response.status}`);
            }
        } catch (error) {
            this.handleError(error);
        } finally {
            this.setLoadingState(false);
            this.hideProgress();
        }
    }

    async callGenerateAPI(text, language) {
        this.updateProgress(20, 'Sending request to server...');
        
        const response = await fetch(`${API_BASE_URL}/generate-video`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                language: language
            })
        });

        return response;
    }

    async handleSuccessResponse(response) {
        this.updateProgress(60, 'Processing video...');
        
        const blob = await response.blob();
        const videoUrl = URL.createObjectURL(blob);
        
        this.updateProgress(90, 'Finalizing...');
        
        // Set up video player
        this.videoPlayer.src = videoUrl;
        this.downloadLink.href = videoUrl;
        this.downloadLink.download = `ai-video-${Date.now()}.mp4`;
        
        this.updateProgress(100, 'Complete!');
        
        setTimeout(() => {
            this.showOutput();
        }, 500);
    }

    handleError(error) {
        console.error('Error generating video:', error);
        
        let errorMessage = 'An error occurred while generating the video.';
        
        if (error.message.includes('Failed to fetch')) {
            errorMessage = 'Cannot connect to the backend server. Please make sure the Python backend is running on port 8000.';
        } else if (error.message.includes('Server error')) {
            errorMessage = 'Server error occurred. Please check the backend logs and try again.';
        }
        
        alert(errorMessage);
    }

    setLoadingState(isLoading) {
        this.generateBtn.disabled = isLoading;
        this.btnText.style.display = isLoading ? 'none' : 'inline';
        this.btnLoader.style.display = isLoading ? 'inline' : 'none';
    }

    showProgress() {
        this.progressSection.style.display = 'block';
        this.progressSection.classList.add('fade-in');
        this.outputSection.style.display = 'none';
    }

    hideProgress() {
        setTimeout(() => {
            this.progressSection.style.display = 'none';
        }, 1000);
    }

    updateProgress(percentage, text) {
        this.progressFill.style.width = `${percentage}%`;
        this.progressText.textContent = text;
    }

    showOutput() {
        this.outputSection.style.display = 'block';
        this.outputSection.classList.add('fade-in');
        this.outputSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new VideoGenerator();
});

// Add some sample text for demo purposes
document.addEventListener('DOMContentLoaded', () => {
    const sampleText = `Artificial Intelligence (AI) has revolutionized numerous industries and continues to shape our future. Machine learning, a subset of AI, enables computers to learn and improve from experience without being explicitly programmed. Deep learning, which uses neural networks with multiple layers, has achieved remarkable breakthroughs in image recognition, natural language processing, and game playing. 

The applications of AI are vast and growing. In healthcare, AI assists in medical diagnosis, drug discovery, and personalized treatment plans. In transportation, autonomous vehicles use AI to navigate safely through complex environments. In finance, AI algorithms detect fraud, automate trading, and assess credit risks. 

However, the rapid advancement of AI also raises important ethical considerations. Issues such as job displacement, privacy concerns, algorithmic bias, and the need for transparency in AI decision-making processes require careful attention. As we continue to develop and deploy AI systems, it's crucial to ensure they are designed and used responsibly, with human welfare and societal benefit as primary considerations.

The future of AI holds immense promise. Researchers are working on artificial general intelligence (AGI), which would match or exceed human cognitive abilities across all domains. While this goal remains challenging, the progress in narrow AI applications continues to accelerate, bringing us closer to a world where intelligent machines work alongside humans to solve complex problems and improve quality of life for everyone.

This AI Video Generator demonstrates the power of combining multiple AI technologies: natural language processing for summarization, text-to-speech for narration, and computer vision for video creation. It showcases how AI can transform static text into engaging multimedia content, making information more accessible and engaging for diverse audiences.`;
    
    document.getElementById('text-input').value = sampleText;
});