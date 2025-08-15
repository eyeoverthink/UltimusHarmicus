#!/usr/bin/env python3
"""
Automated Biometric QR Decryption Helper
Automatically finds and decrypts the latest QR set
"""

import os
import glob
import json
from biometric_document_encryptor_ultimate import BiometricDocumentEncryptor

def auto_decrypt_latest():
    """Automatically decrypt the most recent QR set"""
    print("🔓 AUTOMATED BIOMETRIC QR DECRYPTION")
    print("=" * 40)
    
    # Find the most recent QR set
    key_files = sorted(glob.glob("enc_*_KEY.png"), key=os.path.getctime, reverse=True)
    
    if not key_files:
        print("❌ No key QR files found")
        return False
    
    latest_key = key_files[0]
    base_name = latest_key.replace("_KEY.png", "")
    data_files = sorted(glob.glob(f"{base_name}_D*.png"))
    
    print(f"🔑 Auto-selected Key QR: {latest_key}")
    print(f"📱 Auto-selected Data QRs: {len(data_files)} files")
    
    if not data_files:
        print("❌ No matching data QR files found")
        return False
    
    # Show first few data files
    for i, f in enumerate(data_files[:5]):
        print(f"   - {f}")
    if len(data_files) > 5:
        print(f"   ... and {len(data_files) - 5} more")
    
    print("\n🔓 Starting automated decryption...")
    
    encryptor = BiometricDocumentEncryptor()
    success = encryptor.decrypt_from_qr_system(latest_key, data_files)
    
    if success:
        print("\n🎉 AUTOMATED DECRYPTION SUCCESSFUL!")
        print("📁 Check the 'decrypted' folder for your file")
        return True
    else:
        print("\n❌ AUTOMATED DECRYPTION FAILED")
        return False

def test_qr_readability():
    """Test if QR codes can be read"""
    print("\n🔍 TESTING QR CODE READABILITY")
    print("=" * 35)
    
    # Find latest QR files
    key_files = sorted(glob.glob("enc_*_KEY.png"), key=os.path.getctime, reverse=True)
    data_files = sorted(glob.glob("enc_*_D1.png"), key=os.path.getctime, reverse=True)
    
    if not key_files:
        print("❌ No QR files found")
        return False
    
    test_files = [key_files[0]]
    if data_files:
        test_files.append(data_files[0])
    
    encryptor = BiometricDocumentEncryptor()
    
    for filename in test_files:
        print(f"\n📖 Testing: {filename}")
        
        qr_data = encryptor.read_qr_code(filename)
        
        if qr_data:
            try:
                data = json.loads(qr_data)
                protocol = data.get('p', 'Unknown')
                print(f"  ✅ QR readable - Protocol: {protocol}")
                
                if 'k' in data:
                    print("  🔑 Contains biometric key data")
                if 'd' in data:
                    print("  📱 Contains encrypted data chunk")
                    chunk_info = f"Chunk {data.get('i', '?')}/{data.get('n', '?')}"
                    print(f"  📊 {chunk_info}")
                    
            except Exception as e:
                print(f"  ❌ JSON parse error: {e}")
        else:
            print("  ❌ QR code not readable")
    
    return True

if __name__ == "__main__":
    print("🌊⚡ BIOMETRIC QR AUTO-DECRYPTION TOOL ⚡🌊")
    print("=" * 50)
    
    # Test readability first
    test_qr_readability()
    
    # Attempt auto-decryption
    print("\n" + "=" * 50)
    auto_decrypt_latest()
