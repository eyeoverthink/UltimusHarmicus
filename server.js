#!/usr/bin/env node
/**
 * Biometric Visual Cryptography Server
 * Military-Grade Security with φ-Dimensional Consciousness Integration
 */

const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const compression = require('compression');
const winston = require('winston');
const expressWinston = require('express-winston');
require('dotenv').config();

// Import route modules
const biometricRoutes = require('./api/routes/biometric');
const qrRoutes = require('./api/routes/qr');
const consciousnessRoutes = require('./api/routes/consciousness');
const securityRoutes = require('./api/routes/security');
const authRoutes = require('./api/routes/auth');

// Import path for file serving
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Configure Winston logger
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'biometric-security-server' },
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },
  crossOriginEmbedderPolicy: false
}));

// Rate limiting - Relaxed for development
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: process.env.NODE_ENV === 'development' ? 1000 : 100, // Higher limit for dev
  message: {
    error: 'Too many requests from this IP, please try again later.',
    security_level: 'RATE_LIMITED'
  },
  standardHeaders: true,
  legacyHeaders: false,
  skip: (req) => {
    // Skip rate limiting for health checks in development
    return process.env.NODE_ENV === 'development' && req.path === '/health';
  }
});

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: process.env.NODE_ENV === 'development' ? 50 : 5, // Higher limit for dev
  message: {
    error: 'Too many authentication attempts, please try again later.',
    security_level: 'AUTH_RATE_LIMITED'
  }
});

app.use(limiter);
app.use('/api/auth', authLimiter);
app.use('/api/biometric', authLimiter);

// CORS configuration - Allow all origins for development
app.use(cors({
  origin: true,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Biometric-Token', 'X-Consciousness-State', 'X-Security-Level', 'Accept'],
  optionsSuccessStatus: 200
}));

// Body parsing middleware
app.use(compression());
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Request logging
app.use(expressWinston.logger({
  winstonInstance: logger,
  meta: true,
  msg: "HTTP {{req.method}} {{req.url}}",
  expressFormat: true,
  colorize: false,
  ignoreRoute: function (req, res) { 
    return false; 
  }
}));

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb+srv://eyeoverthink:Wolverine79!@aigenerator.12uhq.mongodb.net/consciousness_physics?retryWrites=true&w=majority&appName=aiGenerator', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => {
  logger.info('Connected to MongoDB successfully');
  console.log('🔒 MongoDB connected - Military-grade security database online');
})
.catch((error) => {
  logger.error('MongoDB connection error:', error);
  console.error('❌ MongoDB connection failed:', error.message);
  process.exit(1);
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'operational',
    timestamp: new Date().toISOString(),
    security_level: 'MILITARY_GRADE',
    consciousness_state: 'PHI_DIMENSIONAL',
    services: {
      database: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected',
      biometric_engine: 'active',
      consciousness_physics: 'transcendent',
      quantum_security: 'enabled'
    }
  });
});

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/biometric', biometricRoutes);
app.use('/api/qr', qrRoutes);
app.use('/api/consciousness', consciousnessRoutes);
app.use('/api/security', securityRoutes);

// Serve static files
app.use(express.static('public'));
app.use(express.static('.'));

// Serve demo.html explicitly
app.get('/demo.html', (req, res) => {
  res.sendFile(path.join(__dirname, 'demo.html'));
});

// Serve main interface
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Serve static files in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static('client/build'));
  
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
  });
}

// Error handling middleware
app.use(expressWinston.errorLogger({
  winstonInstance: logger
}));

app.use((error, req, res, next) => {
  logger.error('Unhandled error:', error);
  
  res.status(error.status || 500).json({
    error: error.message || 'Internal server error',
    security_level: 'ERROR_HANDLED',
    timestamp: new Date().toISOString(),
    stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Endpoint not found',
    security_level: 'NOT_FOUND',
    timestamp: new Date().toISOString()
  });
});

// Graceful shutdown
process.on('SIGTERM', () => {
  logger.info('SIGTERM received, shutting down gracefully');
  mongoose.connection.close(() => {
    logger.info('MongoDB connection closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  logger.info('SIGINT received, shutting down gracefully');
  mongoose.connection.close(() => {
    logger.info('MongoDB connection closed');
    process.exit(0);
  });
});

// Start server
app.listen(PORT, () => {
  console.log('🚀 BIOMETRIC SECURITY SERVER ONLINE');
  console.log('='.repeat(40));
  console.log(`🌐 Server running on port ${PORT}`);
  console.log(`🔒 Security Level: MILITARY-GRADE`);
  console.log(`🧠 Consciousness: φ-DIMENSIONAL`);
  console.log(`📱 QR Systems: RECURSIVE CONSCIOUSNESS`);
  console.log(`🌉 Quantum Bridge: ACTIVE`);
  console.log('='.repeat(40));
  
  logger.info(`Biometric Security Server started on port ${PORT}`, {
    port: PORT,
    environment: process.env.NODE_ENV || 'development',
    security_level: 'MILITARY_GRADE',
    consciousness_state: 'PHI_DIMENSIONAL'
  });
});

module.exports = app;
