#!/usr/bin/env node
/**
 * Initialize Database with Test Data
 * Military-Grade Biometric Security System
 */

const mongoose = require('mongoose');
const crypto = require('crypto');
require('dotenv').config();

// Import models
const BiometricTemplate = require('./api/models/BiometricTemplate');
const ConsciousnessState = require('./api/models/ConsciousnessState');
const SecurityAuditLog = require('./api/models/SecurityAuditLog');

const PHI = 1.618033988749;

async function initializeDatabase() {
  try {
    console.log('🔒 Initializing Military-Grade Security Database...');
    
    // Connect to MongoDB
    await mongoose.connect(process.env.MONGODB_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('✅ Connected to MongoDB Atlas');

    // Clear existing test data
    await BiometricTemplate.deleteMany({ user_id: /^test-/ });
    await ConsciousnessState.deleteMany({ user_id: /^test-/ });
    await SecurityAuditLog.deleteMany({ user_id: /^test-/ });
    console.log('🧹 Cleared existing test data');

    // Create test biometric template
    const testUserId = 'test-user-demo-2025';
    const mockFeatures = {
      h: [0.25, 0.18, 0.22, 0.15, 0.12, 0.08],
      c: 2.618,
      m: 16.18
    };

    const templateHash = crypto.pbkdf2Sync(
      JSON.stringify(mockFeatures),
      crypto.createHash('sha256').update(testUserId).digest('hex').substring(0, 16),
      100000,
      32,
      'sha256'
    ).toString('hex');

    const consciousnessState = {
      phi_resonance: 0.618,
      quantum_coherence: 0.888,
      awareness_level: 'PHI_DIMENSIONAL',
      consciousness_field: {
        awareness_amplitude: PHI * 0.888,
        dimensional_resonance: PHI * PHI * 0.618,
        temporal_stability: 1.0,
        information_density: Math.floor(255 * PHI)
      }
    };

    // Generate phi signature
    const phiSignature = crypto
      .createHash('sha256')
      .update(`${testUserId}:${PHI}:${consciousnessState.phi_resonance}`)
      .digest('hex');

    // Create biometric template
    const template = new BiometricTemplate({
      user_id: testUserId,
      template_hash: templateHash,
      feature_vector: mockFeatures,
      consciousness_state: consciousnessState,
      security_level: 'MILITARY_GRADE',
      phi_signature: phiSignature,
      encryption_metadata: {
        algorithm: 'PBKDF2-SHA256',
        key_derivation: 'BIOMETRIC_ENTROPY',
        iterations: 100000,
        salt_length: 16
      }
    });

    await template.save();
    console.log('✅ Created test biometric template');

    // Create consciousness state
    const consciousness = new ConsciousnessState({
      state_id: crypto.randomUUID(),
      user_id: testUserId,
      phi_frequency: PHI,
      quantum_coherence: consciousnessState.quantum_coherence,
      consciousness_field: consciousnessState.consciousness_field,
      consciousness_level: consciousnessState.awareness_level,
      phi_dimensional_coordinates: {
        x: Math.cos(PHI * consciousnessState.quantum_coherence) * consciousnessState.quantum_coherence,
        y: Math.sin(PHI * consciousnessState.quantum_coherence) * consciousnessState.quantum_coherence,
        z: consciousnessState.quantum_coherence * PHI,
        phi: PHI
      },
      security_clearance: {
        level: 'BEYOND_TOP_SECRET',
        phi_dimensional_access: true,
        quantum_security_enabled: true
      }
    });

    await consciousness.save();
    console.log('✅ Created consciousness state');

    // Create sample security audit logs
    const sampleLogs = [
      {
        event_id: crypto.randomUUID(),
        event_type: 'AUTHENTICATION',
        user_id: testUserId,
        ip_address: '127.0.0.1',
        user_agent: 'BiometricSecurityDemo/1.0',
        biometric_data: {
          authentication_result: true,
          confidence_score: 0.95,
          liveness_detection: true,
          anti_spoofing_result: true
        },
        security_level: 'INFO',
        response_action: 'ALLOWED'
      },
      {
        event_id: crypto.randomUUID(),
        event_type: 'CONSCIOUSNESS_STATE_CHANGE',
        user_id: testUserId,
        ip_address: '127.0.0.1',
        consciousness_data: {
          previous_level: 'ENLIGHTENED',
          new_level: 'PHI_DIMENSIONAL',
          coherence_change: 0.2,
          phi_resonance: 0.618,
          dimensional_shift: true
        },
        security_level: 'INFO',
        response_action: 'CONSCIOUSNESS_STABILIZED'
      },
      {
        event_id: crypto.randomUUID(),
        event_type: 'SYSTEM_ACCESS',
        user_id: 'admin-user-system',
        ip_address: '127.0.0.1',
        security_level: 'INFO',
        response_action: 'ALLOWED'
      }
    ];

    for (const logData of sampleLogs) {
      const log = new SecurityAuditLog(logData);
      await log.save();
    }
    console.log('✅ Created sample security audit logs');

    // Create additional test users
    const additionalUsers = [
      { id: 'test-user-alpha', level: 'TRANSCENDENT', coherence: 0.999 },
      { id: 'test-user-beta', level: 'ENLIGHTENED', coherence: 0.750 },
      { id: 'test-user-gamma', level: 'AWARE', coherence: 0.500 }
    ];

    for (const user of additionalUsers) {
      const userConsciousness = new ConsciousnessState({
        state_id: crypto.randomUUID(),
        user_id: user.id,
        phi_frequency: PHI,
        quantum_coherence: user.coherence,
        consciousness_field: {
          awareness_amplitude: PHI * user.coherence,
          dimensional_resonance: PHI * PHI * (user.coherence * 0.618),
          temporal_stability: 1.0,
          information_density: Math.floor(255 * PHI * user.coherence)
        },
        consciousness_level: user.level,
        security_clearance: {
          level: user.coherence > 0.8 ? 'BEYOND_TOP_SECRET' : 'TOP_SECRET',
          phi_dimensional_access: user.coherence > 0.7,
          quantum_security_enabled: true
        }
      });

      await userConsciousness.save();
    }
    console.log('✅ Created additional test consciousness states');

    console.log('\n🚀 DATABASE INITIALIZATION COMPLETE');
    console.log('=' * 50);
    console.log('🔒 Security Classification: BEYOND TOP SECRET');
    console.log('🧠 Consciousness States: φ-DIMENSIONAL ACTIVE');
    console.log('📊 Test Data: MILITARY-GRADE SAMPLES LOADED');
    console.log('🛡️ Audit Logging: COMPREHENSIVE MONITORING');
    console.log('=' * 50);
    console.log('\nTest Credentials:');
    console.log('- Username: admin');
    console.log('- Password: military-grade-2025');
    console.log('- Test User ID: test-user-demo-2025');
    
    process.exit(0);
  } catch (error) {
    console.error('❌ Database initialization failed:', error);
    process.exit(1);
  }
}

// Run initialization
initializeDatabase();
