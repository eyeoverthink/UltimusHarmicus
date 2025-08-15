#!/usr/bin/env python3
"""
Simple QR Biometric Test - Direct execution without menu
"""

import cv2
import numpy as np
import qrcode
import json
import time
from PIL import Image
import face_recognition
from pyzbar import pyzbar

def test_camera():
    """Test camera access"""
    print("🎥 Testing camera access...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Cannot access camera")
        return False
    
    ret, frame = cap.read()
    if ret:
        print("✅ Camera working - frame captured")
        cv2.imshow('Camera Test - Press any key to close', frame)
        cv2.waitKey(2000)  # Show for 2 seconds
        cv2.destroyAllWindows()
    else:
        print("❌ Cannot read from camera")
        
    cap.release()
    return ret

def create_test_qr():
    """Create a simple test QR without face data"""
    print("📱 Creating test QR code...")
    
    test_data = {
        "protocol": "QUDSP-Test-1.0",
        "timestamp": int(time.time()),
        "test_data": "This is a test QR code",
        "device_config": {
            "wifi_ssid": "TestNetwork",
            "apps": ["test_app"],
            "settings": {"test": True}
        }
    }
    
    json_data = json.dumps(test_data, separators=(',', ':'))
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    
    qr.add_data(json_data)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    filename = "test_qr.png"
    qr_img.save(filename)
    
    print(f"✅ Test QR saved: {filename}")
    return filename

def decode_test_qr(filename):
    """Decode the test QR"""
    print(f"🔍 Decoding QR: {filename}")
    
    image = cv2.imread(filename)
    if image is None:
        print("❌ Cannot read QR image file")
        return None
    
    decoded_objects = pyzbar.decode(image)
    
    if not decoded_objects:
        print("❌ No QR code found")
        return None
    
    qr_data = decoded_objects[0].data.decode('utf-8')
    
    try:
        data = json.loads(qr_data)
        print("✅ QR decoded successfully")
        print(f"📋 Protocol: {data.get('protocol', 'Unknown')}")
        print(f"📋 Test Data: {data.get('test_data', 'None')}")
        return data
    except json.JSONDecodeError:
        print("❌ Invalid JSON in QR")
        return None

def main():
    print("🌊⚡ QR BIOMETRIC SYSTEM - SIMPLE TEST ⚡🌊")
    print("=" * 50)
    
    # Test 1: Camera access
    print("\n🔧 TEST 1: Camera Access")
    camera_ok = test_camera()
    
    # Test 2: QR creation
    print("\n🔧 TEST 2: QR Code Creation")
    qr_file = create_test_qr()
    
    # Test 3: QR decoding
    print("\n🔧 TEST 3: QR Code Decoding")
    decoded_data = decode_test_qr(qr_file)
    
    # Test 4: Face recognition library
    print("\n🔧 TEST 4: Face Recognition Library")
    try:
        # Test if face_recognition imports work
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        face_locations = face_recognition.face_locations(test_image)
        print("✅ Face recognition library working")
    except Exception as e:
        print(f"❌ Face recognition error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 BASIC SYSTEM TESTS COMPLETE")
    
    if camera_ok and decoded_data:
        print("✅ System ready for biometric testing")
        print("\nNext steps:")
        print("1. Run full biometric QR encoder")
        print("2. Capture face and create biometric QR")
        print("3. Test live verification")
    else:
        print("❌ System needs troubleshooting")

if __name__ == "__main__":
    main()
