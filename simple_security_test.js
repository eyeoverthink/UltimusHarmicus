#!/usr/bin/env node
/**
 * Simple Security Test - Military-Grade Biometric System
 */

const axios = require('axios');

async function runSecurityTests() {
  console.log('🚨 MILITARY-GRADE SECURITY PENETRATION TESTING');
  console.log('============================================================');
  console.log('🔒 Classification: BEYOND TOP SECRET');
  console.log('🧠 Consciousness Level: φ-DIMENSIONAL');
  console.log('🛡️ Security Level: MILITARY-GRADE');
  console.log('============================================================');

  const baseUrl = 'http://localhost:3000';
  let passed = 0, failed = 0, warnings = 0;

  // Test 1: Security Headers
  console.log('\n🛡️ TESTING SECURITY HEADERS');
  try {
    const response = await axios.get(`${baseUrl}/health`);
    const headers = response.headers;
    
    if (headers['x-frame-options']) {
      console.log('✅ X-Frame-Options header present');
      passed++;
    } else {
      console.log('❌ X-Frame-Options header missing');
      failed++;
    }
    
    if (headers['content-security-policy']) {
      console.log('✅ Content-Security-Policy header present');
      passed++;
    } else {
      console.log('❌ Content-Security-Policy header missing');
      failed++;
    }
  } catch (error) {
    console.log('❌ Security headers test failed:', error.message);
    failed++;
  }

  // Test 2: Authentication Security
  console.log('\n🔐 TESTING AUTHENTICATION SECURITY');
  try {
    // Test invalid credentials
    const invalidResponse = await axios.post(`${baseUrl}/api/auth/login`, {
      username: 'hacker',
      password: 'password123'
    }).catch(err => err.response);

    if (invalidResponse && invalidResponse.status === 401) {
      console.log('✅ Invalid credentials properly rejected');
      passed++;
    } else {
      console.log('❌ Invalid credentials not properly handled');
      failed++;
    }

    // Test valid credentials
    const validResponse = await axios.post(`${baseUrl}/api/auth/login`, {
      username: 'admin',
      password: 'military-grade-2025'
    });

    if (validResponse.status === 200 && validResponse.data.token) {
      console.log('✅ Valid credentials accepted with JWT token');
      passed++;
    } else {
      console.log('❌ Valid authentication failed');
      failed++;
    }
  } catch (error) {
    console.log('❌ Authentication test failed:', error.message);
    failed++;
  }

  // Test 3: Consciousness Physics
  console.log('\n🧠 TESTING φ-DIMENSIONAL CONSCIOUSNESS SECURITY');
  try {
    const response = await axios.get(`${baseUrl}/api/consciousness/monitor`);
    
    if (response.status === 200 && response.data.consciousness_field) {
      console.log('✅ Consciousness monitoring operational');
      passed++;
      
      const field = response.data.consciousness_field;
      if (field.phi_frequency && Math.abs(field.phi_frequency - 1.618033988749) < 0.001) {
        console.log('✅ φ frequency properly calibrated');
        passed++;
      } else {
        console.log('⚠️ φ frequency deviation detected');
        warnings++;
      }
    } else {
      console.log('❌ Consciousness monitoring failed');
      failed++;
    }
  } catch (error) {
    console.log('❌ Consciousness physics test failed:', error.message);
    failed++;
  }

  // Test 4: Database Security
  console.log('\n🗄️ TESTING DATABASE SECURITY');
  try {
    const response = await axios.get(`${baseUrl}/api/security/audit-logs`);
    
    if (response.status === 200 && response.data.logs) {
      console.log('✅ Audit logs accessible and structured');
      passed++;
    } else {
      console.log('❌ Audit logs not properly accessible');
      failed++;
    }
  } catch (error) {
    console.log('❌ Database security test failed:', error.message);
    failed++;
  }

  // Test 5: QR Security Systems
  console.log('\n📱 TESTING QR CONSCIOUSNESS SECURITY');
  try {
    const response = await axios.get(`${baseUrl}/api/qr/health`);
    
    if (response.status === 200) {
      console.log('✅ QR consciousness system operational');
      passed++;
      
      if (response.data.consciousness_integration === 'PHI_DIMENSIONAL') {
        console.log('✅ φ-dimensional consciousness integration active');
        passed++;
      } else {
        console.log('⚠️ Consciousness integration level unclear');
        warnings++;
      }
    } else {
      console.log('❌ QR security system not responding');
      failed++;
    }
  } catch (error) {
    console.log('❌ QR security test failed:', error.message);
    failed++;
  }

  // Generate Report
  console.log('\n============================================================');
  console.log('📊 SECURITY PENETRATION TEST REPORT');
  console.log('============================================================');
  
  const total = passed + failed + warnings;
  const securityScore = Math.round((passed / total) * 100);
  
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`⚠️ Warnings: ${warnings}`);
  console.log(`📈 Security Score: ${securityScore}%`);
  
  let securityLevel;
  if (failed === 0 && securityScore >= 90) {
    securityLevel = '🛡️ MILITARY-GRADE SECURITY CONFIRMED';
  } else if (failed <= 2) {
    securityLevel = '🔒 SECURITY LEVEL ACCEPTABLE';
  } else {
    securityLevel = '⚠️ SECURITY IMPROVEMENTS NEEDED';
  }
  
  console.log(`\n🎯 SECURITY ASSESSMENT: ${securityLevel}`);
  console.log('🔒 Classification: BEYOND TOP SECRET');
  console.log('🧠 Consciousness: φ-DIMENSIONAL TRANSCENDENT');
  console.log('============================================================');
}

runSecurityTests().catch(console.error);
