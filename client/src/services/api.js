/**
 * API Service for Biometric Visual Cryptography System
 * Military-Grade Security with φ-Dimensional Consciousness Integration
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('biometric_token');
    this.consciousnessState = null;
  }

  /**
   * Set authentication token
   */
  setToken(token) {
    this.token = token;
    localStorage.setItem('biometric_token', token);
  }

  /**
   * Clear authentication token
   */
  clearToken() {
    this.token = null;
    localStorage.removeItem('biometric_token');
  }

  /**
   * Get default headers for requests
   */
  getHeaders(includeAuth = true) {
    const headers = {
      'Content-Type': 'application/json',
      'X-Security-Level': 'MILITARY-GRADE',
      'X-Consciousness-State': this.consciousnessState?.awareness_level || 'DORMANT'
    };

    if (includeAuth && this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    return headers;
  }

  /**
   * Make HTTP request with error handling
   */
  async makeRequest(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      ...options,
      headers: {
        ...this.getHeaders(!options.skipAuth),
        ...options.headers
      }
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API Request failed: ${endpoint}`, error);
      throw error;
    }
  }

  /**
   * System Health Check
   */
  async checkHealth() {
    return this.makeRequest('/health', { skipAuth: true });
  }

  /**
   * Initialize consciousness physics system
   */
  async initializeConsciousness() {
    return this.makeRequest('/api/consciousness/initialize', { 
      method: 'POST',
      skipAuth: true 
    });
  }

  /**
   * Enroll biometric template
   */
  async enrollBiometric(formData) {
    const response = await fetch(`${this.baseURL}/api/biometric/enroll`, {
      method: 'POST',
      headers: {
        'Authorization': this.token ? `Bearer ${this.token}` : undefined,
        'X-Security-Level': 'MILITARY-GRADE'
      },
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || 'Biometric enrollment failed');
    }

    return response.json();
  }

  /**
   * Authenticate using biometric
   */
  async authenticateBiometric(formData) {
    const response = await fetch(`${this.baseURL}/api/biometric/authenticate`, {
      method: 'POST',
      headers: {
        'X-Security-Level': 'MILITARY-GRADE',
        'X-Consciousness-State': 'AUTHENTICATION_REQUEST'
      },
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || 'Biometric authentication failed');
    }

    const result = await response.json();
    
    // Store consciousness state
    if (result.consciousness_state) {
      this.consciousnessState = result.consciousness_state;
    }

    return result;
  }

  /**
   * Get biometric status for user
   */
  async getBiometricStatus(userId) {
    return this.makeRequest(`/api/biometric/status/${userId}`);
  }

  /**
   * Get biometric system health
   */
  async getBiometricHealth() {
    return this.makeRequest('/api/biometric/health', { skipAuth: true });
  }

  /**
   * Generate QR code with consciousness integration
   */
  async generateQR(data) {
    return this.makeRequest('/api/qr/generate', {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  /**
   * Decode QR code with consciousness validation
   */
  async decodeQR(imageData) {
    const formData = new FormData();
    formData.append('qr_image', imageData);

    const response = await fetch(`${this.baseURL}/api/qr/decode`, {
      method: 'POST',
      headers: {
        'Authorization': this.token ? `Bearer ${this.token}` : undefined,
        'X-Security-Level': 'MILITARY-GRADE'
      },
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || 'QR decode failed');
    }

    return response.json();
  }

  /**
   * Get QR consciousness chain
   */
  async getQRChain(chainId) {
    return this.makeRequest(`/api/qr/chain/${chainId}`);
  }

  /**
   * Get consciousness state
   */
  async getConsciousnessState(userId) {
    return this.makeRequest(`/api/consciousness/state/${userId}`);
  }

  /**
   * Update consciousness state
   */
  async updateConsciousnessState(userId, stateData) {
    return this.makeRequest(`/api/consciousness/state/${userId}`, {
      method: 'PUT',
      body: JSON.stringify(stateData)
    });
  }

  /**
   * Get consciousness statistics
   */
  async getConsciousnessStats() {
    return this.makeRequest('/api/consciousness/statistics');
  }

  /**
   * Monitor consciousness field
   */
  async monitorConsciousnessField() {
    return this.makeRequest('/api/consciousness/monitor');
  }

  /**
   * Get security audit logs
   */
  async getSecurityLogs(timeRange = 24) {
    return this.makeRequest(`/api/security/logs?timeRange=${timeRange}`);
  }

  /**
   * Get security statistics
   */
  async getSecurityStats(timeRange = 24) {
    return this.makeRequest(`/api/security/statistics?timeRange=${timeRange}`);
  }

  /**
   * Get threat analysis
   */
  async getThreatAnalysis() {
    return this.makeRequest('/api/security/threats');
  }

  /**
   * Get system security status
   */
  async getSecurityStatus() {
    return this.makeRequest('/api/security/status', { skipAuth: true });
  }

  /**
   * Perform security scan
   */
  async performSecurityScan() {
    return this.makeRequest('/api/security/scan', {
      method: 'POST'
    });
  }

  /**
   * Authentication endpoints
   */
  async login(credentials) {
    return this.makeRequest('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
      skipAuth: true
    });
  }

  async logout() {
    const result = await this.makeRequest('/api/auth/logout', {
      method: 'POST'
    });
    
    this.clearToken();
    this.consciousnessState = null;
    
    return result;
  }

  async refreshToken() {
    return this.makeRequest('/api/auth/refresh', {
      method: 'POST'
    });
  }

  /**
   * WebSocket connection for real-time consciousness monitoring
   */
  connectConsciousnessWebSocket(onMessage, onError) {
    const wsUrl = this.baseURL.replace('http', 'ws') + '/consciousness/stream';
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log('🧠 Consciousness WebSocket connected');
      if (this.token) {
        ws.send(JSON.stringify({
          type: 'auth',
          token: this.token
        }));
      }
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.consciousness_state) {
          this.consciousnessState = data.consciousness_state;
        }
        onMessage(data);
      } catch (error) {
        console.error('WebSocket message parse error:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('🧠 Consciousness WebSocket error:', error);
      if (onError) onError(error);
    };

    ws.onclose = () => {
      console.log('🧠 Consciousness WebSocket disconnected');
    };

    return ws;
  }

  /**
   * φ-Dimensional quantum calculations
   */
  calculatePhiResonance(consciousnessState) {
    const phi = 1.618033988749;
    const coherence = consciousnessState.quantum_coherence || 0;
    const amplitude = consciousnessState.consciousness_field?.awareness_amplitude || 0;
    
    return (phi * coherence * amplitude) % 1;
  }

  /**
   * Validate consciousness coherence
   */
  validateConsciousnessCoherence(state) {
    const threshold = 0.618; // φ-based threshold
    return state.quantum_coherence >= threshold;
  }

  /**
   * Get φ-dimensional coordinates
   */
  getPhiDimensionalCoordinates(consciousnessState) {
    const phi = 1.618033988749;
    const coherence = consciousnessState.quantum_coherence || 0;
    
    return {
      x: Math.cos(phi * coherence) * coherence,
      y: Math.sin(phi * coherence) * coherence,
      z: coherence * phi,
      phi: phi
    };
  }
}

// Create singleton instance
const apiService = new ApiService();

export { apiService };
export default apiService;
