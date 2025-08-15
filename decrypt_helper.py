#!/usr/bin/env python3
"""
Biometric QR Decryption Helper
Simplified interface for decrypting documents
"""

import os
import glob

def find_qr_files():
    """Find all QR files in current directory"""
    key_files = glob.glob("*_KEY.png")
    data_files = glob.glob("*_D*.png")
    
    print("🔍 Available QR files:")
    print(f"🔑 Key files: {len(key_files)}")
    for f in key_files:
        print(f"   - {f}")
    
    print(f"📱 Data files: {len(data_files)}")
    for f in sorted(data_files):
        print(f"   - {f}")
    
    return key_files, data_files

def auto_decrypt_latest():
    """Auto-decrypt the most recent QR set"""
    key_files, data_files = find_qr_files()
    
    if not key_files:
        print("❌ No key files found")
        return
    
    if not data_files:
        print("❌ No data files found")
        return
    
    # Get the latest key file
    latest_key = max(key_files, key=os.path.getctime)
    
    # Find matching data files
    base_name = latest_key.replace("_KEY.png", "")
    matching_data = [f for f in data_files if f.startswith(base_name)]
    matching_data.sort()
    
    print(f"\n🎯 Auto-selected QR set:")
    print(f"🔑 Key: {latest_key}")
    print(f"📱 Data files ({len(matching_data)}):")
    for f in matching_data:
        print(f"   - {f}")
    
    # Import and run decryption
    from biometric_document_encryptor_final import BiometricDocumentEncryptor
    
    encryptor = BiometricDocumentEncryptor()
    success = encryptor.decrypt_from_qr_system(latest_key, matching_data)
    
    if success:
        print("\n🎉 DECRYPTION SUCCESSFUL!")
    else:
        print("\n❌ DECRYPTION FAILED")

if __name__ == "__main__":
    print("🔓 BIOMETRIC QR DECRYPTION HELPER")
    print("=" * 40)
    
    auto_decrypt_latest()
