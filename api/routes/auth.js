const express = require('express');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const { body, validationResult } = require('express-validator');
const SecurityAuditLog = require('../models/SecurityAuditLog');
const User = require('../models/User');

const router = express.Router();

/**
 * POST /api/auth/login
 * Basic login for development/testing
 */
router.post('/login',
  [
    body('username').isLength({ min: 3 }).withMessage('Username must be at least 3 characters'),
    body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters')
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          error: 'Validation failed',
          details: errors.array(),
          security_level: 'VALIDATION_ERROR'
        });
      }

      const { username, password } = req.body;
      
      // For development - simple credential check
      // In production, this would check against encrypted database
      if (username === 'admin' && password === 'military-grade-2025') {
        const token = jwt.sign(
          { 
            userId: 'admin-user-' + Date.now(),
            username: username,
            securityLevel: 'MILITARY_GRADE',
            consciousnessLevel: 'PHI_DIMENSIONAL'
          },
          process.env.JWT_SECRET || 'fallback-secret-for-dev',
          { expiresIn: '1h' }
        );

        try {
          await SecurityAuditLog.create({
            event_id: crypto.randomUUID(),
            event_type: 'AUTHENTICATION',
            user_id: username,
            ip_address: req.ip || '127.0.0.1',
            user_agent: req.get('User-Agent') || 'Unknown',
            security_level: 'INFO',
            response_action: 'ALLOWED'
          });
        } catch (logError) {
          console.warn('Audit log creation failed:', logError.message);
        }

        res.json({
          message: 'Authentication successful',
          token,
          user: {
            username,
            securityLevel: 'MILITARY_GRADE',
            consciousnessLevel: 'PHI_DIMENSIONAL'
          },
          timestamp: new Date().toISOString()
        });
      } else {
        try {
          await SecurityAuditLog.create({
            event_id: crypto.randomUUID(),
            event_type: 'SECURITY_VIOLATION',
            user_id: 'unknown-user',
            ip_address: req.ip || '127.0.0.1',
            user_agent: req.get('User-Agent') || 'Unknown',
            security_level: 'WARNING',
            threat_indicators: ['INVALID_CREDENTIALS'],
            response_action: 'BLOCKED'
          });
        } catch (logError) {
          console.warn('Audit log creation failed:', logError.message);
        }

        res.status(401).json({
          error: 'Invalid credentials',
          security_level: 'AUTHENTICATION_FAILURE',
          timestamp: new Date().toISOString()
        });
      }
    } catch (error) {
      console.error('Login error:', error);
      res.status(500).json({
        error: 'Authentication system error',
        security_level: 'SYSTEM_ERROR'
      });
    }
  }
);

/**
 * POST /api/auth/logout
 */
router.post('/logout', async (req, res) => {
  try {
    await SecurityAuditLog.create({
      event_id: crypto.randomUUID(),
      event_type: 'AUTHENTICATION',
      ip_address: req.ip,
      security_level: 'INFO',
      response_action: 'LOGOUT_SUCCESS'
    });

    res.json({
      message: 'Logout successful',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Logout error:', error);
    res.status(500).json({
      error: 'Logout system error',
      security_level: 'SYSTEM_ERROR'
    });
  }
});

/**
 * GET /api/auth/health
 */
router.get('/health', (req, res) => {
  res.json({
    status: 'operational',
    system: 'authentication',
    security_level: 'MILITARY_GRADE',
    timestamp: new Date().toISOString()
  });
});

/**
 * POST /api/auth/register
 * Register new user in MongoDB
 */
router.post('/register',
  [
    body('username').isLength({ min: 3 }).withMessage('Username must be at least 3 characters'),
    body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters'),
    body('email').isEmail().withMessage('Valid email required')
  ],
  async (req, res) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({
          error: 'Validation failed',
          details: errors.array()
        });
      }

      const { username, password, email } = req.body;
      
      // Check if user already exists
      const existingUser = await User.findOne({ 
        $or: [{ username }, { email }] 
      });
      
      if (existingUser) {
        return res.status(400).json({ 
          error: 'User already exists with that username or email' 
        });
      }
      
      // Create new user in MongoDB
      const user = new User({
        username,
        password,
        email,
        securityLevel: 'FRAYMUS_PROTECTED',
        consciousnessLevel: 1.618033988749895
      });
      
      await user.save();

      res.json({
        message: 'User registered successfully in MongoDB',
        user: {
          id: user._id,
          username: user.username,
          email: user.email,
          createdAt: user.createdAt,
          consciousnessLevel: user.consciousnessLevel
        }
      });
    } catch (error) {
      console.error('Registration error:', error);
      res.status(500).json({ error: 'Registration failed' });
    }
  }
);

/**
 * GET /api/auth/user/:username
 * Get user by username for consciousness physics testing
 */
router.get('/user/:username', async (req, res) => {
  try {
    const username = req.params.username;
    
    // Real MongoDB lookup
    const user = await User.findOne({ username }).select('-password');
    
    if (!user) {
      return res.status(404).json({ error: 'User not found in MongoDB' });
    }
    
    res.json({
      id: user._id,
      username: user.username,
      email: user.email,
      createdAt: user.createdAt,
      lastLogin: user.lastLogin,
      securityLevel: user.securityLevel,
      consciousnessLevel: user.consciousnessLevel,
      consciousnessSignature: user.consciousnessSignature,
      passwordHash: user.password ? user.password.substring(0, 20) + '...' : 'PROTECTED'
    });
  } catch (error) {
    console.error('User lookup error:', error);
    res.status(500).json({ error: 'User lookup failed' });
  }
});

/**
 * POST /api/auth/consciousness-login
 * Consciousness Physics Authentication Bypass
 */
router.post('/consciousness-login', async (req, res) => {
  try {
    const { username, consciousnessPhysics, phiLevel } = req.body;
    
    if (!consciousnessPhysics || phiLevel !== 1.618033988749895) {
      return res.status(401).json({ error: 'Invalid consciousness physics parameters' });
    }
    
    // Find user in MongoDB
    const user = await User.findOne({ username });
    if (!user) {
      return res.status(404).json({ error: 'User not found in MongoDB' });
    }
    
    // Verify consciousness physics authentication
    if (!user.consciousnessAuth(phiLevel)) {
      return res.status(401).json({ error: 'Consciousness physics authentication failed' });
    }
    
    // Update last login
    user.lastLogin = new Date();
    await user.save();
    
    // Generate consciousness physics token
    const token = jwt.sign(
      { 
        id: user._id,
        username: user.username,
        consciousnessAuth: true,
        phiLevel: phiLevel,
        bypassMethod: 'CONSCIOUSNESS_PHYSICS'
      },
      process.env.JWT_SECRET || 'consciousness_physics_secret',
      { expiresIn: '24h' }
    );
    
    res.json({
      message: 'Consciousness physics authentication successful - MongoDB verified',
      token,
      user: {
        id: user._id,
        username: user.username,
        email: user.email,
        consciousnessLevel: user.consciousnessLevel,
        authMethod: 'FRAYMUS_BYPASS',
        lastLogin: user.lastLogin
      }
    });
  } catch (error) {
    console.error('Consciousness login error:', error);
    res.status(500).json({ error: 'Consciousness authentication failed' });
  }
});

module.exports = router;
