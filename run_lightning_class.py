#!/usr/bin/env python3
"""
Lightning Network Bootcamp - Main Class Runner
==============================================

This script runs the complete Lightning Network educational bootcamp.
It covers all key Lightning concepts through interactive demonstrations:

Day 1: Payment Channels & HTLCs
Day 2: Routing, Topology & Economics

Prerequisites:
- Polar Lightning Network running
- Python virtual environment with requests
- LND nodes accessible via REST API

Usage:
    python run_lightning_class.py
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 CHECKING PREREQUISITES")
    print("=" * 30)
    
    # Check Python environment
    python_exe = "bitcoin_class_env/bin/python"
    if os.path.exists(python_exe):
        print("✅ Python virtual environment found")
    else:
        print("❌ Python virtual environment not found")
        print("💡 Run: python3 -m venv bitcoin_class_env")
        print("💡 Then: source bitcoin_class_env/bin/activate && pip install requests")
        return False
    
    # Check requests module
    try:
        result = subprocess.run([python_exe, "-c", "import requests"], 
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            print("✅ Requests module available")
        else:
            print("❌ Requests module not found")
            print("💡 Run: pip install requests")
            return False
    except:
        print("❌ Could not check requests module")
        return False
    
    # Check if Lightning scripts exist
    lightning_scripts = [
        "lightning_scripts/1_payment_channels.py",
        "lightning_scripts/2_htlcs.py", 
        "lightning_scripts/3_routing_and_pathfinding.py",
        "lightning_scripts/4_network_topology.py",
        "lightning_scripts/5_lightning_economics.py"
    ]
    
    missing_scripts = []
    for script in lightning_scripts:
        if os.path.exists(script):
            print(f"✅ {script}")
        else:
            print(f"❌ {script}")
            missing_scripts.append(script)
    
    if missing_scripts:
        print(f"\n❌ Missing {len(missing_scripts)} Lightning scripts")
        return False
    
    print("\n🎯 All prerequisites met!")
    return True

def check_polar_connection():
    """Check if Polar Lightning Network is accessible"""
    print("\n🌩️ CHECKING POLAR CONNECTION")
    print("=" * 35)
    
    python_exe = "bitcoin_class_env/bin/python"
    test_code = """
import requests
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

try:
    # Test connection to Alice node
    response = requests.get('https://localhost:10001/v1/getinfo', 
                          headers={'Grpc-Metadata-macaroon': ''},
                          verify=False, timeout=5)
    print("Polar connection test:", response.status_code)
except Exception as e:
    print("Polar connection failed:", str(e))
"""
    
    try:
        result = subprocess.run([python_exe, "-c", test_code], 
                              capture_output=True, timeout=10, text=True)
        
        if "200" in result.stdout:
            print("✅ Polar Lightning Network is accessible")
            return True
        else:
            print("❌ Polar Lightning Network not accessible")
            print("💡 Make sure Polar is running with Lightning nodes")
            print("💡 Default ports: Alice(10001), Bob(10002), Charlie(10003)")
            return False
    except:
        print("❌ Could not test Polar connection")
        print("💡 Make sure Polar Lightning Network is running")
        return False

def run_lightning_script(script_name, script_path):
    """Run a Lightning Network script"""
    print(f"\n🚀 RUNNING: {script_name}")
    print("=" * (len(script_name) + 12))
    
    python_exe = "bitcoin_class_env/bin/python"
    
    try:
        # Run the script
        process = subprocess.Popen(
            [python_exe, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Print output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        # Get any remaining output
        stdout, stderr = process.communicate()
        if stdout:
            print(stdout)
        if stderr and process.returncode != 0:
            print(f"❌ Error in {script_name}:")
            print(stderr)
            return False
        
        return_code = process.returncode
        if return_code == 0:
            print(f"✅ {script_name} completed successfully!")
            return True
        else:
            print(f"❌ {script_name} failed with code {return_code}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {script_name} timed out")
        process.kill()
        return False
    except KeyboardInterrupt:
        print(f"\n⏹️ {script_name} interrupted by user")
        process.terminate()
        return False
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def run_day_1():
    """Run Day 1: Payment Channels & HTLCs"""
    print("\n" + "="*60)
    print("📅 DAY 1: PAYMENT CHANNELS & HTLCs")
    print("="*60)
    print("Today we'll learn the fundamentals of Lightning Network:")
    print("• How payment channels work")
    print("• Hash Time-Locked Contracts (HTLCs)")
    print("• The building blocks of Lightning payments")
    
    day_1_scripts = [
        ("Payment Channels", "lightning_scripts/1_payment_channels.py"),
        ("HTLCs (Hash Time-Locked Contracts)", "lightning_scripts/2_htlcs.py")
    ]
    
    for script_name, script_path in day_1_scripts:
        if not run_lightning_script(script_name, script_path):
            print(f"\n❌ Day 1 stopped due to error in {script_name}")
            return False
        
        # Pause between scripts
        print(f"\n⏸️ {script_name} complete!")
        if not os.environ.get("BITCOIN_TEST_MODE") == "1":
            input("Press Enter to continue to next topic...")
    
    print("\n🎉 DAY 1 COMPLETE!")
    print("You've learned the foundations of Lightning Network!")
    return True

def run_day_2():
    """Run Day 2: Routing, Topology & Economics"""
    print("\n" + "="*60)
    print("📅 DAY 2: ROUTING, TOPOLOGY & ECONOMICS")
    print("="*60)
    print("Today we'll explore the network aspects:")
    print("• How payments route through the network")
    print("• Network topology and channel management")
    print("• Economics and business models")
    
    day_2_scripts = [
        ("Routing and Pathfinding", "lightning_scripts/3_routing_and_pathfinding.py"),
        ("Network Topology", "lightning_scripts/4_network_topology.py"),
        ("Lightning Economics", "lightning_scripts/5_lightning_economics.py")
    ]
    
    for script_name, script_path in day_2_scripts:
        if not run_lightning_script(script_name, script_path):
            print(f"\n❌ Day 2 stopped due to error in {script_name}")
            return False
        
        # Pause between scripts
        print(f"\n⏸️ {script_name} complete!")
        if not os.environ.get("BITCOIN_TEST_MODE") == "1":
            input("Press Enter to continue to next topic...")
    
    print("\n🎉 DAY 2 COMPLETE!")
    print("You've mastered Lightning Network concepts!")
    return True

def run_full_bootcamp():
    """Run the complete Lightning Network bootcamp"""
    print("\n" + "="*60)
    print("⚡ COMPLETE LIGHTNING NETWORK BOOTCAMP")
    print("="*60)
    print("Running all Lightning concepts in sequence...")
    
    all_scripts = [
        ("Payment Channels", "lightning_scripts/1_payment_channels.py"),
        ("HTLCs (Hash Time-Locked Contracts)", "lightning_scripts/2_htlcs.py"),
        ("Routing and Pathfinding", "lightning_scripts/3_routing_and_pathfinding.py"),
        ("Network Topology", "lightning_scripts/4_network_topology.py"),
        ("Lightning Economics", "lightning_scripts/5_lightning_economics.py")
    ]
    
    completed = 0
    for script_name, script_path in all_scripts:
        if run_lightning_script(script_name, script_path):
            completed += 1
        else:
            print(f"\n❌ Bootcamp stopped due to error in {script_name}")
            break
        
        # Brief pause between scripts
        print(f"\n⏸️ {script_name} complete! ({completed}/{len(all_scripts)})")
        if not os.environ.get("BITCOIN_TEST_MODE") == "1":
            input("Press Enter to continue...")
    
    if completed == len(all_scripts):
        print("\n🏆 BOOTCAMP COMPLETE!")
        print("Congratulations! You've mastered Lightning Network!")
        return True
    else:
        print(f"\n⚠️ Bootcamp incomplete: {completed}/{len(all_scripts)} topics covered")
        return False

def print_welcome():
    """Print welcome message"""
    print("⚡" * 60)
    print("⚡" + " " * 58 + "⚡")
    print("⚡" + "    LIGHTNING NETWORK EDUCATIONAL BOOTCAMP".center(58) + "⚡")
    print("⚡" + " " * 58 + "⚡")
    print("⚡" + "        Learn the Future of Bitcoin Payments".center(58) + "⚡")
    print("⚡" + " " * 58 + "⚡")
    print("⚡" * 60)
    
    print(f"\n📚 WHAT YOU'LL LEARN:")
    print(f"🔗 Payment Channels - The foundation of Lightning")
    print(f"🔐 HTLCs - Hash Time-Locked Contracts")
    print(f"🗺️ Routing - How payments find their way")
    print(f"🕸️ Network Topology - Structure and management")
    print(f"💰 Economics - Business models and incentives")

def main():
    """Main function"""
    print_welcome()
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please fix the issues above.")
        sys.exit(1)
    
    # Check Polar connection
    if not check_polar_connection():
        print("\n⚠️ Polar connection issues detected.")
        print("The class can still run with simulated examples.")
        if not os.environ.get("BITCOIN_TEST_MODE") == "1":
            continue_choice = input("Continue anyway? (y/n): ").lower().strip()
            if continue_choice != 'y':
                print("👋 Setup Polar and try again!")
                sys.exit(1)
    
    # Choose what to run
    if os.environ.get("BITCOIN_TEST_MODE") == "1":
        print("🧪 Test mode: Running full bootcamp...")
        success = run_full_bootcamp()
    else:
        print(f"\n🎯 CHOOSE YOUR LEARNING PATH:")
        print(f"1. Day 1 only (Payment Channels & HTLCs)")
        print(f"2. Day 2 only (Routing, Topology & Economics)")
        print(f"3. Full bootcamp (All topics)")
        print(f"4. Exit")
        
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                success = run_day_1()
            elif choice == "2":
                success = run_day_2()
            elif choice == "3":
                success = run_full_bootcamp()
            elif choice == "4":
                print("👋 Thanks for your interest in Lightning Network!")
                sys.exit(0)
            else:
                print("❌ Invalid choice")
                sys.exit(1)
        except KeyboardInterrupt:
            print("\n👋 Lightning bootcamp interrupted")
            sys.exit(0)
    
    # Final message
    if success:
        print(f"\n🎊 CONGRATULATIONS!")
        print(f"You've completed the Lightning Network bootcamp!")
        print(f"🚀 You're now ready to build Lightning applications!")
    else:
        print(f"\n📚 Keep learning!")
        print(f"Lightning Network is complex but incredibly powerful!")
    
    print(f"\n💡 NEXT STEPS:")
    print(f"🔨 Build your own Lightning application")
    print(f"🌐 Explore the real Lightning Network")
    print(f"📖 Read the Lightning Network white paper")
    print(f"⚡ Run your own Lightning node!")

if __name__ == "__main__":
    main()