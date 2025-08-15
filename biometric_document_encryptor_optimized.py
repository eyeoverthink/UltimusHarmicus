#!/usr/bin/env python3
"""
Biometric Document Encryptor - Optimized for QR Size Limits
Separates biometric key from document data to handle size constraints
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
        self.max_qr_size = 2900  # Conservative QR data limit
        
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
        """Create compact cryptographic key from face data"""
        hist = cv2.calcHist([face_roi], [0], None, [32], [0, 256])  # Reduced bins
        hist = hist.flatten()
        
        height, width = face_roi.shape
        center_brightness = np.mean(face_roi[height//3:2*height//3, width//3:2*width//3])
        
        # Compact key data - only essential features
        key_data = {
            'h': hist[:16].tolist(),  # Only 16 histogram bins
            'cb': round(float(center_brightness), 1),
            'mi': round(float(np.mean(face_roi)), 1),
            'si': round(float(np.std(face_roi)), 1)
        }
        
        key_string = json.dumps(key_data, separators=(',', ':'))
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
                'fn': os.path.basename(file_path),  # Shortened field names
                'fs': len(document_data),
                'et': int(time.time()),
                'bh': hashlib.sha256(biometric_bytes).hexdigest()[:8]  # Shorter hash
            }
            
            print(f"✅ Document encrypted ({len(encrypted_data)} bytes)")
            return encrypted_data, metadata, biometric_data
            
        except Exception as e:
            print(f"❌ Encryption failed: {e}")
            return None, None, None
    
    def create_biometric_key_qr(self, biometric_data, metadata, base_filename):
        """Create separate QR code for biometric key"""
        key_qr_data = {
            'p': 'BIO-KEY-1.0',  # Shortened protocol
            't': int(time.time()),
            'bk': biometric_data,
            'md': metadata,
            'n': f'k_{int(time.time() * 1000)}'
        }
        
        json_data = json.dumps(key_qr_data, separators=(',', ':'))
        
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=4,
        )
        
        qr.add_data(json_data)
        qr.make(fit=True)
        
        key_filename = f"{base_filename}_KEY.png"
        qr_img = qr.make_image(fill_color="red", back_color="white")  # Red for key
        qr_img.save(key_filename)
        
        print(f"🔑 Biometric key QR saved: {key_filename} (Version {qr.version})")
        return key_filename
    
    def create_data_qr_series(self, encrypted_data, base_filename):
        """Create series of QR codes for encrypted data only"""
        print("📱 Creating encrypted data QR series...")
        
        encrypted_b64 = base64.b64encode(encrypted_data).decode('utf-8')
        
        # Calculate chunks for data-only QRs
        chunk_size = self.max_qr_size - 200  # Buffer for metadata
        chunks = [encrypted_b64[i:i + chunk_size] for i in range(0, len(encrypted_b64), chunk_size)]
        total_chunks = len(chunks)
        
        print(f"📊 Data split into {total_chunks} QR codes")
        
        qr_files = []
        
        for i, chunk in enumerate(chunks):
            chunk_qr_data = {
                'p': 'BIO-DATA-1.0',
                'ci': i,
                'tc': total_chunks,
                'ec': chunk,
                'ch': hashlib.sha256(chunk.encode()).hexdigest()[:8]
            }
            
            json_data = json.dumps(chunk_qr_data, separators=(',', ':'))
            
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=8,
                border=4,
            )
            
            try:
                qr.add_data(json_data)
                qr.make(fit=True)
                
                if total_chunks == 1:
                    filename = f"{base_filename}_DATA.png"
                else:
                    filename = f"{base_filename}_DATA_{i+1}_of_{total_chunks}.png"
                
                qr_img = qr.make_image(fill_color="blue", back_color="white")  # Blue for data
                qr_img.save(filename)
                
                qr_files.append(filename)
                print(f"✅ Data QR {i+1}/{total_chunks} saved: {filename} (Version {qr.version})")
                
            except Exception as e:
                print(f"❌ Failed to create data QR {i+1}: {e}")
                return []
        
        return qr_files
    
    def encrypt_and_create_qr_system(self, file_path):
        """Complete encryption and QR creation workflow"""
        print("\n🔑 Generating biometric encryption key...")
        biometric_sig = self.capture_face_signature()
        
        if not biometric_sig:
            return False
        
        encrypted_data, metadata, bio_data = self.encrypt_document(file_path, biometric_sig)
        
        if not encrypted_data:
            return False
        
        base_name = f"encrypted_{os.path.splitext(os.path.basename(file_path))[0]}_{int(time.time())}"
        
        # Create biometric key QR
        key_qr = self.create_biometric_key_qr(bio_data, metadata, base_name)
        
        # Create data QR series
        data_qrs = self.create_data_qr_series(encrypted_data, base_name)
        
        if key_qr and data_qrs:
            print(f"\n🎉 BIOMETRIC ENCRYPTION SYSTEM CREATED!")
            print(f"🔑 Key QR: {key_qr}")
            print(f"📱 Data QRs: {len(data_qrs)} codes")
            for qr_file in data_qrs:
                print(f"   - {qr_file}")
            print("\n🔐 DECRYPTION REQUIRES:")
            print("   1. Your biometric key QR (red)")
            print("   2. All data QRs (blue)")
            print("   3. Live face verification")
            return True
        
        return False
    
    def decrypt_from_qr_system(self, key_qr_file, data_qr_files, output_dir="decrypted"):
        """Decrypt document from separate key and data QRs"""
        print(f"🔍 Decrypting from biometric QR system...")
        
        # Decode key QR
        print(f"🔑 Reading biometric key QR: {key_qr_file}")
        key_image = cv2.imread(key_qr_file)
        if key_image is None:
            print("❌ Cannot read key QR file")
            return False
        
        key_decoded = pyzbar.decode(key_image)
        if not key_decoded:
            print("❌ No QR code found in key file")
            return False
        
        try:
            key_data = json.loads(key_decoded[0].data.decode('utf-8'))
            biometric_key = key_data['bk']
            metadata = key_data['md']
            print("✅ Biometric key QR decoded")
        except:
            print("❌ Invalid key QR data")
            return False
        
        # Decode data QRs
        chunks_data = {}
        total_chunks = None
        
        for data_qr_file in data_qr_files:
            print(f"📖 Reading data QR: {data_qr_file}")
            
            image = cv2.imread(data_qr_file)
            if image is None:
                continue
            
            decoded_objects = pyzbar.decode(image)
            if not decoded_objects:
                continue
            
            try:
                qr_data = json.loads(decoded_objects[0].data.decode('utf-8'))
                chunk_index = qr_data.get('ci', 0)
                total_chunks = qr_data.get('tc', 1)
                encrypted_chunk = qr_data.get('ec', '')
                
                chunks_data[chunk_index] = encrypted_chunk
                print(f"✅ Data chunk {chunk_index + 1} decoded")
                
            except Exception as e:
                print(f"❌ Failed to decode data QR: {e}")
        
        # Verify all chunks present
        if len(chunks_data) != total_chunks:
            print(f"❌ Missing data chunks: have {len(chunks_data)}, need {total_chunks}")
            return False
        
        # Reconstruct encrypted data
        encrypted_b64 = ""
        for i in range(total_chunks):
            encrypted_b64 += chunks_data[i]
        
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
            
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, metadata['fn'])
            
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
            hist1 = np.array(stored_bio['h'])
            hist2 = np.array(live_bio['h'])
            hist_corr = cv2.compareHist(hist1.astype(np.float32), hist2.astype(np.float32), cv2.HISTCMP_CORREL)
            
            brightness_diff = abs(stored_bio['cb'] - live_bio['cb'])
            intensity_diff = abs(stored_bio['mi'] - live_bio['mi'])
            
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
    print("🌊⚡ BIOMETRIC DOCUMENT ENCRYPTOR - OPTIMIZED QR SYSTEM ⚡🌊")
    print("=" * 70)
    
    encryptor = BiometricDocumentEncryptor()
    
    while True:
        print("\nBiometric Cryptography Options:")
        print("1. Encrypt Document (Creates Key QR + Data QRs)")
        print("2. Decrypt Document (From Key QR + Data QRs)")
        print("3. Test Biometric Key Generation")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            file_path = input("Enter document path to encrypt: ").strip()
            
            if not os.path.exists(file_path):
                print("❌ File not found")
                continue
            
            success = encryptor.encrypt_and_create_qr_system(file_path)
            
            if not success:
                print("❌ Encryption failed")
        
        elif choice == "2":
            key_qr = input("Enter KEY QR file path (red): ").strip()
            
            if not os.path.exists(key_qr):
                print("❌ Key QR file not found")
                continue
            
            print("Enter DATA QR file paths (one per line, empty line to finish):")
            data_qrs = []
            while True:
                data_qr = input("Data QR file: ").strip()
                if not data_qr:
                    break
                if os.path.exists(data_qr):
                    data_qrs.append(data_qr)
                else:
                    print(f"❌ File not found: {data_qr}")
            
            if data_qrs:
                success = encryptor.decrypt_from_qr_system(key_qr, data_qrs)
                
                if not success:
                    print("\n❌ DECRYPTION FAILED")
            else:
                print("❌ No valid data QR files provided")
        
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
