const jwt = require('jsonwebtoken');
const SecurityAuditLog = require('../models/SecurityAuditLog');
const crypto = require('crypto');

/**
 * Authentication middleware for military-grade security
 */
const auth = async (req, res, next) => {
  try {
    const token = req.header('Authorization')?.replace('Bearer ', '');
    
    if (!token) {
      await SecurityAuditLog.create({
        event_id: crypto.randomUUID(),
        event_type: 'AUTHORIZATION',
        ip_address: req.ip,
        user_agent: req.get('User-Agent'),
        security_level: 'WARNING',
        threat_indicators: ['MISSING_AUTHENTICATION_TOKEN'],
        response_action: 'BLOCKED'
      });
      
      return res.status(401).json({
        error: 'Access denied - Authentication required',
        security_level: 'UNAUTHORIZED',
        timestamp: new Date().toISOString()
      });
    }

    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET || 'fallback-secret-for-dev');
      req.user = decoded;
      
      // Log successful authentication
      await SecurityAuditLog.create({
        event_id: crypto.randomUUID(),
        event_type: 'AUTHORIZATION',
        user_id: decoded.userId,
        ip_address: req.ip,
        user_agent: req.get('User-Agent'),
        security_level: 'INFO',
        response_action: 'ALLOWED'
      });
      
      next();
    } catch (jwtError) {
      await SecurityAuditLog.create({
        event_id: crypto.randomUUID(),
        event_type: 'SECURITY_VIOLATION',
        ip_address: req.ip,
        user_agent: req.get('User-Agent'),
        security_level: 'ERROR',
        threat_indicators: ['INVALID_JWT_TOKEN'],
        response_action: 'BLOCKED'
      });
      
      return res.status(401).json({
        error: 'Invalid authentication token',
        security_level: 'TOKEN_INVALID',
        timestamp: new Date().toISOString()
      });
    }
  } catch (error) {
    console.error('Auth middleware error:', error);
    
    await SecurityAuditLog.create({
      event_id: crypto.randomUUID(),
      event_type: 'SECURITY_VIOLATION',
      ip_address: req.ip,
      security_level: 'CRITICAL',
      threat_indicators: ['AUTHENTICATION_SYSTEM_ERROR'],
      response_action: 'ERROR_LOGGED'
    });
    
    res.status(500).json({
      error: 'Authentication system error',
      security_level: 'SYSTEM_ERROR',
      timestamp: new Date().toISOString()
    });
  }
};

module.exports = auth;
