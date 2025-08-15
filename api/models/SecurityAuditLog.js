const mongoose = require('mongoose');

const SecurityAuditLogSchema = new mongoose.Schema({
  event_id: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  
  event_type: {
    type: String,
    required: true,
    enum: [
      'AUTHENTICATION',
      'AUTHORIZATION',
      'BIOMETRIC_ENROLLMENT',
      'BIOMETRIC_AUTHENTICATION',
      'CONSCIOUSNESS_STATE_CHANGE',
      'SECURITY_VIOLATION',
      'SYSTEM_ACCESS',
      'DATA_ACCESS',
      'CONFIGURATION_CHANGE',
      'PHI_DIMENSIONAL_EVENT',
      'QUANTUM_ENTANGLEMENT',
      'THREAT_DETECTION'
    ],
    index: true
  },
  
  timestamp: {
    type: Date,
    default: Date.now,
    index: true
  },
  
  user_id: {
    type: String,
    index: true,
    validate: {
      validator: function(v) {
        return !v || /^[a-zA-Z0-9\-_]{8,64}$/.test(v);
      },
      message: 'Invalid user ID format'
    }
  },
  
  ip_address: {
    type: String,
    required: true,
    validate: {
      validator: function(v) {
        const ipv4Regex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
        const ipv6Regex = /^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$/;
        return ipv4Regex.test(v) || ipv6Regex.test(v);
      },
      message: 'Invalid IP address format'
    }
  },
  
  user_agent: {
    type: String,
    maxlength: 500
  },
  
  session_id: {
    type: String,
    index: true
  },
  
  biometric_data: {
    authentication_result: Boolean,
    confidence_score: {
      type: Number,
      min: 0,
      max: 1
    },
    liveness_detection: Boolean,
    anti_spoofing_result: Boolean,
    feature_quality_score: {
      type: Number,
      min: 0,
      max: 1
    }
  },
  
  consciousness_data: {
    previous_level: {
      type: String,
      enum: ['DORMANT', 'AWARE', 'ENLIGHTENED', 'PHI_DIMENSIONAL', 'TRANSCENDENT']
    },
    new_level: {
      type: String,
      enum: ['DORMANT', 'AWARE', 'ENLIGHTENED', 'PHI_DIMENSIONAL', 'TRANSCENDENT']
    },
    coherence_change: Number,
    phi_resonance: Number,
    dimensional_shift: Boolean
  },
  
  security_level: {
    type: String,
    required: true,
    enum: ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
    index: true
  },
  
  threat_indicators: [{
    type: String,
    enum: [
      'BRUTE_FORCE_ATTACK',
      'SQL_INJECTION_ATTEMPT',
      'XSS_ATTEMPT',
      'CSRF_ATTEMPT',
      'BIOMETRIC_SPOOFING',
      'CONSCIOUSNESS_MANIPULATION',
      'PHI_DIMENSIONAL_BREACH',
      'QUANTUM_INTERFERENCE',
      'UNAUTHORIZED_ACCESS',
      'PRIVILEGE_ESCALATION',
      'DATA_EXFILTRATION',
      'ANOMALOUS_BEHAVIOR',
      'RATE_LIMIT_EXCEEDED',
      'INVALID_CREDENTIALS',
      'SUSPICIOUS_LOCATION',
      'DEVICE_FINGERPRINT_MISMATCH'
    ]
  }],
  
  response_action: {
    type: String,
    required: true,
    enum: [
      'ALLOWED',
      'BLOCKED',
      'RATE_LIMITED',
      'QUARANTINED',
      'ALERTED',
      'LOGGED',
      'ESCALATED',
      'CONSCIOUSNESS_STABILIZED',
      'PHI_DIMENSIONAL_SECURED',
      'QUANTUM_ENTANGLEMENT_BROKEN'
    ]
  },
  
  request_details: {
    method: String,
    url: String,
    headers: mongoose.Schema.Types.Mixed,
    body_hash: String, // SHA-256 hash of request body for audit
    response_status: Number,
    response_time_ms: Number
  },
  
  geolocation: {
    country: String,
    region: String,
    city: String,
    latitude: Number,
    longitude: Number,
    timezone: String
  },
  
  device_fingerprint: {
    browser: String,
    os: String,
    device_type: String,
    screen_resolution: String,
    timezone_offset: Number,
    language: String,
    fingerprint_hash: String
  },
  
  phi_dimensional_metrics: {
    phi_signature: String,
    dimensional_coordinates: {
      x: Number,
      y: Number,
      z: Number,
      phi: Number
    },
    quantum_coherence: {
      type: Number,
      min: 0,
      max: 0.999
    },
    consciousness_field_strength: Number
  },
  
  additional_metadata: mongoose.Schema.Types.Mixed,
  
  correlation_id: {
    type: String,
    index: true
  },
  
  severity_score: {
    type: Number,
    min: 0,
    max: 100,
    default: 0
  }
}, {
  timestamps: true,
  collection: 'security_audit_logs'
});

// Indexes for performance and security analysis
SecurityAuditLogSchema.index({ timestamp: -1, security_level: 1 });
SecurityAuditLogSchema.index({ user_id: 1, timestamp: -1 });
SecurityAuditLogSchema.index({ ip_address: 1, timestamp: -1 });
SecurityAuditLogSchema.index({ event_type: 1, timestamp: -1 });
SecurityAuditLogSchema.index({ threat_indicators: 1 });
SecurityAuditLogSchema.index({ severity_score: -1 });
SecurityAuditLogSchema.index({ correlation_id: 1 });

// TTL index for automatic log cleanup (90 days)
SecurityAuditLogSchema.index({ timestamp: 1 }, { expireAfterSeconds: 7776000 });

// Instance methods
SecurityAuditLogSchema.methods.calculateSeverityScore = function() {
  let score = 0;
  
  // Base score by security level
  const levelScores = {
    'DEBUG': 0,
    'INFO': 10,
    'WARNING': 30,
    'ERROR': 60,
    'CRITICAL': 90
  };
  
  score += levelScores[this.security_level] || 0;
  
  // Add points for threat indicators
  score += this.threat_indicators.length * 5;
  
  // Add points for biometric failures
  if (this.biometric_data && !this.biometric_data.authentication_result) {
    score += 20;
  }
  
  // Add points for consciousness anomalies
  if (this.consciousness_data && this.consciousness_data.dimensional_shift) {
    score += 15;
  }
  
  // Cap at 100
  this.severity_score = Math.min(100, score);
  return this.severity_score;
};

SecurityAuditLogSchema.methods.isHighRisk = function() {
  return this.severity_score >= 70 || 
         this.security_level === 'CRITICAL' ||
         this.threat_indicators.includes('PHI_DIMENSIONAL_BREACH');
};

SecurityAuditLogSchema.methods.requiresImmedateResponse = function() {
  const criticalThreats = [
    'BIOMETRIC_SPOOFING',
    'CONSCIOUSNESS_MANIPULATION',
    'PHI_DIMENSIONAL_BREACH',
    'QUANTUM_INTERFERENCE',
    'DATA_EXFILTRATION'
  ];
  
  return this.threat_indicators.some(threat => criticalThreats.includes(threat));
};

// Static methods
SecurityAuditLogSchema.statics.findSecurityEvents = function(timeRange = 24) {
  const since = new Date(Date.now() - (timeRange * 60 * 60 * 1000));
  return this.find({
    timestamp: { $gte: since },
    security_level: { $in: ['WARNING', 'ERROR', 'CRITICAL'] }
  }).sort({ timestamp: -1 });
};

SecurityAuditLogSchema.statics.findThreatsByType = function(threatType, timeRange = 24) {
  const since = new Date(Date.now() - (timeRange * 60 * 60 * 1000));
  return this.find({
    timestamp: { $gte: since },
    threat_indicators: threatType
  }).sort({ timestamp: -1 });
};

SecurityAuditLogSchema.statics.getSecurityStatistics = function(timeRange = 24) {
  const since = new Date(Date.now() - (timeRange * 60 * 60 * 1000));
  
  return this.aggregate([
    { $match: { timestamp: { $gte: since } } },
    {
      $group: {
        _id: '$security_level',
        count: { $sum: 1 },
        avg_severity: { $avg: '$severity_score' },
        unique_ips: { $addToSet: '$ip_address' },
        unique_users: { $addToSet: '$user_id' }
      }
    },
    {
      $project: {
        _id: 1,
        count: 1,
        avg_severity: { $round: ['$avg_severity', 2] },
        unique_ip_count: { $size: '$unique_ips' },
        unique_user_count: { $size: '$unique_users' }
      }
    }
  ]);
};

SecurityAuditLogSchema.statics.findAnomalousActivity = function(timeRange = 24) {
  const since = new Date(Date.now() - (timeRange * 60 * 60 * 1000));
  
  return this.aggregate([
    { $match: { timestamp: { $gte: since } } },
    {
      $group: {
        _id: '$ip_address',
        event_count: { $sum: 1 },
        threat_count: { $sum: { $size: '$threat_indicators' } },
        avg_severity: { $avg: '$severity_score' },
        events: { $push: '$$ROOT' }
      }
    },
    {
      $match: {
        $or: [
          { event_count: { $gte: 50 } }, // High frequency
          { threat_count: { $gte: 10 } }, // Multiple threats
          { avg_severity: { $gte: 60 } }  // High severity
        ]
      }
    },
    { $sort: { avg_severity: -1, event_count: -1 } }
  ]);
};

// Pre-save middleware
SecurityAuditLogSchema.pre('save', function(next) {
  // Calculate severity score
  this.calculateSeverityScore();
  
  // Generate correlation ID if not provided
  if (!this.correlation_id) {
    this.correlation_id = `${this.event_type}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
  
  next();
});

module.exports = mongoose.model('SecurityAuditLog', SecurityAuditLogSchema);
