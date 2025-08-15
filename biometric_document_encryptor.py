#!/usr/bin/env python3
"""
Biometric Document Encryptor - Proof of Concept
Encrypts documents using biometric QR keys for secure storage
"""

import cv2
import numpy as np
import qrcode
import json
import time
import os
import hashlib
from PIL import Image
from pyzbar import pyzbar
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class BiometricDocumentEncryptor:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
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
        # Create histogram-based signature
        hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
        hist = hist.flatten()
        
        # Add geometric features
        height, width = face_roi.shape
        center_brightness = np.mean(face_roi[height//3:2*height//3, width//3:2*width//3])
        edge_brightness = np.mean(face_roi[:10, :]) + np.mean(face_roi[-10:, :])
        
        # Create deterministic key material
        key_data = {
            'histogram': hist[:64].tolist(),  # Use 64 histogram bins
            'center_brightness': float(center_brightness),
            'edge_brightness': float(edge_brightness),
            'mean_intensity': float(np.mean(face_roi)),
            'std_intensity': float(np.std(face_roi))
        }
        
        # Convert to bytes for key derivation
        key_string = json.dumps(key_data, sort_keys=True, separators=(',', ':'))
        key_bytes = key_string.encode('utf-8')
        
        return key_data, key_bytes
    
    def derive_encryption_key(self, biometric_bytes, salt=None):
        """Derive Fernet encryption key from biometric data"""
        if salt is None:
            salt = b'biometric_salt_2025'  # Fixed salt for reproducibility
        
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
            # Read document
            with open(file_path, 'rb') as f:
                document_data = f.read()
            
            # Derive encryption key from biometric data
            biometric_data, biometric_bytes = biometric_signature
            encryption_key = self.derive_encryption_key(biometric_bytes)
            
            # Encrypt document
            fernet = Fernet(encryption_key)
            encrypted_data = fernet.encrypt(document_data)
            
            # Create metadata
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
    
    def create_encrypted_qr(self, encrypted_data, metadata, biometric_data, output_file):
        """Create QR code containing encrypted document and biometric key"""
        print("📱 Creating biometric encrypted QR code...")
        
        # Encode encrypted data as base64 for QR storage
        encrypted_b64 = base64.b64encode(encrypted_data).decode('utf-8')
        
        qr_data = {
            'protocol': 'BIOMETRIC-CRYPTO-1.0',
            'timestamp': int(time.time()),
            'biometric_key': biometric_data,
            'encrypted_document': encrypted_b64,
            'metadata': metadata,
            'nonce': f'crypto_{int(time.time() * 1000)}'
        }
        
        json_data = json.dumps(qr_data, separators=(',', ':'))
        
        # Check size limits
        if len(json_data) > 7000:  # QR code practical limit
            print(f"⚠️  Warning: QR data size {len(json_data)} bytes may be too large")
            print("📝 Consider splitting large documents into multiple QR codes")
        
        # Create QR code
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=4,
        )
        
        qr.add_data(json_data)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save(output_file)
        
        print(f"✅ Encrypted QR saved: {output_file}")
        print(f"📊 QR Version: {qr.version}")
        print(f"📊 Data Size: {len(json_data)} bytes")
        
        return output_file
    
    def decrypt_document_from_qr(self, qr_file, output_dir="decrypted"):
        """Decrypt document from QR using live biometric verification"""
        print(f"🔍 Decrypting document from QR: {qr_file}")
        
        # Decode QR
        image = cv2.imread(qr_file)
        if image is None:
            print("❌ Cannot read QR file")
            return False
        
        decoded_objects = pyzbar.decode(image)
        if not decoded_objects:
            print("❌ No QR code found")
            return False
        
        try:
            qr_data = json.loads(decoded_objects[0].data.decode('utf-8'))
            print("✅ QR decoded successfully")
        except:
            print("❌ Invalid QR data")
            return False
        
        # Extract stored biometric key
        stored_biometric = qr_data['biometric_key']
        encrypted_document = qr_data['encrypted_document']
        metadata = qr_data['metadata']
        
        # Capture live biometric for verification
        print("\n📸 Biometric verification required for decryption...")
        live_signature = self.capture_face_signature()
        
        if not live_signature:
            print("❌ Could not capture biometric key")
            return False
        
        live_biometric, live_bytes = live_signature
        
        # Verify biometric match
        if not self.verify_biometric_match(stored_biometric, live_biometric):
            print("🚫 BIOMETRIC VERIFICATION FAILED - DECRYPTION DENIED")
            return False
        
        print("✅ BIOMETRIC VERIFICATION SUCCESSFUL - DECRYPTION AUTHORIZED")
        
        # Decrypt document
        try:
            encryption_key = self.derive_encryption_key(live_bytes)
            fernet = Fernet(encryption_key)
            
            encrypted_data = base64.b64decode(encrypted_document.encode('utf-8'))
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
            # Compare histograms
            hist1 = np.array(stored_bio['histogram'])
            hist2 = np.array(live_bio['histogram'])
            hist_corr = cv2.compareHist(hist1.astype(np.float32), hist2.astype(np.float32), cv2.HISTCMP_CORREL)
            
            # Compare other features
            brightness_diff = abs(stored_bio['center_brightness'] - live_bio['center_brightness'])
            intensity_diff = abs(stored_bio['mean_intensity'] - live_bio['mean_intensity'])
            
            # Calculate similarity score
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
    print("🌊⚡ BIOMETRIC DOCUMENT ENCRYPTOR - CRYPTOGRAPHIC BREAKTHROUGH ⚡🌊")
    print("=" * 70)
    
    encryptor = BiometricDocumentEncryptor()
    
    while True:
        print("\nBiometric Cryptography Options:")
        print("1. Encrypt Document with Biometric QR")
        print("2. Decrypt Document from Biometric QR")
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
                    qr_file = f"encrypted_{os.path.basename(file_path)}_{int(time.time())}.png"
                    encryptor.create_encrypted_qr(encrypted_data, metadata, bio_data, qr_file)
                    print(f"\n🎉 DOCUMENT ENCRYPTED AND QR CREATED!")
                    print(f"📱 QR File: {qr_file}")
                    print("🔐 Document is now secured with your biometric signature")
        
        elif choice == "2":
            qr_file = input("Enter encrypted QR file path: ").strip()
            
            if not os.path.exists(qr_file):
                print("❌ QR file not found")
                continue
            
            success = encryptor.decrypt_document_from_qr(qr_file)
            
            if success:
                print("\n🎉 BIOMETRIC DECRYPTION COMPLETE!")
            else:
                print("\n❌ DECRYPTION FAILED")
        
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
