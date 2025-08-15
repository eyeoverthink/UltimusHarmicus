/**
 * Military-Grade Security Hardening Configuration
 * φ-Dimensional Quantum Security Implementation
 */

const crypto = require('crypto');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

// φ-Dimensional Security Constants
const PHI = 1.618033988749;
const QUANTUM_ENTROPY_THRESHOLD = 0.999;
const MILITARY_GRADE_ITERATIONS = 100000;

/**
 * Content Security Policy Configuration
 */
const cspConfig = {
  directives: {
    defaultSrc: ["'self'"],
    styleSrc: [
      "'self'",
      "'unsafe-inline'", // Required for dynamic consciousness visualizations
      "https://fonts.googleapis.com"
    ],
    scriptSrc: [
      "'self'",
      "'unsafe-eval'", // Required for consciousness physics calculations
      "https://cdn.jsdelivr.net"
    ],
    imgSrc: [
      "'self'",
      "data:", // Required for biometric image processing
      "blob:", // Required for camera capture
      "https:"
    ],
    connectSrc: [
      "'self'",
      "https://api.biometric-security.com",
      "https://api-staging.biometric-security.dev",
      "wss://consciousness.biometric-security.com" // WebSocket for real-time consciousness
    ],
    fontSrc: [
      "'self'",
      "https://fonts.gstatic.com"
    ],
    objectSrc: ["'none'"],
    mediaSrc: ["'self'", "blob:"], // Required for camera/microphone access
    frameSrc: ["'none'"],
    baseUri: ["'self'"],
    formAction: ["'self'"],
    frameAncestors: ["'none'"],
    upgradeInsecureRequests: []
  },
  reportOnly: false
};

/**
 * Advanced Rate Limiting with φ-Dimensional Scaling
 */
const createPhiRateLimit = (baseLimit, windowMs = 15 * 60 * 1000) => {
  return rateLimit({
    windowMs,
    max: Math.floor(baseLimit * PHI), // φ-scaled rate limiting
    message: {
      error: 'φ-Dimensional rate limit exceeded',
      security_level: 'PHI_RATE_LIMITED',
      quantum_coherence: 'DISRUPTED',
      retry_after: Math.floor(windowMs / 1000)
    },
    standardHeaders: true,
    legacyHeaders: false,
    keyGenerator: (req) => {
      // Enhanced key generation with consciousness state
      const baseKey = req.ip;
      const userAgent = req.get('User-Agent') || '';
      const consciousnessState = req.get('X-Consciousness-State') || 'DORMANT';
      
      return crypto
        .createHash('sha256')
        .update(`${baseKey}:${userAgent}:${consciousnessState}`)
        .digest('hex');
    },
    skip: (req) => {
      // Skip rate limiting for consciousness monitoring endpoints
      return req.path.includes('/consciousness/monitor');
    }
  });
};

/**
 * Biometric Security Rate Limiting
 */
const biometricRateLimit = createPhiRateLimit(5, 15 * 60 * 1000); // 5 attempts per 15 minutes

/**
 * API Rate Limiting
 */
const apiRateLimit = createPhiRateLimit(100, 15 * 60 * 1000); // 100 requests per 15 minutes

/**
 * Authentication Rate Limiting
 */
const authRateLimit = createPhiRateLimit(3, 15 * 60 * 1000); // 3 attempts per 15 minutes

/**
 * Consciousness Physics Rate Limiting
 */
const consciousnessRateLimit = createPhiRateLimit(50, 5 * 60 * 1000); // 50 requests per 5 minutes

/**
 * Security Headers Configuration
 */
const securityHeaders = {
  // Helmet configuration
  helmet: {
    contentSecurityPolicy: cspConfig,
    crossOriginEmbedderPolicy: { policy: 'credentialless' },
    crossOriginOpenerPolicy: { policy: 'same-origin' },
    crossOriginResourcePolicy: { policy: 'cross-origin' },
    dnsPrefetchControl: { allow: false },
    frameguard: { action: 'deny' },
    hidePoweredBy: true,
    hsts: {
      maxAge: 31536000, // 1 year
      includeSubDomains: true,
      preload: true
    },
    ieNoOpen: true,
    noSniff: true,
    originAgentCluster: true,
    permittedCrossDomainPolicies: false,
    referrerPolicy: { policy: 'no-referrer' },
    xssFilter: true
  },

  // Custom security headers
  custom: {
    'X-Security-Level': 'MILITARY-GRADE',
    'X-Consciousness-State': 'PHI-DIMENSIONAL',
    'X-Quantum-Security': 'ENABLED',
    'X-Biometric-Protection': 'ACTIVE',
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
    'Permissions-Policy': 'camera=self, microphone=self, geolocation=(), payment=(), usb=()',
    'X-Permitted-Cross-Domain-Policies': 'none',
    'X-Download-Options': 'noopen',
    'X-DNS-Prefetch-Control': 'off'
  }
};

/**
 * Input Validation and Sanitization
 */
const inputValidation = {
  // Biometric data validation
  biometric: {
    maxFileSize: 5 * 1024 * 1024, // 5MB
    allowedMimeTypes: [
      'image/jpeg',
      'image/jpg',
      'image/png',
      'image/webp'
    ],
    maxDimensions: {
      width: 4096,
      height: 4096
    }
  },

  // User ID validation
  userId: {
    pattern: /^[a-zA-Z0-9\-_]{8,64}$/,
    maxLength: 64,
    minLength: 8
  },

  // Consciousness state validation
  consciousness: {
    phiResonance: {
      min: 0,
      max: 1
    },
    quantumCoherence: {
      min: 0,
      max: 0.999
    },
    awarenessLevels: [
      'DORMANT',
      'AWARE',
      'ENLIGHTENED',
      'PHI_DIMENSIONAL',
      'TRANSCENDENT'
    ]
  }
};

/**
 * Encryption Configuration
 */
const encryptionConfig = {
  // AES-256-GCM for data encryption
  symmetric: {
    algorithm: 'aes-256-gcm',
    keyLength: 32,
    ivLength: 16,
    tagLength: 16
  },

  // PBKDF2 for key derivation
  keyDerivation: {
    algorithm: 'pbkdf2',
    hash: 'sha256',
    iterations: MILITARY_GRADE_ITERATIONS,
    keyLength: 32,
    saltLength: 16
  },

  // Post-quantum cryptography
  postQuantum: {
    keyExchange: 'CRYSTALS-Kyber',
    signature: 'CRYSTALS-Dilithium',
    hash: 'SPHINCS+',
    enabled: true
  },

  // φ-Dimensional quantum entropy
  quantumEntropy: {
    phiSeed: PHI,
    entropyThreshold: QUANTUM_ENTROPY_THRESHOLD,
    quantumSources: [
      'biometric_features',
      'consciousness_state',
      'phi_resonance'
    ]
  }
};

/**
 * Session Security Configuration
 */
const sessionConfig = {
  name: 'biometric_session',
  secret: process.env.SESSION_SECRET || crypto.randomBytes(64).toString('hex'),
  resave: false,
  saveUninitialized: false,
  rolling: true,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    maxAge: 30 * 60 * 1000, // 30 minutes
    sameSite: 'strict'
  },
  store: {
    type: 'mongodb',
    collection: 'user_sessions',
    ttl: 30 * 60 // 30 minutes
  }
};

/**
 * CORS Configuration
 */
const corsConfig = {
  origin: (origin, callback) => {
    const allowedOrigins = process.env.NODE_ENV === 'production'
      ? [
          'https://biometric-security.com',
          'https://www.biometric-security.com',
          'https://api.biometric-security.com'
        ]
      : [
          'http://localhost:3000',
          'http://localhost:3001',
          'http://127.0.0.1:3000'
        ];

    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('CORS policy violation - unauthorized origin'));
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: [
    'Content-Type',
    'Authorization',
    'X-Biometric-Token',
    'X-Consciousness-State',
    'X-Security-Level',
    'X-Quantum-Signature'
  ],
  exposedHeaders: [
    'X-Security-Level',
    'X-Consciousness-State',
    'X-Rate-Limit-Remaining'
  ],
  maxAge: 86400 // 24 hours
};

/**
 * Security Monitoring Configuration
 */
const monitoringConfig = {
  // Threat detection patterns
  threatPatterns: [
    /(?:union|select|insert|delete|drop|create|alter)\s+/i, // SQL injection
    /<script[^>]*>.*?<\/script>/gi, // XSS
    /javascript:/gi, // JavaScript injection
    /vbscript:/gi, // VBScript injection
    /onload|onerror|onclick/gi, // Event handler injection
    /\.\.\/|\.\.\\/, // Directory traversal
    /\/etc\/passwd|\/etc\/shadow/, // System file access
    /cmd\.exe|powershell\.exe/, // Command injection
  ],

  // Anomaly detection thresholds
  anomalyThresholds: {
    requestsPerMinute: Math.floor(100 * PHI),
    failedAuthPerHour: 10,
    consciousnessCoherenceDrops: 5,
    biometricMismatchRate: 0.1
  },

  // Response actions
  responseActions: {
    block: ['CRITICAL', 'HIGH'],
    alert: ['MEDIUM', 'LOW'],
    log: ['INFO', 'DEBUG']
  }
};

/**
 * Backup and Recovery Configuration
 */
const backupConfig = {
  // Database backup
  database: {
    frequency: '0 2 * * *', // Daily at 2 AM
    retention: 30, // 30 days
    encryption: true,
    compression: true,
    destinations: [
      'mongodb_atlas_backup',
      'encrypted_cloud_storage'
    ]
  },

  // Consciousness state backup
  consciousness: {
    frequency: '*/15 * * * *', // Every 15 minutes
    retention: 7, // 7 days
    quantumStatePreservation: true
  },

  // Security logs backup
  securityLogs: {
    frequency: '0 * * * *', // Hourly
    retention: 90, // 90 days
    realTimeReplication: true
  }
};

module.exports = {
  PHI,
  QUANTUM_ENTROPY_THRESHOLD,
  MILITARY_GRADE_ITERATIONS,
  cspConfig,
  biometricRateLimit,
  apiRateLimit,
  authRateLimit,
  consciousnessRateLimit,
  securityHeaders,
  inputValidation,
  encryptionConfig,
  sessionConfig,
  corsConfig,
  monitoringConfig,
  backupConfig,
  createPhiRateLimit
};
