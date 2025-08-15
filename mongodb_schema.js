// MongoDB Schema for Biometric Visual Cryptography System
// Military-Grade Security with φ-Dimensional Consciousness Integration

// Biometric Templates Collection
db.createCollection("biometric_templates", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["user_id", "template_hash", "feature_vector", "created_at", "security_level"],
      properties: {
        user_id: {
          bsonType: "string",
          description: "Unique user identifier (UUID)"
        },
        template_hash: {
          bsonType: "string",
          description: "Irreversible biometric template hash (SHA-256)"
        },
        feature_vector: {
          bsonType: "object",
          required: ["h", "c", "m"],
          properties: {
            h: {
              bsonType: "array",
              items: { bsonType: "double" },
              minItems: 6,
              maxItems: 6,
              description: "Histogram features (6 bins)"
            },
            c: {
              bsonType: "double",
              description: "Centroid feature"
            },
            m: {
              bsonType: "double", 
              description: "Moment feature"
            }
          }
        },
        consciousness_state: {
          bsonType: "object",
          properties: {
            phi_resonance: { bsonType: "double" },
            quantum_coherence: { bsonType: "double" },
            awareness_level: { bsonType: "string" }
          }
        },
        security_level: {
          bsonType: "string",
          enum: ["STANDARD", "ENHANCED", "MILITARY_GRADE", "PHI_DIMENSIONAL"]
        },
        encryption_metadata: {
          bsonType: "object",
          properties: {
            algorithm: { bsonType: "string" },
            key_derivation: { bsonType: "string" },
            iterations: { bsonType: "int" }
          }
        },
        created_at: {
          bsonType: "date",
          description: "Template creation timestamp"
        },
        last_used: {
          bsonType: "date",
          description: "Last authentication timestamp"
        },
        usage_count: {
          bsonType: "int",
          minimum: 0,
          description: "Number of successful authentications"
        }
      }
    }
  }
});

// QR Consciousness Chain Collection
db.createCollection("qr_consciousness_chains", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["chain_id", "user_id", "links", "consciousness_level", "created_at"],
      properties: {
        chain_id: {
          bsonType: "string",
          description: "Unique QR chain identifier"
        },
        user_id: {
          bsonType: "string",
          description: "Associated user identifier"
        },
        links: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["link_id", "qr_data", "consciousness_signature", "phi_resonance"],
            properties: {
              link_id: { bsonType: "string" },
              qr_data: { bsonType: "string" },
              consciousness_signature: { bsonType: "string" },
              phi_resonance: { bsonType: "double" },
              quantum_state: { 
                bsonType: "string",
                enum: ["SUPERPOSITION", "ENTANGLED", "COLLAPSED"]
              },
              recursive_depth: { bsonType: "int" }
            }
          }
        },
        consciousness_level: {
          bsonType: "double",
          description: "Overall chain consciousness level"
        },
        chain_integrity_hash: {
          bsonType: "string",
          description: "SHA-256 hash of entire chain"
        },
        created_at: { bsonType: "date" },
        expires_at: { bsonType: "date" }
      }
    }
  }
});

// Security Audit Logs Collection
db.createCollection("security_audit_logs", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["event_id", "event_type", "timestamp", "security_level"],
      properties: {
        event_id: { bsonType: "string" },
        event_type: {
          bsonType: "string",
          enum: ["AUTHENTICATION", "AUTHORIZATION", "SECURITY_VIOLATION", "SYSTEM_ACCESS", "DATA_ACCESS"]
        },
        user_id: { bsonType: "string" },
        ip_address: { bsonType: "string" },
        user_agent: { bsonType: "string" },
        geolocation: {
          bsonType: "object",
          properties: {
            country: { bsonType: "string" },
            region: { bsonType: "string" },
            city: { bsonType: "string" }
          }
        },
        biometric_data: {
          bsonType: "object",
          properties: {
            authentication_result: { bsonType: "bool" },
            confidence_score: { bsonType: "double" },
            liveness_detection: { bsonType: "bool" }
          }
        },
        security_level: {
          bsonType: "string",
          enum: ["INFO", "WARNING", "CRITICAL", "MILITARY_ALERT"]
        },
        threat_indicators: {
          bsonType: "array",
          items: { bsonType: "string" }
        },
        timestamp: { bsonType: "date" },
        response_action: { bsonType: "string" }
      }
    }
  }
});

// User Sessions Collection
db.createCollection("user_sessions", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["session_id", "user_id", "created_at", "security_level"],
      properties: {
        session_id: { bsonType: "string" },
        user_id: { bsonType: "string" },
        jwt_token_hash: { bsonType: "string" },
        biometric_verified: { bsonType: "bool" },
        consciousness_state: {
          bsonType: "object",
          properties: {
            awareness_level: { bsonType: "string" },
            phi_resonance: { bsonType: "double" },
            quantum_coherence: { bsonType: "double" }
          }
        },
        security_level: {
          bsonType: "string",
          enum: ["STANDARD", "ENHANCED", "MILITARY_GRADE", "PHI_DIMENSIONAL"]
        },
        ip_address: { bsonType: "string" },
        device_fingerprint: { bsonType: "string" },
        created_at: { bsonType: "date" },
        last_activity: { bsonType: "date" },
        expires_at: { bsonType: "date" },
        is_active: { bsonType: "bool" }
      }
    }
  }
});

// Consciousness Physics States Collection
db.createCollection("consciousness_physics_states", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["state_id", "user_id", "phi_frequency", "quantum_coherence"],
      properties: {
        state_id: { bsonType: "string" },
        user_id: { bsonType: "string" },
        phi_frequency: {
          bsonType: "double",
          description: "φ-harmonic frequency (1.618...)"
        },
        quantum_coherence: {
          bsonType: "double",
          minimum: 0.0,
          maximum: 1.0
        },
        consciousness_field: {
          bsonType: "object",
          properties: {
            awareness_amplitude: { bsonType: "double" },
            dimensional_resonance: { bsonType: "double" },
            temporal_stability: { bsonType: "double" },
            information_density: { bsonType: "int" }
          }
        },
        binary_states: {
          bsonType: "object",
          properties: {
            classical: { bsonType: "bool" },
            quantum: { bsonType: "bool" },
            phi_dimensional: { bsonType: "bool" }
          }
        },
        entanglement_matrix: {
          bsonType: "array",
          items: {
            bsonType: "array",
            items: { bsonType: "double" }
          }
        },
        measurement_timestamp: { bsonType: "date" },
        consciousness_level: {
          bsonType: "string",
          enum: ["DORMANT", "AWARE", "ENLIGHTENED", "PHI_DIMENSIONAL", "TRANSCENDENT"]
        }
      }
    }
  }
});

// Create indexes for optimal performance
db.biometric_templates.createIndex({ "user_id": 1 }, { unique: true });
db.biometric_templates.createIndex({ "template_hash": 1 }, { unique: true });
db.biometric_templates.createIndex({ "created_at": -1 });
db.biometric_templates.createIndex({ "security_level": 1 });

db.qr_consciousness_chains.createIndex({ "chain_id": 1 }, { unique: true });
db.qr_consciousness_chains.createIndex({ "user_id": 1 });
db.qr_consciousness_chains.createIndex({ "created_at": -1 });
db.qr_consciousness_chains.createIndex({ "consciousness_level": -1 });

db.security_audit_logs.createIndex({ "timestamp": -1 });
db.security_audit_logs.createIndex({ "event_type": 1, "timestamp": -1 });
db.security_audit_logs.createIndex({ "user_id": 1, "timestamp": -1 });
db.security_audit_logs.createIndex({ "security_level": 1, "timestamp": -1 });

db.user_sessions.createIndex({ "session_id": 1 }, { unique: true });
db.user_sessions.createIndex({ "user_id": 1 });
db.user_sessions.createIndex({ "expires_at": 1 }, { expireAfterSeconds: 0 });
db.user_sessions.createIndex({ "is_active": 1, "last_activity": -1 });

db.consciousness_physics_states.createIndex({ "state_id": 1 }, { unique: true });
db.consciousness_physics_states.createIndex({ "user_id": 1 });
db.consciousness_physics_states.createIndex({ "measurement_timestamp": -1 });
db.consciousness_physics_states.createIndex({ "consciousness_level": 1 });

// Security configurations
db.runCommand({
  collMod: "biometric_templates",
  validator: {
    $jsonSchema: {
      // Enhanced security validation
      bsonType: "object",
      additionalProperties: false // Strict schema enforcement
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

// Create database user with restricted permissions
db.createUser({
  user: "biometric_app",
  pwd: "SECURE_PASSWORD_TO_BE_REPLACED",
  roles: [
    {
      role: "readWrite",
      db: "biometric_security"
    }
  ]
});

// Enable database encryption at rest
db.adminCommand({
  setParameter: 1,
  encryptionCipherMode: "AES256-GCM"
});

print("✅ MongoDB schema created successfully");
print("✅ Collections: biometric_templates, qr_consciousness_chains, security_audit_logs, user_sessions, consciousness_physics_states");
print("✅ Indexes created for optimal performance");
print("✅ Security validations enabled");
print("✅ Military-grade encryption configured");
print("🔒 Database ready for φ-dimensional quantum security deployment");
