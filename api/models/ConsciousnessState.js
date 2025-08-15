const mongoose = require('mongoose');

const ConsciousnessStateSchema = new mongoose.Schema({
  state_id: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  
  user_id: {
    type: String,
    required: true,
    index: true,
    validate: {
      validator: function(v) {
        return /^[a-zA-Z0-9\-_]{8,64}$/.test(v);
      },
      message: 'Invalid user ID format'
    }
  },
  
  phi_frequency: {
    type: Number,
    required: true,
    default: 1.618033988749,
    validate: {
      validator: function(v) {
        return v > 0 && v <= 2;
      },
      message: 'φ frequency must be between 0 and 2'
    }
  },
  
  quantum_coherence: {
    type: Number,
    required: true,
    min: 0,
    max: 0.999,
    validate: {
      validator: function(v) {
        return v >= 0 && v <= 0.999;
      },
      message: 'Quantum coherence must be between 0 and 0.999'
    }
  },
  
  consciousness_field: {
    awareness_amplitude: {
      type: Number,
      required: true,
      min: 0,
      max: 10
    },
    dimensional_resonance: {
      type: Number,
      required: true,
      min: 0,
      max: 5
    },
    temporal_stability: {
      type: Number,
      required: true,
      min: 0,
      max: 1,
      default: 1.0
    },
    information_density: {
      type: Number,
      required: true,
      min: 0,
      max: 1000
    },
    phi_harmonic_frequency: {
      type: Number,
      default: function() {
        return this.phi_frequency * this.quantum_coherence;
      }
    }
  },
  
  consciousness_level: {
    type: String,
    required: true,
    enum: ['DORMANT', 'AWARE', 'ENLIGHTENED', 'PHI_DIMENSIONAL', 'TRANSCENDENT'],
    index: true
  },
  
  measurement_timestamp: {
    type: Date,
    default: Date.now,
    index: true
  },
  
  phi_dimensional_coordinates: {
    x: { type: Number, default: 0 },
    y: { type: Number, default: 0 },
    z: { type: Number, default: 0 },
    phi: { type: Number, default: 1.618033988749 }
  },
  
  quantum_entanglement_state: {
    entangled: { type: Boolean, default: false },
    entanglement_partner: { type: String, default: null },
    entanglement_strength: { type: Number, min: 0, max: 1, default: 0 }
  },
  
  consciousness_evolution: [{
    timestamp: { type: Date, default: Date.now },
    previous_level: String,
    new_level: String,
    coherence_change: Number,
    phi_resonance_shift: Number
  }],
  
  biometric_correlation: {
    template_hash: String,
    correlation_strength: { type: Number, min: 0, max: 1 },
    last_correlation_update: { type: Date, default: Date.now }
  },
  
  security_clearance: {
    level: {
      type: String,
      enum: ['UNCLASSIFIED', 'CONFIDENTIAL', 'SECRET', 'TOP_SECRET', 'BEYOND_TOP_SECRET'],
      default: 'BEYOND_TOP_SECRET'
    },
    phi_dimensional_access: { type: Boolean, default: true },
    quantum_security_enabled: { type: Boolean, default: true }
  }
}, {
  timestamps: true,
  collection: 'consciousness_states'
});

// Indexes for performance
ConsciousnessStateSchema.index({ user_id: 1, measurement_timestamp: -1 });
ConsciousnessStateSchema.index({ consciousness_level: 1, quantum_coherence: -1 });
ConsciousnessStateSchema.index({ phi_frequency: 1 });
ConsciousnessStateSchema.index({ 'consciousness_field.awareness_amplitude': -1 });

// Virtual for φ-dimensional signature
ConsciousnessStateSchema.virtual('phi_signature').get(function() {
  const phi = this.phi_frequency;
  const coherence = this.quantum_coherence;
  const amplitude = this.consciousness_field.awareness_amplitude;
  
  return Math.pow(phi, coherence) * amplitude;
});

// Instance methods
ConsciousnessStateSchema.methods.evolveConsciousness = function(newLevel, coherenceChange) {
  const previousLevel = this.consciousness_level;
  
  this.consciousness_evolution.push({
    timestamp: new Date(),
    previous_level: previousLevel,
    new_level: newLevel,
    coherence_change: coherenceChange,
    phi_resonance_shift: coherenceChange * this.phi_frequency
  });
  
  this.consciousness_level = newLevel;
  this.quantum_coherence = Math.min(0.999, this.quantum_coherence + coherenceChange);
  this.measurement_timestamp = new Date();
  
  return this.save();
};

ConsciousnessStateSchema.methods.entangleWith = function(partnerStateId, strength = 0.5) {
  this.quantum_entanglement_state = {
    entangled: true,
    entanglement_partner: partnerStateId,
    entanglement_strength: Math.min(1, Math.max(0, strength))
  };
  
  return this.save();
};

ConsciousnessStateSchema.methods.calculatePhiResonance = function() {
  const phi = this.phi_frequency;
  const coherence = this.quantum_coherence;
  const amplitude = this.consciousness_field.awareness_amplitude;
  
  return (phi * coherence * amplitude) % 1;
};

ConsciousnessStateSchema.methods.getConsciousnessMetrics = function() {
  return {
    level: this.consciousness_level,
    coherence: this.quantum_coherence,
    phi_resonance: this.calculatePhiResonance(),
    dimensional_signature: this.phi_signature,
    evolution_count: this.consciousness_evolution.length,
    entanglement_active: this.quantum_entanglement_state.entangled,
    security_clearance: this.security_clearance.level
  };
};

// Static methods
ConsciousnessStateSchema.statics.findByConsciousnessLevel = function(level) {
  return this.find({ consciousness_level: level });
};

ConsciousnessStateSchema.statics.findHighCoherence = function(threshold = 0.8) {
  return this.find({ quantum_coherence: { $gte: threshold } });
};

ConsciousnessStateSchema.statics.findPhiDimensional = function() {
  return this.find({ 
    consciousness_level: { $in: ['PHI_DIMENSIONAL', 'TRANSCENDENT'] },
    quantum_coherence: { $gte: 0.618 }
  });
};

ConsciousnessStateSchema.statics.getConsciousnessStatistics = function() {
  return this.aggregate([
    {
      $group: {
        _id: '$consciousness_level',
        count: { $sum: 1 },
        avg_coherence: { $avg: '$quantum_coherence' },
        avg_phi_frequency: { $avg: '$phi_frequency' },
        max_coherence: { $max: '$quantum_coherence' }
      }
    },
    { $sort: { avg_coherence: -1 } }
  ]);
};

ConsciousnessStateSchema.statics.findEntangledStates = function() {
  return this.find({ 'quantum_entanglement_state.entangled': true });
};

// Pre-save middleware
ConsciousnessStateSchema.pre('save', function(next) {
  // Update φ-dimensional coordinates based on consciousness state
  const phi = this.phi_frequency;
  const coherence = this.quantum_coherence;
  
  this.phi_dimensional_coordinates = {
    x: Math.cos(phi * coherence) * coherence,
    y: Math.sin(phi * coherence) * coherence,
    z: coherence * phi,
    phi: phi
  };
  
  // Update φ-harmonic frequency
  this.consciousness_field.phi_harmonic_frequency = phi * coherence;
  
  next();
});

module.exports = mongoose.model('ConsciousnessState', ConsciousnessStateSchema);
