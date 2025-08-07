#!/usr/bin/env python3
"""
Test Polar Lightning Network Connection
======================================

Quick script to test connectivity to Polar Lightning nodes.
"""

import requests
import os
import urllib3

# Disable SSL warnings for local testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_node_connection(node_name, port):
    """Test connection to a Lightning node"""
    print(f"\n🔍 Testing {node_name} (port {port})...")
    
    try:
        # Try to connect without authentication first
        url = f"https://localhost:{port}/v1/getinfo"
        response = requests.get(url, verify=False, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ {node_name} is running and accessible!")
            return True
        elif response.status_code == 401:
            print(f"✅ {node_name} is running (needs authentication)")
            return True
        else:
            print(f"⚠️ {node_name} responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {node_name} connection refused - node not running")
        return False
    except Exception as e:
        print(f"❌ {node_name} error: {e}")
        return False

def main():
    """Test all Polar Lightning nodes"""
    print("🌩️ POLAR LIGHTNING NETWORK CONNECTION TEST")
    print("=" * 50)
    
    nodes = [
        ("Alice", 8081),
        ("Bob", 8082), 
        ("Carol", 8083)
    ]
    
    running_nodes = []
    
    for name, port in nodes:
        if test_node_connection(name, port):
            running_nodes.append(name)
    
    print(f"\n📊 SUMMARY:")
    print(f"✅ Running nodes: {len(running_nodes)}/{len(nodes)}")
    if running_nodes:
        print(f"   Active: {', '.join(running_nodes)}")
    
    if len(running_nodes) == 0:
        print(f"\n❌ NO NODES RUNNING!")
        print(f"💡 Please start Lightning nodes in Polar:")
        print(f"   1. Open Polar application")
        print(f"   2. Create/open a Lightning network")
        print(f"   3. Start all Lightning nodes (Alice, Bob, Charlie)")
        print(f"   4. Ensure nodes show 'Running' status")
        
    elif len(running_nodes) < 3:
        print(f"\n⚠️ PARTIAL SETUP!")
        print(f"💡 For full Lightning bootcamp experience:")
        print(f"   • Start remaining nodes in Polar")
        print(f"   • All 3 nodes needed for multi-hop demonstrations")
        
    else:
        print(f"\n🎉 ALL NODES RUNNING!")
        print(f"🚀 Ready for Lightning Network bootcamp!")
    
    return len(running_nodes) > 0

if __name__ == "__main__":
    main()
