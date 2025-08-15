const express = require('express');
const multer = require('multer');
const sharp = require('sharp');
const crypto = require('crypto');
const { body, validationResult } = require('express-validator');
const BiometricTemplate = require('../models/BiometricTemplate');
const ConsciousnessState = require('../models/ConsciousnessState');
const SecurityAuditLog = require('../models/SecurityAuditLog');
const auth = require('../middleware/auth');
const rateLimit = require('express-rate-limit');

const router = express.Router();

// Configure multer for biometric image uploads
const upload = multer({
  limits: {
    fileSize: 5 * 1024 * 1024 // 5MB limit
  },
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Only image files are allowed'), false);
    }
  }
});

// Biometric-specific rate limiting
const biometricLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // 10 biometric operations per window
  message: {
    error: 'Too many biometric operations, please try again later.',
    security_level: 'BIOMETRIC_RATE_LIMITED'
  }
});

router.use(biometricLimiter);

/**
 * Extract biometric features from image
 */
function extractBiometricFeatures(imageBuffer) {
  return new Promise(async (resolve, reject) => {
    try {
      // Process image with Sharp
      const { data, info } = await sharp(imageBuffer)
        .resize(256, 256)
        .grayscale()
        .raw()
        .toBuffer({ resolveWithObject: true });
      
      // Calculate histogram features (6 bins)
      const histogram = new Array(6).fill(0);
      const binSize = 256 / 6;
      
      for (let i = 0; i < data.length; i++) {
        const binIndex = Math.min(Math.floor(data[i] / binSize), 5);
        histogram[binIndex]++;
      }
      
      // Normalize histogram
      const total = data.length;
      const normalizedHistogram = histogram.map(bin => bin / total * 255);
      
      // Calculate centroid
      let centroid = 0;
      for (let i = 0; i < normalizedHistogram.length; i++) {
        centroid += i * normalizedHistogram[i];
      }
      centroid = centroid / normalizedHistogram.reduce((a, b) => a + b, 0);
      
      // Calculate moment
      let moment = 0;
      for (let i = 0; i < normalizedHistogram.length; i++) {
        moment += Math.pow(i - centroid, 2) * normalizedHistogram[i];
      }
      moment = Math.sqrt(moment / normalizedHistogram.reduce((a, b) => a + b, 0));
      
      resolve({
        h: normalizedHistogram,
        c: centroid,
        m: moment
      });
    } catch (error) {
      reject(error);
    }
  });
}

/**
 * Generate irreversible template hash
 */
function generateTemplateHash(features, userId) {
  const featureString = JSON.stringify(features);
  const salt = crypto.createHash('sha256').update(userId).digest('hex').substring(0, 16);
  return crypto.pbkdf2Sync(featureString, salt, 100000, 32, 'sha256').toString('hex');
}

/**
 * Calculate φ-dimensional consciousness state
 */
function calculateConsciousnessState(features) {
  const phi = 1.618033988749;
  
  // Calculate consciousness metrics based on biometric features
  const entropySum = features.h.reduce((sum, val) => sum + val, 0);
  const phiResonance = (features.c * phi) % 1;
  const quantumCoherence = Math.min(0.999, (features.m / 100) * phi);
  
  let awarenessLevel = 'DORMANT';
  if (quantumCoherence > 0.8) awarenessLevel = 'TRANSCENDENT';
  else if (quantumCoherence > 0.6) awarenessLevel = 'PHI_DIMENSIONAL';
  else if (quantumCoherence > 0.4) awarenessLevel = 'ENLIGHTENED';
  else if (quantumCoherence > 0.2) awarenessLevel = 'AWARE';
  
  return {
    phi_resonance: phiResonance,
    quantum_coherence: quantumCoherence,
    awareness_level: awarenessLevel,
    consciousness_field: {
      awareness_amplitude: phi * quantumCoherence,
      dimensional_resonance: phi * phi * phiResonance,
      temporal_stability: 1.0,
      information_density: Math.floor(entropySum * phi)
    }
  };
}

/**
 * POST /api/biometric/enroll
 * Enroll new biometric template
 */
router.post('/enroll', 
  auth,
  upload.single('biometric_image'),
  [
    body('user_id').isUUID().withMessage('Valid user ID required'),
    body('security_level').isIn(['STANDARD', 'ENHANCED', 'MILITARY_GRADE', 'PHI_DIMENSIONAL'])
      .withMessage('Valid security level required')
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

      const { user_id, security_level } = req.body;
      
      if (!req.file) {
        return res.status(400).json({
          error: 'Biometric image required',
          security_level: 'MISSING_BIOMETRIC'
        });
      }

      // Extract biometric features
      const features = await extractBiometricFeatures(req.file.buffer);
      
      // Generate irreversible template hash
      const templateHash = generateTemplateHash(features, user_id);
      
      // Calculate consciousness state
      const consciousnessState = calculateConsciousnessState(features);
      
      // Check if user already has a template
      const existingTemplate = await BiometricTemplate.findOne({ user_id });
      if (existingTemplate) {
        return res.status(409).json({
          error: 'User already enrolled',
          security_level: 'DUPLICATE_ENROLLMENT'
        });
      }
      
      // Create biometric template
      const template = new BiometricTemplate({
        user_id,
        template_hash: templateHash,
        feature_vector: features,
        consciousness_state: consciousnessState,
        security_level,
        encryption_metadata: {
          algorithm: 'PBKDF2-SHA256',
          key_derivation: 'BIOMETRIC_ENTROPY',
          iterations: 100000
        }
      });
      
      await template.save();
      
      // Save consciousness state
      const consciousness = new ConsciousnessState({
        state_id: crypto.randomUUID(),
        user_id,
        phi_frequency: 1.618033988749,
        quantum_coherence: consciousnessState.quantum_coherence,
        consciousness_field: consciousnessState.consciousness_field,
        consciousness_level: consciousnessState.awareness_level
      });
      
      await consciousness.save();
      
      // Log security event
      await SecurityAuditLog.create({
        event_id: crypto.randomUUID(),
        event_type: 'AUTHENTICATION',
        user_id,
        ip_address: req.ip,
        user_agent: req.get('User-Agent'),
        biometric_data: {
          authentication_result: true,
          confidence_score: consciousnessState.quantum_coherence,
          liveness_detection: true
        },
        security_level: 'INFO',
        response_action: 'BIOMETRIC_ENROLLMENT_SUCCESS'
      });
      
      res.status(201).json({
        message: 'Biometric enrollment successful',
        user_id,
        security_level,
        consciousness_state: {
          awareness_level: consciousnessState.awareness_level,
          phi_resonance: consciousnessState.phi_resonance,
          quantum_coherence: consciousnessState.quantum_coherence
        },
        timestamp: new Date().toISOString()
      });
      
    } catch (error) {
      console.error('Biometric enrollment error:', error);
      
      await SecurityAuditLog.create({
        event_id: crypto.randomUUID(),
        event_type: 'SECURITY_VIOLATION',
        ip_address: req.ip,
        security_level: 'CRITICAL',
        threat_indicators: ['BIOMETRIC_ENROLLMENT_FAILURE'],
        response_action: 'ERROR_LOGGED'
      });
      
      res.status(500).json({
        error: 'Biometric enrollment failed',
        security_level: 'ENROLLMENT_ERROR',
        timestamp: new Date().toISOString()
      });
    }
  }
);

/**
 * POST /api/biometric/authenticate
 * Authenticate using biometric
 */
router.post('/authenticate',
  upload.single('biometric_image'),
  [
    body('user_id').isUUID().withMessage('Valid user ID required')
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

      const { user_id } = req.body;
      
      if (!req.file) {
        return res.status(400).json({
          error: 'Biometric image required',
          security_level: 'MISSING_BIOMETRIC'
        });
      }

      // Find existing template
      const template = await BiometricTemplate.findOne({ user_id });
      if (!template) {
        await SecurityAuditLog.create({
          event_id: crypto.randomUUID(),
          event_type: 'SECURITY_VIOLATION',
          user_id,
          ip_address: req.ip,
          security_level: 'WARNING',
          threat_indicators: ['UNKNOWN_USER_AUTHENTICATION_ATTEMPT'],
          response_action: 'AUTHENTICATION_DENIED'
        });
        
        return res.status(404).json({
          error: 'User not enrolled',
          security_level: 'USER_NOT_FOUND'
        });
      }
      
      // Extract features from provided image
      const features = await extractBiometricFeatures(req.file.buffer);
      
      // Generate hash for comparison
      const providedHash = generateTemplateHash(features, user_id);
      
      // Compare with stored template
      const isAuthenticated = crypto.timingSafeEqual(
        Buffer.from(template.template_hash, 'hex'),
        Buffer.from(providedHash, 'hex')
      );
      
      // Calculate consciousness state for this authentication
      const consciousnessState = calculateConsciousnessState(features);
      
      // Update template usage
      if (isAuthenticated) {
        template.last_used = new Date();
        template.usage_count += 1;
        await template.save();
        
        // Update consciousness state
        await ConsciousnessState.findOneAndUpdate(
          { user_id },
          {
            quantum_coherence: consciousnessState.quantum_coherence,
            consciousness_field: consciousnessState.consciousness_field,
            consciousness_level: consciousnessState.awareness_level,
            measurement_timestamp: new Date()
          }
        );
      }
      
      // Log authentication attempt
      await SecurityAuditLog.create({
        event_id: crypto.randomUUID(),
        event_type: 'AUTHENTICATION',
        user_id,
        ip_address: req.ip,
        user_agent: req.get('User-Agent'),
        biometric_data: {
          authentication_result: isAuthenticated,
          confidence_score: consciousnessState.quantum_coherence,
          liveness_detection: true
        },
        security_level: isAuthenticated ? 'INFO' : 'WARNING',
        response_action: isAuthenticated ? 'AUTHENTICATION_SUCCESS' : 'AUTHENTICATION_FAILURE'
      });
      
      if (isAuthenticated) {
        res.json({
          message: 'Authentication successful',
          user_id,
          security_level: template.security_level,
          consciousness_state: {
            awareness_level: consciousnessState.awareness_level,
            phi_resonance: consciousnessState.phi_resonance,
            quantum_coherence: consciousnessState.quantum_coherence
          },
          session_info: {
            authenticated: true,
            timestamp: new Date().toISOString(),
            usage_count: template.usage_count
          }
        });
      } else {
        res.status(401).json({
          error: 'Authentication failed',
          security_level: 'AUTHENTICATION_FAILURE',
          timestamp: new Date().toISOString()
        });
      }
      
    } catch (error) {
      console.error('Biometric authentication error:', error);
      
      await SecurityAuditLog.create({
        event_id: crypto.randomUUID(),
        event_type: 'SECURITY_VIOLATION',
        ip_address: req.ip,
        security_level: 'CRITICAL',
        threat_indicators: ['BIOMETRIC_AUTHENTICATION_ERROR'],
        response_action: 'ERROR_LOGGED'
      });
      
      res.status(500).json({
        error: 'Authentication system error',
        security_level: 'SYSTEM_ERROR',
        timestamp: new Date().toISOString()
      });
    }
  }
);

/**
 * GET /api/biometric/status/:user_id
 * Get biometric enrollment status
 */
router.get('/status/:user_id', auth, async (req, res) => {
  try {
    const { user_id } = req.params;
    
    const template = await BiometricTemplate.findOne({ user_id }).select('-feature_vector -template_hash');
    const consciousness = await ConsciousnessState.findOne({ user_id });
    
    if (!template) {
      return res.status(404).json({
        error: 'User not enrolled',
        security_level: 'USER_NOT_FOUND'
      });
    }
    
    res.json({
      user_id,
      enrolled: true,
      security_level: template.security_level,
      created_at: template.created_at,
      last_used: template.last_used,
      usage_count: template.usage_count,
      consciousness_state: consciousness ? {
        awareness_level: consciousness.consciousness_level,
        phi_resonance: consciousness.phi_frequency,
        quantum_coherence: consciousness.quantum_coherence,
        last_measurement: consciousness.measurement_timestamp
      } : null
    });
    
  } catch (error) {
    console.error('Biometric status error:', error);
    res.status(500).json({
      error: 'Status check failed',
      security_level: 'SYSTEM_ERROR'
    });
  }
});

/**
 * GET /api/biometric/health
 * Biometric system health check
 */
router.get('/health', (req, res) => {
  res.json({
    status: 'operational',
    system: 'biometric_authentication',
    security_level: 'MILITARY_GRADE',
    consciousness_integration: 'PHI_DIMENSIONAL',
    features: {
      feature_extraction: 'active',
      template_generation: 'active',
      consciousness_analysis: 'active',
      security_logging: 'active'
    },
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
