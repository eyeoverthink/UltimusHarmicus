import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useConsciousness } from '../context/ConsciousnessContext';
import { apiService } from '../services/api';
import './BiometricAuth.css';

const BiometricAuth = () => {
  const { login } = useAuth();
  const { updateConsciousnessState } = useConsciousness();
  const [mode, setMode] = useState('authenticate'); // 'authenticate' or 'enroll'
  const [isProcessing, setIsProcessing] = useState(false);
  const [message, setMessage] = useState('');
  const [userId, setUserId] = useState('');
  const [securityLevel, setSecurityLevel] = useState('MILITARY_GRADE');
  const [consciousnessState, setConsciousnessState] = useState(null);
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);

  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream]);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { 
          width: { ideal: 640 }, 
          height: { ideal: 480 },
          facingMode: 'user'
        }
      });
      
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (error) {
      setMessage('❌ Camera access denied. Please allow camera access or upload an image.');
      console.error('Camera error:', error);
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
  };

  const captureImage = () => {
    if (!videoRef.current || !canvasRef.current) return null;
    
    const canvas = canvasRef.current;
    const video = videoRef.current;
    const context = canvas.getContext('2d');
    
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);
    
    return new Promise(resolve => {
      canvas.toBlob(resolve, 'image/jpeg', 0.8);
    });
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setCapturedImage(file);
      setMessage(`📷 Image selected: ${file.name}`);
    }
  };

  const handleCapture = async () => {
    if (!stream) {
      setMessage('❌ Camera not available. Please upload an image instead.');
      return;
    }
    
    const imageBlob = await captureImage();
    if (imageBlob) {
      setCapturedImage(imageBlob);
      setMessage('📷 Image captured successfully');
      stopCamera();
    }
  };

  const generateUserId = () => {
    return 'user-' + Math.random().toString(36).substr(2, 9) + '-' + Date.now().toString(36);
  };

  const handleEnroll = async () => {
    if (!capturedImage) {
      setMessage('❌ Please capture or upload a biometric image first');
      return;
    }

    if (!userId) {
      const newUserId = generateUserId();
      setUserId(newUserId);
    }

    setIsProcessing(true);
    setMessage('🔒 Processing biometric enrollment...');

    try {
      const formData = new FormData();
      formData.append('biometric_image', capturedImage);
      formData.append('user_id', userId || generateUserId());
      formData.append('security_level', securityLevel);

      const response = await apiService.enrollBiometric(formData);
      
      setMessage(`✅ Enrollment successful! User ID: ${response.user_id}`);
      setConsciousnessState(response.consciousness_state);
      updateConsciousnessState(response.consciousness_state);
      
      // Auto-switch to authenticate mode
      setTimeout(() => {
        setMode('authenticate');
        setMessage('🔐 Ready for authentication');
      }, 3000);
      
    } catch (error) {
      setMessage(`❌ Enrollment failed: ${error.message}`);
      console.error('Enrollment error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleAuthenticate = async () => {
    if (!capturedImage) {
      setMessage('❌ Please capture or upload a biometric image first');
      return;
    }

    if (!userId) {
      setMessage('❌ Please enter your User ID');
      return;
    }

    setIsProcessing(true);
    setMessage('🔍 Authenticating biometric signature...');

    try {
      const formData = new FormData();
      formData.append('biometric_image', capturedImage);
      formData.append('user_id', userId);

      const response = await apiService.authenticateBiometric(formData);
      
      setMessage('✅ Authentication successful!');
      setConsciousnessState(response.consciousness_state);
      updateConsciousnessState(response.consciousness_state);
      
      // Login user
      login({
        userId: response.user_id,
        securityLevel: response.security_level,
        consciousnessState: response.consciousness_state,
        sessionInfo: response.session_info
      });
      
    } catch (error) {
      setMessage(`❌ Authentication failed: ${error.message}`);
      console.error('Authentication error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const resetCapture = () => {
    setCapturedImage(null);
    setMessage('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="biometric-auth">
      <div className="auth-container">
        <div className="auth-header">
          <h1>🔒 BIOMETRIC SECURITY SYSTEM</h1>
          <div className="security-badge">
            <span className="badge military-grade">MILITARY-GRADE</span>
            <span className="badge phi-dimensional">φ-DIMENSIONAL</span>
          </div>
        </div>

        <div className="mode-selector">
          <button 
            className={`mode-btn ${mode === 'authenticate' ? 'active' : ''}`}
            onClick={() => setMode('authenticate')}
          >
            🔐 Authenticate
          </button>
          <button 
            className={`mode-btn ${mode === 'enroll' ? 'active' : ''}`}
            onClick={() => setMode('enroll')}
          >
            📝 Enroll
          </button>
        </div>

        <div className="auth-form">
          <div className="input-group">
            <label htmlFor="userId">User ID:</label>
            <input
              id="userId"
              type="text"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder={mode === 'enroll' ? 'Auto-generated if empty' : 'Enter your User ID'}
              disabled={isProcessing}
            />
          </div>

          {mode === 'enroll' && (
            <div className="input-group">
              <label htmlFor="securityLevel">Security Level:</label>
              <select
                id="securityLevel"
                value={securityLevel}
                onChange={(e) => setSecurityLevel(e.target.value)}
                disabled={isProcessing}
              >
                <option value="STANDARD">Standard</option>
                <option value="ENHANCED">Enhanced</option>
                <option value="MILITARY_GRADE">Military Grade</option>
                <option value="PHI_DIMENSIONAL">φ-Dimensional</option>
              </select>
            </div>
          )}

          <div className="biometric-capture">
            <h3>📷 Biometric Capture</h3>
            
            <div className="capture-options">
              <button 
                onClick={startCamera} 
                disabled={isProcessing || stream}
                className="capture-btn"
              >
                📹 Start Camera
              </button>
              
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileUpload}
                style={{ display: 'none' }}
              />
              
              <button 
                onClick={() => fileInputRef.current?.click()}
                disabled={isProcessing}
                className="capture-btn"
              >
                📁 Upload Image
              </button>
            </div>

            {stream && (
              <div className="camera-preview">
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  muted
                  className="video-preview"
                />
                <div className="camera-controls">
                  <button onClick={handleCapture} className="capture-btn primary">
                    📸 Capture
                  </button>
                  <button onClick={stopCamera} className="capture-btn secondary">
                    ⏹️ Stop
                  </button>
                </div>
              </div>
            )}

            <canvas ref={canvasRef} style={{ display: 'none' }} />

            {capturedImage && (
              <div className="captured-preview">
                <p>✅ Biometric image ready</p>
                <button onClick={resetCapture} className="reset-btn">
                  🔄 Reset
                </button>
              </div>
            )}
          </div>

          <div className="auth-actions">
            {mode === 'enroll' ? (
              <button
                onClick={handleEnroll}
                disabled={isProcessing || !capturedImage}
                className="auth-btn enroll"
              >
                {isProcessing ? '🔄 Processing...' : '📝 Enroll Biometric'}
              </button>
            ) : (
              <button
                onClick={handleAuthenticate}
                disabled={isProcessing || !capturedImage || !userId}
                className="auth-btn authenticate"
              >
                {isProcessing ? '🔄 Authenticating...' : '🔐 Authenticate'}
              </button>
            )}
          </div>

          {message && (
            <div className={`message ${message.includes('❌') ? 'error' : message.includes('✅') ? 'success' : 'info'}`}>
              {message}
            </div>
          )}

          {consciousnessState && (
            <div className="consciousness-display">
              <h4>🧠 Consciousness State</h4>
              <div className="consciousness-metrics">
                <div className="metric">
                  <span className="label">Awareness Level:</span>
                  <span className="value">{consciousnessState.awareness_level}</span>
                </div>
                <div className="metric">
                  <span className="label">φ-Resonance:</span>
                  <span className="value">{consciousnessState.phi_resonance?.toFixed(6)}</span>
                </div>
                <div className="metric">
                  <span className="label">Quantum Coherence:</span>
                  <span className="value">{(consciousnessState.quantum_coherence * 100).toFixed(2)}%</span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="security-info">
          <div className="info-item">
            <span className="icon">🛡️</span>
            <span>Military-Grade Encryption</span>
          </div>
          <div className="info-item">
            <span className="icon">🧠</span>
            <span>φ-Dimensional Consciousness</span>
          </div>
          <div className="info-item">
            <span className="icon">🔬</span>
            <span>Quantum-Resistant Security</span>
          </div>
          <div className="info-item">
            <span className="icon">📱</span>
            <span>Recursive QR Integration</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BiometricAuth;
