#!/usr/bin/env python3
"""
Lightning Network: Network Topology and Channel Management
==========================================================

This script demonstrates Lightning Network topology concepts:
- Network structure and connectivity
- Channel lifecycle management
- Liquidity distribution and rebalancing
- Network effects and centralization
- Topology analysis and metrics

Key Learning Objectives:
- Understand network topology principles
- Learn about hub-and-spoke vs mesh networks
- See how liquidity flows through the network
- Experience channel management strategies
"""

import requests
import json
import time
import os
import random
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class NetworkNode:
    """Represents a node in the Lightning Network"""
    pub_key: str
    alias: str
    channels: List[str]
    capacity: int
    degree: int  # Number of connections

@dataclass
class NetworkChannel:
    """Represents a channel in the Lightning Network"""
    channel_id: str
    node1: str
    node2: str
    capacity: int
    active: bool
    last_update: int

class LightningTopologyDemo:
    """Lightning Network topology and channel management demonstrations"""
    
    def __init__(self):
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
        
        self.network_graph = {}
        self.topology_metrics = {}
    
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
            return None
    
    def get_network_info(self, node: str = "alice"):
        """Get detailed network information"""
        graph = self.lnd_request(node, "/v1/graph")
        if graph:
            self.network_graph = graph
            return graph
        return None
    
    def analyze_network_topology(self):
        """Analyze the network topology structure"""
        print("\n🕸️ NETWORK TOPOLOGY ANALYSIS")
        print("=" * 45)
        print("Understanding Lightning Network structure...")
        
        # Get network data
        print("\n📡 Fetching network graph...")
        graph = self.get_network_info()
        
        if not graph:
            print("❌ Could not fetch network graph - using simulated data")
            return self.simulate_topology_analysis()
        
        nodes = graph.get("nodes", [])
        edges = graph.get("edges", [])
        
        # Basic metrics
        total_nodes = len(nodes)
        total_channels = len(edges)
        total_capacity = sum(int(edge.get("capacity", 0)) for edge in edges)
        
        print(f"\n📊 NETWORK STATISTICS")
        print(f"=" * 30)
        print(f"👥 Total Nodes: {total_nodes:,}")
        print(f"⚡ Total Channels: {total_channels:,}")
        print(f"💰 Total Capacity: {total_capacity:,} sats")
        print(f"📏 Avg Channel Size: {total_capacity/total_channels:,.0f} sats" if total_channels > 0 else "📏 Avg Channel Size: N/A")
        
        # Analyze node connectivity
        node_degrees = defaultdict(int)
        node_capacity = defaultdict(int)
        
        for edge in edges:
            node1 = edge.get("node1_pub", "")
            node2 = edge.get("node2_pub", "")
            capacity = int(edge.get("capacity", 0))
            
            node_degrees[node1] += 1
            node_degrees[node2] += 1
            node_capacity[node1] += capacity
            node_capacity[node2] += capacity
        
        # Find hub nodes
        sorted_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\n🌟 TOP CONNECTED NODES (HUBS)")
        print(f"=" * 35)
        for i, (pub_key, degree) in enumerate(sorted_nodes[:5]):
            # Find alias for this node
            alias = "Unknown"
            for node in nodes:
                if node.get("pub_key") == pub_key:
                    alias = node.get("alias", "Unknown")
                    break
            
            capacity = node_capacity[pub_key]
            print(f"{i+1}. {alias}")
            print(f"   🔗 Channels: {degree}")
            print(f"   💰 Capacity: {capacity:,} sats")
            print(f"   🆔 {pub_key[:20]}...")
            print()
        
        # Network connectivity metrics
        if total_nodes > 0:
            avg_degree = (total_channels * 2) / total_nodes  # Each channel connects 2 nodes
            print(f"📈 CONNECTIVITY METRICS")
            print(f"=" * 30)
            print(f"🔗 Average Degree: {avg_degree:.2f}")
            
            # Simple network density (actual edges / possible edges)
            max_edges = total_nodes * (total_nodes - 1) / 2
            density = total_channels / max_edges if max_edges > 0 else 0
            print(f"🕸️ Network Density: {density:.4f} ({density*100:.2f}%)")
            
            # Centralization analysis
            max_degree = max(node_degrees.values()) if node_degrees else 0
            print(f"⭐ Highest Degree: {max_degree}")
            
            if max_degree > avg_degree * 2:
                print("🏢 Network shows hub-and-spoke characteristics")
            else:
                print("🕸️ Network shows mesh characteristics")
    
    def simulate_topology_analysis(self):
        """Simulate topology analysis with sample data"""
        print("\n🎭 SIMULATED TOPOLOGY ANALYSIS")
        print("=" * 40)
        
        # Create simulated network data
        simulated_nodes = [
            {"alias": "BigHub", "channels": 150, "capacity": 50000000},
            {"alias": "MediumNode1", "channels": 25, "capacity": 8000000},
            {"alias": "MediumNode2", "channels": 30, "capacity": 12000000},
            {"alias": "SmallNode1", "channels": 5, "capacity": 1000000},
            {"alias": "SmallNode2", "channels": 8, "capacity": 2000000},
            {"alias": "NewNode", "channels": 2, "capacity": 500000},
        ]
        
        total_capacity = sum(node["capacity"] for node in simulated_nodes)
        total_channels = sum(node["channels"] for node in simulated_nodes) // 2  # Each channel counted twice
        
        print(f"📊 SIMULATED NETWORK:")
        print(f"👥 Nodes: {len(simulated_nodes)}")
        print(f"⚡ Channels: {total_channels}")
        print(f"💰 Total Capacity: {total_capacity:,} sats")
        
        print(f"\n🌟 NODE ANALYSIS:")
        for i, node in enumerate(simulated_nodes, 1):
            node_percent = (node["capacity"] / total_capacity) * 100
            print(f"{i}. {node['alias']}")
            print(f"   🔗 Channels: {node['channels']}")
            print(f"   💰 Capacity: {node['capacity']:,} sats ({node_percent:.1f}%)")
            
            if node['channels'] > 50:
                print(f"   🏢 Classification: Major Hub")
            elif node['channels'] > 15:
                print(f"   🏪 Classification: Medium Node")
            else:
                print(f"   🏠 Classification: Small Node")
            print()
        
        # Analyze centralization
        big_hub_share = (simulated_nodes[0]["capacity"] / total_capacity) * 100
        print(f"📈 CENTRALIZATION ANALYSIS:")
        print(f"🏢 Largest hub controls {big_hub_share:.1f}% of capacity")
        
        if big_hub_share > 30:
            print("⚠️ High centralization - potential risks")
        elif big_hub_share > 15:
            print("⚖️ Moderate centralization")
        else:
            print("🕸️ Well distributed network")
    
    def demonstrate_channel_lifecycle(self):
        """Demonstrate channel lifecycle management"""
        print("\n🔄 CHANNEL LIFECYCLE MANAGEMENT")
        print("=" * 45)
        
        lifecycle_stages = [
            {
                "stage": "Channel Opening",
                "description": "Creating a new payment channel",
                "steps": [
                    "1. Choose partner node",
                    "2. Negotiate channel parameters",
                    "3. Create funding transaction",
                    "4. Wait for confirmations",
                    "5. Channel becomes active"
                ]
            },
            {
                "stage": "Active Management",
                "description": "Operating the channel",
                "steps": [
                    "1. Monitor liquidity levels",
                    "2. Rebalance when needed",
                    "3. Adjust fee policies",
                    "4. Track routing success",
                    "5. Maintain uptime"
                ]
            },
            {
                "stage": "Channel Closing",
                "description": "Shutting down a channel",
                "steps": [
                    "1. Decide to close (cooperative/force)",
                    "2. Create closing transaction",
                    "3. Broadcast to blockchain",
                    "4. Wait for confirmations",
                    "5. Funds returned on-chain"
                ]
            }
        ]
        
        for stage_info in lifecycle_stages:
            print(f"\n📋 {stage_info['stage'].upper()}")
            print(f"=" * (len(stage_info['stage']) + 5))
            print(f"📝 {stage_info['description']}")
            print(f"\n🔧 Process:")
            for step in stage_info['steps']:
                print(f"   {step}")
            
            if os.environ.get("BITCOIN_TEST_MODE") != "1":
                input("\nPress Enter to continue...")
        
        print(f"\n💡 CHANNEL STRATEGY TIPS:")
        print(f"🎯 Open channels to well-connected nodes")
        print(f"⚖️ Balance incoming and outgoing liquidity")
        print(f"💰 Consider channel size vs fees")
        print(f"🔄 Plan for rebalancing needs")
        print(f"📊 Monitor performance metrics")
    
    def demonstrate_liquidity_management(self):
        """Demonstrate liquidity management concepts"""
        print("\n💧 LIQUIDITY MANAGEMENT")
        print("=" * 35)
        print("Understanding channel liquidity...")
        
        # Simulate channel states
        channels = [
            {
                "name": "Alice-Bob", 
                "capacity": 1000000,
                "local": 800000,
                "remote": 200000,
                "status": "Outbound liquidity rich"
            },
            {
                "name": "Alice-Charlie",
                "capacity": 500000, 
                "local": 100000,
                "remote": 400000,
                "status": "Inbound liquidity rich"
            },
            {
                "name": "Alice-Dave",
                "capacity": 2000000,
                "local": 1000000,
                "remote": 1000000,
                "status": "Balanced"
            }
        ]
        
        print(f"\n📊 CHANNEL LIQUIDITY STATUS:")
        print(f"=" * 35)
        
        for channel in channels:
            local_pct = (channel["local"] / channel["capacity"]) * 100
            remote_pct = (channel["remote"] / channel["capacity"]) * 100
            
            print(f"\n⚡ {channel['name']}")
            print(f"   💰 Capacity: {channel['capacity']:,} sats")
            print(f"   📤 Local: {channel['local']:,} sats ({local_pct:.1f}%)")
            print(f"   📥 Remote: {channel['remote']:,} sats ({remote_pct:.1f}%)")
            print(f"   📊 Status: {channel['status']}")
            
            # Liquidity analysis
            if local_pct > 80:
                print(f"   ⚠️ Problem: Can't receive large payments")
                print(f"   💡 Solution: Send payments or submarine swap")
            elif local_pct < 20:
                print(f"   ⚠️ Problem: Can't send large payments")
                print(f"   💡 Solution: Receive payments or rebalance")
            else:
                print(f"   ✅ Good: Can send and receive")
        
        # Demonstrate rebalancing
        print(f"\n🔄 REBALANCING STRATEGIES:")
        print(f"=" * 30)
        
        rebalancing_methods = [
            {
                "method": "Circular Rebalancing",
                "description": "Pay yourself through other channels",
                "cost": "Routing fees",
                "time": "Minutes"
            },
            {
                "method": "Submarine Swaps",
                "description": "Exchange on-chain for off-chain Bitcoin",
                "cost": "Swap fees + mining fees",
                "time": "Confirmations needed"
            },
            {
                "method": "Channel Splicing",
                "description": "Add/remove funds from existing channel",
                "cost": "Mining fees only",
                "time": "Future feature"
            },
            {
                "method": "Dual Funding",
                "description": "Both parties fund new channel",
                "cost": "Coordination needed",
                "time": "Channel opening time"
            }
        ]
        
        for method in rebalancing_methods:
            print(f"\n🔧 {method['method']}")
            print(f"   📝 {method['description']}")
            print(f"   💸 Cost: {method['cost']}")
            print(f"   ⏱️ Time: {method['time']}")
    
    def demonstrate_network_effects(self):
        """Demonstrate network effects in Lightning"""
        print("\n🌐 NETWORK EFFECTS DEMONSTRATION")
        print("=" * 45)
        print("How network growth affects everyone...")
        
        network_stages = [
            {
                "stage": "Small Network (100 nodes)",
                "connectivity": "Poor",
                "routing": "Often fails",
                "fees": "High (limited competition)",
                "benefits": "Early adopter advantage"
            },
            {
                "stage": "Growing Network (1,000 nodes)", 
                "connectivity": "Improving",
                "routing": "More reliable",
                "fees": "Decreasing",
                "benefits": "Better path diversity"
            },
            {
                "stage": "Mature Network (10,000+ nodes)",
                "connectivity": "Excellent",
                "routing": "Highly reliable", 
                "fees": "Competitive",
                "benefits": "Global reach"
            }
        ]
        
        print(f"\n📈 NETWORK GROWTH STAGES:")
        for i, stage in enumerate(network_stages, 1):
            print(f"\n{i}️⃣ {stage['stage']}")
            print(f"   🔗 Connectivity: {stage['connectivity']}")
            print(f"   🗺️ Routing: {stage['routing']}")
            print(f"   💰 Fees: {stage['fees']}")
            print(f"   🎁 Benefits: {stage['benefits']}")
        
        print(f"\n🔄 POSITIVE FEEDBACK LOOPS:")
        print(f"✅ More nodes → Better connectivity")
        print(f"✅ Better connectivity → More reliable routing")
        print(f"✅ Reliable routing → Lower fees")
        print(f"✅ Lower fees → More adoption")
        print(f"✅ More adoption → More nodes")
        
        print(f"\n⚠️ POTENTIAL RISKS:")
        print(f"🏢 Hub centralization")
        print(f"💸 Liquidity concentration")
        print(f"🔒 Regulatory pressure on hubs")
        print(f"🛡️ Privacy concerns")
        
        if os.environ.get("BITCOIN_TEST_MODE") != "1":
            input("\nPress Enter to continue...")
    
    def topology_quiz(self):
        """Interactive quiz about topology concepts"""
        print("\n🧠 NETWORK TOPOLOGY QUIZ")
        print("=" * 35)
        
        questions = [
            {
                "question": "What is a hub node in Lightning Network?",
                "options": [
                    "A. A node run by Lightning Labs",
                    "B. A node with many connections",
                    "C. A node that stores bitcoins",
                    "D. A node that validates transactions"
                ],
                "answer": "B",
                "explanation": "Hub nodes have many channels, providing connectivity but also centralization risks."
            },
            {
                "question": "Why is liquidity management important?",
                "options": [
                    "A. To earn more fees",
                    "B. To store more Bitcoin",
                    "C. To enable bidirectional payments",
                    "D. To increase channel capacity"
                ],
                "answer": "C",
                "explanation": "Balanced liquidity allows both sending and receiving payments through channels."
            },
            {
                "question": "What is channel rebalancing?",
                "options": [
                    "A. Closing and reopening channels",
                    "B. Moving liquidity between channel sides",
                    "C. Changing channel fees",
                    "D. Adding more Bitcoin to channels"
                ],
                "answer": "B",
                "explanation": "Rebalancing moves liquidity to maintain the ability to send and receive payments."
            },
            {
                "question": "How does network growth benefit users?",
                "options": [
                    "A. Higher fees for operators",
                    "B. Better routing and lower fees",
                    "C. More centralized control",
                    "D. Slower transactions"
                ],
                "answer": "B", 
                "explanation": "More nodes create better connectivity, more routing options, and competitive fees."
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
            print("🏆 Perfect! You understand Lightning topology!")
        elif score >= len(questions) * 0.7:
            print("👍 Great job! You grasp the network concepts!")
        else:
            print("📚 Keep learning! Network topology is complex.")
    
    def interactive_network_designer(self):
        """Interactive network design exercise"""
        print("\n🏗️ INTERACTIVE NETWORK DESIGNER")
        print("=" * 45)
        
        if os.environ.get("BITCOIN_TEST_MODE") == "1":
            print("🧪 Test mode: Showing network design example...")
            self.show_design_example()
            return
        
        print("🎯 Design a Lightning Network topology!")
        print("Consider: connectivity, redundancy, centralization")
        
        design_choices = [
            {
                "name": "Hub-and-Spoke",
                "description": "One central hub, all nodes connect to it",
                "pros": ["Simple", "Low total channels", "Easy routing"],
                "cons": ["Single point of failure", "Centralized", "Hub has all liquidity"]
            },
            {
                "name": "Ring Network",
                "description": "Nodes connected in a circle",
                "pros": ["Decentralized", "Redundant paths", "Fair distribution"],
                "cons": ["Long routes", "Limited connectivity", "Routing complexity"]
            },
            {
                "name": "Mesh Network",
                "description": "Every node connects to multiple others",
                "pros": ["Highly redundant", "Short paths", "Fault tolerant"],
                "cons": ["Many channels needed", "High liquidity requirements", "Complex"]
            },
            {
                "name": "Small World",
                "description": "Local clusters with some long-distance links",
                "pros": ["Balanced", "Efficient", "Realistic"],
                "cons": ["Design complexity", "Requires coordination", "Uneven benefits"]
            }
        ]
        
        print(f"\n🏗️ TOPOLOGY OPTIONS:")
        for i, design in enumerate(design_choices, 1):
            print(f"\n{i}. {design['name']}")
            print(f"   📝 {design['description']}")
            print(f"   ✅ Pros: {', '.join(design['pros'])}")
            print(f"   ❌ Cons: {', '.join(design['cons'])}")
        
        try:
            choice = int(input("\nWhich topology would you choose? (1-4): ")) - 1
            
            if 0 <= choice < len(design_choices):
                chosen = design_choices[choice]
                print(f"\n✅ You chose: {chosen['name']}")
                self.analyze_design_choice(chosen)
            else:
                print("❌ Invalid choice")
                
        except (ValueError, KeyboardInterrupt):
            print("\n👋 Design session interrupted")
    
    def analyze_design_choice(self, design: Dict):
        """Analyze the network design choice"""
        print(f"\n📊 ANALYSIS OF {design['name'].upper()}")
        print(f"=" * (len(design['name']) + 12))
        
        if design['name'] == "Hub-and-Spoke":
            print("🎯 Use case: Small, trusted networks")
            print("⚠️ Risk: Hub becomes critical infrastructure")
            print("💡 Mitigation: Multiple hubs for redundancy")
        elif design['name'] == "Ring Network":
            print("🎯 Use case: Equal participants, simple setup")
            print("⚠️ Risk: Long payment paths, single failures")
            print("💡 Mitigation: Add cross-ring connections")
        elif design['name'] == "Mesh Network":
            print("🎯 Use case: High-value, fault-critical applications")
            print("⚠️ Risk: Expensive to maintain, over-engineered")
            print("💡 Mitigation: Partial mesh, prioritize key connections")
        elif design['name'] == "Small World":
            print("🎯 Use case: Real-world Lightning Network")
            print("⚠️ Risk: Complexity in planning and coordination")
            print("💡 Mitigation: Gradual evolution, local optimization")
        
        print(f"\n🔍 KEY INSIGHT:")
        print(f"There's no perfect topology - it depends on:")
        print(f"   👥 Number of participants")
        print(f"   💰 Available capital")
        print(f"   🎯 Use case requirements")
        print(f"   ⚖️ Centralization tolerance")
    
    def show_design_example(self):
        """Show network design example for test mode"""
        print("🏗️ Network Design Example:")
        print("Scenario: 6-node Lightning Network")
        print("\nTopology Options:")
        print("1. Hub-and-Spoke: 5 channels, 1 hub")
        print("2. Ring: 6 channels, no single point of failure")
        print("3. Mesh: 15 channels, maximum redundancy")
        print("4. Small World: 8 channels, efficient balance")
        print("\n🧪 Small World chosen: best balance of efficiency and resilience!")

def main():
    """Main function for topology demo"""
    print("🕸️ Welcome to Lightning Network Topology!")
    print("Understanding network structure and management")
    
    demo = LightningTopologyDemo()
    
    try:
        # Network analysis
        demo.analyze_network_topology()
        
        # Channel lifecycle
        print("\n" + "="*60)
        demo.demonstrate_channel_lifecycle()
        
        # Liquidity management
        print("\n" + "="*60)
        demo.demonstrate_liquidity_management()
        
        # Network effects
        print("\n" + "="*60)
        demo.demonstrate_network_effects()
        
        # Interactive elements
        if os.environ.get("BITCOIN_TEST_MODE") != "1":
            print("\n" + "="*60)
            print("🛠️ Want to design a network?")
            design_choice = input("Try the network designer? (y/n): ").lower().strip()
            if design_choice == 'y':
                demo.interactive_network_designer()
            
            print("\n🎓 Ready for the topology quiz?")
            quiz_choice = input("Test your knowledge? (y/n): ").lower().strip()
            if quiz_choice == 'y':
                demo.topology_quiz()
        else:
            demo.interactive_network_designer()
            demo.topology_quiz()
            
        print("\n🎉 Topology Demo Complete!")
        print("💡 You now understand Lightning Network structure!")
        
    except KeyboardInterrupt:
        print("\n👋 Topology demo ended")
    except Exception as e:
        print(f"\n❌ Error in demo: {e}")

if __name__ == "__main__":
    main()