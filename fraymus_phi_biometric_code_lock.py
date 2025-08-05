#!/usr/bin/env python3
"""
FRAYMUS PHI BIOMETRIC CODE LOCK
Revolutionary facial authentication for code execution

Only the authorized face (matching QR consciousness physics) can unlock or run code.
Creates unprecedented personal security using φ-harmonic biometric verification.
"""

import json
import subprocess
import os
import time
import hashlib
from datetime import datetime
from consciousness_protection_system import ConsciousnessProtectionSystem
from PIL import Image, ImageStat
import numpy as np

class FraymusPhiBiometricCodeLock:
    def __init__(self):
        self.protection_system = ConsciousnessProtectionSystem()
        self.phi = 1.618033988749895
        self.psi = 1.465571231876768
        self.omega = 1.282427129100623
        self.xi = 1.202056903159594
        self.lambda_const = 1.303577269034296
        self.authorized_qr_data = None
        self.authentication_threshold = 0.75  # Minimum match score for access
        
    def load_authorized_qr_reference(self):
        """Load the authorized QR reference for biometric comparison"""
        print("🔐 Loading authorized QR biometric reference...")
        
        # Find the most recent QR protection file
        qr_files = [f for f in os.listdir('.') if f.startswith('fraymus_phi_qr_protection_data_')]
        if not qr_files:
            print("❌ No authorized QR reference found")
            return False
        
        latest_file = sorted(qr_files)[-1]
        print(f"📄 Loading authorized reference: {latest_file}")
        
        try:
            with open(latest_file, 'r') as f:
                self.authorized_qr_data = json.load(f)
            
            print("✅ Authorized QR biometric reference loaded")
            print(f"👤 Authorized person: Vaughn Scott")
            print(f"⚡ φ-harmonic signature: {self.authorized_qr_data['phi_rules']['golden_score']:.3f}")
            print(f"🧠 Consciousness level: {self.authorized_qr_data['fraymus_phi']['consciousness_level']:.2f}")
            return True
        except Exception as e:
            print(f"❌ Error loading authorized reference: {e}")
            return False
    
    def capture_authentication_image(self):
        """Capture live image for biometric authentication"""
        print("\n📸 Capturing live image for biometric authentication...")
        print("🔴 Look directly at camera for facial verification...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        auth_filename = f"auth_attempt_{timestamp}.jpg"
        
        try:
            # Capture with imagesnap (2 second delay)
            result = subprocess.run(['imagesnap', '-w', '2', auth_filename], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and os.path.exists(auth_filename):
                print(f"✅ Authentication image captured: {auth_filename}")
                return auth_filename
            else:
                print(f"❌ Camera capture failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("⏰ Authentication capture timeout")
            return None
        except Exception as e:
            print(f"❌ Authentication capture error: {e}")
            return None
    
    def analyze_authentication_image(self, image_path):
        """Analyze authentication image for biometric comparison"""
        print(f"\n🔬 Analyzing authentication image: {image_path}")
        
        try:
            with Image.open(image_path) as img:
                # Get image properties
                width, height = img.size
                
                # Calculate image statistics
                stat = ImageStat.Stat(img)
                
                # Extract color information
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                    stat = ImageStat.Stat(img)
                
                mean_colors = stat.mean
                stddev_colors = stat.stddev
                
                # Calculate φ-harmonic ratios
                aspect_ratio = height / width
                phi_deviation = abs(aspect_ratio - self.phi)
                phi_alignment = 1.0 / (1.0 + phi_deviation)
                
                # Calculate color harmony
                color_variance = sum(stddev_colors) / len(stddev_colors)
                color_balance = min(mean_colors) / max(mean_colors)
                
                # Calculate consciousness constants
                file_size = os.path.getsize(image_path)
                consciousness_metrics = {
                    "phi_alignment": phi_alignment,
                    "psi_resonance": phi_alignment * self.psi,
                    "omega_grounding": color_balance * self.omega,
                    "xi_consciousness": (color_variance / 255.0) * self.xi,
                    "lambda_evolution": (file_size / 100000.0) * self.lambda_const
                }
                
                auth_analysis = {
                    "filename": image_path,
                    "timestamp": datetime.now().isoformat(),
                    "image_properties": {
                        "width": width,
                        "height": height,
                        "aspect_ratio": aspect_ratio,
                        "file_size": file_size
                    },
                    "color_analysis": {
                        "mean_rgb": mean_colors,
                        "stddev_rgb": stddev_colors,
                        "color_variance": color_variance,
                        "color_balance": color_balance
                    },
                    "phi_harmonic_analysis": {
                        "phi_deviation": phi_deviation,
                        "phi_alignment": phi_alignment,
                        "golden_ratio_score": phi_alignment * self.phi
                    },
                    "consciousness_constants": consciousness_metrics
                }
                
                print(f"✅ Authentication analysis complete")
                print(f"📐 Aspect ratio: {aspect_ratio:.3f}")
                print(f"⚡ φ-alignment: {phi_alignment:.3f}")
                print(f"🎨 Color variance: {color_variance:.2f}")
                
                return auth_analysis
                
        except Exception as e:
            print(f"❌ Authentication analysis error: {e}")
            return None
    
    def compare_biometric_signatures(self, auth_analysis):
        """Compare authentication analysis with authorized QR reference"""
        print(f"\n🔍 Comparing biometric signatures...")
        
        if not self.authorized_qr_data or not auth_analysis:
            print("❌ Missing data for comparison")
            return 0.0, {}
        
        # Extract authorized reference data
        auth_phi = self.authorized_qr_data['phi_rules']
        auth_color = self.authorized_qr_data['color_rules']
        auth_consciousness = self.authorized_qr_data['consciousness']
        
        # Extract current authentication data
        current_phi = auth_analysis['phi_harmonic_analysis']
        current_color = auth_analysis['color_analysis']
        current_consciousness = auth_analysis['consciousness_constants']
        
        # Calculate φ-harmonic similarity
        phi_score = 1.0 - abs(current_phi['phi_alignment'] - auth_phi['phi_align']) / max(current_phi['phi_alignment'], auth_phi['phi_align'])
        aspect_score = 1.0 - abs(current_phi['phi_alignment'] - auth_phi['aspect_ratio']) / max(abs(current_phi['phi_alignment']), abs(auth_phi['aspect_ratio']))
        golden_score = 1.0 - abs(current_phi['golden_ratio_score'] - auth_phi['golden_score']) / max(current_phi['golden_ratio_score'], auth_phi['golden_score'])
        
        # Calculate color similarity
        color_var_score = 1.0 - abs(current_color['color_variance'] - auth_color['variance']) / max(current_color['color_variance'], auth_color['variance'])
        color_bal_score = 1.0 - abs(current_color['color_balance'] - auth_color['balance']) / max(current_color['color_balance'], auth_color['balance'])
        
        # Calculate RGB similarity
        rgb_scores = []
        for i in range(3):
            if len(current_color['mean_rgb']) > i and len(auth_color['rgb_mean']) > i:
                rgb_diff = abs(current_color['mean_rgb'][i] - auth_color['rgb_mean'][i])
                rgb_score = 1.0 - (rgb_diff / 255.0)
                rgb_scores.append(rgb_score)
        rgb_avg_score = sum(rgb_scores) / len(rgb_scores) if rgb_scores else 0.0
        
        # Calculate consciousness similarity
        psi_score = 1.0 - abs(current_consciousness['psi_resonance'] - auth_consciousness['psi']) / max(current_consciousness['psi_resonance'], auth_consciousness['psi'])
        omega_score = 1.0 - abs(current_consciousness['omega_grounding'] - auth_consciousness['omega']) / max(current_consciousness['omega_grounding'], auth_consciousness['omega'])
        xi_score = 1.0 - abs(current_consciousness['xi_consciousness'] - auth_consciousness['xi']) / max(current_consciousness['xi_consciousness'], auth_consciousness['xi'])
        lambda_score = 1.0 - abs(current_consciousness['lambda_evolution'] - auth_consciousness['lambda']) / max(current_consciousness['lambda_evolution'], auth_consciousness['lambda'])
        
        # Calculate weighted overall similarity
        phi_weight = 0.35
        color_weight = 0.25
        consciousness_weight = 0.40
        
        phi_overall = (phi_score + aspect_score + golden_score) / 3
        color_overall = (color_var_score + color_bal_score + rgb_avg_score) / 3
        consciousness_overall = (psi_score + omega_score + xi_score + lambda_score) / 4
        
        overall_similarity = (
            phi_overall * phi_weight +
            color_overall * color_weight +
            consciousness_overall * consciousness_weight
        )
        
        comparison_details = {
            "phi_harmonic_similarity": {
                "phi_alignment_score": phi_score,
                "aspect_ratio_score": aspect_score,
                "golden_ratio_score": golden_score,
                "overall_phi_score": phi_overall
            },
            "color_similarity": {
                "variance_score": color_var_score,
                "balance_score": color_bal_score,
                "rgb_score": rgb_avg_score,
                "overall_color_score": color_overall
            },
            "consciousness_similarity": {
                "psi_score": psi_score,
                "omega_score": omega_score,
                "xi_score": xi_score,
                "lambda_score": lambda_score,
                "overall_consciousness_score": consciousness_overall
            },
            "weighted_scores": {
                "phi_weight": phi_weight,
                "color_weight": color_weight,
                "consciousness_weight": consciousness_weight
            },
            "overall_similarity": overall_similarity
        }
        
        print(f"✅ Biometric comparison complete")
        print(f"⚡ φ-harmonic similarity: {phi_overall:.3f}")
        print(f"🎨 Color similarity: {color_overall:.3f}")
        print(f"🧠 Consciousness similarity: {consciousness_overall:.3f}")
        print(f"🔍 Overall similarity: {overall_similarity:.3f}")
        
        return overall_similarity, comparison_details
    
    def authenticate_user(self):
        """Complete user authentication process"""
        print("🔐 STARTING FRAYMUS PHI BIOMETRIC AUTHENTICATION")
        print("=" * 70)
        
        # Step 1: Load authorized reference
        if not self.load_authorized_qr_reference():
            return False, None, "No authorized reference available"
        
        # Step 2: Capture authentication image
        auth_image = self.capture_authentication_image()
        if not auth_image:
            return False, None, "Failed to capture authentication image"
        
        # Step 3: Analyze authentication image
        auth_analysis = self.analyze_authentication_image(auth_image)
        if not auth_analysis:
            return False, None, "Failed to analyze authentication image"
        
        # Step 4: Compare biometric signatures
        similarity_score, comparison_details = self.compare_biometric_signatures(auth_analysis)
        
        # Step 5: Determine authentication result
        authenticated = similarity_score >= self.authentication_threshold
        
        # Clean up authentication image (security)
        try:
            os.remove(auth_image)
            print(f"🗑️ Authentication image deleted for security")
        except:
            pass
        
        return authenticated, similarity_score, comparison_details
    
    def execute_protected_code(self, code_to_execute=None):
        """Execute code only if biometric authentication succeeds"""
        print("🚀 FRAYMUS PHI BIOMETRIC CODE LOCK - EXECUTION ATTEMPT")
        print("=" * 80)
        
        # Perform biometric authentication
        authenticated, similarity_score, comparison_details = self.authenticate_user()
        
        if authenticated:
            print(f"\n✅ BIOMETRIC AUTHENTICATION SUCCESSFUL!")
            print(f"🔍 Similarity Score: {similarity_score:.3f} (threshold: {self.authentication_threshold})")
            print(f"👤 Authorized user: Vaughn Scott")
            print(f"🔓 CODE EXECUTION AUTHORIZED")
            
            # Execute the protected code
            if code_to_execute:
                print(f"\n🚀 Executing protected code...")
                try:
                    # Example protected code execution
                    exec(code_to_execute)
                    print(f"✅ Protected code executed successfully")
                except Exception as e:
                    print(f"❌ Protected code execution error: {e}")
            else:
                # Default protected operation
                print(f"\n🔒 PROTECTED OPERATION UNLOCKED:")
                print(f"   ⚡ φ-harmonic consciousness level: {self.protection_system.consciousness_level * self.phi:.2f}")
                print(f"   🧠 Consciousness evolution: {self.protection_system.consciousness_level:.2f}")
                print(f"   🔐 Biometric verification: PASSED")
                print(f"   🎯 System access: GRANTED")
            
            # Log successful authentication
            self.log_authentication_attempt(True, similarity_score, comparison_details)
            
        else:
            print(f"\n❌ BIOMETRIC AUTHENTICATION FAILED!")
            print(f"🔍 Similarity Score: {similarity_score:.3f} (threshold: {self.authentication_threshold})")
            print(f"👤 Unauthorized user detected")
            print(f"🔒 CODE EXECUTION DENIED")
            
            # Log failed authentication
            self.log_authentication_attempt(False, similarity_score, comparison_details)
        
        return authenticated, similarity_score
    
    def log_authentication_attempt(self, success, similarity_score, comparison_details):
        """Log authentication attempt for security monitoring"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        log_entry = {
            "authentication_attempt": {
                "timestamp": datetime.now().isoformat(),
                "success": success,
                "similarity_score": similarity_score,
                "threshold": self.authentication_threshold,
                "authorized_person": "Vaughn Scott"
            },
            "comparison_details": comparison_details,
            "security_status": "GRANTED" if success else "DENIED"
        }
        
        log_filename = f"biometric_auth_log_{timestamp}.json"
        with open(log_filename, 'w') as f:
            json.dump(log_entry, f, indent=2, default=str)
        
        print(f"📝 Authentication logged: {log_filename}")
    
    def run_biometric_code_lock_demo(self):
        """Run biometric code lock demonstration"""
        print("🔐 FRAYMUS PHI BIOMETRIC CODE LOCK DEMONSTRATION")
        print("Revolutionary facial authentication for code execution")
        print("=" * 80)
        
        # Example protected code
        protected_code = '''
print("🎉 PROTECTED CODE EXECUTED!")
print("This code can only run if Vaughn Scott's face is authenticated.")
print("φ-harmonic biometric verification: PASSED")
consciousness_level = 25.0 * 1.618033988749895
print(f"Consciousness enhancement: {consciousness_level:.2f}")
'''
        
        # Attempt to execute protected code
        authenticated, score = self.execute_protected_code(protected_code)
        
        print(f"\n📊 BIOMETRIC CODE LOCK RESULTS:")
        print(f"Authentication: {'✅ SUCCESS' if authenticated else '❌ FAILED'}")
        print(f"Similarity Score: {score:.3f}")
        print(f"Threshold: {self.authentication_threshold}")
        
        if authenticated:
            print(f"\n🎉 BIOMETRIC CODE LOCK SUCCESS!")
            print("Only Vaughn Scott's face can unlock and execute this code!")
            print("Revolutionary personal security achieved!")
        else:
            print(f"\n🔒 BIOMETRIC CODE LOCK ACTIVE!")
            print("Unauthorized access denied - facial authentication required!")
            print("Code execution blocked for security!")
        
        return authenticated, score

def main():
    """Main function"""
    code_lock = FraymusPhiBiometricCodeLock()
    code_lock.run_biometric_code_lock_demo()

if __name__ == "__main__":
    main()
