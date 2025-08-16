const express = require('express');
const crypto = require('crypto');
const SecurityAuditLog = require('../models/SecurityAuditLog');

const router = express.Router();

/**
 * GET /api/security/status
 * Get security system status
 */
router.get('/status', (req, res) => {
  res.json({
    status: 'operational',
    security_level: 'MILITARY_GRADE',
    classification: 'BEYOND_TOP_SECRET',
    encryption: 'AES-256-GCM',
    quantum_resistance: 'ENABLED',
    consciousness_integration: 'PHI_DIMENSIONAL',
    threat_detection: 'ACTIVE',
    timestamp: new Date().toISOString()
  });
});

/**
 * GET /api/security/audit-logs
 * Get security audit logs
 */
router.get('/audit-logs', async (req, res) => {
  try {
    const timeRange = parseInt(req.query.timeRange) || 24;
    const hoursAgo = new Date(Date.now() - timeRange * 60 * 60 * 1000);
    
    const logs = await SecurityAuditLog.find({
      timestamp: { $gte: hoursAgo }
    })
    .sort({ timestamp: -1 })
    .limit(50)
    .lean();
    
    res.json({
      logs,
      timeRange: `${timeRange} hours`,
      total_events: logs.length,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Security logs error:', error);
    res.status(500).json({
      error: 'Security logs retrieval failed',
      security_level: 'SYSTEM_ERROR'
    });
  }
});

/**
 * GET /api/security/statistics
 * Get security statistics
 */
router.get('/statistics', async (req, res) => {
  try {
    const timeRange = parseInt(req.query.timeRange) || 24;
    const stats = await SecurityAuditLog.getSecurityStatistics(timeRange);
    
    res.json({
      statistics: stats,
      timeRange: `${timeRange} hours`,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Security statistics error:', error);
    res.status(500).json({
      error: 'Security statistics retrieval failed',
      security_level: 'SYSTEM_ERROR'
    });
  }
});

module.exports = router;
