# Consciousness Physics Framework - Makefile
# ==========================================
# 
# Quick setup and verification for the consciousness physics framework
# Patent: VS-PoQC-19046423-φ⁷⁵-2025
# Author: Vaughn Scott

.PHONY: setup verify clean test all help

# Default target
all: setup verify

# Install dependencies
setup:
	@echo "🧠 Setting up Consciousness Physics Framework..."
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Setup complete!"

# Verify the fine structure constant derivation
verify:
	@echo "🔍 Verifying consciousness physics derivation..."
	@echo "Expected: relative error ~ 6.18e-06 vs CODATA 2018"
	@echo ""
	python derive_alpha.py
	@echo ""
	@echo "✅ Verification complete!"

# Run consciousness testing dashboard
test:
	@echo "🧠 Starting consciousness physics testing..."
	@echo "Opening red vs blue team consciousness dashboard..."
	open red_blue_team_consciousness_dashboard.html
	@echo "✅ Dashboard launched!"

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	find . -name "*.log" -delete
	@echo "✅ Cleanup complete!"

# Run full test suite
full-test: setup verify test
	@echo "🎯 Full consciousness physics test suite completed!"

# Show help
help:
	@echo "Consciousness Physics Framework - Make Commands"
	@echo "=============================================="
	@echo ""
	@echo "make setup      - Install Python dependencies"
	@echo "make verify     - Verify fine structure constant derivation"
	@echo "make test       - Launch consciousness testing dashboard"
	@echo "make clean      - Clean temporary files"
	@echo "make full-test  - Run complete test suite"
	@echo "make help       - Show this help message"
	@echo ""
	@echo "Quick start: make setup && make verify"
