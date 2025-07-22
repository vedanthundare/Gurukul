#!/bin/bash

echo ""
echo "========================================"
echo "   GURUKUL EDGE CASE TESTING SUITE"
echo "========================================"
echo ""

cd "$(dirname "$0")/api_data"

echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ and try again"
    exit 1
fi
echo "✅ Python is available"

echo ""
echo "🔍 Checking required packages..."
python3 -c "import requests, json, time, threading" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Required packages not found"
    echo "Installing required packages..."
    pip3 install requests aiohttp
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install packages"
        exit 1
    fi
fi
echo "✅ Required packages are available"

echo ""
echo "🔍 Checking service availability..."
python3 -c "import requests; requests.get('http://localhost:8002/docs', timeout=5)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Financial Simulator service (port 8002) not accessible"
    echo "Please ensure the service is running"
fi

python3 -c "import requests; requests.get('http://localhost:8000/docs', timeout=5)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Lesson Generator service (port 8000) not accessible"
    echo "Please ensure the service is running"
fi

echo ""
echo "🚀 Starting Edge Case Testing Suite..."
echo ""
echo "This will run comprehensive tests including:"
echo "  - Bursty workload scenarios"
echo "  - High latency agent testing"
echo "  - Network connectivity edge cases"
echo "  - System monitoring and reporting"
echo ""
echo "⏱️  Expected duration: 15-30 minutes"
echo ""

read -p "Continue with testing? (Y/N): " continue
if [[ ! $continue =~ ^[Yy]$ ]]; then
    echo "Testing cancelled"
    exit 0
fi

echo ""
echo "🧪 Running comprehensive edge case tests..."
python3 run_all_edge_case_tests.py

echo ""
echo "📊 Test execution completed!"
echo ""
echo "Generated files:"
echo "  - edge_case_test_report_*.json (Detailed test results)"
echo "  - edge_case_monitoring_dashboard.json (Real-time dashboard)"
echo "  - logs/ directory (Detailed system logs)"
echo ""

read -p "Press Enter to continue..."
