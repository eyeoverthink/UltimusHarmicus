#!/usr/bin/env python3
"""
QR Biometric System - OpenCV Only (No face_recognition library)
Uses OpenCV's built-in face detection for proof of concept
"""

import cv2
import numpy as np
import qrcode
import json
import time
from PIL import Image
from pyzbar import pyzbar
import hashlib

class QRBiometricOpenCV:
    def __init__(self):
        # Load OpenCV face detection cascade
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
    def capture_face_from_camera(self):
        """Capture face from camera using OpenCV"""
        print("🎥 Starting camera for face capture...")
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Cannot access camera")
            return None, None
        
        face_data = None
        face_image = None
        
        print("📸 Position your face in the camera frame and press SPACE to capture")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Cannot read from camera")
                break
                
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # Draw rectangles around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Press SPACE to capture", (x, y-10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            cv2.imshow('Face Capture - Press SPACE to capture, ESC to exit', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  # Space key
                if len(faces) > 0:
                    # Extract face region
                    x, y, w, h = faces[0]  # Use first detected face
                    face_roi = gray[y:y+h, x:x+w]
                    
                    # Resize to standard size for consistency
                    face_roi = cv2.resize(face_roi, (100, 100))
                    
                    # Create simple face "encoding" using image histogram
                    face_data = self.create_face_signature(face_roi)
                    face_image = frame
                    
                    print("✅ Face captured and encoded!")
                    break
                else:
                    print("❌ No face detected. Please position your face in the frame.")
            elif key == 27:  # ESC key
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return face_data, face_image
    
    def create_face_signature(self, face_roi):
        """Create a simple face signature using OpenCV features"""
        # Method 1: Histogram-based signature
        hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
        hist = hist.flatten()
        
        # Method 2: Add some geometric features
        height, width = face_roi.shape
        
        # Simple geometric ratios
        center_brightness = np.mean(face_roi[height//3:2*height//3, width//3:2*width//3])
        edge_brightness = np.mean(face_roi[:10, :]) + np.mean(face_roi[-10:, :])
        
        # Combine features
        signature = {
            'histogram': hist[:50].tolist(),  # First 50 histogram bins
            'center_brightness': float(center_brightness),
            'edge_brightness': float(edge_brightness),
            'width': width,
            'height': height,
            'mean_intensity': float(np.mean(face_roi)),
            'std_intensity': float(np.std(face_roi))
        }
        
        return signature
    
    def create_biometric_qr(self, face_signature, device_config=None, filename="biometric_qr_opencv.png"):
        """Create QR code with face signature and device config"""
        
        # Create QR data structure
        qr_data = {
            "protocol": "QUDSP-OpenCV-1.0",
            "timestamp": int(time.time()),
            "biometric": {
                "type": "opencv_face_signature",
                "data": face_signature,
                "method": "histogram_geometric"
            },
            "device_config": device_config or {
                "wifi_ssid": "TestNetwork",
                "apps": ["com.spotify.music", "com.netflix.mediaclient"],
                "settings": {"auto_brightness": True, "notifications": True}
            },
            "nonce": f"opencv_{int(time.time() * 1000)}"
        }
        
        # Convert to JSON string
        json_data = json.dumps(qr_data, separators=(',', ':'))
        
        print(f"📊 QR Data Size: {len(json_data)} bytes")
        
        # Create QR code
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
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
        
        return filename, qr_data
    
    def decode_biometric_qr(self, qr_image_path):
        """Decode QR code and extract biometric data"""
        print(f"🔍 Decoding QR code: {qr_image_path}")
        
        # Load QR image
        image = cv2.imread(qr_image_path)
        
        if image is None:
            print("❌ Cannot read QR image file")
            return None
        
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
    
    def compare_face_signatures(self, sig1, sig2):
        """Compare two face signatures"""
        if not sig1 or not sig2:
            return False, 0.0
        
        # Compare histograms
        hist1 = np.array(sig1['histogram'])
        hist2 = np.array(sig2['histogram'])
        hist_correlation = cv2.compareHist(hist1.astype(np.float32), hist2.astype(np.float32), cv2.HISTCMP_CORREL)
        
        # Compare geometric features
        brightness_diff = abs(sig1['center_brightness'] - sig2['center_brightness'])
        intensity_diff = abs(sig1['mean_intensity'] - sig2['mean_intensity'])
        
        # Combine scores (weights can be tuned)
        similarity_score = (
            hist_correlation * 0.7 +  # Histogram similarity (70%)
            (1 - brightness_diff / 255) * 0.2 +  # Brightness similarity (20%)
            (1 - intensity_diff / 255) * 0.1  # Intensity similarity (10%)
        )
        
        # Threshold for match (can be adjusted)
        is_match = similarity_score > 0.6
        
        return is_match, similarity_score
    
    def verify_face_against_qr(self, qr_data, live_face_signature):
        """Verify live face against QR biometric data"""
        if not qr_data or 'biometric' not in qr_data:
            return False, "No biometric data in QR"
        
        # Extract stored face signature
        stored_signature = qr_data['biometric']['data']
        
        # Compare signatures
        is_match, confidence = self.compare_face_signatures(stored_signature, live_face_signature)
        
        print(f"🔍 Face Verification Results:")
        print(f"   Match: {'✅ YES' if is_match else '❌ NO'}")
        print(f"   Confidence: {confidence:.2%}")
        
        return is_match, confidence
    
    def full_demo(self):
        """Complete biometric QR demo"""
        print("\n🎬 FULL BIOMETRIC QR DEMO - OpenCV Version")
        print("=" * 60)
        
        # Step 1: Create biometric QR
        print("\nStep 1: Creating your biometric QR...")
        face_signature, face_image = self.capture_face_from_camera()
        
        if face_signature is None:
            print("❌ Demo failed - could not capture face")
            return False
        
        filename = f"demo_biometric_opencv_{int(time.time())}.png"
        qr_file, qr_data = self.create_biometric_qr(face_signature, filename=filename)
        
        print(f"\n✅ Biometric QR created: {filename}")
        
        # Step 2: Verify against created QR
        print(f"\nStep 2: Verifying against created QR...")
        input("Press Enter to continue with verification...")
        
        print("\n📸 Please look at camera for verification...")
        live_signature, live_image = self.capture_face_from_camera()
        
        if live_signature is None:
            print("❌ Could not capture live face for verification")
            return False
        
        # Step 3: Compare
        is_match, confidence = self.verify_face_against_qr(qr_data, live_signature)
        
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
    print("🌊⚡ QR BIOMETRIC SYSTEM - OpenCV Version ⚡🌊")
    print("=" * 60)
    
    encoder = QRBiometricOpenCV()
    
    while True:
        print("\nSelect option:")
        print("1. Create Biometric QR Code")
        print("2. Verify Face Against QR Code")
        print("3. Full Demo (Create + Verify)")
        print("4. Test Camera")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            print("\n📸 Creating Biometric QR Code...")
            face_signature, face_image = encoder.capture_face_from_camera()
            
            if face_signature is not None:
                filename = f"biometric_opencv_{int(time.time())}.png"
                encoder.create_biometric_qr(face_signature, filename=filename)
            else:
                print("❌ Failed to capture face")
        
        elif choice == "2":
            qr_path = input("Enter QR image path: ").strip()
            qr_data = encoder.decode_biometric_qr(qr_path)
            
            if qr_data:
                print("\n📸 Please look at camera for verification...")
                live_signature, live_image = encoder.capture_face_from_camera()
                
                if live_signature:
                    encoder.verify_face_against_qr(qr_data, live_signature)
                else:
                    print("❌ Could not capture live face")
        
        elif choice == "3":
            encoder.full_demo()
        
        elif choice == "4":
            print("\n🎥 Testing camera...")
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    cv2.imshow('Camera Test - Press any key to close', frame)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    print("✅ Camera working")
                else:
                    print("❌ Cannot read from camera")
            else:
                print("❌ Cannot access camera")
            cap.release()
        
        elif choice == "5":
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()
