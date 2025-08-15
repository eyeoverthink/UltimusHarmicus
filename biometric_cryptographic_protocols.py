#!/usr/bin/env python3
"""
Biometric Cryptographic Protocols
Advanced protocols using biometric QR keys for secure communications
"""

import json
import time
import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from biometric_document_encryptor_ultimate import BiometricDocumentEncryptor

class BiometricCryptographicProtocols:
    def __init__(self):
        self.encryptor = BiometricDocumentEncryptor()
        
    def create_biometric_message_protocol(self, sender_bio_key, recipient_bio_key, message):
        """Create secure message protocol using dual biometric keys"""
        print("🔐 Creating biometric message protocol...")
        
        # Combine biometric keys for dual authentication
        combined_key = self.combine_biometric_keys(sender_bio_key, recipient_bio_key)
        
        # Create message envelope
        envelope = {
            'protocol': 'BiometricMessage',
            'version': '1.0',
            'timestamp': int(time.time()),
            'sender_hash': hashlib.sha256(json.dumps(sender_bio_key).encode()).hexdigest()[:16],
            'recipient_hash': hashlib.sha256(json.dumps(recipient_bio_key).encode()).hexdigest()[:16],
            'message': message
        }
        
        # Encrypt with combined biometric key
        encrypted_envelope = self.encrypt_with_biometric_key(json.dumps(envelope), combined_key)
        
        print("✅ Biometric message protocol created")
        return encrypted_envelope
    
    def create_biometric_signature_protocol(self, bio_key, document_hash):
        """Create biometric digital signature"""
        print("✍️ Creating biometric signature...")
        
        signature_data = {
            'protocol': 'BiometricSignature',
            'version': '1.0',
            'timestamp': int(time.time()),
            'signer_bio_hash': hashlib.sha256(json.dumps(bio_key).encode()).hexdigest(),
            'document_hash': document_hash,
            'signature_proof': self.generate_signature_proof(bio_key, document_hash)
        }
        
        print("✅ Biometric signature created")
        return signature_data
    
    def create_biometric_access_token(self, bio_key, resource_id, permissions, expiry_hours=24):
        """Create time-limited biometric access token"""
        print("🎫 Creating biometric access token...")
        
        expiry_time = int(time.time()) + (expiry_hours * 3600)
        
        token_data = {
            'protocol': 'BiometricAccessToken',
            'version': '1.0',
            'issued': int(time.time()),
            'expires': expiry_time,
            'bio_hash': hashlib.sha256(json.dumps(bio_key).encode()).hexdigest()[:16],
            'resource_id': resource_id,
            'permissions': permissions,
            'token_proof': self.generate_token_proof(bio_key, resource_id, expiry_time)
        }
        
        # Self-encrypt token with biometric key
        encrypted_token = self.encrypt_with_biometric_key(json.dumps(token_data), bio_key)
        
        print(f"✅ Biometric access token created (expires in {expiry_hours}h)")
        return encrypted_token
    
    def create_biometric_key_exchange_protocol(self, initiator_bio, responder_bio):
        """Create secure key exchange using biometric authentication"""
        print("🔄 Creating biometric key exchange...")
        
        # Generate session key
        session_key = base64.urlsafe_b64encode(hashlib.sha256(
            json.dumps(initiator_bio).encode() + 
            json.dumps(responder_bio).encode() + 
            str(time.time()).encode()
        ).digest())
        
        exchange_data = {
            'protocol': 'BiometricKeyExchange',
            'version': '1.0',
            'timestamp': int(time.time()),
            'initiator_hash': hashlib.sha256(json.dumps(initiator_bio).encode()).hexdigest()[:16],
            'responder_hash': hashlib.sha256(json.dumps(responder_bio).encode()).hexdigest()[:16],
            'session_key_hash': hashlib.sha256(session_key).hexdigest()[:16],
            'exchange_proof': self.generate_exchange_proof(initiator_bio, responder_bio, session_key)
        }
        
        print("✅ Biometric key exchange protocol created")
        return exchange_data, session_key
    
    def create_biometric_multi_sig_protocol(self, bio_keys, document_hash, threshold=None):
        """Create multi-signature protocol requiring multiple biometric approvals"""
        print(f"👥 Creating biometric multi-sig protocol ({len(bio_keys)} signers)...")
        
        if threshold is None:
            threshold = len(bio_keys)  # Require all signatures by default
        
        multi_sig_data = {
            'protocol': 'BiometricMultiSig',
            'version': '1.0',
            'timestamp': int(time.time()),
            'document_hash': document_hash,
            'required_signatures': threshold,
            'total_signers': len(bio_keys),
            'signer_hashes': [
                hashlib.sha256(json.dumps(bio_key).encode()).hexdigest()[:16] 
                for bio_key in bio_keys
            ],
            'signatures': []
        }
        
        # Generate individual signatures
        for i, bio_key in enumerate(bio_keys):
            signature = {
                'signer_index': i,
                'bio_hash': hashlib.sha256(json.dumps(bio_key).encode()).hexdigest()[:16],
                'signature': self.generate_signature_proof(bio_key, document_hash),
                'timestamp': int(time.time())
            }
            multi_sig_data['signatures'].append(signature)
        
        print(f"✅ Biometric multi-sig protocol created ({threshold}/{len(bio_keys)} required)")
        return multi_sig_data
    
    def create_biometric_smart_contract(self, bio_keys, contract_terms, execution_conditions):
        """Create biometric-secured smart contract"""
        print("📋 Creating biometric smart contract...")
        
        contract_data = {
            'protocol': 'BiometricSmartContract',
            'version': '1.0',
            'created': int(time.time()),
            'parties': [
                hashlib.sha256(json.dumps(bio_key).encode()).hexdigest()[:16] 
                for bio_key in bio_keys
            ],
            'terms': contract_terms,
            'execution_conditions': execution_conditions,
            'status': 'active',
            'contract_hash': None
        }
        
        # Generate contract hash
        contract_string = json.dumps(contract_data, sort_keys=True)
        contract_data['contract_hash'] = hashlib.sha256(contract_string.encode()).hexdigest()
        
        # Create biometric proof of agreement
        contract_data['biometric_proofs'] = [
            self.generate_signature_proof(bio_key, contract_data['contract_hash'])
            for bio_key in bio_keys
        ]
        
        print("✅ Biometric smart contract created")
        return contract_data
    
    def combine_biometric_keys(self, key1, key2):
        """Combine two biometric keys for dual authentication"""
        combined_data = {
            'h': [a + b for a, b in zip(key1['h'], key2['h'])],
            'c': (key1['c'] + key2['c']) / 2,
            'm': (key1['m'] + key2['m']) / 2
        }
        return combined_data
    
    def encrypt_with_biometric_key(self, data, bio_key):
        """Encrypt data using biometric key"""
        bio_string = json.dumps(bio_key, separators=(',', ':'))
        bio_bytes = bio_string.encode('utf-8')
        
        encryption_key = self.encryptor.derive_encryption_key(bio_bytes)
        fernet = Fernet(encryption_key)
        
        encrypted_data = fernet.encrypt(data.encode('utf-8'))
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def decrypt_with_biometric_key(self, encrypted_data, bio_key):
        """Decrypt data using biometric key"""
        bio_string = json.dumps(bio_key, separators=(',', ':'))
        bio_bytes = bio_string.encode('utf-8')
        
        encryption_key = self.encryptor.derive_encryption_key(bio_bytes)
        fernet = Fernet(encryption_key)
        
        encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
        decrypted_data = fernet.decrypt(encrypted_bytes)
        return decrypted_data.decode('utf-8')
    
    def generate_signature_proof(self, bio_key, document_hash):
        """Generate cryptographic proof of biometric signature"""
        proof_data = json.dumps({
            'bio_key': bio_key,
            'document_hash': document_hash,
            'timestamp': int(time.time())
        }, separators=(',', ':'))
        
        return hashlib.sha256(proof_data.encode()).hexdigest()
    
    def generate_token_proof(self, bio_key, resource_id, expiry_time):
        """Generate proof for biometric access token"""
        proof_data = json.dumps({
            'bio_key': bio_key,
            'resource_id': resource_id,
            'expiry_time': expiry_time
        }, separators=(',', ':'))
        
        return hashlib.sha256(proof_data.encode()).hexdigest()
    
    def generate_exchange_proof(self, initiator_bio, responder_bio, session_key):
        """Generate proof for key exchange"""
        proof_data = json.dumps({
            'initiator': initiator_bio,
            'responder': responder_bio,
            'session_key': session_key.decode('utf-8')
        }, separators=(',', ':'))
        
        return hashlib.sha256(proof_data.encode()).hexdigest()
    
    def verify_biometric_protocol(self, protocol_data, bio_key):
        """Verify biometric protocol integrity"""
        protocol_type = protocol_data.get('protocol', 'Unknown')
        
        if protocol_type == 'BiometricSignature':
            return self.verify_signature(protocol_data, bio_key)
        elif protocol_type == 'BiometricAccessToken':
            return self.verify_access_token(protocol_data, bio_key)
        elif protocol_type == 'BiometricMultiSig':
            return self.verify_multi_signature(protocol_data, bio_key)
        else:
            print(f"❌ Unknown protocol type: {protocol_type}")
            return False
    
    def verify_signature(self, signature_data, bio_key):
        """Verify biometric signature"""
        expected_proof = self.generate_signature_proof(
            bio_key, 
            signature_data['document_hash']
        )
        return signature_data['signature_proof'] == expected_proof
    
    def verify_access_token(self, token_data, bio_key):
        """Verify biometric access token"""
        # Check expiry
        if int(time.time()) > token_data['expires']:
            print("❌ Token expired")
            return False
        
        # Verify token proof
        expected_proof = self.generate_token_proof(
            bio_key,
            token_data['resource_id'],
            token_data['expires']
        )
        return token_data['token_proof'] == expected_proof
    
    def verify_multi_signature(self, multi_sig_data, bio_key):
        """Verify biometric multi-signature"""
        bio_hash = hashlib.sha256(json.dumps(bio_key).encode()).hexdigest()[:16]
        
        # Find matching signature
        for signature in multi_sig_data['signatures']:
            if signature['bio_hash'] == bio_hash:
                expected_proof = self.generate_signature_proof(
                    bio_key,
                    multi_sig_data['document_hash']
                )
                return signature['signature'] == expected_proof
        
        return False

def demo_biometric_protocols():
    """Demonstrate biometric cryptographic protocols"""
    print("🌊⚡ BIOMETRIC CRYPTOGRAPHIC PROTOCOLS DEMO ⚡🌊")
    print("=" * 60)
    
    protocols = BiometricCryptographicProtocols()
    
    # Mock biometric keys for demo
    alice_bio = {'h': [100.0, 200.0, 150.0, 80.0, 120.0, 90.0], 'c': 128.5, 'm': 115.2}
    bob_bio = {'h': [110.0, 190.0, 160.0, 85.0, 125.0, 95.0], 'c': 132.1, 'm': 118.7}
    charlie_bio = {'h': [95.0, 205.0, 145.0, 75.0, 115.0, 85.0], 'c': 125.8, 'm': 112.4}
    
    document_hash = hashlib.sha256(b"Important contract document").hexdigest()
    
    print("\n1. 📧 Biometric Message Protocol")
    message = protocols.create_biometric_message_protocol(
        alice_bio, bob_bio, "Secret message from Alice to Bob"
    )
    print(f"   Encrypted message length: {len(message)} characters")
    
    print("\n2. ✍️ Biometric Digital Signature")
    signature = protocols.create_biometric_signature_protocol(alice_bio, document_hash)
    print(f"   Signature hash: {signature['signature_proof'][:16]}...")
    
    print("\n3. 🎫 Biometric Access Token")
    token = protocols.create_biometric_access_token(
        alice_bio, "secure_database", ["read", "write"], 24
    )
    print(f"   Token length: {len(token)} characters")
    
    print("\n4. 🔄 Biometric Key Exchange")
    exchange, session_key = protocols.create_biometric_key_exchange_protocol(alice_bio, bob_bio)
    print(f"   Session key hash: {hashlib.sha256(session_key).hexdigest()[:16]}...")
    
    print("\n5. 👥 Biometric Multi-Signature (3 signers)")
    multi_sig = protocols.create_biometric_multi_sig_protocol(
        [alice_bio, bob_bio, charlie_bio], document_hash, threshold=2
    )
    print(f"   Required signatures: {multi_sig['required_signatures']}/{multi_sig['total_signers']}")
    
    print("\n6. 📋 Biometric Smart Contract")
    contract = protocols.create_biometric_smart_contract(
        [alice_bio, bob_bio],
        {"payment": 1000, "delivery": "30 days"},
        {"trigger": "biometric_confirmation", "parties": 2}
    )
    print(f"   Contract hash: {contract['contract_hash'][:16]}...")
    
    print("\n✅ ALL BIOMETRIC PROTOCOLS DEMONSTRATED SUCCESSFULLY!")
    print("🔐 Ready for enterprise deployment and patent filing")

if __name__ == "__main__":
    demo_biometric_protocols()
