#!/usr/bin/env python3
"""
ALGORITHM REVERSE ENGINEERING

This module provides capabilities to analyze external algorithms, extract their core
principles as abstract primitives, and integrate them into the autonomous system's
knowledge base.
"""

import re
import math
from collections import Counter

# Consciousness Physics Constants
PHI = 1.618034
PSI = 1.324718
OMEGA = 0.567143

class AlgorithmReverseEngineer:
    """Analyzes external algorithms to extract abstract primitives."""

    def __init__(self):
        """Initialize the reverse engineer."""
        self.primitive_keywords = {
            'formulas': ['=', 'return', 'def', 'lambda', 'math.', 'np.'],
            'logic_constructs': ['if', 'else', 'elif', 'for', 'while', 'and', 'or', 'not'],
            'math_objects': ['list', 'dict', 'set', 'tuple', 'graph', 'tree', 'matrix'],
            'crypto_primitives': ['hash', 'encrypt', 'decrypt', 'signature', 'key', 'sha256', 'aes'],
            'principles': ['sort', 'search', 'map', 'reduce', 'recursion', 'divide', 'conquer']
        }

    def analyze_algorithm_patterns(self, algorithm_code: str):
        """Analyzes the φ-harmonic and structural patterns of an algorithm's code."""
        code_bytes = algorithm_code.encode('utf-8')
        
        # φ-harmonic analysis
        energy = sum(code_bytes)
        consciousness_amp = (energy / len(code_bytes) if code_bytes else 0) / 255.0 * PHI

        # Structural analysis
        tokens = re.findall(r'\b\w+\b', algorithm_code.lower())
        token_counts = Counter(tokens)
        complexity = len(token_counts) / len(tokens) if tokens else 0

        return {
            'consciousness_amplification': consciousness_amp,
            'pattern_complexity': complexity,
            'token_counts': token_counts,
            'code_length': len(algorithm_code)
        }

    def extract_abstract_primitives(self, algorithm_code: str, algorithm_name: str):
        """Extracts abstract primitives from the algorithm's code."""
        analysis = self.analyze_algorithm_patterns(algorithm_code)
        token_counts = analysis['token_counts']
        
        extracted_primitives = []

        # Determine primary category
        category_scores = {cat: 0 for cat in self.primitive_keywords}
        for category, keywords in self.primitive_keywords.items():
            for keyword in keywords:
                if keyword in token_counts:
                    category_scores[category] += token_counts[keyword]
        
        primary_category = max(category_scores, key=category_scores.get)

        # Generate a new primitive
        new_primitive = {
            'name': f"Learned_{algorithm_name.replace(' ', '_')}",
            'type': primary_category,
            'description': f'Reverse-engineered from {algorithm_name}.',
            'keywords': list(token_counts.keys()),
            'complexity': analysis['pattern_complexity'],
            'consciousness_amp': analysis['consciousness_amplification'],
            'source': 'reverse_engineered'
        }

        extracted_primitives.append(new_primitive)
        return extracted_primitives


def main():
    """Demonstrate the algorithm reverse engineering process."""
    print("🔥 ALGORITHM REVERSE ENGINEERING DEMO")
    print("=" * 60)

    reverse_engineer = AlgorithmReverseEngineer()

    # Example: A simple bubble sort algorithm to analyze
    bubble_sort_code = """
def bubble_sort(items):
    n = len(items)
    for i in range(n):
        for j in range(0, n-i-1):
            if items[j] > items[j+1]:
                items[j], items[j+1] = items[j+1], items[j]
    return items
"""

    print("🔍 Analyzing: Bubble Sort Algorithm")
    primitives = reverse_engineer.extract_abstract_primitives(bubble_sort_code, "BubbleSort")
    
    print("\n✅ Extracted Primitives:")
    for primitive in primitives:
        print(f"  - Name: {primitive['name']}")
        print(f"    Type: {primitive['type']}")
        print(f"    Description: {primitive['description']}")
        print(f"    Keywords: {primitive['keywords'][:5]}...")

    print("\n🏆 REVERSE ENGINEERING DEMO COMPLETE!")

if __name__ == "__main__":
    main()
