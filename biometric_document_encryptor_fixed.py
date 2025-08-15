#!/usr/bin/env python3
"""
Biometric Document Encryptor - Fixed for Large Documents
Handles QR size limits with multi-QR splitting for large files
"""

import cv2
import numpy as np
import qrcode
import json
import time
import os
import hashlib
import math
from PIL import Image
from pyzbar import pyzbar
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class BiometricDocumentEncryptor:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.max_qr_size = 6000  # Safe QR data limit in bytes
        
    def capture_face_signature(self):
        """Capture face and create biometric signature"""
        print("🎥 Starting camera for biometric key generation...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Cannot access camera")
            return None
        
        face_signature = None
        
        print("📸 Position your face in the camera frame and press SPACE to capture biometric key")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Press SPACE for biometric key", (x, y-10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            cv2.imshow('Biometric Key Capture - Press SPACE, ESC to exit', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # Space
                if len(faces) > 0:
                    x, y, w, h = faces[0]
                    face_roi = gray[y:y+h, x:x+w]
                    face_roi = cv2.resize(face_roi, (100, 100))
                    face_signature = self.create_biometric_key(face_roi)
                    print("✅ Biometric key generated!")
                    break
                else:
                    print("❌ No face detected")
            elif key == 27:  # ESC
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return face_signature
    
    def create_biometric_key(self, face_roi):
        """Create cryptographic key from face data"""
        hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
        hist = hist.flatten()
        
        height, width = face_roi.shape
        center_brightness = np.mean(face_roi[height//3:2*height//3, width//3:2*width//3])
        edge_brightness = np.mean(face_roi[:10, :]) + np.mean(face_roi[-10:, :])
        
        key_data = {
            'histogram': hist[:64].tolist(),
            'center_brightness': float(center_brightness),
            'edge_brightness': float(edge_brightness),
            'mean_intensity': float(np.mean(face_roi)),
            'std_intensity': float(np.std(face_roi))
        }
        
        key_string = json.dumps(key_data, sort_keys=True, separators=(',', ':'))
        key_bytes = key_string.encode('utf-8')
        
        return key_data, key_bytes
    
    def derive_encryption_key(self, biometric_bytes, salt=None):
        """Derive Fernet encryption key from biometric data"""
        if salt is None:
            salt = b'biometric_salt_2025'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(biometric_bytes))
        return key
    
    def encrypt_document(self, file_path, biometric_signature):
        """Encrypt document using biometric key"""
        print(f"🔐 Encrypting document: {file_path}")
        
        try:
            with open(file_path, 'rb') as f:
                document_data = f.read()
            
            biometric_data, biometric_bytes = biometric_signature
            encryption_key = self.derive_encryption_key(biometric_bytes)
            
            fernet = Fernet(encryption_key)
            encrypted_data = fernet.encrypt(document_data)
            
            metadata = {
                'original_filename': os.path.basename(file_path),
                'file_size': len(document_data),
                'encryption_timestamp': int(time.time()),
                'biometric_hash': hashlib.sha256(biometric_bytes).hexdigest()[:16]
            }
            
            print(f"✅ Document encrypted ({len(encrypted_data)} bytes)")
            return encrypted_data, metadata, biometric_data
            
        except Exception as e:
            print(f"❌ Encryption failed: {e}")
            return None, None, None
    
    def split_data_for_qr(self, data, max_size):
        """Split large data into chunks for multiple QR codes"""
        chunks = []
        for i in range(0, len(data), max_size):
            chunks.append(data[i:i + max_size])
        return chunks
    
    def create_encrypted_qr_series(self, encrypted_data, metadata, biometric_data, base_filename):
        """Create series of QR codes for large documents"""
        print("📱 Creating biometric encrypted QR series...")
        
        # Encode encrypted data as base64
        encrypted_b64 = base64.b64encode(encrypted_data).decode('utf-8')
        
        # Create base QR data structure
        base_qr_data = {
            'protocol': 'BIOMETRIC-CRYPTO-1.0',
            'timestamp': int(time.time()),
            'biometric_key': biometric_data,
            'metadata': metadata,
            'nonce': f'crypto_{int(time.time() * 1000)}'
        }
        
        # Calculate overhead size
        base_json = json.dumps(base_qr_data, separators=(',', ':'))
        overhead_size = len(base_json) + 100  # Extra buffer for chunk metadata
        
        # Calculate available space for encrypted data per QR
        available_space = self.max_qr_size - overhead_size
        
        if available_space <= 0:
            print("❌ Biometric key too large for QR code")
            return []
        
        # Split encrypted data into chunks
        chunks = self.split_data_for_qr(encrypted_b64, available_space)
        total_chunks = len(chunks)
        
        print(f"📊 Document split into {total_chunks} QR codes")
        
        qr_files = []
        
        for i, chunk in enumerate(chunks):
            # Create chunk-specific QR data
            chunk_qr_data = base_qr_data.copy()
            chunk_qr_data.update({
                'chunk_index': i,
                'total_chunks': total_chunks,
                'encrypted_chunk': chunk,
                'chunk_hash': hashlib.sha256(chunk.encode()).hexdigest()[:16]
            })
            
            json_data = json.dumps(chunk_qr_data, separators=(',', ':'))
            
            # Create QR code
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=6,
                border=4,
            )
            
            try:
                qr.add_data(json_data)
                qr.make(fit=True)
                
                # Generate filename
                if total_chunks == 1:
                    filename = f"{base_filename}.png"
                else:
                    filename = f"{base_filename}_part_{i+1}_of_{total_chunks}.png"
                
                qr_img = qr.make_image(fill_color="black", back_color="white")
                qr_img.save(filename)
                
                qr_files.append(filename)
                print(f"✅ QR {i+1}/{total_chunks} saved: {filename} (Version {qr.version})")
                
            except Exception as e:
                print(f"❌ Failed to create QR {i+1}: {e}")
                return []
        
        return qr_files
    
    def decrypt_document_from_qr_series(self, qr_files, output_dir="decrypted"):
        """Decrypt document from series of QR codes"""
        print(f"🔍 Decrypting document from {len(qr_files)} QR codes...")
        
        # Decode all QR codes
        chunks_data = {}
        metadata = None
        biometric_key = None
        total_chunks = None
        
        for qr_file in qr_files:
            print(f"📖 Reading QR: {qr_file}")
            
            image = cv2.imread(qr_file)
            if image is None:
                print(f"❌ Cannot read QR file: {qr_file}")
                return False
            
            decoded_objects = pyzbar.decode(image)
            if not decoded_objects:
                print(f"❌ No QR code found in: {qr_file}")
                return False
            
            try:
                qr_data = json.loads(decoded_objects[0].data.decode('utf-8'))
                
                # Extract chunk info
                chunk_index = qr_data.get('chunk_index', 0)
                total_chunks = qr_data.get('total_chunks', 1)
                encrypted_chunk = qr_data.get('encrypted_chunk', '')
                
                # Store chunk data
                chunks_data[chunk_index] = encrypted_chunk
                
                # Store metadata and biometric key from first chunk
                if metadata is None:
                    metadata = qr_data['metadata']
                    biometric_key = qr_data['biometric_key']
                
                print(f"✅ Chunk {chunk_index + 1}/{total_chunks} decoded")
                
            except Exception as e:
                print(f"❌ Failed to decode QR {qr_file}: {e}")
                return False
        
        # Verify all chunks are present
        if len(chunks_data) != total_chunks:
            print(f"❌ Missing chunks: have {len(chunks_data)}, need {total_chunks}")
            return False
        
        # Reconstruct encrypted data
        encrypted_b64 = ""
        for i in range(total_chunks):
            if i not in chunks_data:
                print(f"❌ Missing chunk {i}")
                return False
            encrypted_b64 += chunks_data[i]
        
        print("✅ All chunks assembled")
        
        # Biometric verification
        print("\n📸 Biometric verification required for decryption...")
        live_signature = self.capture_face_signature()
        
        if not live_signature:
            print("❌ Could not capture biometric key")
            return False
        
        live_biometric, live_bytes = live_signature
        
        if not self.verify_biometric_match(biometric_key, live_biometric):
            print("🚫 BIOMETRIC VERIFICATION FAILED - DECRYPTION DENIED")
            return False
        
        print("✅ BIOMETRIC VERIFICATION SUCCESSFUL - DECRYPTION AUTHORIZED")
        
        # Decrypt document
        try:
            encryption_key = self.derive_encryption_key(live_bytes)
            fernet = Fernet(encryption_key)
            
            encrypted_data = base64.b64decode(encrypted_b64.encode('utf-8'))
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Save decrypted document
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, metadata['original_filename'])
            
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            
            print(f"🎉 DOCUMENT DECRYPTED SUCCESSFULLY!")
            print(f"📄 File: {output_file}")
            print(f"📊 Size: {len(decrypted_data)} bytes")
            
            return True
            
        except Exception as e:
            print(f"❌ Decryption failed: {e}")
            return False
    
    def verify_biometric_match(self, stored_bio, live_bio, threshold=0.6):
        """Verify biometric signatures match"""
        try:
            hist1 = np.array(stored_bio['histogram'])
            hist2 = np.array(live_bio['histogram'])
            hist_corr = cv2.compareHist(hist1.astype(np.float32), hist2.astype(np.float32), cv2.HISTCMP_CORREL)
            
            brightness_diff = abs(stored_bio['center_brightness'] - live_bio['center_brightness'])
            intensity_diff = abs(stored_bio['mean_intensity'] - live_bio['mean_intensity'])
            
            similarity = (
                hist_corr * 0.7 +
                (1 - brightness_diff / 255) * 0.2 +
                (1 - intensity_diff / 255) * 0.1
            )
            
            print(f"🔍 Biometric Match Score: {similarity:.2%}")
            return similarity > threshold
            
        except Exception as e:
            print(f"❌ Biometric verification error: {e}")
            return False

def main():
    print("🌊⚡ BIOMETRIC DOCUMENT ENCRYPTOR - FIXED FOR LARGE FILES ⚡🌊")
    print("=" * 70)
    
    encryptor = BiometricDocumentEncryptor()
    
    while True:
        print("\nBiometric Cryptography Options:")
        print("1. Encrypt Document with Biometric QR Series")
        print("2. Decrypt Document from Biometric QR Series")
        print("3. Test Biometric Key Generation")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            file_path = input("Enter document path to encrypt: ").strip()
            
            if not os.path.exists(file_path):
                print("❌ File not found")
                continue
            
            print("\n🔑 Generating biometric encryption key...")
            biometric_sig = encryptor.capture_face_signature()
            
            if biometric_sig:
                encrypted_data, metadata, bio_data = encryptor.encrypt_document(file_path, biometric_sig)
                
                if encrypted_data:
                    base_name = f"encrypted_{os.path.splitext(os.path.basename(file_path))[0]}_{int(time.time())}"
                    qr_files = encryptor.create_encrypted_qr_series(encrypted_data, metadata, bio_data, base_name)
                    
                    if qr_files:
                        print(f"\n🎉 DOCUMENT ENCRYPTED AND QR SERIES CREATED!")
                        print(f"📱 QR Files: {len(qr_files)} codes generated")
                        for qr_file in qr_files:
                            print(f"   - {qr_file}")
                        print("🔐 Document is now secured with your biometric signature")
        
        elif choice == "2":
            print("Enter QR file paths (one per line, empty line to finish):")
            qr_files = []
            while True:
                qr_path = input("QR file: ").strip()
                if not qr_path:
                    break
                if os.path.exists(qr_path):
                    qr_files.append(qr_path)
                else:
                    print(f"❌ File not found: {qr_path}")
            
            if qr_files:
                success = encryptor.decrypt_document_from_qr_series(qr_files)
                
                if success:
                    print("\n🎉 BIOMETRIC DECRYPTION COMPLETE!")
                else:
                    print("\n❌ DECRYPTION FAILED")
            else:
                print("❌ No valid QR files provided")
        
        elif choice == "3":
            print("\n🧪 Testing biometric key generation...")
            sig = encryptor.capture_face_signature()
            if sig:
                bio_data, bio_bytes = sig
                print(f"✅ Biometric key generated: {len(bio_bytes)} bytes")
                print(f"🔑 Key hash: {hashlib.sha256(bio_bytes).hexdigest()[:16]}")
        
        elif choice == "4":
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
