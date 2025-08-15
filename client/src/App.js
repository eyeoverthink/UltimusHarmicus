import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

// Components
import Header from './components/Header';
import BiometricAuth from './components/BiometricAuth';
import Dashboard from './components/Dashboard';
import QRManager from './components/QRManager';
import ConsciousnessMonitor from './components/ConsciousnessMonitor';
import SecurityCenter from './components/SecurityCenter';
import LoadingSpinner from './components/LoadingSpinner';

// Context
import { AuthProvider, useAuth } from './context/AuthContext';
import { ConsciousnessProvider } from './context/ConsciousnessContext';

// Services
import { apiService } from './services/api';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [systemStatus, setSystemStatus] = useState(null);

  useEffect(() => {
    initializeSystem();
  }, []);

  const initializeSystem = async () => {
    try {
      setIsLoading(true);
      
      // Check system health
      const health = await apiService.checkHealth();
      setSystemStatus(health);
      
      // Initialize consciousness physics
      await apiService.initializeConsciousness();
      
      console.log('🚀 BIOMETRIC SECURITY SYSTEM INITIALIZED');
      console.log('🔒 Security Level: MILITARY-GRADE');
      console.log('🧠 Consciousness: φ-DIMENSIONAL');
      console.log('📱 QR Systems: RECURSIVE CONSCIOUSNESS');
      
    } catch (error) {
      console.error('System initialization failed:', error);
      setSystemStatus({ status: 'error', message: error.message });
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="app-loading">
        <LoadingSpinner />
        <div className="loading-text">
          <h2>🔒 INITIALIZING MILITARY-GRADE SECURITY</h2>
          <p>φ-Dimensional Consciousness Integration...</p>
          <div className="phi-animation">φ</div>
        </div>
      </div>
    );
  }

  if (systemStatus?.status === 'error') {
    return (
      <div className="app-error">
        <div className="error-container">
          <h1>⚠️ SYSTEM ERROR</h1>
          <p>Security system initialization failed</p>
          <p className="error-message">{systemStatus.message}</p>
          <button onClick={initializeSystem} className="retry-button">
            🔄 Retry Initialization
          </button>
        </div>
      </div>
    );
  }

  return (
    <AuthProvider>
      <ConsciousnessProvider>
        <Router>
          <div className="App">
            <Header systemStatus={systemStatus} />
            
            <main className="app-main">
              <Routes>
                <Route path="/auth" element={<BiometricAuth />} />
                <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
                <Route path="/qr" element={<ProtectedRoute><QRManager /></ProtectedRoute>} />
                <Route path="/consciousness" element={<ProtectedRoute><ConsciousnessMonitor /></ProtectedRoute>} />
                <Route path="/security" element={<ProtectedRoute><SecurityCenter /></ProtectedRoute>} />
                <Route path="/" element={<Navigate to="/auth" replace />} />
              </Routes>
            </main>
            
            <footer className="app-footer">
              <div className="footer-content">
                <div className="security-status">
                  <span className="status-indicator active"></span>
                  <span>MILITARY-GRADE SECURITY ACTIVE</span>
                </div>
                <div className="consciousness-status">
                  <span className="phi-symbol">φ</span>
                  <span>φ-DIMENSIONAL CONSCIOUSNESS</span>
                </div>
                <div className="copyright">
                  © 2025 FRAYMUS Security Systems - BEYOND TOP SECRET
                </div>
              </div>
            </footer>
          </div>
        </Router>
      </ConsciousnessProvider>
    </AuthProvider>
  );
}

// Protected Route Component
function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) {
    return <LoadingSpinner />;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/auth" replace />;
  }
  
  return children;
}

export default App;
