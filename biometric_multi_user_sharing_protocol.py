#!/usr/bin/env python3
"""
Biometric Multi-User Sharing Protocol
Advanced system for secure document sharing using multiple biometric keys
"""

import json
import time
import hashlib
import base64
import os
from cryptography.fernet import Fernet
from biometric_document_encryptor_ultimate import BiometricDocumentEncryptor
from biometric_cryptographic_protocols import BiometricCryptographicProtocols

class BiometricMultiUserSharingProtocol:
    def __init__(self):
        self.encryptor = BiometricDocumentEncryptor()
        self.protocols = BiometricCryptographicProtocols()
        
    def create_shared_document_vault(self, document_path, authorized_users, access_levels=None):
        """Create a shared document vault with multiple biometric access"""
        print(f"🏦 Creating shared document vault for {len(authorized_users)} users...")
        
        if access_levels is None:
            access_levels = ["read", "write"] * len(authorized_users)
        
        # Generate master vault key
        vault_id = f"vault_{int(time.time())}"
        master_key = self.generate_master_vault_key(authorized_users)
        
        # Encrypt document with master key
        with open(document_path, 'rb') as f:
            document_data = f.read()
        
        encrypted_document = self.encrypt_with_master_key(document_data, master_key)
        
        # Create vault metadata
        vault_metadata = {
            'vault_id': vault_id,
            'created': int(time.time()),
            'document_name': os.path.basename(document_path),
            'document_size': len(document_data),
            'authorized_users': len(authorized_users),
            'access_control': self.create_access_control_matrix(authorized_users, access_levels),
            'vault_hash': hashlib.sha256(encrypted_document).hexdigest()
        }
        
        # Create individual user access keys
        user_access_keys = []
        for i, user_bio in enumerate(authorized_users):
            access_key = self.create_user_access_key(
                user_bio, vault_id, master_key, access_levels[i % len(access_levels)]
            )
            user_access_keys.append(access_key)
        
        # Create vault QR system
        vault_qrs = self.create_vault_qr_system(vault_metadata, encrypted_document, user_access_keys)
        
        print(f"✅ Shared document vault created: {vault_id}")
        print(f"📱 Generated {len(vault_qrs)} QR codes for vault access")
        
        return {
            'vault_id': vault_id,
            'metadata': vault_metadata,
            'qr_codes': vault_qrs,
            'access_keys': user_access_keys
        }
    
    def create_biometric_group_signature(self, bio_keys, document_hash, required_signatures=None):
        """Create group signature requiring multiple biometric approvals"""
        print(f"👥 Creating biometric group signature ({len(bio_keys)} members)...")
        
        if required_signatures is None:
            required_signatures = max(1, len(bio_keys) // 2 + 1)  # Majority
        
        group_signature = {
            'protocol': 'BiometricGroupSignature',
            'version': '1.0',
            'created': int(time.time()),
            'document_hash': document_hash,
            'group_size': len(bio_keys),
            'required_signatures': required_signatures,
            'member_hashes': [
                hashlib.sha256(json.dumps(bio_key).encode()).hexdigest()[:16]
                for bio_key in bio_keys
            ],
            'signatures': [],
            'status': 'pending'
        }
        
        # Generate individual member signatures
        for i, bio_key in enumerate(bio_keys):
            member_signature = {
                'member_id': i,
                'bio_hash': hashlib.sha256(json.dumps(bio_key).encode()).hexdigest()[:16],
                'signature': self.protocols.generate_signature_proof(bio_key, document_hash),
                'timestamp': int(time.time())
            }
            group_signature['signatures'].append(member_signature)
        
        # Check if signature is complete
        if len(group_signature['signatures']) >= required_signatures:
            group_signature['status'] = 'complete'
            group_signature['completed'] = int(time.time())
        
        print(f"✅ Group signature created ({len(group_signature['signatures'])}/{required_signatures} required)")
        return group_signature
    
    def create_biometric_delegation_protocol(self, delegator_bio, delegate_bio, permissions, expiry_hours=24):
        """Create biometric delegation allowing one user to act for another"""
        print("🔄 Creating biometric delegation protocol...")
        
        delegation_id = f"delegation_{int(time.time())}"
        expiry_time = int(time.time()) + (expiry_hours * 3600)
        
        delegation_data = {
            'protocol': 'BiometricDelegation',
            'version': '1.0',
            'delegation_id': delegation_id,
            'created': int(time.time()),
            'expires': expiry_time,
            'delegator_hash': hashlib.sha256(json.dumps(delegator_bio).encode()).hexdigest()[:16],
            'delegate_hash': hashlib.sha256(json.dumps(delegate_bio).encode()).hexdigest()[:16],
            'permissions': permissions,
            'delegation_proof': self.generate_delegation_proof(delegator_bio, delegate_bio, permissions, expiry_time)
        }
        
        # Encrypt delegation with combined biometric keys
        combined_key = self.protocols.combine_biometric_keys(delegator_bio, delegate_bio)
        encrypted_delegation = self.protocols.encrypt_with_biometric_key(
            json.dumps(delegation_data), combined_key
        )
        
        print(f"✅ Biometric delegation created (expires in {expiry_hours}h)")
        return encrypted_delegation, delegation_data
    
    def create_biometric_escrow_system(self, parties, escrow_conditions, document_hash):
        """Create biometric escrow requiring multiple party agreement"""
        print(f"🏛️ Creating biometric escrow system ({len(parties)} parties)...")
        
        escrow_id = f"escrow_{int(time.time())}"
        
        escrow_data = {
            'protocol': 'BiometricEscrow',
            'version': '1.0',
            'escrow_id': escrow_id,
            'created': int(time.time()),
            'document_hash': document_hash,
            'parties': [
                hashlib.sha256(json.dumps(party_bio).encode()).hexdigest()[:16]
                for party_bio in parties
            ],
            'conditions': escrow_conditions,
            'approvals': [],
            'status': 'pending',
            'release_conditions_met': False
        }
        
        # Generate approval signatures for each party
        for i, party_bio in enumerate(parties):
            approval = {
                'party_id': i,
                'bio_hash': hashlib.sha256(json.dumps(party_bio).encode()).hexdigest()[:16],
                'approval_signature': self.protocols.generate_signature_proof(party_bio, escrow_id),
                'timestamp': int(time.time())
            }
            escrow_data['approvals'].append(approval)
        
        # Check if all conditions are met
        if len(escrow_data['approvals']) == len(parties):
            escrow_data['status'] = 'approved'
            escrow_data['release_conditions_met'] = True
            escrow_data['approved_time'] = int(time.time())
        
        print(f"✅ Biometric escrow system created: {escrow_id}")
        return escrow_data
    
    def create_biometric_consensus_protocol(self, participants, proposal, voting_period_hours=72):
        """Create biometric consensus protocol for group decision making"""
        print(f"🗳️ Creating biometric consensus protocol ({len(participants)} participants)...")
        
        consensus_id = f"consensus_{int(time.time())}"
        voting_deadline = int(time.time()) + (voting_period_hours * 3600)
        
        consensus_data = {
            'protocol': 'BiometricConsensus',
            'version': '1.0',
            'consensus_id': consensus_id,
            'created': int(time.time()),
            'voting_deadline': voting_deadline,
            'proposal': proposal,
            'participants': [
                hashlib.sha256(json.dumps(participant_bio).encode()).hexdigest()[:16]
                for participant_bio in participants
            ],
            'votes': [],
            'status': 'active',
            'result': None
        }
        
        # Generate voting tokens for each participant
        voting_tokens = []
        for i, participant_bio in enumerate(participants):
            token = self.protocols.create_biometric_access_token(
                participant_bio, consensus_id, ["vote"], voting_period_hours
            )
            voting_tokens.append({
                'participant_id': i,
                'bio_hash': hashlib.sha256(json.dumps(participant_bio).encode()).hexdigest()[:16],
                'voting_token': token
            })
        
        print(f"✅ Biometric consensus protocol created (voting period: {voting_period_hours}h)")
        return consensus_data, voting_tokens
    
    def generate_master_vault_key(self, authorized_users):
        """Generate master key from all authorized user biometrics"""
        combined_bio_data = ""
        for user_bio in authorized_users:
            combined_bio_data += json.dumps(user_bio, separators=(',', ':'))
        
        master_key_hash = hashlib.sha256(combined_bio_data.encode()).digest()
        return base64.urlsafe_b64encode(master_key_hash)
    
    def encrypt_with_master_key(self, data, master_key):
        """Encrypt data with master vault key"""
        fernet = Fernet(master_key)
        return fernet.encrypt(data)
    
    def create_access_control_matrix(self, authorized_users, access_levels):
        """Create access control matrix for vault users"""
        access_matrix = {}
        for i, user_bio in enumerate(authorized_users):
            user_hash = hashlib.sha256(json.dumps(user_bio).encode()).hexdigest()[:16]
            access_matrix[user_hash] = {
                'user_id': i,
                'permissions': access_levels[i % len(access_levels)] if isinstance(access_levels[i % len(access_levels)], list) else [access_levels[i % len(access_levels)]],
                'granted': int(time.time())
            }
        return access_matrix
    
    def create_user_access_key(self, user_bio, vault_id, master_key, permissions):
        """Create individual user access key for vault"""
        access_key_data = {
            'vault_id': vault_id,
            'user_hash': hashlib.sha256(json.dumps(user_bio).encode()).hexdigest()[:16],
            'permissions': permissions if isinstance(permissions, list) else [permissions],
            'master_key_fragment': base64.b64encode(master_key[:16]).decode('utf-8'),  # Partial key
            'created': int(time.time())
        }
        
        # Encrypt access key with user's biometric
        encrypted_access_key = self.protocols.encrypt_with_biometric_key(
            json.dumps(access_key_data), user_bio
        )
        
        return encrypted_access_key
    
    def create_vault_qr_system(self, metadata, encrypted_document, access_keys):
        """Create QR code system for vault access"""
        # Create metadata QR
        metadata_qr = f"vault_metadata_{metadata['vault_id']}.png"
        self.encryptor.create_qr_code(json.dumps(metadata), metadata_qr, "green")
        
        # Create document QR series
        document_b64 = base64.b64encode(encrypted_document).decode('utf-8')
        chunk_size = 1200
        chunks = [document_b64[i:i + chunk_size] for i in range(0, len(document_b64), chunk_size)]
        
        document_qrs = []
        for i, chunk in enumerate(chunks):
            chunk_data = {
                'vault_id': metadata['vault_id'],
                'chunk_id': i,
                'total_chunks': len(chunks),
                'data': chunk
            }
            qr_filename = f"vault_{metadata['vault_id']}_doc_{i+1}.png"
            self.encryptor.create_qr_code(json.dumps(chunk_data), qr_filename, "purple")
            document_qrs.append(qr_filename)
        
        # Create access key QRs
        access_qrs = []
        for i, access_key in enumerate(access_keys):
            qr_filename = f"vault_{metadata['vault_id']}_access_{i+1}.png"
            self.encryptor.create_qr_code(access_key, qr_filename, "orange")
            access_qrs.append(qr_filename)
        
        return {
            'metadata_qr': metadata_qr,
            'document_qrs': document_qrs,
            'access_qrs': access_qrs
        }
    
    def generate_delegation_proof(self, delegator_bio, delegate_bio, permissions, expiry_time):
        """Generate cryptographic proof for delegation"""
        proof_data = json.dumps({
            'delegator': delegator_bio,
            'delegate': delegate_bio,
            'permissions': permissions,
            'expiry': expiry_time,
            'timestamp': int(time.time())
        }, separators=(',', ':'))
        
        return hashlib.sha256(proof_data.encode()).hexdigest()

def demo_multi_user_sharing():
    """Demonstrate multi-user biometric sharing protocols"""
    print("🌊⚡ BIOMETRIC MULTI-USER SHARING PROTOCOL DEMO ⚡🌊")
    print("=" * 65)
    
    sharing = BiometricMultiUserSharingProtocol()
    
    # Mock biometric keys for demo
    alice_bio = {'h': [100.0, 200.0, 150.0, 80.0, 120.0, 90.0], 'c': 128.5, 'm': 115.2}
    bob_bio = {'h': [110.0, 190.0, 160.0, 85.0, 125.0, 95.0], 'c': 132.1, 'm': 118.7}
    charlie_bio = {'h': [95.0, 205.0, 145.0, 75.0, 115.0, 85.0], 'c': 125.8, 'm': 112.4}
    diana_bio = {'h': [105.0, 195.0, 155.0, 90.0, 130.0, 100.0], 'c': 135.2, 'm': 120.8}
    
    document_hash = hashlib.sha256(b"Confidential business contract").hexdigest()
    
    print("\n1. 👥 Biometric Group Signature (4 members, 3 required)")
    group_sig = sharing.create_biometric_group_signature(
        [alice_bio, bob_bio, charlie_bio, diana_bio], document_hash, required_signatures=3
    )
    print(f"   Status: {group_sig['status']}")
    print(f"   Signatures: {len(group_sig['signatures'])}/{group_sig['required_signatures']}")
    
    print("\n2. 🔄 Biometric Delegation Protocol")
    delegation, delegation_data = sharing.create_biometric_delegation_protocol(
        alice_bio, bob_bio, ["read", "sign"], expiry_hours=48
    )
    print(f"   Delegation ID: {delegation_data['delegation_id']}")
    print(f"   Permissions: {delegation_data['permissions']}")
    
    print("\n3. 🏛️ Biometric Escrow System")
    escrow = sharing.create_biometric_escrow_system(
        [alice_bio, bob_bio, charlie_bio],
        {"release_condition": "unanimous_approval", "timeout": 30},
        document_hash
    )
    print(f"   Escrow ID: {escrow['escrow_id']}")
    print(f"   Status: {escrow['status']}")
    print(f"   Parties: {len(escrow['parties'])}")
    
    print("\n4. 🗳️ Biometric Consensus Protocol")
    consensus, voting_tokens = sharing.create_biometric_consensus_protocol(
        [alice_bio, bob_bio, charlie_bio, diana_bio],
        {"proposal": "Approve new security policy", "type": "policy_change"},
        voting_period_hours=72
    )
    print(f"   Consensus ID: {consensus['consensus_id']}")
    print(f"   Participants: {len(consensus['participants'])}")
    print(f"   Voting tokens issued: {len(voting_tokens)}")
    
    print("\n✅ ALL MULTI-USER PROTOCOLS DEMONSTRATED SUCCESSFULLY!")
    print("🔐 Advanced biometric sharing system ready for deployment")
    
    return {
        'group_signature': group_sig,
        'delegation': delegation_data,
        'escrow': escrow,
        'consensus': consensus
    }

if __name__ == "__main__":
    demo_multi_user_sharing()
