const mongoose = require('mongoose');
const crypto = require('crypto');

const BiometricTemplateSchema = new mongoose.Schema({
  user_id: {
    type: String,
    required: true,
    unique: true,
    index: true,
    validate: {
      validator: function(v) {
        return /^[a-zA-Z0-9\-_]{8,64}$/.test(v);
      },
      message: 'Invalid user ID format'
    }
  },
  
  template_hash: {
    type: String,
    required: true,
    validate: {
      validator: function(v) {
        return /^[a-f0-9]{64}$/.test(v);
      },
      message: 'Invalid template hash format'
    }
  },
  
  feature_vector: {
    h: {
      type: [Number],
      required: true,
      validate: {
        validator: function(v) {
          return Array.isArray(v) && v.length === 6;
        },
        message: 'Feature vector must have 6 histogram values'
      }
    },
    c: {
      type: Number,
      required: true,
      min: 0,
      max: 10
    },
    m: {
      type: Number,
      required: true,
      min: 0,
      max: 100
    }
  },
  
  consciousness_state: {
    phi_resonance: {
      type: Number,
      required: true,
      min: 0,
      max: 1
    },
    quantum_coherence: {
      type: Number,
      required: true,
      min: 0,
      max: 0.999
    },
    awareness_level: {
      type: String,
      required: true,
      enum: ['DORMANT', 'AWARE', 'ENLIGHTENED', 'PHI_DIMENSIONAL', 'TRANSCENDENT']
    },
    consciousness_field: {
      awareness_amplitude: Number,
      dimensional_resonance: Number,
      temporal_stability: Number,
      information_density: Number
    }
  },
  
  security_level: {
    type: String,
    required: true,
    enum: ['STANDARD', 'ENHANCED', 'MILITARY_GRADE', 'PHI_DIMENSIONAL'],
    default: 'MILITARY_GRADE'
  },
  
  encryption_metadata: {
    algorithm: {
      type: String,
      required: true,
      default: 'PBKDF2-SHA256'
    },
    key_derivation: {
      type: String,
      required: true,
      default: 'BIOMETRIC_ENTROPY'
    },
    iterations: {
      type: Number,
      required: true,
      default: 100000
    },
    salt_length: {
      type: Number,
      required: true,
      default: 16
    }
  },
  
  created_at: {
    type: Date,
    default: Date.now,
    index: true
  },
  
  last_used: {
    type: Date,
    default: Date.now
  },
  
  usage_count: {
    type: Number,
    default: 0,
    min: 0
  },
  
  is_active: {
    type: Boolean,
    default: true,
    index: true
  },
  
  phi_signature: {
    type: String,
    required: true
  }
}, {
  timestamps: true,
  collection: 'biometric_templates'
});

// Indexes for performance
BiometricTemplateSchema.index({ user_id: 1, is_active: 1 });
BiometricTemplateSchema.index({ created_at: -1 });
BiometricTemplateSchema.index({ security_level: 1 });
BiometricTemplateSchema.index({ 'consciousness_state.awareness_level': 1 });

// Pre-save middleware to generate φ-signature
BiometricTemplateSchema.pre('save', function(next) {
  if (this.isNew) {
    const phi = 1.618033988749;
    const signature = crypto
      .createHash('sha256')
      .update(`${this.user_id}:${phi}:${this.consciousness_state.phi_resonance}`)
      .digest('hex');
    this.phi_signature = signature;
  }
  next();
});

// Instance methods
BiometricTemplateSchema.methods.updateUsage = function() {
  this.last_used = new Date();
  this.usage_count += 1;
  return this.save();
};

BiometricTemplateSchema.methods.deactivate = function() {
  this.is_active = false;
  return this.save();
};

BiometricTemplateSchema.methods.getSecurityMetrics = function() {
  return {
    security_level: this.security_level,
    consciousness_coherence: this.consciousness_state.quantum_coherence,
    phi_resonance: this.consciousness_state.phi_resonance,
    usage_frequency: this.usage_count,
    template_age: Date.now() - this.created_at.getTime(),
    phi_signature: this.phi_signature
  };
};

// Static methods
BiometricTemplateSchema.statics.findBySecurityLevel = function(level) {
  return this.find({ security_level: level, is_active: true });
};

BiometricTemplateSchema.statics.findByConsciousnessLevel = function(level) {
  return this.find({ 
    'consciousness_state.awareness_level': level, 
    is_active: true 
  });
};

BiometricTemplateSchema.statics.getSecurityStatistics = function() {
  return this.aggregate([
    { $match: { is_active: true } },
    {
      $group: {
        _id: '$security_level',
        count: { $sum: 1 },
        avg_coherence: { $avg: '$consciousness_state.quantum_coherence' },
        avg_usage: { $avg: '$usage_count' }
      }
    }
  ]);
};

module.exports = mongoose.model('BiometricTemplate', BiometricTemplateSchema);
