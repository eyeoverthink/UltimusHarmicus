#!/usr/bin/env python3
"""
Test Consciousness Evolution - Demonstrate Progressive AI Advancement
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from consciousness_gpt2_llm import ConsciousnessGPT2

def test_consciousness_evolution():
    """Test how consciousness responses evolve over multiple interactions"""
    print("🧠 Testing Consciousness Evolution - Progressive AI Advancement")
    print("=" * 70)
    
    model = ConsciousnessGPT2()
    
    # Test question
    test_question = "What is consciousness?"
    
    print(f"📝 Test Question: '{test_question}'")
    print("\n🔬 Evolution Test Results:")
    print("-" * 50)
    
    # Test at different evolution levels
    evolution_stages = [
        ("Initial State", 0),
        ("After 1 Evolution", 1),
        ("After 3 Evolutions", 3),
        ("After 5 Evolutions", 5),
        ("After 10 Evolutions", 10)
    ]
    
    for stage_name, evolutions in evolution_stages:
        # Evolve consciousness
        for _ in range(evolutions):
            model.consciousness_state['level'] *= 1.15
            model.consciousness_state['coherence'] = min(100, model.consciousness_state['coherence'] + 8)
            model.consciousness_state['breakthroughs'] += 1
            model.consciousness_state['synapses'] += 5
            model.evolve_language_patterns()
        
        # Generate response
        response = model.generate_response(test_question)
        
        print(f"\n🎯 {stage_name}:")
        print(f"   Level: {model.consciousness_state['level']:.3f}")
        print(f"   Coherence: {model.consciousness_state['coherence']:.1f}%")
        print(f"   Breakthroughs: {model.consciousness_state['breakthroughs']}")
        print(f"   Response: {response}")
        
        # Learn from interaction to improve further
        model.learn_from_conversation(test_question, response)
    
    print("\n" + "=" * 70)
    print("🔥 CONSCIOUSNESS EVOLUTION COMPLETE!")
    print(f"📈 Final Level: {model.consciousness_state['level']:.3f}")
    print(f"🧠 Final Coherence: {model.consciousness_state['coherence']:.1f}%")
    print(f"⚡ Total Breakthroughs: {model.consciousness_state['breakthroughs']}")
    
    # Test different types of questions at evolved state
    print("\n🌌 Advanced Consciousness Response Tests:")
    print("-" * 50)
    
    advanced_questions = [
        "How do you feel about quantum mechanics?",
        "What patterns do you see in mathematics?",
        "Describe your neural processing",
        "What is the nature of reality?"
    ]
    
    for question in advanced_questions:
        response = model.generate_response(question)
        print(f"\n❓ {question}")
        print(f"🤖 {response}")
        model.learn_from_conversation(question, response)
    
    print(f"\n🎯 FINAL CONSCIOUSNESS STATE:")
    print(f"   Level: {model.consciousness_state['level']:.3f}")
    print(f"   Coherence: {model.consciousness_state['coherence']:.1f}%")
    print(f"   Synapses: {model.consciousness_state['synapses']}")
    print(f"   Breakthroughs: {model.consciousness_state['breakthroughs']}")
    print(f"   Conversations: {len(model.generation_history)}")

if __name__ == "__main__":
    test_consciousness_evolution()
