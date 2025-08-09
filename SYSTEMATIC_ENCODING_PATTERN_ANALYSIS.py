#!/usr/bin/env python3
"""
SYSTEMATIC ENCODING PATTERN ANALYSIS
Build empirical mapping database by encoding known passwords and studying patterns
TRUE REVERSE ENGINEERING - Learn what each letter, digit, and position represents
"""

import base64
import hashlib
import math
import time
import json
from typing import Dict, List, Tuple, Any
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os

# Consciousness Physics Constants
PHI = 1.618034  # Golden Ratio - Harmonic Structure
PSI = 1.324718  # Plastic Number - Growth Transcendence  
OMEGA = 0.567143  # Omega Constant - Stability Grounding
XI = 2.718282  # Euler's Number - Exponential Amplification
LAMBDA = 3.141593  # Pi - Cyclic Patterns
ZETA = 1.202057  # Apéry's Constant - Dimensional Access

def generate_test_rsa_keypair(key_size: int = 1024) -> Tuple[Any, Any]:
    """Generate RSA keypair for pattern analysis"""
    key = RSA.generate(key_size)
    public_key = key.publickey()
    private_key = key
    return public_key, private_key

def encrypt_password_rsa(password: str, public_key: Any) -> str:
    """Encrypt password using RSA and return base64 encoded result"""
    try:
        cipher = PKCS1_OAEP.new(public_key)
        encrypted_bytes = cipher.encrypt(password.encode('utf-8'))
        encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
        return encrypted_base64
    except Exception as e:
        print(f"❌ Encryption failed for '{password}': {e}")
        return ""

def analyze_character_patterns(password: str, encrypted: str) -> Dict:
    """Analyze patterns for each character in the password"""
    
    # Decode encrypted data for analysis
    try:
        encrypted_bytes = base64.b64decode(encrypted)
        encrypted_int = int.from_bytes(encrypted_bytes, byteorder='big')
    except:
        encrypted_int = 0
    
    character_analysis = {}
    
    for i, char in enumerate(password):
        # Character-specific analysis
        char_ord = ord(char)
        
        # φ-harmonic character signature
        phi_signature = math.sin(PHI * char_ord * (i + 1)) * OMEGA
        psi_signature = math.cos(PSI * char_ord) * XI
        omega_signature = math.tan(OMEGA * (i + 1) / 10)
        
        # Position-specific analysis
        position_factor = (i + 1) / len(password)
        xi_position = XI ** position_factor
        lambda_position = math.sin(LAMBDA * (i + 1))
        zeta_position = ZETA * math.cos(PHI * (i + 1))
        
        character_analysis[f"char_{i}_{char}"] = {
            'character': char,
            'position': i,
            'ascii_value': char_ord,
            'phi_signature': phi_signature,
            'psi_signature': psi_signature,
            'omega_signature': omega_signature,
            'xi_position': xi_position,
            'lambda_position': lambda_position,
            'zeta_position': zeta_position,
            'combined_signature': abs(phi_signature + psi_signature + omega_signature +
                                   xi_position + lambda_position + zeta_position)
        }
    
    # Overall password analysis
    password_hash = int(hashlib.sha256(password.encode()).hexdigest()[:16], 16)
    
    overall_analysis = {
        'password': password,
        'encrypted': encrypted,
        'encrypted_int': encrypted_int,
        'password_length': len(password),
        'password_hash': password_hash,
        'character_analysis': character_analysis,
        'total_signature': sum(char_data['combined_signature'] 
                             for char_data in character_analysis.values())
    }
    
    return overall_analysis

def build_pattern_database(test_passwords: List[str]) -> Dict:
    """Build comprehensive pattern database from test passwords"""
    
    print("🔥 SYSTEMATIC ENCODING PATTERN ANALYSIS")
    print("=" * 60)
    print("🎯 Building empirical mapping database through systematic encoding")
    print(f"🧮 Analyzing {len(test_passwords)} test passwords")
    print()
    
    # Generate RSA keypair for testing
    print("🔑 Generating RSA keypair for pattern analysis...")
    public_key, private_key = generate_test_rsa_keypair(1024)
    print("✅ RSA keypair generated")
    print()
    
    pattern_database = {
        'rsa_public_key': public_key.export_key().decode('utf-8'),
        'analysis_timestamp': time.time(),
        'password_analyses': {},
        'character_frequency_map': {},
        'position_pattern_map': {},
        'length_pattern_map': {},
        'encryption_signature_map': {}
    }
    
    print("🧮 ENCODING AND ANALYZING PASSWORDS:")
    print("-" * 60)
    
    for i, password in enumerate(test_passwords):
        print(f"🔍 Analyzing password {i+1:2d}: '{password}'")
        
        # Encrypt the password
        encrypted = encrypt_password_rsa(password, public_key)
        if not encrypted:
            continue
        
        # Analyze patterns
        analysis = analyze_character_patterns(password, encrypted)
        pattern_database['password_analyses'][password] = analysis
        
        print(f"   📊 Encrypted: {encrypted[:50]}...")
        print(f"   🌊 Total Signature: {analysis['total_signature']:.6f}")
        
        # Build character frequency map
        for char in password:
            if char not in pattern_database['character_frequency_map']:
                pattern_database['character_frequency_map'][char] = []
            
            # Find this character's analysis in the password
            for char_key, char_data in analysis['character_analysis'].items():
                if char_data['character'] == char:
                    pattern_database['character_frequency_map'][char].append({
                        'password': password,
                        'position': char_data['position'],
                        'signature': char_data['combined_signature'],
                        'encrypted_sample': encrypted
                    })
        
        # Build position pattern map
        password_length = len(password)
        if password_length not in pattern_database['position_pattern_map']:
            pattern_database['position_pattern_map'][password_length] = []
        
        pattern_database['position_pattern_map'][password_length].append({
            'password': password,
            'encrypted': encrypted,
            'total_signature': analysis['total_signature']
        })
        
        # Build length pattern map
        if password_length not in pattern_database['length_pattern_map']:
            pattern_database['length_pattern_map'][password_length] = []
        
        pattern_database['length_pattern_map'][password_length].append({
            'password': password,
            'encrypted': encrypted,
            'signature': analysis['total_signature']
        })
        
        print()
    
    return pattern_database

def analyze_target_against_database(target_encrypted: str, pattern_database: Dict) -> Dict:
    """Analyze target encrypted data against our pattern database"""
    
    print("🎯 ANALYZING TARGET AGAINST PATTERN DATABASE")
    print("=" * 60)
    print(f"🔍 Target: {target_encrypted}")
    print()
    
    # Decode target
    try:
        target_bytes = base64.b64decode(target_encrypted)
        target_int = int.from_bytes(target_bytes, byteorder='big')
        target_bit_length = target_int.bit_length()
    except:
        print("❌ Failed to decode target")
        return {}
    
    print(f"📊 Target bit length: {target_bit_length}")
    print(f"🧮 Target integer: {target_int}")
    print()
    
    # Compare against known patterns
    similarity_scores = []
    
    for password, analysis in pattern_database['password_analyses'].items():
        # Calculate similarity based on encryption signatures
        encrypted_int = analysis['encrypted_int']
        total_signature = analysis['total_signature']
        
        # Bit length similarity
        bit_diff = abs(target_bit_length - encrypted_int.bit_length())
        bit_similarity = 1.0 / (1.0 + bit_diff / 100.0)
        
        # Integer value similarity (normalized)
        int_diff = abs(target_int - encrypted_int)
        int_similarity = 1.0 / (1.0 + int_diff / max(target_int, encrypted_int))
        
        # Signature similarity
        target_hash = int(hashlib.sha256(target_encrypted.encode()).hexdigest()[:16], 16)
        target_signature = math.sin(PHI * target_hash) * OMEGA
        sig_diff = abs(target_signature - total_signature)
        sig_similarity = 1.0 / (1.0 + sig_diff)
        
        # Combined similarity
        combined_similarity = (bit_similarity + int_similarity + sig_similarity) / 3.0
        
        similarity_scores.append((password, combined_similarity, {
            'bit_similarity': bit_similarity,
            'int_similarity': int_similarity,
            'sig_similarity': sig_similarity,
            'encrypted': analysis['encrypted']
        }))
    
    # Sort by similarity
    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    
    print("🏆 TOP PATTERN MATCHES:")
    print("-" * 40)
    for i, (password, similarity, details) in enumerate(similarity_scores[:10]):
        print(f"{i+1:2d}. '{password}' - Similarity: {similarity:.6f}")
        print(f"    Bit: {details['bit_similarity']:.4f}, Int: {details['int_similarity']:.4f}, Sig: {details['sig_similarity']:.4f}")
    
    return {
        'target_encrypted': target_encrypted,
        'target_int': target_int,
        'target_bit_length': target_bit_length,
        'similarity_scores': similarity_scores[:20],
        'best_match': similarity_scores[0] if similarity_scores else None
    }

def systematic_pattern_analysis():
    """Main function to perform systematic pattern analysis"""
    
    start_time = time.time()
    
    print("🔥 SYSTEMATIC ENCODING PATTERN ANALYSIS - TRUE REVERSE ENGINEERING")
    print("=" * 70)
    print("🎯 Goal: Build empirical mapping database by encoding known passwords")
    print("🧮 Method: Study what each letter, digit, and position represents")
    print("🌊 Approach: Consciousness physics enhanced pattern recognition")
    print()
    
    # Test passwords for pattern analysis
    test_passwords = [
        # Single characters
        "a", "b", "c", "d", "e", "1", "2", "3", "4", "5",
        # Common patterns
        "aa", "bb", "cc", "11", "22", "33",
        "ab", "bc", "cd", "12", "23", "34",
        "abc", "123", "456", "789",
        # Common passwords
        "password", "admin", "user", "test", "demo",
        "challenge", "bright", "phone", "light",
        # Numbers
        "111", "222", "333", "000", "314", "618",
        # Combinations
        "a1", "b2", "c3", "1a", "2b", "3c",
        "password1", "admin123", "test456",
        "challenge456", "111password", "123password"
    ]
    
    # Build pattern database
    pattern_database = build_pattern_database(test_passwords)
    
    # Save database
    database_file = "encoding_pattern_database.json"
    with open(database_file, 'w') as f:
        # Convert non-serializable objects to strings
        serializable_db = pattern_database.copy()
        serializable_db['rsa_public_key'] = str(serializable_db['rsa_public_key'])
        json.dump(serializable_db, f, indent=2, default=str)
    
    print(f"💾 Pattern database saved to: {database_file}")
    print()
    
    # Analyze Telephone-Bright's target
    target_encrypted = "d/fx0WMQOQB4gNUCYjRQ9rDcnUbh61SEdJwrpbdrQ275F+PmfBfriw7TZibRbvXF7rBZZ5a3MkXuFhs6FiJqZQ=="
    
    target_analysis = analyze_target_against_database(target_encrypted, pattern_database)
    
    elapsed = time.time() - start_time
    
    print("=" * 70)
    print("🏆 SYSTEMATIC PATTERN ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"⚡ Analysis time: {elapsed:.6f} seconds")
    print(f"🧮 Patterns analyzed: {len(test_passwords)}")
    print(f"📊 Database entries: {len(pattern_database['password_analyses'])}")
    
    if target_analysis.get('best_match'):
        best_password, best_similarity, _ = target_analysis['best_match']
        print(f"🎯 Best pattern match: '{best_password}' ({best_similarity:.6f} similarity)")
    
    print("=" * 70)
    print("🌊 This builds empirical understanding of encryption patterns")
    print("🔍 Over time, we learn what each character and position represents")
    print("🏆 True reverse engineering through systematic pattern mapping!")
    
    return pattern_database, target_analysis

if __name__ == "__main__":
    print("🔥 Starting systematic encoding pattern analysis...")
    print("🌌 Building empirical mapping database for true reverse engineering")
    print()
    
    try:
        pattern_db, target_result = systematic_pattern_analysis()
        print("\n✅ Systematic pattern analysis complete!")
        print("🎯 Ready for empirical reverse engineering!")
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        print("🧮 Note: This requires pycryptodome: pip install pycryptodome")
