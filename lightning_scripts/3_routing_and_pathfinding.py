#!/usr/bin/env python3
"""
Lightning Network: Routing and Pathfinding
==========================================

This script demonstrates Lightning Network routing concepts:
- How payments find paths through the network
- Source routing vs onion routing
- Channel liquidity and routing failures
- Fee calculation and optimization
- Route discovery algorithms

Key Learning Objectives:
- Understand how Lightning routing works
- Learn about onion routing for privacy
- See how liquidity affects routing
- Experience route optimization
"""

import requests
import json
import time
import os
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class Channel:
    """Represents a Lightning Network channel"""
    channel_id: str
    node1: str
    node2: str
    capacity: int
    fee_base_msat: int
    fee_rate_milli_msat: int
    min_htlc: int
    max_htlc: int
    enabled: bool

@dataclass
class Node:
    """Represents a Lightning Network node"""
    pub_key: str
    alias: str
    color: str
    channels: List[str]

@dataclass
class Route:
    """Represents a payment route"""
    hops: List[Dict]
    total_amt: int
    total_fees: int
    total_time_lock: int
    success_prob: float

class LightningRoutingDemo:
    """Lightning Network routing and pathfinding demonstrations"""
    
    def __init__(self):
        # Polar node configurations (same as payment channels)
        self.nodes = {
            "alice": {
                "rpc_host": "localhost",
                "rpc_port": "10001",
                "name": "Alice",
                "pubkey": None
            },
            "bob": {
                "rpc_host": "localhost", 
                "rpc_port": "10002",
                "name": "Bob",
                "pubkey": None
            },
            "charlie": {
                "rpc_host": "localhost",
                "rpc_port": "10003",
                "name": "Charlie", 
                "pubkey": None
            }
        }
        
        self.network_graph = {}  # Store network topology
        self.routes = []  # Store calculated routes
    
    def lnd_request(self, node: str, endpoint: str, data=None, method="GET"):
        """Make REST API request to LND node"""
        base_url = f"https://{self.nodes[node]['rpc_host']}:{self.nodes[node]['rpc_port']}"
        url = f"{base_url}{endpoint}"
        
        try:
            macaroon_path = f"/Users/{os.getenv('USER')}/.polar/networks/1/volumes/lnd/{node}/data/chain/bitcoin/regtest/admin.macaroon"
            with open(macaroon_path, 'rb') as f:
                macaroon = f.read().hex()
        except:
            print(f"❌ Could not read macaroon for {node}")
            return None
            
        headers = {
            'Grpc-Metadata-macaroon': macaroon,
            'Content-Type': 'application/json'
        }
        
        try:
            if method == "POST":
                response = requests.post(url, json=data, headers=headers, verify=False, timeout=10)
            else:
                response = requests.get(url, headers=headers, verify=False, timeout=10)
                
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"❌ Error connecting to {node}: {e}")
            return None
    
    def get_network_info(self, node: str = "alice"):
        """Get Lightning Network graph information"""
        graph = self.lnd_request(node, "/v1/graph")
        if graph:
            self.network_graph = graph
            return graph
        return None
    
    def find_route(self, from_node: str, to_node: str, amount_sats: int):
        """Find a route between two nodes"""
        if not self.nodes[to_node]["pubkey"]:
            info = self.lnd_request(to_node, "/v1/getinfo")
            if info:
                self.nodes[to_node]["pubkey"] = info["identity_pubkey"]
        
        to_pubkey = self.nodes[to_node]["pubkey"]
        if not to_pubkey:
            return None
            
        # Use LND's route finding
        query_params = f"pub_key={to_pubkey}&amt={amount_sats}&num_routes=3"
        routes = self.lnd_request(from_node, f"/v1/graph/routes?{query_params}")
        return routes
    
    def demonstrate_network_topology(self):
        """Show the Lightning Network topology"""
        print("\n🌐 LIGHTNING NETWORK TOPOLOGY")
        print("=" * 45)
        print("Understanding the network structure...")
        
        # Get network graph
        print("\n📡 Fetching network graph...")
        graph = self.get_network_info()
        
        if not graph:
            print("❌ Could not fetch network graph")
            return
        
        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        
        print(f"📊 Network Statistics:")
        print(f"   👥 Nodes: {len(nodes)}")
        print(f"   ⚡ Channels: {len(edges)}")
        
        # Show some example nodes and channels
        print(f"\n🔍 Sample Network Nodes:")
        for i, node in enumerate(nodes[:5]):
            alias = node.get("alias", "Unknown")
            pubkey = node.get("pub_key", "")
            print(f"   {i+1}. {alias} ({pubkey[:20]}...)")
        
        print(f"\n⚡ Sample Channels:")
        for i, edge in enumerate(edges[:5]):
            capacity = int(edge.get("capacity", 0))
            node1 = edge.get("node1_pub", "")[:20]
            node2 = edge.get("node2_pub", "")[:20]
            print(f"   {i+1}. {node1}... ↔ {node2}... ({capacity:,} sats)")
        
        if os.environ.get("BITCOIN_TEST_MODE") != "1":
            input("\nPress Enter to continue...")
    
    def demonstrate_route_finding(self):
        """Demonstrate how routes are found"""
        print("\n🗺️ ROUTE FINDING DEMONSTRATION")
        print("=" * 45)
        print("How does Lightning find payment paths?")
        
        print("\n📚 Route Finding Process:")
        print("1. 🎯 Define source and destination")
        print("2. 🔍 Search for possible paths")
        print("3. 💰 Calculate fees for each path")
        print("4. ⚖️ Optimize for cost vs reliability")
        print("5. 🎭 Use onion routing for privacy")
        
        # Simulate route finding
        print("\n🎯 SCENARIO: Alice wants to pay Charlie 100,000 sats")
        amount = 100000
        
        print("\n🔍 Finding routes...")
        routes = self.find_route("alice", "charlie", amount)
        
        if routes and routes.get("routes"):
            route_list = routes["routes"]
            print(f"✅ Found {len(route_list)} possible routes!")
            
            for i, route in enumerate(route_list[:3], 1):
                hops = route.get("hops", [])
                total_fees = int(route.get("total_fees", 0))
                total_amt = int(route.get("total_amt", 0))
                
                print(f"\n📍 Route {i}:")
                print(f"   💰 Amount: {total_amt:,} sats")
                print(f"   💸 Fees: {total_fees:,} sats ({total_fees/total_amt*100:.3f}%)")
                print(f"   🔗 Hops: {len(hops)}")
                
                for j, hop in enumerate(hops):
                    pub_key = hop.get("pub_key", "")
                    fee = int(hop.get("fee", 0))
                    print(f"      {j+1}. {pub_key[:20]}... (fee: {fee} sats)")
                    
        else:
            print("❌ No routes found!")
            print("💡 This could happen due to:")
            print("   • Insufficient channel liquidity")
            print("   • No connected path")
            print("   • Channels are offline")
            
            # Create a simulated route for educational purposes
            print("\n🎭 Let's simulate a route for learning...")
            self.simulate_route_demo(amount)
    
    def simulate_route_demo(self, amount: int):
        """Simulate a route finding demonstration"""
        print("\n🎭 SIMULATED ROUTE DEMONSTRATION")
        print("=" * 45)
        
        # Create a simulated network topology
        simulated_network = {
            "Alice": {
                "channels": [
                    {"to": "Bob", "capacity": 1000000, "fee_rate": 0.001},
                    {"to": "Dave", "capacity": 500000, "fee_rate": 0.002}
                ]
            },
            "Bob": {
                "channels": [
                    {"to": "Alice", "capacity": 1000000, "fee_rate": 0.001},
                    {"to": "Charlie", "capacity": 800000, "fee_rate": 0.0015},
                    {"to": "Eve", "capacity": 600000, "fee_rate": 0.003}
                ]
            },
            "Charlie": {
                "channels": [
                    {"to": "Bob", "capacity": 800000, "fee_rate": 0.0015},
                    {"to": "Eve", "capacity": 400000, "fee_rate": 0.002}
                ]
            },
            "Dave": {
                "channels": [
                    {"to": "Alice", "capacity": 500000, "fee_rate": 0.002},
                    {"to": "Eve", "capacity": 300000, "fee_rate": 0.0025}
                ]
            },
            "Eve": {
                "channels": [
                    {"to": "Bob", "capacity": 600000, "fee_rate": 0.003},
                    {"to": "Charlie", "capacity": 400000, "fee_rate": 0.002},
                    {"to": "Dave", "capacity": 300000, "fee_rate": 0.0025}
                ]
            }
        }
        
        print("🏗️ Simulated Network:")
        for node, data in simulated_network.items():
            channels = data["channels"]
            print(f"   👤 {node}: {len(channels)} channels")
        
        # Find possible routes from Alice to Eve
        target_amount = amount
        print(f"\n🎯 Finding routes: Alice → Eve ({target_amount:,} sats)")
        
        possible_routes = [
            {
                "path": ["Alice", "Bob", "Eve"],
                "hops": [
                    {"from": "Alice", "to": "Bob", "capacity": 1000000, "fee_rate": 0.001},
                    {"from": "Bob", "to": "Eve", "capacity": 600000, "fee_rate": 0.003}
                ]
            },
            {
                "path": ["Alice", "Bob", "Charlie", "Eve"], 
                "hops": [
                    {"from": "Alice", "to": "Bob", "capacity": 1000000, "fee_rate": 0.001},
                    {"from": "Bob", "to": "Charlie", "capacity": 800000, "fee_rate": 0.0015},
                    {"from": "Charlie", "to": "Eve", "capacity": 400000, "fee_rate": 0.002}
                ]
            },
            {
                "path": ["Alice", "Dave", "Eve"],
                "hops": [
                    {"from": "Alice", "to": "Dave", "capacity": 500000, "fee_rate": 0.002},
                    {"from": "Dave", "to": "Eve", "capacity": 300000, "fee_rate": 0.0025}
                ]
            }
        ]
        
        print("\n📊 Route Analysis:")
        for i, route in enumerate(possible_routes, 1):
            path_str = " → ".join(route["path"])
            total_fees = 0
            feasible = True
            
            # Calculate fees and check capacity
            for hop in route["hops"]:
                if hop["capacity"] < target_amount:
                    feasible = False
                    break
                hop_fee = int(target_amount * hop["fee_rate"])
                total_fees += hop_fee
            
            print(f"\n   Route {i}: {path_str}")
            if feasible:
                print(f"   ✅ Feasible: {total_fees:,} sats fees ({total_fees/target_amount*100:.3f}%)")
                print(f"   🔗 Hops: {len(route['hops'])}")
            else:
                print(f"   ❌ Not feasible: Insufficient capacity")
        
        if os.environ.get("BITCOIN_TEST_MODE") != "1":
            input("\nPress Enter to continue...")
    
    def demonstrate_onion_routing(self):
        """Demonstrate onion routing for privacy"""
        print("\n🧅 ONION ROUTING DEMONSTRATION")
        print("=" * 45)
        print("How Lightning preserves payment privacy...")
        
        print("\n📚 Onion Routing Basics:")
        print("🧅 Like layers of an onion")
        print("🔒 Each node only knows the next hop")
        print("🎭 Sender and receiver are hidden")
        print("🛡️ Prevents payment surveillance")
        
        # Demonstrate onion packet construction
        print("\n🔨 BUILDING AN ONION PACKET")
        route_path = ["Alice", "Bob", "Charlie", "Dave"]
        amount = 50000
        
        print(f"📍 Route: {' → '.join(route_path)}")
        print(f"💰 Amount: {amount:,} sats")
        
        # Simulate onion construction (backwards)
        print(f"\n🏗️ Constructing onion (backwards from destination):")
        
        onion_layers = []
        for i in reversed(range(len(route_path)-1)):
            from_node = route_path[i]
            to_node = route_path[i+1]
            
            if i == len(route_path)-2:  # Last hop
                instruction = f"Deliver {amount} sats to {to_node}"
            else:
                instruction = f"Forward to {to_node}"
            
            layer = {
                "for_node": from_node,
                "instruction": instruction,
                "encrypted": True
            }
            onion_layers.append(layer)
            print(f"   🧅 Layer {len(onion_layers)}: For {from_node} → {instruction}")
        
        # Simulate onion peeling (forwards)
        print(f"\n🔓 Processing onion (forwards through route):")
        
        for i, layer in enumerate(reversed(onion_layers)):
            node = route_path[i]
            print(f"   {i+1}. {node} decrypts layer:")
            print(f"      🔍 Sees: {layer['instruction']}")
            if i < len(route_path) - 2:
                print(f"      ➡️ Forwards onion to next node")
            else:
                print(f"      🎯 Delivers payment to final recipient")
            
            time.sleep(0.5)  # Dramatic effect
        
        print(f"\n💡 PRIVACY PROTECTION:")
        print(f"   🧅 Bob only knows: Alice sent something to Charlie")
        print(f"   🧅 Charlie only knows: Bob sent something to Dave")
        print(f"   🛡️ No one knows the full path except Alice!")
        
        if os.environ.get("BITCOIN_TEST_MODE") != "1":
            input("\nPress Enter to continue...")
    
    def demonstrate_routing_failures(self):
        """Demonstrate routing failures and how they're handled"""
        print("\n❌ ROUTING FAILURES DEMONSTRATION")
        print("=" * 45)
        print("What happens when payments fail?")
        
        failure_scenarios = [
            {
                "name": "Insufficient Liquidity",
                "description": "Channel doesn't have enough balance",
                "error_code": "TEMPORARY_CHANNEL_FAILURE",
                "action": "Try alternative route"
            },
            {
                "name": "Channel Offline",
                "description": "Node is temporarily unavailable",
                "error_code": "UNKNOWN_NEXT_PEER", 
                "action": "Route around offline node"
            },
            {
                "name": "Fee Too Low",
                "description": "Offered fee below minimum",
                "error_code": "FEE_INSUFFICIENT",
                "action": "Increase fees and retry"
            },
            {
                "name": "Payment Timeout",
                "description": "HTLC expired before completion",
                "error_code": "PAYMENT_TIMEOUT",
                "action": "Shorten route or increase timeout"
            }
        ]
        
        print(f"\n🔍 Common Routing Failure Scenarios:")
        
        for i, scenario in enumerate(failure_scenarios, 1):
            print(f"\n{i}️⃣ {scenario['name']}")
            print(f"   📝 {scenario['description']}")
            print(f"   🚨 Error: {scenario['error_code']}")
            print(f"   🔧 Solution: {scenario['action']}")
            
            if os.environ.get("BITCOIN_TEST_MODE") != "1":
                input("   Press Enter for next scenario...")
        
        # Demonstrate adaptive routing
        print(f"\n🧠 ADAPTIVE ROUTING")
        print(f"=" * 25)
        print(f"How Lightning learns from failures:")
        print(f"   📊 Track success rates per channel")
        print(f"   🎯 Penalize unreliable routes") 
        print(f"   🔄 Automatically try alternatives")
        print(f"   📈 Improve over time")
    
    def routing_quiz(self):
        """Interactive quiz about routing concepts"""
        print("\n🧠 LIGHTNING ROUTING QUIZ")
        print("=" * 35)
        
        questions = [
            {
                "question": "Why does Lightning use onion routing?",
                "options": [
                    "A. To make payments faster",
                    "B. To reduce fees",
                    "C. To protect privacy",
                    "D. To increase capacity"
                ],
                "answer": "C",
                "explanation": "Onion routing ensures that intermediate nodes don't know the full payment path, protecting privacy."
            },
            {
                "question": "What happens if a payment route fails?",
                "options": [
                    "A. Payment is lost forever",
                    "B. Lightning tries an alternative route", 
                    "C. All channels close",
                    "D. Network shuts down"
                ],
                "answer": "B",
                "explanation": "Lightning automatically attempts alternative routes when payments fail, ensuring reliability."
            },
            {
                "question": "Who chooses the payment route?",
                "options": [
                    "A. The receiver",
                    "B. Lightning Network servers",
                    "C. The sender",
                    "D. Random routing nodes"
                ],
                "answer": "C", 
                "explanation": "The sender chooses and constructs the entire route - this is called 'source routing'."
            },
            {
                "question": "What limits the size of Lightning payments?",
                "options": [
                    "A. Bitcoin block size",
                    "B. Channel liquidity",
                    "C. Number of nodes",
                    "D. Internet speed"
                ],
                "answer": "B",
                "explanation": "Payment size is limited by the available liquidity in the channels along the route."
            }
        ]
        
        if os.environ.get("BITCOIN_TEST_MODE") == "1":
            print("🧪 Test mode: Showing quiz questions without interaction...")
            for i, q in enumerate(questions, 1):
                print(f"\n{i}. {q['question']}")
                for option in q['options']:
                    print(f"   {option}")
                print(f"✅ Answer: {q['answer']} - {q['explanation']}")
            return
        
        score = 0
        for i, q in enumerate(questions, 1):
            print(f"\n{i}. {q['question']}")
            for option in q['options']:
                print(f"   {option}")
            
            try:
                answer = input("Your answer (A/B/C/D): ").upper().strip()
                if answer == q['answer']:
                    print("✅ Correct!")
                    score += 1
                else:
                    print(f"❌ Incorrect. The answer is {q['answer']}")
                print(f"💡 {q['explanation']}")
            except KeyboardInterrupt:
                print("\n👋 Quiz interrupted")
                return
        
        print(f"\n🎯 Final Score: {score}/{len(questions)}")
        if score == len(questions):
            print("🏆 Perfect! You're a routing expert!")
        elif score >= len(questions) * 0.7:
            print("👍 Great job! You understand Lightning routing!")
        else:
            print("📚 Keep studying! Routing is complex but important.")
    
    def interactive_route_optimizer(self):
        """Interactive route optimization exercise"""
        print("\n⚖️ INTERACTIVE ROUTE OPTIMIZER")
        print("=" * 45)
        
        if os.environ.get("BITCOIN_TEST_MODE") == "1":
            print("🧪 Test mode: Showing route optimization example...")
            self.show_optimization_example()
            return
        
        print("🎯 Goal: Find the best route for a payment")
        print("⚖️ Consider: fees, reliability, privacy")
        
        routes = [
            {
                "name": "Direct Route",
                "hops": 1,
                "fees": 100,
                "reliability": 0.9,
                "privacy": 0.3
            },
            {
                "name": "Low Fee Route", 
                "hops": 3,
                "fees": 50,
                "reliability": 0.7,
                "privacy": 0.8
            },
            {
                "name": "Reliable Route",
                "hops": 2,
                "fees": 150,
                "reliability": 0.95,
                "privacy": 0.6
            },
            {
                "name": "Private Route",
                "hops": 4,
                "fees": 200,
                "reliability": 0.6, 
                "privacy": 0.95
            }
        ]
        
        print(f"\n📊 Available Routes:")
        for i, route in enumerate(routes, 1):
            print(f"{i}. {route['name']}")
            print(f"   🔗 Hops: {route['hops']}")
            print(f"   💸 Fees: {route['fees']} sats")
            print(f"   🎯 Reliability: {route['reliability']*100:.0f}%")
            print(f"   🛡️ Privacy: {route['privacy']*100:.0f}%")
            print()
        
        try:
            print("🤔 Which route would you choose?")
            print("Consider your priorities: cost, reliability, or privacy?")
            choice = int(input("Enter route number (1-4): ")) - 1
            
            if 0 <= choice < len(routes):
                chosen = routes[choice]
                print(f"\n✅ You chose: {chosen['name']}")
                print(f"📊 Trade-offs analysis:")
                print(f"   💸 Cost efficiency: {'High' if chosen['fees'] < 100 else 'Medium' if chosen['fees'] < 150 else 'Low'}")
                print(f"   🎯 Reliability: {'High' if chosen['reliability'] > 0.85 else 'Medium' if chosen['reliability'] > 0.7 else 'Low'}")
                print(f"   🛡️ Privacy: {'High' if chosen['privacy'] > 0.8 else 'Medium' if chosen['privacy'] > 0.5 else 'Low'}")
                
                self.explain_choice(chosen)
            else:
                print("❌ Invalid choice")
                
        except (ValueError, KeyboardInterrupt):
            print("\n👋 Optimizer interrupted")
    
    def explain_choice(self, route: Dict):
        """Explain the implications of route choice"""
        print(f"\n💡 Analysis of your choice:")
        
        if route['name'] == "Direct Route":
            print("   ✅ Fast and reliable")
            print("   ❌ Poor privacy (direct connection)")
            print("   💰 Medium cost")
        elif route['name'] == "Low Fee Route":
            print("   ✅ Cost effective")
            print("   ✅ Good privacy (multiple hops)")
            print("   ❌ Lower reliability")
        elif route['name'] == "Reliable Route":
            print("   ✅ High success probability")
            print("   ✅ Reasonable privacy")
            print("   ❌ Higher cost")
        elif route['name'] == "Private Route":
            print("   ✅ Maximum privacy")
            print("   ❌ Highest cost")
            print("   ❌ Lower reliability")
        
        print(f"\n🎓 Remember: There's no perfect route!")
        print(f"   ⚖️ Always trade-offs between cost, speed, and privacy")
        print(f"   🔄 Optimal choice depends on use case")
    
    def show_optimization_example(self):
        """Show route optimization example for test mode"""
        print("📊 Route Optimization Example:")
        print("Payment: 100,000 sats from Alice to Eve")
        print("\nRoute Options:")
        print("1. Direct: 2 hops, 150 sats fee, 95% reliability")
        print("2. Cheap: 4 hops, 75 sats fee, 70% reliability") 
        print("3. Private: 5 hops, 200 sats fee, 85% reliability")
        print("\n🧪 Optimal choice depends on priorities!")

def main():
    """Main function for routing demo"""
    print("🗺️ Welcome to Lightning Network Routing!")
    print("Understanding how payments find their way")
    
    demo = LightningRoutingDemo()
    
    try:
        # Network topology
        demo.demonstrate_network_topology()
        
        # Route finding
        print("\n" + "="*60)
        demo.demonstrate_route_finding()
        
        # Onion routing
        print("\n" + "="*60)
        demo.demonstrate_onion_routing()
        
        # Routing failures
        print("\n" + "="*60)
        demo.demonstrate_routing_failures()
        
        # Interactive elements
        if os.environ.get("BITCOIN_TEST_MODE") != "1":
            print("\n" + "="*60)
            print("🛠️ Want to try route optimization?")
            opt_choice = input("Try the route optimizer? (y/n): ").lower().strip()
            if opt_choice == 'y':
                demo.interactive_route_optimizer()
            
            print("\n🎓 Ready for the routing quiz?")
            quiz_choice = input("Test your knowledge? (y/n): ").lower().strip()
            if quiz_choice == 'y':
                demo.routing_quiz()
        else:
            demo.interactive_route_optimizer()
            demo.routing_quiz()
            
        print("\n🎉 Routing Demo Complete!")
        print("💡 You now understand how Lightning finds payment paths!")
        
    except KeyboardInterrupt:
        print("\n👋 Routing demo ended")
    except Exception as e:
        print(f"\n❌ Error in demo: {e}")

if __name__ == "__main__":
    main()