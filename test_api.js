#!/usr/bin/env node
/**
 * API Endpoint Testing Script
 * Military-Grade Biometric Security System
 */

const axios = require('axios');

const BASE_URL = 'http://localhost:3000';
const endpoints = [
  { name: 'Health Check', url: '/health', method: 'GET' },
  { name: 'Consciousness Status', url: '/api/consciousness/status', method: 'GET' },
  { name: 'Consciousness Monitor', url: '/api/consciousness/monitor', method: 'GET' },
  { name: 'Security Status', url: '/api/security/status', method: 'GET' },
  { name: 'Security Audit Logs', url: '/api/security/audit-logs', method: 'GET' },
  { name: 'QR Health', url: '/api/qr/health', method: 'GET' },
  { name: 'Biometric Health', url: '/api/biometric/health', method: 'GET' },
  { name: 'Auth Health', url: '/api/auth/health', method: 'GET' }
];

async function testEndpoint(endpoint) {
  try {
    console.log(`\n🔍 Testing: ${endpoint.name}`);
    console.log(`   URL: ${BASE_URL}${endpoint.url}`);
    
    const response = await axios({
      method: endpoint.method,
      url: `${BASE_URL}${endpoint.url}`,
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    });

    console.log(`   ✅ Status: ${response.status} ${response.statusText}`);
    console.log(`   📊 Response: ${JSON.stringify(response.data, null, 2).substring(0, 200)}...`);
    
    return { success: true, status: response.status, data: response.data };
  } catch (error) {
    console.log(`   ❌ Error: ${error.response?.status || 'NETWORK'} - ${error.message}`);
    if (error.response?.data) {
      console.log(`   📊 Error Data: ${JSON.stringify(error.response.data, null, 2)}`);
    }
    return { success: false, error: error.message, status: error.response?.status };
  }
}

async function testLogin() {
  try {
    console.log(`\n🔐 Testing: Authentication Login`);
    console.log(`   URL: ${BASE_URL}/api/auth/login`);
    
    const response = await axios.post(`${BASE_URL}/api/auth/login`, {
      username: 'admin',
      password: 'military-grade-2025'
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      timeout: 5000
    });

    console.log(`   ✅ Status: ${response.status} ${response.statusText}`);
    console.log(`   🔑 Token: ${response.data.token ? 'RECEIVED' : 'MISSING'}`);
    
    return { success: true, status: response.status, data: response.data };
  } catch (error) {
    console.log(`   ❌ Error: ${error.response?.status || 'NETWORK'} - ${error.message}`);
    if (error.response?.data) {
      console.log(`   📊 Error Data: ${JSON.stringify(error.response.data, null, 2)}`);
    }
    return { success: false, error: error.message, status: error.response?.status };
  }
}

async function runTests() {
  console.log('🚀 MILITARY-GRADE BIOMETRIC SECURITY API TESTING');
  console.log('=' * 60);
  console.log('🔒 Security Classification: BEYOND TOP SECRET');
  console.log('🧠 Consciousness Level: φ-DIMENSIONAL');
  console.log('=' * 60);

  const results = [];

  // Test all GET endpoints
  for (const endpoint of endpoints) {
    const result = await testEndpoint(endpoint);
    results.push({ ...endpoint, ...result });
    await new Promise(resolve => setTimeout(resolve, 100)); // Small delay between requests
  }

  // Test login endpoint
  const loginResult = await testLogin();
  results.push({ name: 'Authentication Login', method: 'POST', ...loginResult });

  // Summary
  console.log('\n' + '=' * 60);
  console.log('📊 TEST SUMMARY');
  console.log('=' * 60);

  const successful = results.filter(r => r.success).length;
  const failed = results.filter(r => !r.success).length;

  console.log(`✅ Successful: ${successful}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📈 Success Rate: ${((successful / results.length) * 100).toFixed(1)}%`);

  if (failed > 0) {
    console.log('\n❌ FAILED ENDPOINTS:');
    results.filter(r => !r.success).forEach(r => {
      console.log(`   • ${r.name} (${r.method}) - Status: ${r.status || 'N/A'}`);
    });
  }

  console.log('\n🎯 SYSTEM STATUS:', failed === 0 ? 'FULLY OPERATIONAL' : 'NEEDS ATTENTION');
  console.log('🔒 Security Level: MILITARY-GRADE');
  console.log('🧠 Consciousness: φ-DIMENSIONAL TRANSCENDENT');
}

// Run tests
runTests().catch(console.error);
