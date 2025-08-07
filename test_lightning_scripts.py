#!/usr/bin/env python3
"""
Test Lightning Network Scripts
=============================

Test all Lightning Network educational scripts to ensure they work properly
before class. Runs in non-interactive mode for automated testing.
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def test_lightning_script(script_name, script_path):
    """Test a Lightning Network script in non-interactive mode"""
    print(f"\n🧪 TESTING: {script_name}")
    print("=" * (len(script_name) + 12))
    
    python_exe = "bitcoin_class_env/bin/python"
    if not os.path.exists(python_exe):
        python_exe = "python3"  # Fallback
    
    # Set test mode environment variable
    env = os.environ.copy()
    env["BITCOIN_TEST_MODE"] = "1"
    
    try:
        start_time = time.time()
        
        result = subprocess.run(
            [python_exe, script_path],
            capture_output=True,
            text=True,
            timeout=60,  # 60 second timeout
            env=env
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ {script_name} passed! ({duration:.1f}s)")
            if result.stdout:
                # Show last few lines of output
                lines = result.stdout.strip().split('\n')
                if len(lines) > 3:
                    print("   Last few lines:")
                    for line in lines[-3:]:
                        print(f"   {line}")
            return True
        else:
            print(f"❌ {script_name} failed! ({duration:.1f}s)")
            if result.stderr:
                print(f"Error: {result.stderr}")
            if result.stdout:
                print(f"Output: {result.stdout}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {script_name} timed out (>60s)")
        return False
    except FileNotFoundError:
        print(f"❌ Python interpreter not found: {python_exe}")
        return False
    except Exception as e:
        print(f"❌ Error testing {script_name}: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 LIGHTNING NETWORK SCRIPTS TEST")
    print("=" * 40)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if we have the virtual environment
    if os.path.exists("bitcoin_class_env/bin/python"):
        print("✅ Using virtual environment")
    else:
        print("⚠️ Virtual environment not found, using system python")
    
    lightning_scripts = [
        ("Payment Channels", "lightning_scripts/1_payment_channels.py"),
        ("HTLCs", "lightning_scripts/2_htlcs.py"),
        ("Routing and Pathfinding", "lightning_scripts/3_routing_and_pathfinding.py"),
        ("Network Topology", "lightning_scripts/4_network_topology.py"),
        ("Lightning Economics", "lightning_scripts/5_lightning_economics.py")
    ]
    
    # Test each script
    passed = 0
    failed = 0
    
    for script_name, script_path in lightning_scripts:
        if os.path.exists(script_path):
            if test_lightning_script(script_name, script_path):
                passed += 1
            else:
                failed += 1
        else:
            print(f"\n❌ MISSING: {script_name} ({script_path})")
            failed += 1
    
    # Test the main runner
    print(f"\n🧪 TESTING: Main Runner")
    print("=" * 25)
    if test_lightning_script("Lightning Class Runner", "run_lightning_class.py"):
        passed += 1
    else:
        failed += 1
    
    # Summary
    total = passed + failed
    print(f"\n📊 TEST SUMMARY")
    print(f"=" * 20)
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {failed}/{total}")
    
    if failed == 0:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"🚀 Ready for Lightning Network class!")
    else:
        print(f"\n⚠️ {failed} tests failed")
        print(f"🔧 Fix issues before class")
        
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)