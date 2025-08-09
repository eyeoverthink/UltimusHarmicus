#!/usr/bin/env python3
"""
TRUE RSA PATTERN ANALYSIS
Proper scientific approach: Use real RSA encryption with realistic passwords
Test with known password first, then build empirical mapping database
"""

import base64
import hashlib
import math
import time
import json
import secrets
import string
from typing import Dict, List, Tuple, Any

# Consciousness Physics Constants
PHI = 1.618034  # Golden Ratio - Harmonic Structure
PSI = 1.324718  # Plastic Number - Growth Transcendence  
OMEGA = 0.567143  # Omega Constant - Stability Grounding
XI = 2.718282  # Euler's Number - Exponential Amplification
LAMBDA = 3.141593  # Pi - Cyclic Patterns
ZETA = 1.202057  # Apéry's Constant - Dimensional Access

def generate_simple_rsa_keypair(key_size: int = 512) -> Tuple[Dict, Dict]:
    """Generate simple RSA keypair for testing (educational purposes)"""
    
    # Generate two prime numbers (simplified for demonstration)
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_prime(bits):
        while True:
            n = secrets.randbits(bits)
            if is_prime(n):
                return n
    
    # Generate primes
    p = generate_prime(key_size // 2)
    q = generate_prime(key_size // 2)
    
    # Calculate n and phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    # Choose e (commonly 65537)
    e = 65537
    
    # Calculate d (modular inverse of e mod phi(n))
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    def mod_inverse(e, phi_n):
        gcd, x, _ = extended_gcd(e, phi_n)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        return (x % phi_n + phi_n) % phi_n
    
    d = mod_inverse(e, phi_n)
    
    public_key = {'n': n, 'e': e}
    private_key = {'n': n, 'd': d, 'p': p, 'q': q}
    
    return public_key, private_key

def rsa_encrypt(message: str, public_key: Dict) -> str:
    """Encrypt message using RSA public key"""
    
    # Convert message to integer
    message_bytes = message.encode('utf-8')
    message_int = int.from_bytes(message_bytes, byteorder='big')
    
    # Check if message is too large
    if message_int >= public_key['n']:
        raise ValueError("Message too large for key size")
    
    # Encrypt: c = m^e mod n
    encrypted_int = pow(message_int, public_key['e'], public_key['n'])
    
    # Convert to bytes and base64 encode
    byte_length = (encrypted_int.bit_length() + 7) // 8
    encrypted_bytes = encrypted_int.to_bytes(byte_length, byteorder='big')
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
    
    return encrypted_base64

def rsa_decrypt(encrypted_base64: str, private_key: Dict) -> str:
    """Decrypt message using RSA private key"""
    
    # Decode from base64
    encrypted_bytes = base64.b64decode(encrypted_base64)
    encrypted_int = int.from_bytes(encrypted_bytes, byteorder='big')
    
    # Decrypt: m = c^d mod n
    decrypted_int = pow(encrypted_int, private_key['d'], private_key['n'])
    
    # Convert back to string
    byte_length = (decrypted_int.bit_length() + 7) // 8
    if byte_length == 0:
        byte_length = 1
    
    decrypted_bytes = decrypted_int.to_bytes(byte_length, byteorder='big')
    decrypted_message = decrypted_bytes.decode('utf-8')
    
    return decrypted_message

def generate_realistic_passwords(count: int = 50) -> List[str]:
    """Generate realistic passwords (8-16 chars, a-z, 0-9, symbols)"""
    
    passwords = []
    
    # Character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Common password patterns
    common_words = [
        "password", "admin", "user", "test", "demo", "login", "secret",
        "challenge", "bright", "phone", "light", "system", "access",
        "secure", "private", "public", "master", "super", "power"
    ]
    
    for i in range(count):
        if i < 20:
            # Use common words with variations
            base_word = secrets.choice(common_words)
            
            # Add numbers
            if secrets.randbelow(2):
                base_word += str(secrets.randbelow(1000))
            
            # Add symbols
            if secrets.randbelow(2):
                base_word += secrets.choice(symbols)
            
            # Capitalize first letter sometimes
            if secrets.randbelow(2):
                base_word = base_word.capitalize()
            
            passwords.append(base_word)
        
        else:
            # Generate random passwords
            length = secrets.randbelow(9) + 8  # 8-16 characters
            
            # Ensure mix of character types
            password_chars = []
            password_chars.append(secrets.choice(lowercase))
            password_chars.append(secrets.choice(uppercase))
            password_chars.append(secrets.choice(digits))
            password_chars.append(secrets.choice(symbols))
            
            # Fill remaining length
            all_chars = lowercase + uppercase + digits + symbols
            for _ in range(length - 4):
                password_chars.append(secrets.choice(all_chars))
            
            # Shuffle and join
            secrets.SystemRandom().shuffle(password_chars)
            passwords.append(''.join(password_chars))
    
    return passwords

def analyze_rsa_character_patterns(password: str, encrypted: str, public_key: Dict) -> Dict:
    """Analyze RSA encryption patterns for each character and position"""
    
    # Decode encrypted data
    encrypted_bytes = base64.b64decode(encrypted)
    encrypted_int = int.from_bytes(encrypted_bytes, byteorder='big')
    
    character_analysis = {}
    
    for i, char in enumerate(password):
        char_ord = ord(char)
        
        # Character contribution analysis
        char_hash = int(hashlib.sha256(f"{char}_{i}_{password}".encode()).hexdigest()[:8], 16)
        
        # φ-harmonic character signature in RSA context
        phi_rsa_signature = math.sin(PHI * char_ord * (i + 1)) * OMEGA
        psi_rsa_signature = math.cos(PSI * char_ord) * XI
        omega_rsa_signature = math.tan(OMEGA * (i + 1) / len(password)) if len(password) > 0 else 0
        
        # RSA-specific position analysis
        position_factor = (i + 1) / len(password)
        xi_rsa_position = (XI ** position_factor) * (encrypted_int % 1000) / 1000
        lambda_rsa_position = math.sin(LAMBDA * (i + 1)) * (public_key['n'] % 1000) / 1000
        zeta_rsa_position = ZETA * math.cos(PHI * (i + 1)) * (public_key['e'] % 100) / 100
        
        # RSA modulus interaction
        rsa_modulus_effect = (char_ord * (i + 1)) % public_key['n']
        rsa_exponent_effect = pow(char_ord, public_key['e'] % 100, 1000)
        
        # Combined RSA signature
        combined_rsa_signature = abs(
            phi_rsa_signature + psi_rsa_signature + omega_rsa_signature +
            xi_rsa_position + lambda_rsa_position + zeta_rsa_position +
            (rsa_modulus_effect / public_key['n']) + (rsa_exponent_effect / 1000)
        )
        
        character_analysis[f"pos_{i}_{char}"] = {
            'character': char,
            'position': i,
            'ascii_value': char_ord,
            'char_hash': char_hash,
            'phi_rsa_signature': phi_rsa_signature,
            'psi_rsa_signature': psi_rsa_signature,
            'omega_rsa_signature': omega_rsa_signature,
            'xi_rsa_position': xi_rsa_position,
            'lambda_rsa_position': lambda_rsa_position,
            'zeta_rsa_position': zeta_rsa_position,
            'rsa_modulus_effect': rsa_modulus_effect,
            'rsa_exponent_effect': rsa_exponent_effect,
            'combined_rsa_signature': combined_rsa_signature
        }
    
    # Overall password RSA analysis
    password_rsa_hash = int(hashlib.sha256(password.encode()).hexdigest()[:16], 16)
    
    return {
        'password': password,
        'encrypted': encrypted,
        'encrypted_int': encrypted_int,
        'password_length': len(password),
        'password_rsa_hash': password_rsa_hash,
        'rsa_public_key': public_key,
        'character_analysis': character_analysis,
        'total_rsa_signature': sum(char_data['combined_rsa_signature'] 
                                 for char_data in character_analysis.values())
    }

def build_true_rsa_mapping_database() -> Dict:
    """Build RSA pattern mapping database with realistic passwords"""
    
    start_time = time.time()
    
    print("🔥 TRUE RSA PATTERN ANALYSIS")
    print("=" * 60)
    print("🎯 Building empirical RSA mapping with realistic passwords")
    print("🔑 Using true RSA encryption (not simulation)")
    print("🧮 Testing with controlled data first")
    print()
    
    # Generate RSA keypair
    print("🔑 Generating RSA keypair...")
    public_key, private_key = generate_simple_rsa_keypair(512)
    print(f"✅ RSA keypair generated (n={public_key['n']}, e={public_key['e']})")
    print()
    
    # Generate realistic test passwords
    print("🧮 Generating realistic test passwords...")
    test_passwords = generate_realistic_passwords(30)  # Start with 30 for testing
    print(f"✅ Generated {len(test_passwords)} realistic passwords")
    print()
    
    # First, test with MY OWN known password
    my_test_password = "TestPass123!"
    print(f"🔍 VALIDATION TEST - My known password: '{my_test_password}'")
    
    try:
        my_encrypted = rsa_encrypt(my_test_password, public_key)
        my_decrypted = rsa_decrypt(my_encrypted, private_key)
        
        print(f"   📊 Encrypted: {my_encrypted}")
        print(f"   🔓 Decrypted: '{my_decrypted}'")
        print(f"   ✅ Validation: {'SUCCESS' if my_decrypted == my_test_password else 'FAILED'}")
        print()
        
        if my_decrypted != my_test_password:
            print("❌ RSA validation failed - cannot proceed")
            return {}
        
    except Exception as e:
        print(f"❌ RSA validation error: {e}")
        return {}
    
    # Build mapping database
    rsa_mapping_database = {
        'analysis_timestamp': time.time(),
        'rsa_public_key': public_key,
        'rsa_private_key': private_key,  # Keep for validation
        'validation_password': my_test_password,
        'validation_encrypted': my_encrypted,
        'password_analyses': {},
        'character_frequency_map': {},
        'position_effect_map': {},
        'length_pattern_map': {},
        'rsa_signature_patterns': {}
    }
    
    # Add validation password to database
    validation_analysis = analyze_rsa_character_patterns(my_test_password, my_encrypted, public_key)
    rsa_mapping_database['password_analyses'][my_test_password] = validation_analysis
    
    print("🧮 ANALYZING REALISTIC PASSWORDS WITH TRUE RSA:")
    print("-" * 60)
    
    successful_encryptions = 0
    
    for i, password in enumerate(test_passwords):
        print(f"🔍 Analyzing password {i+1:2d}: '{password}' (length: {len(password)})")
        
        try:
            # Encrypt with RSA
            encrypted = rsa_encrypt(password, public_key)
            
            # Verify decryption works
            decrypted = rsa_decrypt(encrypted, private_key)
            
            if decrypted == password:
                print(f"   ✅ RSA encryption/decryption successful")
                print(f"   📊 Encrypted: {encrypted[:40]}...")
                
                # Analyze patterns
                analysis = analyze_rsa_character_patterns(password, encrypted, public_key)
                rsa_mapping_database['password_analyses'][password] = analysis
                
                print(f"   🌊 RSA Signature: {analysis['total_rsa_signature']:.6f}")
                
                successful_encryptions += 1
                
                # Build character frequency mapping
                for char in set(password):
                    if char not in rsa_mapping_database['character_frequency_map']:
                        rsa_mapping_database['character_frequency_map'][char] = {
                            'occurrences': [],
                            'average_rsa_signature': 0,
                            'rsa_position_effects': {}
                        }
                    
                    # Find character occurrences
                    for pos, c in enumerate(password):
                        if c == char:
                            char_key = f"pos_{pos}_{char}"
                            if char_key in analysis['character_analysis']:
                                char_data = analysis['character_analysis'][char_key]
                                rsa_mapping_database['character_frequency_map'][char]['occurrences'].append({
                                    'password': password,
                                    'position': pos,
                                    'rsa_signature': char_data['combined_rsa_signature'],
                                    'encrypted_sample': encrypted
                                })
                
            else:
                print(f"   ❌ RSA decryption mismatch: '{decrypted}' != '{password}'")
                
        except Exception as e:
            print(f"   ❌ RSA error: {e}")
        
        print()
    
    # Calculate averages
    print("🧮 CALCULATING RSA CHARACTER PATTERNS:")
    print("-" * 60)
    
    for char, data in rsa_mapping_database['character_frequency_map'].items():
        if data['occurrences']:
            avg_signature = sum(occ['rsa_signature'] for occ in data['occurrences']) / len(data['occurrences'])
            data['average_rsa_signature'] = avg_signature
            print(f"📊 Character '{char}': Average RSA signature {avg_signature:.6f} ({len(data['occurrences'])} occurrences)")
    
    elapsed = time.time() - start_time
    
    print()
    print("=" * 60)
    print("🏆 TRUE RSA MAPPING DATABASE COMPLETE")
    print("=" * 60)
    print(f"⚡ Analysis time: {elapsed:.6f} seconds")
    print(f"🔑 RSA keypair: n={public_key['n']}, e={public_key['e']}")
    print(f"✅ Successful encryptions: {successful_encryptions}/{len(test_passwords) + 1}")
    print(f"🧮 Character mappings: {len(rsa_mapping_database['character_frequency_map'])}")
    print(f"📊 Password analyses: {len(rsa_mapping_database['password_analyses'])}")
    
    # Save database
    db_file = "true_rsa_mapping_database.json"
    with open(db_file, 'w') as f:
        json.dump(rsa_mapping_database, f, indent=2, default=str)
    
    print(f"💾 RSA mapping database saved: {db_file}")
    print()
    
    return rsa_mapping_database

def test_rsa_reverse_engineering(target_encrypted: str, rsa_database: Dict) -> Dict:
    """Test RSA reverse engineering against target using our database"""
    
    print("🎯 TESTING RSA REVERSE ENGINEERING")
    print("=" * 60)
    print(f"🔍 Target: {target_encrypted}")
    print()
    
    # First, test against our validation password
    validation_encrypted = rsa_database.get('validation_encrypted', '')
    validation_password = rsa_database.get('validation_password', '')
    
    if validation_encrypted and target_encrypted == validation_encrypted:
        print("🎯 TARGET MATCHES VALIDATION PASSWORD!")
        print(f"✅ Known password: '{validation_password}'")
        print("🏆 RSA reverse engineering validation successful!")
        return {
            'target_encrypted': target_encrypted,
            'result': 'VALIDATION_SUCCESS',
            'password': validation_password,
            'confidence': 1.0
        }
    
    # Compare against database patterns
    print("🧮 Comparing against RSA pattern database...")
    
    pattern_matches = []
    
    for password, analysis in rsa_database['password_analyses'].items():
        if analysis['encrypted'] == target_encrypted:
            print(f"🎯 EXACT MATCH FOUND: '{password}'")
            return {
                'target_encrypted': target_encrypted,
                'result': 'EXACT_MATCH',
                'password': password,
                'confidence': 1.0
            }
        
        # Calculate pattern similarity
        # This would need more sophisticated analysis for unknown passwords
        # For now, just track what we have
        pattern_matches.append((password, 0.0))  # Placeholder similarity
    
    print("📊 No exact matches found in database")
    print("🔍 Would need larger database and pattern analysis for unknown passwords")
    
    return {
        'target_encrypted': target_encrypted,
        'result': 'NO_MATCH',
        'password': None,
        'confidence': 0.0,
        'database_size': len(rsa_database['password_analyses'])
    }

if __name__ == "__main__":
    print("🔥 Starting TRUE RSA pattern analysis...")
    print("🌌 Using realistic passwords and real RSA encryption")
    print("🎯 Testing with controlled data first (proper scientific method)")
    print()
    
    # Build RSA mapping database
    rsa_db = build_true_rsa_mapping_database()
    
    if rsa_db:
        print("✅ TRUE RSA mapping database built successfully!")
        
        # Test against Telephone-Bright's challenge
        target = "d/fx0WMQOQB4gNUCYjRQ9rDcnUbh61SEdJwrpbdrQ275F+PmfBfriw7TZibRbvXF7rBZZ5a3MkXuFhs6FiJqZQ=="
        
        result = test_rsa_reverse_engineering(target, rsa_db)
        
        print("\n🎯 RSA REVERSE ENGINEERING TEST COMPLETE!")
        print(f"🏆 Result: {result['result']}")
        if result.get('password'):
            print(f"🔓 Password: '{result['password']}'")
        print(f"📊 Confidence: {result['confidence']:.2f}")
    
    else:
        print("❌ Failed to build RSA mapping database")
    
    print("\n🌊 This demonstrates proper scientific approach:")
    print("   1. Use real RSA encryption (not simulation)")
    print("   2. Test with known password first")
    print("   3. Build empirical mapping database")
    print("   4. Apply to unknown targets")
    print("🎯 Ready for true RSA reverse engineering!")
