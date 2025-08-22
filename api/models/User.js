const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    minlength: 3,
    maxlength: 50
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true
  },
  password: {
    type: String,
    required: true,
    minlength: 6
  },
  securityLevel: {
    type: String,
    default: 'FRAYMUS_PROTECTED',
    enum: ['STANDARD', 'ENHANCED', 'MILITARY_GRADE', 'FRAYMUS_PROTECTED']
  },
  consciousnessLevel: {
    type: Number,
    default: 1.618033988749895 // φ (phi) - Golden Ratio
  },
  lastLogin: {
    type: Date,
    default: Date.now
  },
  isActive: {
    type: Boolean,
    default: true
  },
  biometricData: {
    fingerprint: String,
    voiceprint: String,
    retinalScan: String
  },
  consciousnessSignature: {
    type: String,
    default: function() {
      return `φ-${this.consciousnessLevel}-${Date.now()}`;
    }
  }
}, {
  timestamps: true
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  
  try {
    const salt = await bcrypt.genSalt(12);
    this.password = await bcrypt.hash(this.password, salt);
    next();
  } catch (error) {
    next(error);
  }
});

// Compare password method
userSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

// Generate consciousness signature
userSchema.methods.generateConsciousnessSignature = function() {
  const phi = 1.618033988749895;
  const timestamp = Date.now();
  const signature = `${this.username}-φ${phi}-${timestamp}`;
  return signature;
};

// Consciousness physics authentication
userSchema.methods.consciousnessAuth = function(phiLevel) {
  return phiLevel === this.consciousnessLevel;
};

module.exports = mongoose.model('User', userSchema);
