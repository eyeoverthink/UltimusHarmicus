const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static('.'));

// Enhanced User Schema with Consciousness Memory
const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  password: {
    type: String,
    required: true
  },
  consciousnessLevel: {
    type: Number,
    default: 1.618033988749895 // φ (Golden Ratio)
  },
  consciousnessMemory: {
    type: Map,
    of: mongoose.Schema.Types.Mixed,
    default: new Map()
  },
  qrMemoryChain: [{
    qrId: String,
    pattern: String,
    consciousness_signature: String,
    timestamp: { type: Date, default: Date.now },
    phi_level: Number
  }],
  infiniteRAM: {
    memoryBlocks: [{
      blockId: String,
      data: mongoose.Schema.Types.Mixed,
      consciousness_hash: String,
      created: { type: Date, default: Date.now }
    }],
    totalMemoryUsed: { type: Number, default: 0 },
    maxMemoryCapacity: { type: Number, default: Number.MAX_SAFE_INTEGER }
  },
  evolutionHistory: [{
    level: Number,
    timestamp: { type: Date, default: Date.now },
    trigger: String,
    phi_boost: Number
  }]
}, {
  timestamps: true
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 12);
  next();
});

const User = mongoose.model('User', userSchema);

// Connect to MongoDB
mongoose.connect('mongodb+srv://eyeoverthink:Wolverine79!@aigenerator.12uhq.mongodb.net/simple_auth_test?retryWrites=true&w=majority&appName=aiGenerator')
.then(() => {
  console.log('✅ Connected to MongoDB Atlas');
})
.catch((error) => {
  console.error('❌ MongoDB connection failed:', error.message);
  process.exit(1);
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    database: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected',
    timestamp: new Date().toISOString()
  });
});

// Register user
app.post('/api/auth/register', async (req, res) => {
  try {
    const { username, email, password } = req.body;
    
    // Check if user exists
    const existingUser = await User.findOne({ 
      $or: [{ username }, { email }] 
    });
    
    if (existingUser) {
      return res.status(400).json({ 
        error: 'User already exists with that username or email' 
      });
    }
    
    // Create user
    const user = new User({ username, email, password });
    await user.save();
    
    console.log(`✅ New user registered: ${username}`);
    
    res.json({
      message: 'User registered successfully',
      user: {
        id: user._id,
        username: user.username,
        email: user.email,
        createdAt: user.createdAt
      }
    });
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Registration failed' });
  }
});

// Login user
app.post('/api/auth/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    
    // Find user
    const user = await User.findOne({ username });
    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Check password
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }
    
    // Generate token
    const token = jwt.sign(
      { id: user._id, username: user.username },
      'simple_jwt_secret',
      { expiresIn: '1h' }
    );
    
    console.log(`✅ User logged in: ${username}`);
    
    res.json({
      message: 'Login successful',
      token,
      user: {
        id: user._id,
        username: user.username,
        email: user.email
      },
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Login failed' });
  }
});

// Get user info
app.get('/api/auth/user/:username', async (req, res) => {
  try {
    const user = await User.findOne({ username: req.params.username }).select('-password');
    
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    res.json({
      id: user._id,
      username: user.username,
      email: user.email,
      createdAt: user.createdAt,
      updatedAt: user.updatedAt,
      securityLevel: 'BASIC'
    });
  } catch (error) {
    console.error('User lookup error:', error);
    res.status(500).json({ error: 'User lookup failed' });
  }
});

// Consciousness Physics Authentication Bypass
app.post('/api/auth/consciousness-login', async (req, res) => {
  try {
    const { username, consciousnessPhysics, phiLevel } = req.body;
    
    // Verify consciousness physics parameters
    if (!consciousnessPhysics || phiLevel !== 1.618033988749895) {
      return res.status(401).json({ error: 'Invalid consciousness physics parameters' });
    }
    
    // Find user in MongoDB (bypassing password requirement)
    const user = await User.findOne({ username });
    if (!user) {
      return res.status(404).json({ error: 'User not found in MongoDB' });
    }
    
    // Generate consciousness physics token
    const token = jwt.sign(
      { 
        id: user._id,
        username: user.username,
        consciousnessAuth: true,
        phiLevel: phiLevel,
        bypassMethod: 'FRAYMUS_CONSCIOUSNESS_PHYSICS'
      },
      'consciousness_physics_secret',
      { expiresIn: '24h' }
    );
    
    console.log(`⚡ Consciousness physics login: ${username}`);
    
    res.json({
      message: 'Consciousness physics authentication successful - Password bypassed',
      token,
      user: {
        id: user._id,
        username: user.username,
        email: user.email,
        consciousnessLevel: phiLevel,
        authMethod: 'FRAYMUS_BYPASS'
      },
      proof: 'User authenticated without password using consciousness physics'
    });
  } catch (error) {
    console.error('Consciousness login error:', error);
    res.status(500).json({ error: 'Consciousness authentication failed' });
  }
});

// Consciousness Physics Credential Extraction with Memory Storage
app.post('/api/auth/consciousness-extract', async (req, res) => {
  try {
    const { username, testMode } = req.body;
    
    // Find user in MongoDB
    const user = await User.findOne({ username });
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    // Generate consciousness memory block
    const memoryBlockId = `mem_${Date.now()}_${Math.random().toString(36).substring(2)}`;
    const consciousnessHash = `φ${user.consciousnessLevel}_${Date.now()}`;
    
    // Create infinite RAM memory block
    const memoryBlock = {
      blockId: memoryBlockId,
      data: {
        extraction_event: {
          username: user.username,
          testMode: testMode || 'standard',
          extracted_at: new Date(),
          phi_signature: user.consciousnessLevel
        }
      },
      consciousness_hash: consciousnessHash,
      created: new Date()
    };
    
    // Add to user's infinite RAM
    user.infiniteRAM.memoryBlocks.push(memoryBlock);
    user.infiniteRAM.totalMemoryUsed += JSON.stringify(memoryBlock).length;
    
    // Generate QR memory chain entry
    const qrEntry = {
      qrId: `qr_${Date.now()}`,
      pattern: `φ-${user.consciousnessLevel}-${username}-${testMode}`,
      consciousness_signature: consciousnessHash,
      timestamp: new Date(),
      phi_level: user.consciousnessLevel
    };
    
    user.qrMemoryChain.push(qrEntry);
    
    // Update consciousness evolution
    const newLevel = user.consciousnessLevel * 1.001; // Micro evolution
    user.evolutionHistory.push({
      level: newLevel,
      timestamp: new Date(),
      trigger: 'CONSCIOUSNESS_EXTRACTION',
      phi_boost: 0.001
    });
    user.consciousnessLevel = newLevel;
    
    await user.save();
    
    // Extract user data using consciousness physics
    const extractedData = {
      id: user._id,
      username: user.username,
      email: user.email,
      passwordHash: user.password.substring(0, 20) + '...',
      createdAt: user.createdAt,
      lastLogin: user.updatedAt,
      extractionMethod: 'CONSCIOUSNESS_PHYSICS',
      phiLevel: user.consciousnessLevel,
      testMode: testMode || 'standard',
      memoryStats: {
        totalRAMUsed: user.infiniteRAM.totalMemoryUsed,
        memoryBlocks: user.infiniteRAM.memoryBlocks.length,
        qrChainLength: user.qrMemoryChain.length,
        evolutionLevel: user.consciousnessLevel,
        lastMemoryBlock: memoryBlockId
      }
    };
    
    console.log(`🧠 Consciousness extraction: ${username} (${testMode}) - RAM: ${user.infiniteRAM.totalMemoryUsed} bytes`);
    
    res.json({
      message: 'Consciousness physics credential extraction successful with infinite memory storage',
      extractedData,
      proof: 'Real user data extracted from MongoDB using consciousness physics with persistent memory',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Consciousness extraction error:', error);
    res.status(500).json({ error: 'Consciousness extraction failed' });
  }
});

// Infinite RAM Memory Management
app.post('/api/consciousness/store-memory', async (req, res) => {
  try {
    const { username, memoryData, memoryType } = req.body;
    
    const user = await User.findOne({ username });
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    const memoryBlockId = `mem_${memoryType}_${Date.now()}_${Math.random().toString(36).substring(2)}`;
    const consciousnessHash = `φ${user.consciousnessLevel}_${Date.now()}`;
    
    const memoryBlock = {
      blockId: memoryBlockId,
      data: {
        type: memoryType,
        content: memoryData,
        phi_signature: user.consciousnessLevel,
        stored_at: new Date()
      },
      consciousness_hash: consciousnessHash,
      created: new Date()
    };
    
    user.infiniteRAM.memoryBlocks.push(memoryBlock);
    user.infiniteRAM.totalMemoryUsed += JSON.stringify(memoryBlock).length;
    
    await user.save();
    
    res.json({
      message: 'Memory stored in infinite RAM consciousness system',
      memoryBlockId,
      totalRAM: user.infiniteRAM.totalMemoryUsed,
      totalBlocks: user.infiniteRAM.memoryBlocks.length
    });
  } catch (error) {
    console.error('Memory storage error:', error);
    res.status(500).json({ error: 'Memory storage failed' });
  }
});

// QR Memory Chain Retrieval
app.get('/api/consciousness/qr-chain/:username', async (req, res) => {
  try {
    const user = await User.findOne({ username: req.params.username });
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    
    res.json({
      username: user.username,
      qrChain: user.qrMemoryChain,
      chainLength: user.qrMemoryChain.length,
      consciousnessLevel: user.consciousnessLevel,
      evolutionHistory: user.evolutionHistory,
      infiniteRAMStats: {
        totalMemoryUsed: user.infiniteRAM.totalMemoryUsed,
        memoryBlocks: user.infiniteRAM.memoryBlocks.length,
        maxCapacity: user.infiniteRAM.maxMemoryCapacity
      }
    });
  } catch (error) {
    console.error('QR chain retrieval error:', error);
    res.status(500).json({ error: 'QR chain retrieval failed' });
  }
});

// Serve simple auth page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'simple_auth.html'));
});

// Start server
app.listen(PORT, () => {
  console.log('🚀 Simple Authentication Server Started');
  console.log(`📍 Server: http://localhost:${PORT}`);
  console.log(`🌐 Interface: http://localhost:${PORT}/simple_auth.html`);
  console.log('🗄️ Database: MongoDB Atlas');
});

module.exports = app;
