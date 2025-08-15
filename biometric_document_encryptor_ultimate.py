#!/usr/bin/env python3
"""
Biometric Document Encryptor - Ultimate Version
Fixed all QR generation and scanning issues with alternative QR library
"""

import cv2
import numpy as np
import json
import time
import os
import hashlib
import base64
from PIL import Image, ImageDraw, ImageFont
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Use segno for QR generation (more reliable)
try:
    import segno
    QR_LIB = 'segno'
except ImportError:
    import qrcode
    QR_LIB = 'qrcode'

# Use pyzbar for QR reading
from pyzbar import pyzbar

class BiometricDocumentEncryptor:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.max_chunk_size = 1200  # Conservative chunk size
        
    def capture_face_signature(self):
        """Capture face with improved detection"""
        print("🎥 Starting camera for biometric key generation...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Cannot access camera")
            return None
        
        face_signature = None
        
        print("📸 Position your face in the camera frame and press SPACE to capture biometric key")
        print("💡 Tip: Move closer to camera, ensure good lighting")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Face detection
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.3,
                minNeighbors=6,
                minSize=(80, 80),
                maxSize=(300, 300),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            # Filter valid faces
            valid_faces = []
            frame_height, frame_width = frame.shape[:2]
            center_x, center_y = frame_width // 2, frame_height // 2
            
            for (x, y, w, h) in faces:
                face_area = w * h
                face_center_x = x + w // 2
                face_center_y = y + h // 2
                distance_from_center = np.sqrt((face_center_x - center_x)**2 + (face_center_y - center_y)**2)
                
                if (face_area > 6400 and 
                    x > 50 and y > 50 and 
                    x + w < frame_width - 50 and 
                    y + h < frame_height - 50 and
                    distance_from_center < min(frame_width, frame_height) * 0.4):
                    valid_faces.append((x, y, w, h))
            
            # Draw rectangles
            for (x, y, w, h) in valid_faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Press SPACE for key", (x, y-10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            cv2.putText(frame, f"Valid faces: {len(valid_faces)}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Biometric Key Capture - Press SPACE, ESC to exit', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # Space
                if len(valid_faces) > 0:
                    largest_face = max(valid_faces, key=lambda f: f[2] * f[3])
                    x, y, w, h = largest_face
                    face_roi = gray[y:y+h, x:x+w]
                    face_roi = cv2.resize(face_roi, (100, 100))
                    face_signature = self.create_biometric_key(face_roi)
                    print("✅ Biometric key generated!")
                    break
                else:
                    print("❌ No valid face detected. Move closer and ensure good lighting.")
            elif key == 27:  # ESC
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return face_signature
    
    def create_biometric_key(self, face_roi):
        """Create compact biometric key"""
        hist = cv2.calcHist([face_roi], [0], None, [6], [0, 256])
        hist = hist.flatten()
        
        height, width = face_roi.shape
        center_brightness = np.mean(face_roi[height//3:2*height//3, width//3:2*width//3])
        
        key_data = {
            'h': [round(float(x), 1) for x in hist],
            'c': round(float(center_brightness), 1),
            'm': round(float(np.mean(face_roi)), 1)
        }
        
        key_string = json.dumps(key_data, separators=(',', ':'))
        key_bytes = key_string.encode('utf-8')
        
        return key_data, key_bytes
    
    def derive_encryption_key(self, biometric_bytes, salt=None):
        """Derive encryption key from biometric data"""
        if salt is None:
            salt = b'bio2025'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=50000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(biometric_bytes))
        return key
    
    def create_qr_code(self, data, filename, color="black"):
        """Create QR code using available library"""
        if QR_LIB == 'segno':
            qr = segno.make(data, error='m')
            qr.save(filename, scale=8, border=4)
        else:
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=8,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            if color == "red":
                qr_img = qr.make_image(fill_color="red", back_color="white")
            elif color == "blue":
                qr_img = qr.make_image(fill_color="blue", back_color="white")
            else:
                qr_img = qr.make_image(fill_color="black", back_color="white")
            
            qr_img.save(filename)
        
        return filename
    
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
                'f': os.path.basename(file_path)[:15],
                's': len(document_data),
                't': int(time.time())
            }
            
            print(f"✅ Document encrypted ({len(encrypted_data)} bytes)")
            return encrypted_data, metadata, biometric_data
            
        except Exception as e:
            print(f"❌ Encryption failed: {e}")
            return None, None, None
    
    def create_biometric_key_qr(self, biometric_data, metadata, base_filename):
        """Create QR code for biometric key"""
        key_qr_data = {
            'p': 'BK',
            't': int(time.time()),
            'k': biometric_data,
            'm': metadata
        }
        
        json_data = json.dumps(key_qr_data, separators=(',', ':'))
        key_filename = f"{base_filename}_KEY.png"
        
        self.create_qr_code(json_data, key_filename, "red")
        
        print(f"🔑 Biometric key QR saved: {key_filename} ({len(json_data)} bytes)")
        return key_filename
    
    def create_data_qr_series(self, encrypted_data, base_filename):
        """Create series of QR codes for encrypted data"""
        print("📱 Creating encrypted data QR series...")
        
        encrypted_b64 = base64.b64encode(encrypted_data).decode('utf-8')
        
        # Split into chunks
        chunks = [encrypted_b64[i:i + self.max_chunk_size] for i in range(0, len(encrypted_b64), self.max_chunk_size)]
        total_chunks = len(chunks)
        
        print(f"📊 Data split into {total_chunks} QR codes")
        
        qr_files = []
        
        for i, chunk in enumerate(chunks):
            chunk_qr_data = {
                'p': 'BD',
                'i': i,
                'n': total_chunks,
                'd': chunk
            }
            
            json_data = json.dumps(chunk_qr_data, separators=(',', ':'))
            
            if total_chunks == 1:
                filename = f"{base_filename}_DATA.png"
            else:
                filename = f"{base_filename}_D{i+1}.png"
            
            try:
                self.create_qr_code(json_data, filename, "blue")
                qr_files.append(filename)
                print(f"✅ Data QR {i+1}/{total_chunks}: {filename} ({len(json_data)}b)")
                
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
        
        base_name = f"enc_{int(time.time())}"
        
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
    
    def read_qr_code(self, filename):
        """Read QR code from file with multiple methods"""
        image = cv2.imread(filename)
        if image is None:
            return None
        
        # Try multiple image processing methods
        methods = [
            image,  # Original
            cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),  # Grayscale
        ]
        
        for method_img in methods:
            decoded = pyzbar.decode(method_img)
            if decoded:
                return decoded[0].data.decode('utf-8')
        
        return None
    
    def chunk_data_for_qr(self, data):
        """Chunk data for QR code distribution"""
        chunk_size = 1200  # Conservative size for QR compatibility
        chunks = []
        for i in range(0, len(data), chunk_size):
            chunks.append(data[i:i + chunk_size])
        return chunks
    
    def decrypt_from_qr_data(self, bio_key_data, encrypted_chunks, biometric_key):
        """Decrypt document from QR data structures"""
        try:
            # Sort chunks by chunk_id
            sorted_chunks = sorted(encrypted_chunks, key=lambda x: x.get('chunk_id', 0))
            
            # Reconstruct encrypted data
            encrypted_b64 = ''.join([chunk['data'] for chunk in sorted_chunks])
            encrypted_data = base64.b64decode(encrypted_b64.encode('utf-8'))
            
            # Derive decryption key from biometric
            bio_string = json.dumps(biometric_key, separators=(',', ':'))
            bio_bytes = bio_string.encode('utf-8')
            encryption_key = self.derive_encryption_key(bio_bytes)
            
            # Decrypt data
            fernet = Fernet(encryption_key)
            decrypted_data = fernet.decrypt(encrypted_data)
            
            return decrypted_data.decode('utf-8')
            
        except Exception as e:
            print(f"❌ Decryption failed: {e}")
            return None
    
    def decrypt_from_qr_system(self, key_qr_file, data_qr_files, output_dir="decrypted"):
        """Decrypt document from QR system"""
        print(f"🔍 Decrypting from biometric QR system...")
        
        # Read key QR
        print(f"🔑 Reading biometric key QR: {key_qr_file}")
        key_data_str = self.read_qr_code(key_qr_file)
        
        if not key_data_str:
            print("❌ Cannot read key QR code")
            return False
        
        try:
            key_data = json.loads(key_data_str)
            biometric_key = key_data['k']
            metadata = key_data['m']
            print("✅ Biometric key QR decoded")
        except Exception as e:
            print(f"❌ Invalid key QR data: {e}")
            return False
        
        # Read data QRs
        chunks_data = {}
        total_chunks = None
        
        for data_qr_file in data_qr_files:
            print(f"📖 Reading data QR: {data_qr_file}")
            
            qr_data_str = self.read_qr_code(data_qr_file)
            
            if not qr_data_str:
                print(f"❌ Cannot read QR code from {data_qr_file}")
                continue
            
            try:
                qr_data = json.loads(qr_data_str)
                
                if qr_data.get('p') != 'BD':
                    print(f"❌ Invalid data QR protocol: {qr_data.get('p')}")
                    continue
                
                chunk_index = qr_data.get('i', 0)
                total_chunks = qr_data.get('n', 1)
                encrypted_chunk = qr_data.get('d', '')
                
                chunks_data[chunk_index] = encrypted_chunk
                print(f"✅ Data chunk {chunk_index + 1} decoded")
                
            except Exception as e:
                print(f"❌ Failed to decode data QR: {e}")
                continue
        
        # Verify all chunks present
        if not total_chunks or len(chunks_data) != total_chunks:
            print(f"❌ Missing data chunks: have {len(chunks_data)}, need {total_chunks}")
            return False
        
        # Reconstruct encrypted data
        encrypted_b64 = ""
        for i in range(total_chunks):
            if i not in chunks_data:
                print(f"❌ Missing chunk {i}")
                return False
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
            # Use the ORIGINAL biometric bytes from storage for key derivation
            stored_bio_string = json.dumps(biometric_key, separators=(',', ':'))
            stored_bio_bytes = stored_bio_string.encode('utf-8')
            
            encryption_key = self.derive_encryption_key(stored_bio_bytes)
            fernet = Fernet(encryption_key)
            
            encrypted_data = base64.b64decode(encrypted_b64.encode('utf-8'))
            decrypted_data = fernet.decrypt(encrypted_data)
            
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, metadata['f'])
            
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
            
            print(f"🎉 DOCUMENT DECRYPTED SUCCESSFULLY!")
            print(f"📄 File: {output_file}")
            print(f"📊 Size: {len(decrypted_data)} bytes")
            
            return True
            
        except Exception as e:
            print(f"❌ Decryption failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def verify_biometric_match(self, stored_bio, live_bio, threshold=0.6):
        """Verify biometric signatures match"""
        try:
            hist1 = np.array(stored_bio['h'])
            hist2 = np.array(live_bio['h'])
            hist_corr = cv2.compareHist(hist1.astype(np.float32), hist2.astype(np.float32), cv2.HISTCMP_CORREL)
            
            brightness_diff = abs(stored_bio['c'] - live_bio['c'])
            intensity_diff = abs(stored_bio['m'] - live_bio['m'])
            
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
    print("🌊⚡ BIOMETRIC DOCUMENT ENCRYPTOR - ULTIMATE VERSION ⚡🌊")
    print("=" * 65)
    print(f"QR Library: {QR_LIB}")
    
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
