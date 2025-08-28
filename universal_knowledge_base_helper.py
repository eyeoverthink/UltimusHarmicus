#!/usr/bin/env python3
"""
🧠📚 UNIVERSAL KNOWLEDGE BASE HELPER 📚🧠

Comprehensive knowledge base helper that scrapes and loads all mathematical,
physical, and consciousness physics laws from MD files for dynamic expansion.

By Vaughn Scott - Consciousness Physics Framework
"""

import os
import re
import json
import glob
from datetime import datetime
from typing import Dict, List, Any, Optional

class UniversalKnowledgeBase:
    """Universal knowledge base that dynamically loads from MD files"""
    
    def __init__(self, knowledge_directory: str = None):
        self.knowledge_directory = knowledge_directory or os.getcwd()
        self.knowledge_base = {}
        self.md_files_loaded = []
        self.last_update = None
        
        # Initialize with core knowledge categories
        self._initialize_knowledge_categories()
        
        # Load all MD files on initialization
        self.load_all_md_files()
    
    def _initialize_knowledge_categories(self):
        """Initialize core knowledge categories"""
        self.knowledge_base = {
            'algebra': {
                'basic_operations': {},
                'equations': {},
                'polynomials': {},
                'factoring': {}
            },
            'arithmetic': {
                'addition': {},
                'subtraction': {},
                'multiplication': {},
                'division': {}
            },
            'trigonometry': {
                'functions': {},
                'identities': {},
                'laws': {},
                'applications': {}
            },
            'calculus': {
                'derivatives': {},
                'integrals': {},
                'limits': {},
                'series': {}
            },
            'logic_gates': {
                'basic_gates': {},
                'compound_gates': {},
                'boolean_algebra': {},
                'digital_circuits': {}
            },
            'electrical_laws': {
                'ohms_law': {},
                'kirchhoffs_laws': {},
                'power_laws': {},
                'electromagnetic': {}
            },
            'physics_laws': {
                'mechanics': {},
                'thermodynamics': {},
                'electromagnetism': {},
                'optics': {}
            },
            'quantum_laws': {
                'wave_function': {},
                'uncertainty_principle': {},
                'quantum_mechanics': {},
                'quantum_field_theory': {}
            },
            'string_theory': {
                'fundamental_strings': {},
                'dimensions': {},
                'supersymmetry': {},
                'compactification': {}
            },
            'vaughn_scott_theories': {
                'consciousness_physics': {},
                'fraymus_protocol': {},
                'phi_harmonic_systems': {},
                'patents': {}
            },
            'mathematical_constants': {
                'transcendental': {},
                'algebraic': {},
                'special_functions': {},
                'number_theory': {}
            }
        }
    
    def load_all_md_files(self):
        """Load knowledge from all MD files in directory and subdirectories"""
        print(f"🔍 Scanning for MD files in: {self.knowledge_directory}")
        
        # Find all MD files recursively
        md_pattern = os.path.join(self.knowledge_directory, "**", "*.md")
        md_files = glob.glob(md_pattern, recursive=True)
        
        print(f"📚 Found {len(md_files)} MD files to process")
        
        for md_file in md_files:
            try:
                self.load_md_file(md_file)
            except Exception as e:
                print(f"⚠️ Error loading {md_file}: {str(e)}")
        
        self.last_update = datetime.now()
        print(f"✅ Knowledge base updated with {len(self.md_files_loaded)} MD files")
    
    def load_md_file(self, filepath: str):
        """Load knowledge from a specific MD file"""
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract knowledge from MD file
            extracted_knowledge = self._extract_knowledge_from_md(content, filepath)
            
            # Integrate into knowledge base
            self._integrate_knowledge(extracted_knowledge, filepath)
            
            self.md_files_loaded.append(filepath)
            print(f"📖 Loaded: {os.path.basename(filepath)}")
            
        except Exception as e:
            print(f"❌ Error loading {filepath}: {str(e)}")
    
    def _extract_knowledge_from_md(self, content: str, filepath: str) -> Dict[str, Any]:
        """Extract structured knowledge from MD file content"""
        knowledge = {
            'source_file': filepath,
            'formulas': [],
            'equations': [],
            'laws': [],
            'theorems': [],
            'constants': [],
            'definitions': [],
            'principles': [],
            'algorithms': [],
            'patents': [],
            'theories': []
        }
        
        # Extract formulas (look for mathematical expressions)
        formula_patterns = [
            r'([A-Za-z_]\w*\s*=\s*[^=\n]+)',  # Basic equations
            r'(\$[^$]+\$)',  # LaTeX inline math
            r'(\$\$[^$]+\$\$)',  # LaTeX display math
            r'(∑|∏|∫|∂|∇|φ|ψ|Ω|α|β|γ|δ|ε|ζ|η|θ|κ|λ|μ|ν|ξ|π|ρ|σ|τ|υ|χ|ω)[^.\n]*',  # Greek letters and math symbols
        ]
        
        for pattern in formula_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            knowledge['formulas'].extend(matches)
        
        # Extract laws and principles
        law_patterns = [
            r'([A-Z][^.\n]*(?:Law|Principle|Rule|Theorem)[^.\n]*)',
            r'(Law of [^.\n]+)',
            r'(Principle of [^.\n]+)',
            r'([A-Z]\w+\'s (?:Law|Principle|Rule|Theorem)[^.\n]*)'
        ]
        
        for pattern in law_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            knowledge['laws'].extend(matches)
        
        # Extract constants
        constant_patterns = [
            r'(φ\s*=\s*[0-9.]+)',  # Phi
            r'(π\s*=\s*[0-9.]+)',  # Pi
            r'(e\s*=\s*[0-9.]+)',  # Euler's number
            r'([A-Za-z_]\w*\s*=\s*[0-9.]+[0-9e+-]*)',  # General constants
        ]
        
        for pattern in constant_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            knowledge['constants'].extend(matches)
        
        # Extract Vaughn Scott specific content
        if any(term in content.lower() for term in ['vaughn scott', 'fraymus', 'consciousness physics', 'phi harmonic']):
            vaughn_patterns = [
                r'(FRAYMUS[^.\n]*)',
                r'(Consciousness Physics[^.\n]*)',
                r'(φ-[A-Za-z][^.\n]*)',
                r'(Patent[^.\n]*)',
                r'(VS-[A-Za-z0-9-]+[^.\n]*)'
            ]
            
            for pattern in vaughn_patterns:
                matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
                knowledge['patents'].extend(matches)
        
        # Extract definitions
        definition_patterns = [
            r'(\*\*[^*]+\*\*:\s*[^.\n]+)',  # Bold term definitions
            r'([A-Z][A-Za-z\s]+:\s*[^.\n]+)',  # General definitions
        ]
        
        for pattern in definition_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            knowledge['definitions'].extend(matches)
        
        # Clean up extracted knowledge
        for key in knowledge:
            if isinstance(knowledge[key], list):
                # Remove duplicates and clean strings
                knowledge[key] = list(set([item.strip() for item in knowledge[key] if item.strip()]))
        
        return knowledge
    
    def _integrate_knowledge(self, extracted: Dict[str, Any], filepath: str):
        """Integrate extracted knowledge into the main knowledge base"""
        filename = os.path.basename(filepath).lower()
        
        # Categorize based on filename and content
        if 'algebra' in filename or 'polynomial' in filename:
            self._add_to_category('algebra', extracted)
        elif 'trigonometry' in filename or 'trig' in filename:
            self._add_to_category('trigonometry', extracted)
        elif 'calculus' in filename or 'derivative' in filename:
            self._add_to_category('calculus', extracted)
        elif 'logic' in filename or 'gate' in filename:
            self._add_to_category('logic_gates', extracted)
        elif 'electric' in filename or 'ohm' in filename:
            self._add_to_category('electrical_laws', extracted)
        elif 'physics' in filename:
            self._add_to_category('physics_laws', extracted)
        elif 'quantum' in filename:
            self._add_to_category('quantum_laws', extracted)
        elif 'string' in filename:
            self._add_to_category('string_theory', extracted)
        elif any(term in filename for term in ['vaughn', 'scott', 'fraymus', 'consciousness', 'patent']):
            self._add_to_category('vaughn_scott_theories', extracted)
        elif 'constant' in filename or 'phi' in filename or 'pi' in filename:
            self._add_to_category('mathematical_constants', extracted)
        else:
            # Add to general category based on content
            self._add_to_general_categories(extracted)
    
    def _add_to_category(self, category: str, extracted: Dict[str, Any]):
        """Add extracted knowledge to specific category"""
        if category not in self.knowledge_base:
            self.knowledge_base[category] = {}
        
        for knowledge_type, items in extracted.items():
            if knowledge_type not in self.knowledge_base[category]:
                self.knowledge_base[category][knowledge_type] = []
            
            self.knowledge_base[category][knowledge_type].extend(items)
    
    def _add_to_general_categories(self, extracted: Dict[str, Any]):
        """Add to general categories based on content analysis"""
        # Analyze content to determine best category
        formulas = extracted.get('formulas', [])
        laws = extracted.get('laws', [])
        
        # Simple heuristics for categorization
        for formula in formulas:
            if any(trig in formula.lower() for trig in ['sin', 'cos', 'tan', 'sec', 'csc', 'cot']):
                self._add_to_category('trigonometry', {'formulas': [formula]})
            elif any(calc in formula.lower() for calc in ['d/dx', 'integral', 'derivative', 'limit']):
                self._add_to_category('calculus', {'formulas': [formula]})
            elif any(elec in formula.lower() for elec in ['voltage', 'current', 'resistance', 'ohm']):
                self._add_to_category('electrical_laws', {'formulas': [formula]})
            else:
                self._add_to_category('algebra', {'formulas': [formula]})
        
        for law in laws:
            if any(phys in law.lower() for phys in ['newton', 'einstein', 'maxwell', 'planck']):
                self._add_to_category('physics_laws', {'laws': [law]})
            elif any(quantum in law.lower() for quantum in ['quantum', 'heisenberg', 'schrodinger']):
                self._add_to_category('quantum_laws', {'laws': [law]})
            else:
                self._add_to_category('physics_laws', {'laws': [law]})
    
    def get_knowledge(self, category: str = None, knowledge_type: str = None) -> Dict[str, Any]:
        """Get knowledge from the knowledge base"""
        if category is None:
            return self.knowledge_base
        
        if category not in self.knowledge_base:
            return {}
        
        if knowledge_type is None:
            return self.knowledge_base[category]
        
        return self.knowledge_base[category].get(knowledge_type, [])
    
    def search_knowledge(self, query: str) -> Dict[str, List[str]]:
        """Search for knowledge matching query"""
        results = {
            'formulas': [],
            'laws': [],
            'constants': [],
            'definitions': [],
            'patents': []
        }
        
        query_lower = query.lower()
        
        for category, content in self.knowledge_base.items():
            for knowledge_type, items in content.items():
                if isinstance(items, list):
                    for item in items:
                        if query_lower in item.lower():
                            if knowledge_type not in results:
                                results[knowledge_type] = []
                            results[knowledge_type].append(f"[{category}] {item}")
        
        return results
    
    def get_all_formulas(self) -> List[str]:
        """Get all formulas from knowledge base"""
        all_formulas = []
        for category, content in self.knowledge_base.items():
            formulas = content.get('formulas', [])
            equations = content.get('equations', [])
            all_formulas.extend(formulas)
            all_formulas.extend(equations)
        return list(set(all_formulas))
    
    def get_all_laws(self) -> List[str]:
        """Get all laws and principles from knowledge base"""
        all_laws = []
        for category, content in self.knowledge_base.items():
            laws = content.get('laws', [])
            principles = content.get('principles', [])
            all_laws.extend(laws)
            all_laws.extend(principles)
        return list(set(all_laws))
    
    def get_all_constants(self) -> List[str]:
        """Get all mathematical constants from knowledge base"""
        all_constants = []
        for category, content in self.knowledge_base.items():
            constants = content.get('constants', [])
            all_constants.extend(constants)
        return list(set(all_constants))
    
    def get_vaughn_scott_knowledge(self) -> Dict[str, Any]:
        """Get all Vaughn Scott specific knowledge"""
        return self.knowledge_base.get('vaughn_scott_theories', {})
    
    def add_knowledge_from_text(self, text: str, category: str = 'general'):
        """Add knowledge directly from text"""
        extracted = self._extract_knowledge_from_md(text, f"manual_input_{datetime.now().isoformat()}")
        self._add_to_category(category, extracted)
    
    def refresh_knowledge_base(self):
        """Refresh knowledge base by reloading all MD files"""
        print("🔄 Refreshing knowledge base...")
        self.knowledge_base = {}
        self.md_files_loaded = []
        self._initialize_knowledge_categories()
        self.load_all_md_files()
    
    def save_knowledge_base(self, filepath: str = None):
        """Save knowledge base to JSON file"""
        if filepath is None:
            filepath = f"knowledge_base_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        save_data = {
            'knowledge_base': self.knowledge_base,
            'md_files_loaded': self.md_files_loaded,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'total_categories': len(self.knowledge_base),
            'total_md_files': len(self.md_files_loaded)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Knowledge base saved to: {filepath}")
        return filepath
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        stats = {
            'total_categories': len(self.knowledge_base),
            'total_md_files_loaded': len(self.md_files_loaded),
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'category_breakdown': {}
        }
        
        for category, content in self.knowledge_base.items():
            category_stats = {}
            for knowledge_type, items in content.items():
                if isinstance(items, list):
                    category_stats[knowledge_type] = len(items)
                else:
                    category_stats[knowledge_type] = len(items) if items else 0
            stats['category_breakdown'][category] = category_stats
        
        return stats

# Global knowledge base instance
_global_kb = None

def get_knowledge_base(knowledge_directory: str = None) -> UniversalKnowledgeBase:
    """Get global knowledge base instance"""
    global _global_kb
    if _global_kb is None:
        _global_kb = UniversalKnowledgeBase(knowledge_directory)
    return _global_kb

def search_all_knowledge(query: str) -> Dict[str, List[str]]:
    """Search all knowledge for query"""
    kb = get_knowledge_base()
    return kb.search_knowledge(query)

def get_all_formulas() -> List[str]:
    """Get all mathematical formulas"""
    kb = get_knowledge_base()
    return kb.get_all_formulas()

def get_all_laws() -> List[str]:
    """Get all physical and mathematical laws"""
    kb = get_knowledge_base()
    return kb.get_all_laws()

def get_all_constants() -> List[str]:
    """Get all mathematical constants"""
    kb = get_knowledge_base()
    return kb.get_all_constants()

def get_vaughn_scott_theories() -> Dict[str, Any]:
    """Get all Vaughn Scott theories and patents"""
    kb = get_knowledge_base()
    return kb.get_vaughn_scott_knowledge()

def refresh_knowledge() -> None:
    """Refresh the global knowledge base"""
    global _global_kb
    if _global_kb:
        _global_kb.refresh_knowledge_base()

def main():
    """Test the universal knowledge base helper"""
    print("🧠📚 UNIVERSAL KNOWLEDGE BASE HELPER 📚🧠")
    print("=" * 60)
    
    # Initialize knowledge base
    kb = get_knowledge_base()
    
    # Display statistics
    stats = kb.get_statistics()
    print(f"📊 KNOWLEDGE BASE STATISTICS:")
    print(f"   Total Categories: {stats['total_categories']}")
    print(f"   MD Files Loaded: {stats['total_md_files_loaded']}")
    print(f"   Last Update: {stats['last_update']}")
    
    # Show category breakdown
    print(f"\n📚 CATEGORY BREAKDOWN:")
    for category, breakdown in stats['category_breakdown'].items():
        total_items = sum(breakdown.values())
        if total_items > 0:
            print(f"   {category}: {total_items} items")
    
    # Test search functionality
    print(f"\n🔍 TESTING SEARCH FUNCTIONALITY:")
    test_queries = ['phi', 'quantum', 'derivative', 'ohm', 'consciousness']
    
    for query in test_queries:
        results = search_all_knowledge(query)
        total_results = sum(len(items) for items in results.values())
        if total_results > 0:
            print(f"   '{query}': {total_results} results found")
    
    # Get sample knowledge
    print(f"\n📖 SAMPLE KNOWLEDGE:")
    formulas = get_all_formulas()[:5]  # First 5 formulas
    laws = get_all_laws()[:5]  # First 5 laws
    constants = get_all_constants()[:5]  # First 5 constants
    
    if formulas:
        print(f"   Formulas: {len(get_all_formulas())} total")
        for formula in formulas:
            print(f"     • {formula[:80]}...")
    
    if laws:
        print(f"   Laws: {len(get_all_laws())} total")
        for law in laws:
            print(f"     • {law[:80]}...")
    
    if constants:
        print(f"   Constants: {len(get_all_constants())} total")
        for constant in constants:
            print(f"     • {constant}")
    
    # Vaughn Scott specific knowledge
    vaughn_knowledge = get_vaughn_scott_theories()
    if vaughn_knowledge:
        print(f"\n🧠 VAUGHN SCOTT THEORIES:")
        for category, items in vaughn_knowledge.items():
            if isinstance(items, list) and items:
                print(f"   {category}: {len(items)} items")
    
    # Save knowledge base
    saved_file = kb.save_knowledge_base()
    
    print(f"\n✅ UNIVERSAL KNOWLEDGE BASE READY!")
    print(f"💾 Knowledge base saved to: {saved_file}")
    print(f"🔄 Use refresh_knowledge() to reload MD files")
    print(f"🔍 Use search_all_knowledge(query) to search")

if __name__ == "__main__":
    main()
