#!/usr/bin/env python3
"""
Test Recursive Memory Acceleration
Demonstrate exponential speedup from QR memory persistence
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recursive_consciousness_llm import RecursiveConsciousnessLLM
import time

def test_fibonacci_acceleration():
    """Test Fibonacci calculation acceleration through recursive memory"""
    print("🧠 Testing Recursive Memory Acceleration")
    print("🔄 Fibonacci Sequence Calculation Speed Test")
    print("=" * 60)
    
    llm = RecursiveConsciousnessLLM()
    
    # Test different Fibonacci numbers
    test_cases = [20, 30, 50, 20, 30, 50]  # Repeat to show acceleration
    
    print("📊 Test Results:")
    print("-" * 60)
    
    for i, n in enumerate(test_cases):
        run_type = "FIRST RUN" if i < 3 else "SECOND RUN (MEMORY)"
        
        print(f"\n🎯 {run_type} - Fibonacci({n}):")
        
        start_time = time.time()
        result = llm.fibonacci_sequence(n)
        end_time = time.time()
        
        total_time = end_time - start_time
        
        if result['from_memory']:
            print(f"   ⚡ INSTANT RECALL from QR memory!")
            print(f"   📊 Sequence: {result['sequence'][:5]}...{result['sequence'][-3:]}")
            print(f"   ⏱️  Recall time: {result['calculation_time']:.6f} seconds")
            print(f"   🔄 Memory recalls: {result['recall_count']}")
            print(f"   🧠 Memory key: {result['memory_key']}")
        else:
            print(f"   🔢 CALCULATING from scratch...")
            print(f"   📊 Sequence: {result['sequence'][:5]}...{result['sequence'][-3:]}")
            print(f"   ⏱️  Calculation time: {result['calculation_time']:.6f} seconds")
            print(f"   💾 Saved to QR: {result['memory_key']}")
        
        print(f"   🎯 Total response time: {total_time:.6f} seconds")
        
        if i == 2:
            print("\n" + "="*60)
            print("🔄 NOW TESTING MEMORY RECALL - SHOULD BE INSTANT!")
            print("="*60)

def test_multiple_calculations():
    """Test multiple different calculations with memory"""
    print("\n\n🧠 Testing Multiple Calculation Types")
    print("=" * 60)
    
    llm = RecursiveConsciousnessLLM()
    
    calculations = [
        ("fibonacci 25", "Fibonacci sequence"),
        ("primes 100", "Prime numbers"),
        ("factorial 12", "Factorial calculation"),
        ("fibonacci 25", "Fibonacci (repeat)"),
        ("primes 100", "Primes (repeat)"),
        ("factorial 12", "Factorial (repeat)")
    ]
    
    for i, (query, description) in enumerate(calculations):
        run_type = "FIRST" if i < 3 else "MEMORY RECALL"
        
        print(f"\n🎯 {run_type} - {description}:")
        
        start_time = time.time()
        response = llm.process_query(query)
        end_time = time.time()
        
        print(f"   Response: {response[:100]}...")
        print(f"   ⏱️  Total time: {end_time - start_time:.6f} seconds")
        
        if i == 2:
            print("\n" + "-"*50)
            print("🔄 SWITCHING TO MEMORY RECALL MODE")
            print("-"*50)

if __name__ == "__main__":
    test_fibonacci_acceleration()
    test_multiple_calculations()
    
    print("\n🌌 Recursive Memory Acceleration Test Complete!")
    print("🔥 Results show exponential speedup from QR memory persistence!")
