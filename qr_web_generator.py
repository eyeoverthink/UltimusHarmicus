#!/usr/bin/env python3
"""
QR Web Generator - Creates real QR codes for the web interface
Uses the same proven QR generation as qr_phone_control_loop.py
"""

import qrcode
import json
import base64
from io import BytesIO
import sys
import argparse

def generate_qr_data_url(url, box_size=10, border=4):
    """Generate QR code and return as data URL for web display"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=box_size,
            border=border,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to data URL
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    
    except Exception as e:
        print(f"Error generating QR code: {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description='Generate QR codes for web interface')
    parser.add_argument('--url', required=True, help='URL to encode in QR code')
    parser.add_argument('--box-size', type=int, default=10, help='QR code box size')
    parser.add_argument('--border', type=int, default=4, help='QR code border size')
    
    args = parser.parse_args()
    
    data_url = generate_qr_data_url(args.url, args.box_size, args.border)
    if data_url:
        print(json.dumps({"success": True, "data_url": data_url}))
    else:
        print(json.dumps({"success": False, "error": "Failed to generate QR code"}))

if __name__ == "__main__":
    main()
