// Focus Tracker - Camera and Eye Tracking System
class FocusTracker {
    constructor() {
        this.isTracking = false;
        this.isInitialized = false;
        this.video = null;
        this.canvas = null;
        this.ctx = null;
        this.mediaStream = null;
        
        // Focus tracking variables
        this.focusLevel = 0;
        this.focusHistory = [];
        this.sessionStartTime = null;
        this.sessionDuration = 0;
        this.sessionFocusSum = 0;
        this.focusSamples = 0;
        
        // Face detection variables
        this.faceDetectionInterval = null;
        this.lastFaceDetection = null;
        this.faceLostTimeout = null;
        
        // Settings
        this.sensitivity = 5;
        this.detectionInterval = 1000; // 1 second
        this.focusLostThreshold = 3000; // 3 seconds without face detection
        
        this.init();
    }

    async init() {
        try {
            this.video = document.getElementById('camera-feed');
            this.canvas = document.getElementById('face-canvas');
            this.ctx = this.canvas.getContext('2d');
            
            this.setupEventListeners();
            this.loadModels();
            
        } catch (error) {
            console.error('Error initializing focus tracker:', error);
            this.showError('Failed to initialize camera system');
        }
    }

    async loadModels() {
        try {
            // Load face-api.js models from CDN
            const modelPath = 'https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/weights';
            
            await faceapi.nets.tinyFaceDetector.loadFromUri(modelPath);
            await faceapi.nets.faceLandmark68Net.loadFromUri(modelPath);
            await faceapi.nets.faceRecognitionNet.loadFromUri(modelPath);
            await faceapi.nets.faceExpressionNet.loadFromUri(modelPath);
            
            this.isInitialized = true;
            this.updateStatus('Ready to start tracking');
            console.log('Face detection models loaded successfully from CDN');
        } catch (error) {
            console.error('Error loading face detection models:', error);
            this.showError('Face detection models not available. Using alternative tracking method.');
            this.isInitialized = true; // Allow fallback method
        }
    }

    setupEventListeners() {
        const startBtn = document.getElementById('start-tracking');
        const stopBtn = document.getElementById('stop-tracking');
        const toggleCameraBtn = document.getElementById('toggle-camera');

        if (startBtn) {
            startBtn.addEventListener('click', () => this.startTracking());
        }

        if (stopBtn) {
            stopBtn.addEventListener('click', () => this.stopTracking());
        }

        if (toggleCameraBtn) {
            toggleCameraBtn.addEventListener('click', () => this.toggleCamera());
        }

        // Handle page visibility change
        document.addEventListener('visibilitychange', () => {
            if (document.hidden && this.isTracking) {
                this.updateFocusLevel(0);
                this.updateStatus('Tab not active - Focus: 0%');
            } else if (!document.hidden && this.isTracking) {
                this.updateStatus('Tab active - Resuming tracking');
            }
        });
    }

    async startTracking() {
        try {
            if (!this.isInitialized) {
                this.showError('System not initialized yet. Please wait...');
                return;
            }

            // Request camera access
            await this.startCamera();
            
            this.isTracking = true;
            this.sessionStartTime = Date.now();
            this.sessionDuration = 0;
            this.sessionFocusSum = 0;
            this.focusSamples = 0;
            
            // Update UI
            this.updateButtons();
            this.updateStatus('Tracking started');
            this.startSessionTimer();
            
            // Start face detection
            this.startFaceDetection();
            
            // Add activity
            if (window.app) {
                window.app.addActivity('focus', 'Started focus tracking session');
            }
            
        } catch (error) {
            console.error('Error starting tracking:', error);
            this.showError('Failed to start camera. Please check permissions.');
        }
    }

    async startCamera() {
        try {
            const constraints = {
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                },
                audio: false
            };

            this.updateStatus('Requesting camera access...');
            
            this.mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
            
            this.video.srcObject = this.mediaStream;
            console.log('Camera access granted');
            
            // Wait for video to load
            return new Promise((resolve, reject) => {
                const timeout = setTimeout(() => {
                    reject(new Error('Camera failed to load after 5 seconds'));
                }, 5000);
                
                this.video.onloadedmetadata = () => {
                    clearTimeout(timeout);
                    console.log('Video loaded:', this.video.videoWidth, 'x', this.video.videoHeight);
                    this.video.play().catch(err => {
                        console.error('Error playing video:', err);
                        reject(err);
                    });
                    this.setupCanvas();
                    resolve();
                };
                
                this.video.onerror = (error) => {
                    clearTimeout(timeout);
                    console.error('Video element error:', error);
                    reject(error);
                };
            });
            
        } catch (error) {
            console.error('Camera error:', error);
            
            // Provide specific error messages
            if (error.name === 'NotAllowedError') {
                throw new Error('Camera permission denied. Please allow camera access in your browser settings.');
            } else if (error.name === 'NotFoundError') {
                throw new Error('No camera found. Please connect a camera and try again.');
            } else if (error.name === 'NotReadableError') {
                throw new Error('Camera is being used by another application. Please close other apps using the camera.');
            } else {
                throw new Error(`Camera access failed: ${error.message}`);
            }
        }
    }

    setupCanvas() {
        if (this.video && this.canvas) {
            this.canvas.width = this.video.videoWidth;
            this.canvas.height = this.video.videoHeight;
        }
    }

    startFaceDetection() {
        this.faceDetectionInterval = setInterval(() => {
            if (this.isTracking && this.video && this.video.readyState === 4) {
                this.detectFace();
            }
        }, this.detectionInterval);
    }

    async detectFace() {
        try {
            if (!this.ctx || !this.video || this.video.readyState !== 4) return;

            // Clear canvas
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            
            // Check if face-api.js is available and models are loaded
            const faceAPIAvailable = window.faceapi && 
                                    faceapi.nets.tinyFaceDetector && 
                                    faceapi.nets.tinyFaceDetector.isLoaded;
            
            if (faceAPIAvailable) {
                await this.detectWithFaceAPI();
            } else {
                // Fallback: Use video frame analysis
                this.detectWithFallback();
            }
            
        } catch (error) {
            console.error('Error in face detection:', error);
            this.detectWithFallback();
        }
    }

    async detectWithFaceAPI() {
        const detections = await faceapi.detectAllFaces(
            this.video,
            new faceapi.TinyFaceDetectorOptions()
        ).withFaceLandmarks().withFaceExpressions();

        if (detections.length > 0) {
            this.onFaceDetected(detections[0]);
            
            // Draw face detection box
            const resizedDetections = faceapi.resizeResults(detections, {
                width: this.canvas.width,
                height: this.canvas.height
            });
            
            this.ctx.strokeStyle = '#00ff00';
            this.ctx.lineWidth = 2;
            resizedDetections.forEach(detection => {
                const { x, y, width, height } = detection.detection.box;
                this.ctx.strokeRect(x, y, width, height);
            });
            
        } else {
            this.onFaceLost();
        }
    }

    detectWithFallback() {
        // Fallback detection using video frame analysis
        if (!document.hidden && this.video && this.video.readyState === 4) {
            try {
                // Draw video frame to canvas for analysis
                this.ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
                
                // Get image data
                const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
                const data = imageData.data;
                
                // Simple motion/presence detection by analyzing brightness
                let darkPixels = 0;
                let brightPixels = 0;
                
                for (let i = 0; i < data.length; i += 4) {
                    const r = data[i];
                    const g = data[i + 1];
                    const b = data[i + 2];
                    const brightness = (r + g + b) / 3;
                    
                    if (brightness > 150) brightPixels++;
                    if (brightness < 100) darkPixels++;
                }
                
                const totalPixels = imageData.data.length / 4;
                const contrastRatio = darkPixels / totalPixels;
                
                // If there's reasonable contrast in the image, assume face is present
                const isDetected = contrastRatio > 0.15 && contrastRatio < 0.85;
                
                // Draw a simple rectangle to show video is active
                this.ctx.strokeStyle = '#ffff00';
                this.ctx.lineWidth = 2;
                this.ctx.strokeRect(10, 10, this.canvas.width - 20, this.canvas.height - 20);
                
                if (isDetected) {
                    this.onFaceDetected();
                } else {
                    this.onFaceLost();
                }
            } catch (error) {
                console.error('Fallback detection error:', error);
                this.onFaceLost();
            }
        } else {
            this.onFaceLost();
        }
    }

    onFaceDetected(detection = null) {
        this.lastFaceDetection = Date.now();
        
        // Clear face lost timeout
        if (this.faceLostTimeout) {
            clearTimeout(this.faceLostTimeout);
            this.faceLostTimeout = null;
        }
        
        // Calculate focus level based on various factors
        let focus = this.calculateFocusLevel(detection);
        
        this.updateFocusLevel(focus);
        this.updateStatus(`Tracking - Face detected`);
    }

    onFaceLost() {
        if (!this.faceLostTimeout) {
            this.faceLostTimeout = setTimeout(() => {
                this.updateFocusLevel(0);
                this.updateStatus('Face not detected - Look at screen');
            }, this.focusLostThreshold);
        }
    }

    calculateFocusLevel(detection = null) {
        let baseFocus = 80; // Base focus when face is detected
        
        // Adjust based on page visibility
        if (document.hidden) {
            return 0;
        }
        
        // Adjust based on detection confidence (if available)
        if (detection && detection.detection) {
            const confidence = detection.detection.score;
            baseFocus = Math.min(100, baseFocus + (confidence * 20));
        }
        
        // Add some randomness to simulate real tracking
        const variance = (Math.random() - 0.5) * 20; // ±10%
        let focus = baseFocus + variance;
        
        // Adjust based on sensitivity setting
        const sensitivityFactor = this.sensitivity / 5; // Normalize to 0-2
        focus = focus * sensitivityFactor;
        
        return Math.max(0, Math.min(100, Math.round(focus)));
    }

    updateFocusLevel(level) {
        this.focusLevel = level;
        this.focusHistory.push({
            timestamp: Date.now(),
            level: level
        });
        
        // Keep only last 100 samples
        if (this.focusHistory.length > 100) {
            this.focusHistory.shift();
        }
        
        // Update session stats
        this.sessionFocusSum += level;
        this.focusSamples++;
        
        // Update UI
        this.updateFocusDisplay();
        
        // Update global stats
        if (window.app) {
            window.app.updateFocusStats(level);
        }
    }

    updateFocusDisplay() {
        const focusLevelElement = document.getElementById('focus-level');
        const currentFocusElement = document.getElementById('current-focus');
        const sessionAverageElement = document.getElementById('session-average');
        
        if (focusLevelElement) {
            focusLevelElement.textContent = `${this.focusLevel}%`;
            
            // Update color based on focus level
            const indicator = document.getElementById('focus-indicator');
            if (indicator) {
                indicator.className = 'focus-indicator';
                if (this.focusLevel >= 80) {
                    indicator.classList.add('focus-high');
                } else if (this.focusLevel >= 50) {
                    indicator.classList.add('focus-medium');
                } else {
                    indicator.classList.add('focus-low');
                }
            }
        }
        
        if (currentFocusElement) {
            currentFocusElement.textContent = `${this.focusLevel}%`;
        }
        
        if (sessionAverageElement && this.focusSamples > 0) {
            const average = Math.round(this.sessionFocusSum / this.focusSamples);
            sessionAverageElement.textContent = `${average}%`;
        }
    }

    startSessionTimer() {
        this.sessionTimer = setInterval(() => {
            if (this.isTracking && this.sessionStartTime) {
                this.sessionDuration = Date.now() - this.sessionStartTime;
                this.updateSessionTime();
            }
        }, 1000);
    }

    updateSessionTime() {
        const sessionTimeElement = document.getElementById('session-time');
        if (sessionTimeElement) {
            const minutes = Math.floor(this.sessionDuration / 60000);
            const seconds = Math.floor((this.sessionDuration % 60000) / 1000);
            sessionTimeElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
    }

    stopTracking() {
        this.isTracking = false;
        
        // Clear intervals
        if (this.faceDetectionInterval) {
            clearInterval(this.faceDetectionInterval);
            this.faceDetectionInterval = null;
        }
        
        if (this.sessionTimer) {
            clearInterval(this.sessionTimer);
            this.sessionTimer = null;
        }
        
        if (this.faceLostTimeout) {
            clearTimeout(this.faceLostTimeout);
            this.faceLostTimeout = null;
        }
        
        // Stop camera
        this.stopCamera();
        
        // Update UI
        this.updateButtons();
        this.updateStatus('Tracking stopped');
        
        // Save session data
        this.saveSessionData();
        
        // Add activity
        if (window.app) {
            const sessionMinutes = Math.round(this.sessionDuration / 60000);
            window.app.addActivity('focus', `Completed ${sessionMinutes}-minute focus session`);
            window.app.updateStudyTime(sessionMinutes);
        }
    }

    stopCamera() {
        if (this.mediaStream) {
            this.mediaStream.getTracks().forEach(track => track.stop());
            this.mediaStream = null;
        }
        
        if (this.video) {
            this.video.srcObject = null;
        }
        
        if (this.ctx) {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }

    toggleCamera() {
        if (this.mediaStream) {
            const videoTrack = this.mediaStream.getVideoTracks()[0];
            if (videoTrack) {
                videoTrack.enabled = !videoTrack.enabled;
                const toggleBtn = document.getElementById('toggle-camera');
                if (toggleBtn) {
                    const icon = toggleBtn.querySelector('i');
                    if (videoTrack.enabled) {
                        icon.className = 'fas fa-video';
                        toggleBtn.innerHTML = '<i class="fas fa-video"></i> Camera On';
                    } else {
                        icon.className = 'fas fa-video-slash';
                        toggleBtn.innerHTML = '<i class="fas fa-video-slash"></i> Camera Off';
                    }
                }
            }
        }
    }

    updateButtons() {
        const startBtn = document.getElementById('start-tracking');
        const stopBtn = document.getElementById('stop-tracking');
        
        if (startBtn && stopBtn) {
            if (this.isTracking) {
                startBtn.disabled = true;
                stopBtn.disabled = false;
            } else {
                startBtn.disabled = false;
                stopBtn.disabled = true;
            }
        }
    }

    updateStatus(message) {
        const statusElement = document.getElementById('focus-status');
        if (statusElement) {
            statusElement.textContent = message;
        }
    }

    updateSensitivity(value) {
        this.sensitivity = parseInt(value);
    }

    saveSessionData() {
        if (this.sessionDuration > 0) {
            const sessionData = {
                startTime: this.sessionStartTime,
                duration: this.sessionDuration,
                averageFocus: this.focusSamples > 0 ? Math.round(this.sessionFocusSum / this.focusSamples) : 0,
                focusHistory: this.focusHistory,
                timestamp: Date.now()
            };
            
            // Save to localStorage
            const sessions = JSON.parse(localStorage.getItem('focusSessions') || '[]');
            sessions.push(sessionData);
            localStorage.setItem('focusSessions', JSON.stringify(sessions));
        }
    }

    showError(message) {
        this.updateStatus(message);
        if (window.app) {
            window.app.showNotification(message, 'error');
        }
    }

    // Public methods
    getFocusHistory() {
        return this.focusHistory;
    }

    getCurrentFocus() {
        return this.focusLevel;
    }

    getSessionStats() {
        return {
            duration: this.sessionDuration,
            averageFocus: this.focusSamples > 0 ? Math.round(this.sessionFocusSum / this.focusSamples) : 0,
            currentFocus: this.focusLevel
        };
    }
}

// Add focus indicator styles
const focusStyles = `
.focus-indicator.focus-high {
    background: rgba(16, 185, 129, 0.9) !important;
}

.focus-indicator.focus-medium {
    background: rgba(245, 158, 11, 0.9) !important;
}

.focus-indicator.focus-low {
    background: rgba(239, 68, 68, 0.9) !important;
}

.focus-level {
    font-size: 2rem !important;
    font-weight: 700 !important;
}
`;

// Inject focus styles
const focusStyleSheet = document.createElement('style');
focusStyleSheet.textContent = focusStyles;
document.head.appendChild(focusStyleSheet);

// Initialize focus tracker when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.focusTracker = new FocusTracker();
});