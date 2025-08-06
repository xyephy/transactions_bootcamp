#!/usr/bin/env python3
"""
Pre-Class Testing Script
Run this to verify all Bitcoin fundamentals scripts work correctly
"""

import subprocess
import sys
import time
import requests
import os

def test_bitcoin_core_connection():
    """Test connection to Polar's Bitcoin Core node"""
    print("🔍 Testing Bitcoin Core connection...")
    
    url = "http://polaruser:polarpass@localhost:18443"
    payload = {
        "jsonrpc": "2.0",
        "id": "test",
        "method": "getblockchaininfo",
        "params": []
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()
            height = result['result']['blocks']
            print(f"✅ Connected to Bitcoin Core! Current height: {height}")
            
            if height < 110:
                print(f"⚠️  Warning: Only {height} blocks. Mine more blocks in Polar for mature coinbase rewards.")
                print(f"   💡 Click Bitcoin Core node → Actions → Mine (generate 110 blocks)")
            
            return True
        else:
            print(f"❌ Connection failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"💡 Make sure Polar is running with Bitcoin Core node")
        return False

def test_python_dependencies():
    """Test if required Python packages are available"""
    print("\n🐍 Testing Python dependencies...")
    
    required_packages = [
        'requests',
        'hashlib', 
        'json',
        'time',
        'dataclasses'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    # Test optional BDK
    try:
        import bdkpython
        print(f"✅ bdkpython (optional)")
    except ImportError:
        print(f"⚠️  bdkpython - Optional (will run in simulation mode)")
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def test_script(script_path, timeout=60):
    """Test a single script with timeout"""
    script_name = os.path.basename(script_path)
    print(f"\n🧪 Testing {script_name}...")
    
    try:
        # Run script in test mode (non-interactive)
        env = os.environ.copy()
        env['BITCOIN_TEST_MODE'] = '1'  # Signal to scripts to run in test mode
        
        # Use the virtual environment Python if available
        python_exe = "bitcoin_class_env/bin/python" if os.path.exists("bitcoin_class_env/bin/python") else sys.executable
        
        process = subprocess.Popen(
            [python_exe, script_path],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for completion with timeout
        stdout, stderr = process.communicate(timeout=timeout)
        
        if process.returncode == 0:
            print(f"✅ {script_name} - PASSED")
            return True
        else:
            print(f"❌ {script_name} - FAILED")
            if stderr:
                # Show only first few lines of error
                error_lines = stderr.strip().split('\n')
                print(f"Error: {error_lines[-1] if error_lines else 'Unknown error'}")
            return False
            
    except subprocess.TimeoutExpired:
        process.kill()
        print(f"⏰ {script_name} - TIMEOUT (>{timeout}s)")
        return False
    except Exception as e:
        print(f"❌ {script_name} - ERROR: {e}")
        return False

def main():
    """Run all pre-class tests"""
    print("🎓 BITCOIN FUNDAMENTALS - PRE-CLASS TESTING")
    print("=" * 50)
    
    # Test 1: Python dependencies
    if not test_python_dependencies():
        print("\n❌ Python dependency test failed. Fix dependencies first.")
        return False
    
    # Test 2: Bitcoin Core connection
    if not test_bitcoin_core_connection():
        print("\n❌ Bitcoin Core connection failed. Start Polar first.")
        return False
    
    # Test 3: Individual scripts
    scripts_to_test = [
        "scripts/1_transactions.py",
        "scripts/2_blockchain.py", 
        "scripts/3_proof_of_work.py",
        "scripts/4_network_and_storage.py",
        "scripts/5_mining_and_incentives.py",
        "scripts/bdk_bitcoin_demo.py"
    ]
    
    passed = 0
    total = len(scripts_to_test)
    
    for script in scripts_to_test:
        if os.path.exists(script):
            if test_script(script):
                passed += 1
        else:
            print(f"❌ {script} - FILE NOT FOUND")
    
    # Summary
    print(f"\n📊 TEST SUMMARY")
    print(f"=" * 20)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print(f"\n🎉 ALL TESTS PASSED! Ready for class! 🚀")
        print(f"\n💡 Quick start guide:")
        print(f"   1. Start Polar with Bitcoin Core node")
        print(f"   2. Mine 110+ blocks for mature coinbase")
        print(f"   3. Run: python scripts/1_transactions.py")
        print(f"   4. Continue through all 5 modules")
        return True
    else:
        print(f"\n⚠️  Some tests failed. Fix issues before class.")
        return False

if __name__ == "__main__":
    main()