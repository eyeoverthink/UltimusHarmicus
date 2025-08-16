#!/usr/bin/env node
/**
 * Direct Server Test - Bypass curl issues
 */

const http = require('http');

function testEndpoint(path, callback) {
  const options = {
    hostname: 'localhost',
    port: 3000,
    path: path,
    method: 'GET',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  };

  const req = http.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => data += chunk);
    res.on('end', () => {
      try {
        const parsed = JSON.parse(data);
        callback(null, { status: res.statusCode, data: parsed });
      } catch (e) {
        callback(null, { status: res.statusCode, data: data, error: 'JSON parse error' });
      }
    });
  });

  req.on('error', (e) => callback(e));
  req.setTimeout(5000, () => {
    req.destroy();
    callback(new Error('Timeout'));
  });
  req.end();
}

console.log('🚨 DIRECT SERVER TESTING');
console.log('============================================================');

// Test health endpoint
testEndpoint('/health', (err, result) => {
  if (err) {
    console.log('❌ Health endpoint error:', err.message);
  } else {
    console.log('✅ Health endpoint - Status:', result.status);
    console.log('   Response:', JSON.stringify(result.data, null, 2));
  }

  // Test consciousness monitor
  testEndpoint('/api/consciousness/monitor', (err, result) => {
    if (err) {
      console.log('❌ Consciousness monitor error:', err.message);
    } else {
      console.log('✅ Consciousness monitor - Status:', result.status);
      console.log('   Response:', JSON.stringify(result.data, null, 2));
    }

    // Test authentication
    const postData = JSON.stringify({
      username: 'admin',
      password: 'military-grade-2025'
    });

    const authOptions = {
      hostname: 'localhost',
      port: 3000,
      path: '/api/auth/login',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    const authReq = http.request(authOptions, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          console.log('✅ Authentication - Status:', res.statusCode);
          console.log('   Response:', JSON.stringify(parsed, null, 2));
        } catch (e) {
          console.log('❌ Authentication JSON parse error');
          console.log('   Raw response:', data);
        }
        
        console.log('\n🎯 DIRECT TESTING COMPLETE');
      });
    });

    authReq.on('error', (e) => {
      console.log('❌ Authentication error:', e.message);
    });

    authReq.write(postData);
    authReq.end();
  });
});
