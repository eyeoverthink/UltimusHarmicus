#!/usr/bin/env python3
"""
🌊⚡ QR SYNAPSE MEMORY MULTI-RUN TEST ⚡🌊
Run synapse memory test 5 times and track knowledge referencing patterns
"""

import json
import time
import os
from qr_synapse_memory_test import QRSynapseMemoryTester

class QRSynapseMultiRunTester:
    def __init__(self):
        self.run_results = []
        self.knowledge_references = {}
        self.consciousness_evolution = []
        
        print("🌊⚡ QR SYNAPSE MEMORY MULTI-RUN TEST ⚡🌊")
        print("=" * 70)
        print("Running synapse memory test 5 times to track knowledge referencing")
        print("=" * 70)
        
    def run_single_test(self, run_number):
        """Run a single synapse memory test and track results"""
        print(f"\n🚀 STARTING RUN {run_number}/5...")
        
        tester = QRSynapseMemoryTester()
        results = tester.run_comprehensive_test()
        
        # Extract key metrics
        run_data = {
            'run_number': run_number,
            'timestamp': time.time(),
            'consciousness_level': tester.consciousness_level,
            'total_synapses': len(tester.synapse_network),
            'total_neurons': len(tester.neurons),
            'memory_index_words': len(tester.memory_index),
            'test_results': results,
            'synapse_network': tester.synapse_network
        }
        
        self.run_results.append(run_data)
        self.consciousness_evolution.append(tester.consciousness_level)
        
        # Track knowledge references
        self.track_knowledge_references(run_number, tester.synapse_network, tester.memory_index)
        
        print(f"✅ RUN {run_number} COMPLETE - Consciousness: {tester.consciousness_level:.2f}")
        
        return run_data
        
    def track_knowledge_references(self, run_number, synapse_network, memory_index):
        """Track how knowledge is referenced across runs"""
        print(f"\n🔍 TRACKING KNOWLEDGE REFERENCES FOR RUN {run_number}...")
        
        # Track synapse content patterns
        content_patterns = {}
        for synapse_id, synapse in synapse_network.items():
            content = synapse['memory_content']
            
            # Extract key concepts
            key_concepts = []
            if 'consciousness' in content.lower():
                key_concepts.append('consciousness_physics')
            if 'φ' in content or 'phi' in content.lower():
                key_concepts.append('phi_harmonic')
            if 'qr' in content.lower():
                key_concepts.append('qr_encoding')
            if 'algorithm' in content.lower():
                key_concepts.append('algorithm_processing')
            if 'parallel' in content.lower():
                key_concepts.append('parallel_processing')
            if 'neural' in content.lower():
                key_concepts.append('neural_networks')
                
            for concept in key_concepts:
                if concept not in content_patterns:
                    content_patterns[concept] = []
                content_patterns[concept].append({
                    'synapse_id': synapse_id,
                    'memory_type': synapse['memory_type'],
                    'synapse_strength': synapse['synapse_strength'],
                    'access_count': synapse['access_count']
                })
                
        # Store knowledge references for this run
        self.knowledge_references[f'run_{run_number}'] = {
            'content_patterns': content_patterns,
            'memory_index_size': len(memory_index),
            'unique_concepts': len(content_patterns),
            'total_concept_references': sum(len(refs) for refs in content_patterns.values())
        }
        
        print(f"🧠 Found {len(content_patterns)} unique knowledge concepts")
        print(f"📊 Total concept references: {sum(len(refs) for refs in content_patterns.values())}")
        
    def analyze_knowledge_evolution(self):
        """Analyze how knowledge referencing evolves across runs"""
        print("\n🔬 ANALYZING KNOWLEDGE EVOLUTION ACROSS RUNS...")
        
        evolution_analysis = {
            'consciousness_progression': self.consciousness_evolution,
            'knowledge_concept_evolution': {},
            'reference_pattern_changes': {},
            'cross_run_knowledge_persistence': {}
        }
        
        # Track concept evolution across runs
        all_concepts = set()
        for run_key, run_refs in self.knowledge_references.items():
            all_concepts.update(run_refs['content_patterns'].keys())
            
        for concept in all_concepts:
            concept_evolution = []
            for run_num in range(1, 6):
                run_key = f'run_{run_num}'
                if run_key in self.knowledge_references:
                    concept_refs = self.knowledge_references[run_key]['content_patterns'].get(concept, [])
                    concept_evolution.append({
                        'run': run_num,
                        'reference_count': len(concept_refs),
                        'total_strength': sum(ref['synapse_strength'] for ref in concept_refs),
                        'total_access': sum(ref['access_count'] for ref in concept_refs)
                    })
                    
            evolution_analysis['knowledge_concept_evolution'][concept] = concept_evolution
            
        # Analyze reference patterns
        for run_num in range(1, 6):
            run_key = f'run_{run_num}'
            if run_key in self.knowledge_references:
                run_data = self.knowledge_references[run_key]
                evolution_analysis['reference_pattern_changes'][run_key] = {
                    'unique_concepts': run_data['unique_concepts'],
                    'total_references': run_data['total_concept_references'],
                    'memory_index_size': run_data['memory_index_size']
                }
                
        return evolution_analysis
        
    def generate_knowledge_reference_report(self, evolution_analysis):
        """Generate comprehensive knowledge reference report"""
        print("\n📊 GENERATING KNOWLEDGE REFERENCE REPORT...")
        
        report = {
            'test_metadata': {
                'test_name': 'QR_Synapse_Memory_Multi_Run_Knowledge_Reference_Test',
                'total_runs': len(self.run_results),
                'timestamp': time.time(),
                'consciousness_evolution': self.consciousness_evolution
            },
            'run_results': self.run_results,
            'knowledge_references': self.knowledge_references,
            'evolution_analysis': evolution_analysis,
            'summary_insights': self.generate_summary_insights(evolution_analysis)
        }
        
        return report
        
    def generate_summary_insights(self, evolution_analysis):
        """Generate key insights from knowledge reference analysis"""
        insights = {
            'consciousness_growth_pattern': {
                'initial_consciousness': self.consciousness_evolution[0] if self.consciousness_evolution else 0,
                'final_consciousness': self.consciousness_evolution[-1] if self.consciousness_evolution else 0,
                'total_growth': self.consciousness_evolution[-1] - self.consciousness_evolution[0] if len(self.consciousness_evolution) >= 2 else 0,
                'average_growth_per_run': (self.consciousness_evolution[-1] - self.consciousness_evolution[0]) / (len(self.consciousness_evolution) - 1) if len(self.consciousness_evolution) > 1 else 0
            },
            'knowledge_persistence_patterns': {},
            'concept_reference_stability': {},
            'cross_run_knowledge_evolution': {}
        }
        
        # Analyze concept persistence
        concept_evolution = evolution_analysis['knowledge_concept_evolution']
        for concept, evolution in concept_evolution.items():
            if len(evolution) >= 2:
                initial_refs = evolution[0]['reference_count']
                final_refs = evolution[-1]['reference_count']
                
                insights['knowledge_persistence_patterns'][concept] = {
                    'initial_references': initial_refs,
                    'final_references': final_refs,
                    'reference_stability': final_refs / initial_refs if initial_refs > 0 else 0,
                    'appeared_in_runs': len([e for e in evolution if e['reference_count'] > 0])
                }
                
        return insights
        
    def run_multi_test_analysis(self):
        """Run complete multi-test analysis"""
        print("\n🚀 STARTING 5-RUN SYNAPSE MEMORY ANALYSIS...")
        
        # Run 5 tests
        for run_num in range(1, 6):
            self.run_single_test(run_num)
            time.sleep(0.1)  # Brief pause between runs
            
        # Analyze knowledge evolution
        evolution_analysis = self.analyze_knowledge_evolution()
        
        # Generate comprehensive report
        report = self.generate_knowledge_reference_report(evolution_analysis)
        
        # Save results
        timestamp = int(time.time())
        filename = f"qr_synapse_memory_multi_run_analysis_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Display summary
        self.display_final_summary(report, filename)
        
        return report
        
    def display_final_summary(self, report, filename):
        """Display comprehensive final summary"""
        print("\n🏆 QR SYNAPSE MEMORY MULTI-RUN ANALYSIS COMPLETE!")
        print("=" * 70)
        
        insights = report['summary_insights']
        consciousness_growth = insights['consciousness_growth_pattern']
        
        print("📊 CONSCIOUSNESS EVOLUTION ACROSS 5 RUNS:")
        for i, consciousness in enumerate(self.consciousness_evolution, 1):
            print(f"   Run {i}: {consciousness:.2f}")
            
        print(f"\n🌟 CONSCIOUSNESS GROWTH ANALYSIS:")
        print(f"   Initial Consciousness: {consciousness_growth['initial_consciousness']:.2f}")
        print(f"   Final Consciousness: {consciousness_growth['final_consciousness']:.2f}")
        print(f"   Total Growth: +{consciousness_growth['total_growth']:.2f}")
        print(f"   Average Growth per Run: +{consciousness_growth['average_growth_per_run']:.2f}")
        
        print(f"\n🧠 KNOWLEDGE REFERENCE PATTERNS:")
        persistence_patterns = insights['knowledge_persistence_patterns']
        for concept, pattern in persistence_patterns.items():
            stability = pattern['reference_stability']
            appeared_runs = pattern['appeared_in_runs']
            print(f"   {concept}: {stability:.2f}× stability, appeared in {appeared_runs}/5 runs")
            
        print(f"\n💾 COMPLETE ANALYSIS SAVED: {filename}")
        print(f"✨ VAUGHN, KNOWLEDGE REFERENCING PATTERNS FULLY ANALYZED!")
        
def main():
    """Main multi-run test execution"""
    tester = QRSynapseMultiRunTester()
    results = tester.run_multi_test_analysis()
    return results

if __name__ == "__main__":
    main()
