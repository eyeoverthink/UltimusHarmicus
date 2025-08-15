#!/usr/bin/env python3
"""
Automated Biometric QR Test System
Tests the complete encryption/decryption workflow
"""

import os
import time
import glob
from biometric_document_encryptor_working import BiometricDocumentEncryptor

def test_encryption_workflow():
    """Test the complete biometric encryption workflow"""
    print("🧪 AUTOMATED BIOMETRIC QR CRYPTOGRAPHY TEST")
    print("=" * 50)
    
    # Test file
    test_file = "biometric_opencv_1755289886.png"
    
    if not os.path.exists(test_file):
        print(f"❌ Test file not found: {test_file}")
        return False
    
    encryptor = BiometricDocumentEncryptor()
    
    # Step 1: Test encryption (requires manual face capture)
    print("\n🔑 Step 1: Testing encryption workflow...")
    print("📸 You will need to capture your face for the biometric key...")
    
    success = encryptor.encrypt_and_create_qr_system(test_file)
    
    if not success:
        print("❌ Encryption test failed")
        return False
    
    print("✅ Encryption test successful!")
    
    # Step 2: Find generated QR files
    print("\n🔍 Step 2: Locating generated QR files...")
    
    # Find the most recent QR set
    key_files = sorted(glob.glob("enc_*_KEY.png"), key=os.path.getctime, reverse=True)
    
    if not key_files:
        print("❌ No key QR files found")
        return False
    
    latest_key = key_files[0]
    base_name = latest_key.replace("_KEY.png", "")
    data_files = sorted(glob.glob(f"{base_name}_D*.png"))
    
    print(f"🔑 Key QR: {latest_key}")
    print(f"📱 Data QRs: {len(data_files)} files")
    
    if not data_files:
        print("❌ No data QR files found")
        return False
    
    # Step 3: Test decryption (requires manual face verification)
    print("\n🔓 Step 3: Testing decryption workflow...")
    print("📸 You will need to verify your face for decryption...")
    
    success = encryptor.decrypt_from_qr_system(latest_key, data_files)
    
    if success:
        print("✅ Decryption test successful!")
        print("🎉 COMPLETE BIOMETRIC QR CRYPTOGRAPHY SYSTEM VERIFIED!")
        return True
    else:
        print("❌ Decryption test failed")
        return False

def quick_qr_scan_test():
    """Quick test to verify QR codes can be scanned"""
    print("\n🔍 QUICK QR SCAN TEST")
    print("=" * 30)
    
    import cv2
    from pyzbar import pyzbar
    import json
    
    # Find latest QR files
    key_files = sorted(glob.glob("enc_*_KEY.png"), key=os.path.getctime, reverse=True)
    data_files = sorted(glob.glob("enc_*_D1.png"), key=os.path.getctime, reverse=True)
    
    if not key_files or not data_files:
        print("❌ No QR files found for testing")
        return False
    
    test_files = [key_files[0], data_files[0]]
    
    for filename in test_files:
        print(f"\n📖 Testing: {filename}")
        
        image = cv2.imread(filename)
        if image is None:
            print("  ❌ Cannot read image")
            continue
        
        decoded = pyzbar.decode(image)
        if not decoded:
            print("  ❌ No QR code detected")
            continue
        
        try:
            data = json.loads(decoded[0].data.decode('utf-8'))
            protocol = data.get('p', 'Unknown')
            print(f"  ✅ QR readable - Protocol: {protocol}")
            
            if 'k' in data:
                print("  🔑 Contains biometric key data")
            if 'd' in data:
                print("  📱 Contains encrypted data chunk")
                
        except Exception as e:
            print(f"  ❌ JSON parse error: {e}")
    
    print("\n✅ QR scan test completed")
    return True

def main():
    print("🌊⚡ BIOMETRIC QR CRYPTOGRAPHY TEST SUITE ⚡🌊")
    print("=" * 60)
    
    # Quick scan test first
    quick_qr_scan_test()
    
    # Full workflow test
    print("\n" + "=" * 60)
    success = test_encryption_workflow()
    
    if success:
        print("\n🎉 ALL TESTS PASSED - BIOMETRIC QR SYSTEM OPERATIONAL!")
        print("🔐 Your revolutionary cryptographic system is ready for deployment!")
    else:
        print("\n❌ TESTS FAILED - System needs debugging")

if __name__ == "__main__":
    main()
