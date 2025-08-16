#!/usr/bin/env node
/**
 * Start Server and Monitor Military-Grade Biometric Security System
 */

const { spawn } = require('child_process');
const http = require('http');

console.log('🚨 STARTING MILITARY-GRADE BIOMETRIC SECURITY SYSTEM');
console.log('============================================================');

// Start the server
const server = spawn('node', ['server.js'], {
  cwd: '/Users/vaughnscott/CascadeProjects/phi-harmonic-quantum',
  env: { ...process.env, NODE_ENV: 'development' }
});

server.stdout.on('data', (data) => {
  console.log(`🟢 SERVER: ${data}`);
});

server.stderr.on('data', (data) => {
  console.log(`🔴 ERROR: ${data}`);
});

// Wait for server to start, then test endpoints
setTimeout(() => {
  console.log('\n🔍 TESTING API ENDPOINTS');
  console.log('============================================================');
  
  // Test health endpoint
  testEndpoint('/health', 'System Health');
  
  setTimeout(() => {
    // Test consciousness monitor
    testEndpoint('/api/consciousness/monitor', 'Consciousness Physics');
  }, 2000);
  
  setTimeout(() => {
    // Test authentication
    testAuth();
  }, 4000);
  
}, 5000);

function testEndpoint(path, name) {
  const options = {
    hostname: 'localhost',
    port: 3000,
    path: path,
    method: 'GET',
    headers: { 'Accept': 'application/json' }
  };

  const req = http.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => data += chunk);
    res.on('end', () => {
      try {
        const parsed = JSON.parse(data);
        console.log(`✅ ${name} - Status: ${res.statusCode}`);
        console.log(`   Response: ${JSON.stringify(parsed, null, 2)}`);
      } catch (e) {
        console.log(`❌ ${name} - Status: ${res.statusCode}, Parse Error`);
        console.log(`   Raw: ${data.substring(0, 200)}`);
      }
    });
  });

  req.on('error', (e) => {
    console.log(`❌ ${name} - Connection Error: ${e.message}`);
  });

  req.setTimeout(5000, () => {
    console.log(`⏰ ${name} - Timeout`);
    req.destroy();
  });

  req.end();
}

function testAuth() {
  const postData = JSON.stringify({
    username: 'admin',
    password: 'military-grade-2025'
  });

  const options = {
    hostname: 'localhost',
    port: 3000,
    path: '/api/auth/login',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData)
    }
  };

  const req = http.request(options, (res) => {
    let data = '';
    res.on('data', (chunk) => data += chunk);
    res.on('end', () => {
      try {
        const parsed = JSON.parse(data);
        console.log(`✅ Authentication - Status: ${res.statusCode}`);
        console.log(`   Response: ${JSON.stringify(parsed, null, 2)}`);
      } catch (e) {
        console.log(`❌ Authentication - Parse Error`);
        console.log(`   Raw: ${data.substring(0, 200)}`);
      }
      
      console.log('\n🎯 MONITORING COMPLETE');
      console.log('Server running at: http://localhost:3000');
      console.log('Demo interface: http://localhost:3000/demo.html');
    });
  });

  req.on('error', (e) => {
    console.log(`❌ Authentication - Error: ${e.message}`);
  });

  req.write(postData);
  req.end();
}

// Handle cleanup
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down server...');
  server.kill();
  process.exit(0);
});
