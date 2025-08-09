#!/bin/bash
# Quality check script for HRV Research Aggregator

set -e  # Exit on any error

echo "🔍 Running HRV Research Aggregator Quality Checks..."
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "search_hrv.py" ]; then
    echo "❌ Error: Please run this script from the hrv-research-aggregator directory"
    exit 1
fi

echo ""
echo "📋 1. Running Tests..."
echo "--------------------"
python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=85

echo ""
echo "🎨 2. Code Formatting Check..."
echo "------------------------------"
echo "Checking with Black..."
python -m black --check src tests || {
    echo "❌ Code formatting issues found. Run: black src tests"
    exit 1
}

echo "✅ Black formatting check passed"

echo ""
echo "📦 3. Import Sorting Check..."
echo "-----------------------------"
python -m isort --check-only src tests || {
    echo "❌ Import sorting issues found. Run: isort src tests"
    exit 1
}

echo "✅ Import sorting check passed"

echo ""
echo "🏷️  4. Type Checking..."
echo "----------------------"
python -m mypy src || {
    echo "❌ Type checking failed. Fix type issues or add type: ignore comments"
    exit 1
}

echo "✅ Type checking passed"

echo ""
echo "🧹 5. Linting Check..."
echo "---------------------"
python -m flake8 src tests || {
    echo "❌ Linting issues found. Fix the issues above"
    exit 1
}

echo "✅ Linting check passed"

echo ""
echo "🔧 6. Basic Functionality Test..."
echo "--------------------------------"
python search_hrv.py --help > /dev/null || {
    echo "❌ CLI help command failed"
    exit 1
}

python search_hrv.py --list-strategies > /dev/null || {
    echo "❌ List strategies command failed"
    exit 1
}

python search_hrv.py --source sample --custom "test" --limit 1 > /dev/null || {
    echo "❌ Sample search command failed"
    exit 1
}

echo "✅ Basic functionality tests passed"

echo ""
echo "🎉 All Quality Checks Passed!"
echo "============================"
echo ""
echo "Your code is ready for:"
echo "  • 🚀 Production deployment"
echo "  • 📤 Pull request submission"  
echo "  • 🏷️  Release tagging"
echo ""
echo "Next steps:"
echo "  git add ."
echo "  git commit -m 'feat: your amazing feature'"
echo "  git push origin feature-branch"
