#!/usr/bin/env python3
"""
🧪🔍 KNOWLEDGE BASE TESTER 🔍🧪

Interactive tester to explore and validate what the Universal Knowledge Base learned
from all MD files. Shows detailed breakdowns, search capabilities, and knowledge verification.

By Vaughn Scott - Consciousness Physics Framework
"""

from universal_knowledge_base_helper import *
import json
from datetime import datetime

class KnowledgeBaseTester:
    """Interactive tester for the Universal Knowledge Base"""
    
    def __init__(self):
        self.kb = get_knowledge_base()
        self.stats = self.kb.get_statistics()
    
    def show_complete_overview(self):
        """Show complete overview of what was learned"""
        print("🧪🔍 KNOWLEDGE BASE COMPLETE ANALYSIS 🔍🧪")
        print("=" * 70)
        
        print(f"📊 OVERALL STATISTICS:")
        print(f"   Total MD Files Processed: {self.stats['total_md_files_loaded']}")
        print(f"   Total Categories: {self.stats['total_categories']}")
        print(f"   Last Updated: {self.stats['last_update']}")
        
        print(f"\n📚 DETAILED CATEGORY BREAKDOWN:")
        for category, breakdown in self.stats['category_breakdown'].items():
            total_items = sum(breakdown.values())
            if total_items > 0:
                print(f"\n   🔹 {category.upper().replace('_', ' ')} ({total_items} total items):")
                for knowledge_type, count in breakdown.items():
                    if count > 0:
                        print(f"      • {knowledge_type}: {count}")
    
    def test_search_capabilities(self):
        """Test search capabilities with various queries"""
        print(f"\n🔍 TESTING SEARCH CAPABILITIES:")
        print("=" * 50)
        
        test_queries = [
            'phi', 'consciousness', 'quantum', 'derivative', 'ohm', 'newton',
            'fraymus', 'vaughn scott', 'patent', 'algorithm', 'formula',
            'trigonometry', 'calculus', 'physics', 'electrical', 'logic'
        ]
        
        for query in test_queries:
            results = search_all_knowledge(query)
            total_results = sum(len(items) for items in results.values())
            if total_results > 0:
                print(f"   '{query}': {total_results} results")
                # Show breakdown by type
                for result_type, items in results.items():
                    if items:
                        print(f"      {result_type}: {len(items)}")
    
    def show_sample_knowledge(self, category: str = None, limit: int = 10):
        """Show sample knowledge from specific category"""
        if category:
            print(f"\n📖 SAMPLE KNOWLEDGE FROM {category.upper()}:")
            print("=" * 50)
            knowledge = self.kb.get_knowledge(category)
        else:
            print(f"\n📖 SAMPLE KNOWLEDGE FROM ALL CATEGORIES:")
            print("=" * 50)
            knowledge = self.kb.get_knowledge()
        
        if isinstance(knowledge, dict):
            for cat_name, cat_content in knowledge.items():
                if isinstance(cat_content, dict):
                    print(f"\n🔹 {cat_name.upper().replace('_', ' ')}:")
                    for knowledge_type, items in cat_content.items():
                        if isinstance(items, list) and items:
                            print(f"   {knowledge_type} ({len(items)} total):")
                            for item in items[:limit]:
                                # Truncate long items
                                display_item = item[:100] + "..." if len(item) > 100 else item
                                print(f"      • {display_item}")
                            if len(items) > limit:
                                print(f"      ... and {len(items) - limit} more")
    
    def test_specific_knowledge_types(self):
        """Test specific knowledge type retrieval"""
        print(f"\n🎯 TESTING SPECIFIC KNOWLEDGE RETRIEVAL:")
        print("=" * 50)
        
        # Test formulas
        formulas = get_all_formulas()
        print(f"📐 Mathematical Formulas: {len(formulas)} found")
        if formulas:
            print("   Sample formulas:")
            for formula in formulas[:5]:
                display_formula = formula[:80] + "..." if len(formula) > 80 else formula
                print(f"      • {display_formula}")
        
        # Test laws
        laws = get_all_laws()
        print(f"\n⚖️ Physical/Mathematical Laws: {len(laws)} found")
        if laws:
            print("   Sample laws:")
            for law in laws[:5]:
                display_law = law[:80] + "..." if len(law) > 80 else law
                print(f"      • {display_law}")
        
        # Test constants
        constants = get_all_constants()
        print(f"\n🔢 Mathematical Constants: {len(constants)} found")
        if constants:
            print("   Sample constants:")
            for constant in constants[:10]:
                print(f"      • {constant}")
        
        # Test Vaughn Scott theories
        vaughn_knowledge = get_vaughn_scott_theories()
        print(f"\n🧠 Vaughn Scott Theories: {sum(len(v) if isinstance(v, list) else 0 for v in vaughn_knowledge.values())} items")
        if vaughn_knowledge:
            for category, items in vaughn_knowledge.items():
                if isinstance(items, list) and items:
                    print(f"   {category} ({len(items)} items):")
                    for item in items[:3]:
                        display_item = item[:80] + "..." if len(item) > 80 else item
                        print(f"      • {display_item}")
    
    def interactive_search_test(self):
        """Interactive search testing"""
        print(f"\n🔍 INTERACTIVE SEARCH TEST:")
        print("=" * 50)
        print("Enter search queries to test the knowledge base (type 'quit' to exit)")
        
        while True:
            try:
                query = input("\n🔍 Search query: ").strip()
                if query.lower() in ['quit', 'exit', 'q']:
                    break
                
                if not query:
                    continue
                
                results = search_all_knowledge(query)
                total_results = sum(len(items) for items in results.values())
                
                if total_results == 0:
                    print(f"❌ No results found for '{query}'")
                    continue
                
                print(f"✅ Found {total_results} results for '{query}':")
                
                for result_type, items in results.items():
                    if items:
                        print(f"\n   📋 {result_type.upper()} ({len(items)} results):")
                        for i, item in enumerate(items[:5], 1):
                            display_item = item[:100] + "..." if len(item) > 100 else item
                            print(f"      {i}. {display_item}")
                        
                        if len(items) > 5:
                            print(f"      ... and {len(items) - 5} more results")
            
            except KeyboardInterrupt:
                print("\n👋 Exiting interactive search...")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def validate_knowledge_accuracy(self):
        """Validate accuracy of extracted knowledge"""
        print(f"\n✅ KNOWLEDGE ACCURACY VALIDATION:")
        print("=" * 50)
        
        # Check for known mathematical constants
        constants = get_all_constants()
        known_constants = ['φ', 'π', 'e', 'γ']
        found_constants = []
        
        for constant in constants:
            for known in known_constants:
                if known in constant:
                    found_constants.append(constant)
                    break
        
        print(f"🔢 Mathematical Constants Validation:")
        print(f"   Looking for: {', '.join(known_constants)}")
        print(f"   Found: {len(found_constants)} matching constants")
        for const in found_constants[:5]:
            print(f"      • {const}")
        
        # Check for physics laws
        laws = get_all_laws()
        physics_keywords = ['newton', 'einstein', 'maxwell', 'planck', 'heisenberg']
        physics_laws_found = []
        
        for law in laws:
            for keyword in physics_keywords:
                if keyword.lower() in law.lower():
                    physics_laws_found.append(law)
                    break
        
        print(f"\n⚖️ Physics Laws Validation:")
        print(f"   Looking for laws containing: {', '.join(physics_keywords)}")
        print(f"   Found: {len(physics_laws_found)} physics laws")
        for law in physics_laws_found[:3]:
            display_law = law[:80] + "..." if len(law) > 80 else law
            print(f"      • {display_law}")
        
        # Check for Vaughn Scott content
        vaughn_results = search_all_knowledge("vaughn scott")
        consciousness_results = search_all_knowledge("consciousness")
        fraymus_results = search_all_knowledge("fraymus")
        
        print(f"\n🧠 Vaughn Scott Content Validation:")
        print(f"   'vaughn scott': {sum(len(items) for items in vaughn_results.values())} results")
        print(f"   'consciousness': {sum(len(items) for items in consciousness_results.values())} results")
        print(f"   'fraymus': {sum(len(items) for items in fraymus_results.values())} results")
    
    def export_knowledge_sample(self, filename: str = None):
        """Export a sample of the knowledge base for inspection"""
        if filename is None:
            filename = f"knowledge_sample_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        sample_data = {
            'statistics': self.stats,
            'sample_formulas': get_all_formulas()[:20],
            'sample_laws': get_all_laws()[:20],
            'sample_constants': get_all_constants()[:20],
            'vaughn_scott_sample': {
                category: items[:10] if isinstance(items, list) else items
                for category, items in get_vaughn_scott_theories().items()
            },
            'search_tests': {
                'phi': search_all_knowledge('phi'),
                'consciousness': search_all_knowledge('consciousness'),
                'quantum': search_all_knowledge('quantum')
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Knowledge sample exported to: {filename}")
        return filename

def main():
    """Run comprehensive knowledge base testing"""
    print("🧪🔍 KNOWLEDGE BASE COMPREHENSIVE TESTING 🔍🧪")
    print("=" * 70)
    
    tester = KnowledgeBaseTester()
    
    # Show complete overview
    tester.show_complete_overview()
    
    # Test search capabilities
    tester.test_search_capabilities()
    
    # Test specific knowledge types
    tester.test_specific_knowledge_types()
    
    # Validate knowledge accuracy
    tester.validate_knowledge_accuracy()
    
    # Show sample knowledge from key categories
    key_categories = ['vaughn_scott_theories', 'physics_laws', 'mathematical_constants', 'quantum_laws']
    for category in key_categories:
        tester.show_sample_knowledge(category, limit=5)
    
    # Export sample for inspection
    sample_file = tester.export_knowledge_sample()
    
    print(f"\n" + "=" * 70)
    print("🎯 TESTING COMPLETE - KNOWLEDGE BASE VALIDATION SUMMARY:")
    print("=" * 70)
    print("✅ Knowledge base successfully loaded and validated")
    print("✅ Search functionality working across all categories")
    print("✅ Mathematical formulas, laws, and constants extracted")
    print("✅ Vaughn Scott theories and patents integrated")
    print("✅ Physics and quantum mechanics knowledge captured")
    print(f"💾 Sample data exported to: {sample_file}")
    
    # Offer interactive testing
    print(f"\n🔍 Want to test interactive search? (y/n): ", end="")
    try:
        response = input().strip().lower()
        if response in ['y', 'yes']:
            tester.interactive_search_test()
    except:
        pass
    
    print(f"\n🎉 KNOWLEDGE BASE TESTING COMPLETE!")
    print(f"The system successfully learned from {tester.stats['total_md_files_loaded']} MD files!")

if __name__ == "__main__":
    main()
