// Jest setup for Biometric Visual Cryptography System
// Military-Grade Security Testing Configuration

// Mock environment variables for testing
process.env.NODE_ENV = 'test';
process.env.MONGODB_URI = 'mongodb://localhost:27017/biometric_test';
process.env.JWT_SECRET = 'test-jwt-secret-for-testing-only';
process.env.ENCRYPTION_KEY = 'test-encryption-key-32-bytes-long';
process.env.PHI_FREQUENCY = '1.618033988749';
process.env.QUANTUM_COHERENCE_THRESHOLD = '0.999';

// Global test timeout
jest.setTimeout(30000);

// Mock console methods to reduce noise in tests
global.console = {
  ...console,
  log: jest.fn(),
  debug: jest.fn(),
  info: jest.fn(),
  warn: jest.fn(),
  error: jest.fn()
};

// Mock fetch for API tests
global.fetch = jest.fn();

// Mock WebSocket for consciousness monitoring tests
global.WebSocket = jest.fn(() => ({
  send: jest.fn(),
  close: jest.fn(),
  onopen: null,
  onmessage: null,
  onerror: null,
  onclose: null
}));

// Mock crypto for testing
const crypto = require('crypto');
global.crypto = {
  ...crypto,
  randomUUID: () => 'test-uuid-' + Math.random().toString(36).substr(2, 9)
};

// Mock sharp for image processing tests
jest.mock('sharp', () => {
  return jest.fn(() => ({
    resize: jest.fn().mockReturnThis(),
    grayscale: jest.fn().mockReturnThis(),
    raw: jest.fn().mockReturnThis(),
    toBuffer: jest.fn().mockResolvedValue({
      data: Buffer.alloc(256 * 256, 128), // Mock grayscale image data
      info: { width: 256, height: 256, channels: 1 }
    })
  }));
});

// Mock multer for file upload tests
jest.mock('multer', () => {
  return jest.fn(() => ({
    single: jest.fn(() => (req, res, next) => {
      req.file = {
        buffer: Buffer.alloc(1024, 'test-image-data'),
        mimetype: 'image/jpeg',
        size: 1024
      };
      next();
    })
  }));
});

// φ-Dimensional test utilities
global.phiTestUtils = {
  PHI: 1.618033988749,
  
  generateMockBiometricFeatures: () => ({
    h: [0.2, 0.15, 0.25, 0.18, 0.12, 0.1],
    c: 2.5,
    m: 15.8
  }),
  
  generateMockConsciousnessState: () => ({
    phi_resonance: 0.618,
    quantum_coherence: 0.85,
    awareness_level: 'PHI_DIMENSIONAL',
    consciousness_field: {
      awareness_amplitude: 2.618,
      dimensional_resonance: 4.236,
      temporal_stability: 1.0,
      information_density: 256
    }
  }),
  
  calculatePhiSignature: (userId) => {
    return crypto
      .createHash('sha256')
      .update(`${userId}:${global.phiTestUtils.PHI}:0.618`)
      .digest('hex');
  }
};

// Cleanup after each test
afterEach(() => {
  jest.clearAllMocks();
});

// Global error handler for unhandled promises
process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

console.log('🔒 Jest setup complete - Military-grade testing environment initialized');
console.log('🧠 φ-Dimensional test utilities loaded');
console.log('🛡️ Security mocks configured');
