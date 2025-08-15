#!/usr/bin/env python3
"""
QR Biometric Face Encoder - Proof of Concept
Encodes face data into QR codes for device authentication
"""

import cv2
import numpy as np
import qrcode
import json
import base64
from PIL import Image
import face_recognition
import time
from pyzbar import pyzbar

class QRBiometricEncoder:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def capture_face_from_camera(self):
        """Capture face from camera and return face encoding"""
        print("🎥 Starting camera for face capture...")
        cap = cv2.VideoCapture(0)
        
        face_encoding = None
        face_image = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert to RGB for face_recognition
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Find faces
            face_locations = face_recognition.face_locations(rgb_frame)
            
            if face_locations:
                # Draw rectangle around face
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, "Press SPACE to capture", (left, top-10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            cv2.imshow('Face Capture - Press SPACE to capture, ESC to exit', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # Space key
                if face_locations:
                    # Get face encoding
                    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                    if face_encodings:
                        face_encoding = face_encodings[0]
                        face_image = rgb_frame
                        print("✅ Face captured and encoded!")
                        break
                else:
                    print("❌ No face detected. Please position your face in the frame.")
            elif key == 27:  # ESC key
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return face_encoding, face_image
    
    def compress_face_encoding(self, face_encoding, precision=3):
        """Compress face encoding for QR storage"""
        # Round to reduce precision and size
        compressed = np.round(face_encoding, precision)
        # Convert to list for JSON serialization
        return compressed.tolist()
    
    def create_biometric_qr(self, face_encoding, device_config=None, filename="biometric_qr.png"):
        """Create QR code with face encoding and device config"""
        
        # Compress face encoding
        compressed_face = self.compress_face_encoding(face_encoding)
        
        # Create QR data structure
        qr_data = {
            "protocol": "QUDSP-Biometric-1.0",
            "timestamp": int(time.time()),
            "biometric": {
                "type": "face_encoding",
                "data": compressed_face,
                "precision": 3,
                "verification": "face_recognition_lib"
            },
            "device_config": device_config or {
                "wifi_ssid": "TestNetwork",
                "apps": ["com.spotify.music", "com.netflix.mediaclient"],
                "settings": {"auto_brightness": True, "notifications": True}
            },
            "nonce": f"bio_{int(time.time() * 1000)}"
        }
        
        # Convert to JSON string
        json_data = json.dumps(qr_data, separators=(',', ':'))
        
        print(f"📊 QR Data Size: {len(json_data)} bytes")
        
        # Create QR code with high error correction
        qr = qrcode.QRCode(
            version=None,  # Auto-determine version
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
            box_size=10,
            border=4,
        )
        
        qr.add_data(json_data)
        qr.make(fit=True)
        
        # Create QR image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save(filename)
        
        print(f"✅ Biometric QR code saved: {filename}")
        print(f"📱 QR Version: {qr.version}")
        print(f"🔒 Error Correction: HIGH")
        
        return filename, qr_data
    
    def decode_biometric_qr(self, qr_image_path):
        """Decode QR code and extract biometric data"""
        print(f"🔍 Decoding QR code: {qr_image_path}")
        
        # Load QR image
        image = cv2.imread(qr_image_path)
        
        # Decode QR codes
        decoded_objects = pyzbar.decode(image)
        
        if not decoded_objects:
            print("❌ No QR code found in image")
            return None
        
        # Get first QR code data
        qr_data = decoded_objects[0].data.decode('utf-8')
        
        try:
            # Parse JSON
            biometric_data = json.loads(qr_data)
            print("✅ QR code decoded successfully")
            print(f"📋 Protocol: {biometric_data.get('protocol', 'Unknown')}")
            
            return biometric_data
        except json.JSONDecodeError:
            print("❌ Invalid JSON in QR code")
            return None
    
    def verify_face_against_qr(self, qr_data, live_face_encoding):
        """Verify live face against QR biometric data"""
        if not qr_data or 'biometric' not in qr_data:
            return False, "No biometric data in QR"
        
        # Extract stored face encoding
        stored_face_data = qr_data['biometric']['data']
        stored_face_encoding = np.array(stored_face_data)
        
        # Compare faces
        matches = face_recognition.compare_faces([stored_face_encoding], live_face_encoding, tolerance=0.6)
        distance = face_recognition.face_distance([stored_face_encoding], live_face_encoding)[0]
        
        is_match = matches[0]
        confidence = 1 - distance
        
        print(f"🔍 Face Verification Results:")
        print(f"   Match: {'✅ YES' if is_match else '❌ NO'}")
        print(f"   Confidence: {confidence:.2%}")
        print(f"   Distance: {distance:.3f}")
        
        return is_match, confidence
    
    def live_verification_demo(self, qr_image_path):
        """Demo: Verify live face against QR biometric data"""
        print("\n🔒 BIOMETRIC QR VERIFICATION DEMO")
        print("=" * 50)
        
        # Decode QR
        qr_data = self.decode_biometric_qr(qr_image_path)
        if not qr_data:
            return False
        
        # Capture live face
        print("\n📸 Please look at camera for verification...")
        live_encoding, live_image = self.capture_face_from_camera()
        
        if live_encoding is None:
            print("❌ Could not capture live face")
            return False
        
        # Verify
        is_match, confidence = self.verify_face_against_qr(qr_data, live_encoding)
        
        if is_match:
            print("\n🎉 BIOMETRIC VERIFICATION SUCCESSFUL!")
            print("✅ Device setup authorized")
            print(f"🔧 Applying configuration: {qr_data.get('device_config', {})}")
            return True
        else:
            print("\n🚫 BIOMETRIC VERIFICATION FAILED!")
            print("❌ Device setup denied")
            return False

def main():
    print("🌊⚡ QR BIOMETRIC FACE ENCODER - PROOF OF CONCEPT ⚡🌊")
    print("=" * 60)
    
    encoder = QRBiometricEncoder()
    
    while True:
        print("\nSelect option:")
        print("1. Create Biometric QR Code")
        print("2. Verify Face Against QR Code")
        print("3. Full Demo (Create + Verify)")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            print("\n📸 Creating Biometric QR Code...")
            face_encoding, face_image = encoder.capture_face_from_camera()
            
            if face_encoding is not None:
                filename = f"biometric_qr_{int(time.time())}.png"
                encoder.create_biometric_qr(face_encoding, filename=filename)
            else:
                print("❌ Failed to capture face")
        
        elif choice == "2":
            qr_path = input("Enter QR image path: ").strip()
            encoder.live_verification_demo(qr_path)
        
        elif choice == "3":
            print("\n🎬 FULL BIOMETRIC QR DEMO")
            print("Step 1: Creating your biometric QR...")
            
            face_encoding, face_image = encoder.capture_face_from_camera()
            if face_encoding is not None:
                filename = f"demo_biometric_qr_{int(time.time())}.png"
                qr_file, qr_data = encoder.create_biometric_qr(face_encoding, filename=filename)
                
                print(f"\nStep 2: Verifying against created QR...")
                input("Press Enter to continue with verification...")
                
                encoder.live_verification_demo(filename)
            else:
                print("❌ Demo failed - could not capture face")
        
        elif choice == "4":
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
