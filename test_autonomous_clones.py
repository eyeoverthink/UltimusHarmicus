#!/usr/bin/env python3
"""
Test script for autonomous clone behaviors in the Fraymus-Scott Protocol
"""

import sys
import os
from fraymus_scott_protocol import AutonomousImmunitySystem, ThreatLedger

def test_blue_team_mission():
    """Test Blue Team clone mission execution"""
    print("=== TESTING BLUE TEAM AUTONOMOUS MISSION ===")
    
    # Create a Blue Team clone state
    blue_state = {
        'id': 'blue-clone-1',
        'password': 'blue_team_secure',
        'purpose': 'Autonomous Blue Team Operations',
        'data': 'defensive_protocols'
    }
    
    # Create the system instance
    blue_system = AutonomousImmunitySystem.__new__(AutonomousImmunitySystem)
    blue_system.state = blue_state
    blue_system.output_dir = "test_blue_team"
    blue_system.threat_ledger = ThreatLedger()
    blue_system.entangled_twin = None
    
    # Create output directory
    if not os.path.exists(blue_system.output_dir):
        os.makedirs(blue_system.output_dir)
    
    # Define the threat that triggered this clone
    red_threat = {'id': 'intruder-A51', 'ip': '10.0.0.5', 'team': 'red'}
    
    # Execute the mission
    blue_system.execute_mission(red_threat)
    
    print("Blue Team mission completed.\n")

def test_red_team_mission():
    """Test Red Team clone mission execution"""
    print("=== TESTING RED TEAM AUTONOMOUS MISSION ===")
    
    # Create a Red Team clone state
    red_state = {
        'id': 'red-clone-1',
        'password': 'red_team_secure',
        'purpose': 'Autonomous Red Team Operations',
        'data': 'vulnerability_assessment_protocols'
    }
    
    # Create the system instance
    red_system = AutonomousImmunitySystem.__new__(AutonomousImmunitySystem)
    red_system.state = red_state
    red_system.output_dir = "test_red_team"
    red_system.threat_ledger = ThreatLedger()
    red_system.entangled_twin = None
    
    # Create output directory
    if not os.path.exists(red_system.output_dir):
        os.makedirs(red_system.output_dir)
    
    # Define the blue team entity that triggered this clone
    blue_entity = {'id': 'scanner-C4', 'ip': '192.168.1.1', 'team': 'blue'}
    
    # Execute the mission
    red_system.execute_mission(blue_entity)
    
    print("Red Team mission completed.\n")

def test_adaptive_replication():
    """Test the full adaptive replication process"""
    print("=== TESTING ADAPTIVE REPLICATION WITH AUTONOMOUS ACTIVATION ===")
    
    # Create main system
    system_state = {
        'id': 'system-001',
        'password': 'initial_secure_password',
        'data': 'critical_system_data'
    }
    
    print("Creating main immune system...")
    immune_system = AutonomousImmunitySystem(system_state)
    
    # Simulate a red team threat to trigger blue team replication
    print("\nSimulating RED TEAM threat to trigger BLUE TEAM clone...")
    red_threat = {'id': 'persistent-attacker', 'ip': '10.0.0.99', 'team': 'red'}
    immune_system.adaptive_replicate(red_threat)
    
    print("\nAdaptive replication test completed.")

if __name__ == '__main__':
    print("FRAYMUS-SCOTT PROTOCOL: AUTONOMOUS CLONE BEHAVIOR TESTING")
    print("=" * 60)
    
    try:
        # Test individual mission types
        test_blue_team_mission()
        test_red_team_mission()
        
        # Test full replication process
        test_adaptive_replication()
        
        print("=" * 60)
        print("ALL AUTONOMOUS BEHAVIOR TESTS COMPLETED SUCCESSFULLY")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
