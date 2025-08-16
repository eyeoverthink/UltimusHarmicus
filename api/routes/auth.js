const express = require('express');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const { body, validationResult } = require('express-validator');
const SecurityAuditLog = require('../models/SecurityAuditLog');

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

module.exports = router;
