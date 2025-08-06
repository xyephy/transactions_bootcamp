#!/usr/bin/env python3
"""
Bitcoin Fundamentals Module 4: NETWORK & STORAGE
Understanding Bitcoin's peer-to-peer network and data storage

Learning Goals:
- Understand how Bitcoin nodes communicate
- Explore Bitcoin's data storage structure
- See network propagation in action
- Understand mempool and node synchronization
"""

import json
import time
import requests
from dataclasses import dataclass
from typing import Dict, List, Optional
import os
import sqlite3

# Bitcoin Core RPC connection (via Polar)
RPC_USER = "polaruser" 
RPC_PASS = "polarpass"
RPC_HOST = "localhost"
RPC_PORT = "18443"

class BitcoinRPC:
    """Simple Bitcoin Core RPC client"""
    
    def __init__(self):
        self.url = f"http://{RPC_USER}:{RPC_PASS}@{RPC_HOST}:{RPC_PORT}"
    
    def call(self, method: str, params: list = []) -> Dict:
        """Make RPC call to Bitcoin Core"""
        payload = {
            "jsonrpc": "2.0",
            "id": "python",
            "method": method,
            "params": params
        }
        
        try:
            response = requests.post(self.url, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if "error" in result and result["error"]:
                raise Exception(f"RPC Error: {result['error']}")
                
            return result.get("result")
        except Exception as e:
            print(f"❌ RPC Error: {e}")
            return {}

@dataclass
class BitcoinNode:
    """Represents a Bitcoin network node"""
    
    id: str
    address: str
    port: int
    version: str
    services: List[str]
    last_seen: int
    connected: bool = False
    
    def display_info(self):
        """Display node information"""
        status = "🟢 Connected" if self.connected else "🔴 Disconnected"
        print(f"🖥️  Node {self.id}:")
        print(f"   📍 Address: {self.address}:{self.port}")
        print(f"   🏷️  Version: {self.version}")
        print(f"   ⚙️  Services: {', '.join(self.services)}")
        print(f"   🕐 Last seen: {time.ctime(self.last_seen)}")
        print(f"   📊 Status: {status}")

class NetworkExplorer:
    """Educational Bitcoin network explorer"""
    
    def __init__(self, rpc_client: BitcoinRPC):
        self.rpc = rpc_client
        self.connected_peers = []
    
    def get_network_info(self) -> Dict:
        """Get basic network information"""
        try:
            network_info = self.rpc.call("getnetworkinfo")
            return network_info
        except Exception as e:
            print(f"❌ Error getting network info: {e}")
            return {}
    
    def get_peer_info(self) -> List[Dict]:
        """Get information about connected peers"""
        try:
            peer_info = self.rpc.call("getpeerinfo")
            return peer_info
        except Exception as e:
            print(f"❌ Error getting peer info: {e}")
            return []
    
    def display_network_status(self):
        """Display current network status"""
        print("\n🌐 BITCOIN NETWORK STATUS")
        print("="*30)
        
        # Get network info
        net_info = self.get_network_info()
        if net_info:
            print(f"🏷️  Version: {net_info.get('version', 'Unknown')}")
            print(f"🔌 Connections: {net_info.get('connections', 0)}")
            print(f"🌍 Network: {net_info.get('networkactive', False)}")
            print(f"📡 Reachable: {net_info.get('reachable', False)}")
            
            # Show enabled networks
            networks = net_info.get('networks', [])
            print(f"🌐 Enabled networks:")
            for network in networks:
                if network.get('reachable'):
                    print(f"   ✅ {network.get('name')}: {network.get('proxy', 'direct')}")
        
        # Get peer info
        peers = self.get_peer_info()
        print(f"\n👥 Connected Peers: {len(peers)}")
        
        for i, peer in enumerate(peers[:3]):  # Show first 3 peers
            print(f"\n   Peer #{i+1}:")
            print(f"     📍 Address: {peer.get('addr', 'Unknown')}")
            print(f"     🏷️  Version: {peer.get('subver', 'Unknown')}")
            print(f"     ⏱️  Connected: {peer.get('conntime', 0)}s ago")
            print(f"     📊 Bytes sent: {peer.get('bytessent', 0):,}")
            print(f"     📊 Bytes received: {peer.get('bytesrecv', 0):,}")

def demonstrate_p2p_network():
    """Demonstrate Bitcoin's peer-to-peer network"""
    
    print("\n🕸️  BITCOIN PEER-TO-PEER NETWORK")
    print("="*37)
    
    print("🎯 Bitcoin is a peer-to-peer network:")
    print("   • No central servers or authorities")
    print("   • Each node connects to ~8-10 other nodes")
    print("   • Nodes share transactions and blocks")
    print("   • Network is self-organizing and resilient")
    
    # Simulate network structure
    print("\n🖥️  Example Network Structure:")
    print("     Node A ←→ Node B ←→ Node C")
    print("        ↕        ↕        ↕  ")
    print("     Node D ←→ Node E ←→ Node F")
    print("        ↕        ↕        ↕  ")
    print("     Node G ←→ Node H ←→ Node I")
    
    print("\n📡 How information spreads:")
    print("   1. Node A creates a transaction")
    print("   2. Sends to connected peers (B, D)")
    print("   3. They forward to their peers (C, E, G)")
    print("   4. Continues until entire network knows")
    print("   5. Usually takes 1-3 seconds globally!")
    
    # Real network exploration
    rpc = BitcoinRPC()
    explorer = NetworkExplorer(rpc)
    explorer.display_network_status()

def demonstrate_mempool():
    """Show how the mempool works"""
    
    print("\n🏊 BITCOIN MEMPOOL (MEMORY POOL)")
    print("="*36)
    
    print("🎯 The mempool holds unconfirmed transactions:")
    print("   • Transactions wait here before being mined")
    print("   • Each node has its own mempool")
    print("   • Miners select transactions from their mempool")
    print("   • Higher fee transactions get priority")
    
    rpc = BitcoinRPC()
    
    try:
        # Get mempool info
        mempool_info = rpc.call("getmempoolinfo")
        if mempool_info:
            print(f"\n📊 Current Mempool Status:")
            print(f"   🧾 Transactions: {mempool_info.get('size', 0):,}")
            print(f"   💾 Memory usage: {mempool_info.get('usage', 0):,} bytes")
            print(f"   💰 Total fees: {mempool_info.get('total_fee', 0)} BTC")
            print(f"   📏 Max mempool: {mempool_info.get('maxmempool', 0):,} bytes")
        
        # Get raw mempool
        raw_mempool = rpc.call("getrawmempool")
        if raw_mempool:
            print(f"\n🧾 Transactions in mempool: {len(raw_mempool)}")
            
            if raw_mempool:
                print("   First few transaction IDs:")
                for i, txid in enumerate(raw_mempool[:3]):
                    print(f"     {i+1}. {txid}")
            else:
                print("   📭 Mempool is empty")
                print("   💡 This is normal in regtest mode")
        
        # Demonstrate creating a transaction to see mempool in action
        print(f"\n🎮 Want to see mempool in action?")
        create_tx = input("Create a test transaction? (y/n): ") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...").lower().strip()
        
        if create_tx == 'y':
            try:
                # Get a new address to send to
                new_address = rpc.call("getnewaddress")
                if new_address:
                    print(f"   📍 Generated address: {new_address}")
                    
                    # Create and send transaction (small amount)
                    txid = rpc.call("sendtoaddress", [new_address, 0.001])
                    if txid:
                        print(f"   ✅ Created transaction: {txid}")
                        print(f"   🏊 Transaction now in mempool!")
                        
                        # Check mempool again
                        time.sleep(1)
                        new_mempool = rpc.call("getrawmempool")
                        if new_mempool and txid in new_mempool:
                            print(f"   👀 Confirmed: Transaction is in mempool")
                        
                        # Mine a block to confirm it
                        mine_block = input("   Mine a block to confirm? (y/n): ") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...").lower().strip()
                        if mine_block == 'y':
                            block_hash = rpc.call("generatetoaddress", [1, new_address])
                            if block_hash:
                                print(f"   ⛏️  Mined block: {block_hash[0][:16]}...")
                                print(f"   ✅ Transaction confirmed and removed from mempool!")
                            
            except Exception as e:
                print(f"   ❌ Error creating transaction: {e}")
    
    except Exception as e:
        print(f"❌ Error exploring mempool: {e}")

def demonstrate_data_storage():
    """Show how Bitcoin stores data"""
    
    print("\n💾 BITCOIN DATA STORAGE")
    print("="*26)
    
    print("🎯 Bitcoin Core stores data in several files:")
    print("   📦 blocks/blk*.dat - Raw block data")
    print("   🗂️  blocks/index/ - Block index database")
    print("   🔗 chainstate/ - UTXO set (current balances)")
    print("   📝 wallet.dat - Wallet private keys")
    print("   ⚙️  bitcoin.conf - Configuration")
    
    # Try to find data directory (works with Polar)
    possible_dirs = [
        os.path.expanduser("~/.bitcoin"),
        os.path.expanduser("~/.polar"),
        "/tmp/polar",
        "."
    ]
    
    print(f"\n🔍 Looking for Bitcoin data directory...")
    
    for data_dir in possible_dirs:
        if os.path.exists(data_dir):
            print(f"   📁 Found directory: {data_dir}")
            
            # Look for common Bitcoin files
            bitcoin_files = [
                "blocks",
                "chainstate", 
                "wallet.dat",
                "bitcoin.conf",
                "debug.log"
            ]
            
            for filename in bitcoin_files:
                filepath = os.path.join(data_dir, filename)
                if os.path.exists(filepath):
                    if os.path.isdir(filepath):
                        file_count = len(os.listdir(filepath)) if os.path.isdir(filepath) else 0
                        print(f"     📂 {filename}/ ({file_count} files)")
                    else:
                        file_size = os.path.getsize(filepath)
                        print(f"     📄 {filename} ({file_size:,} bytes)")
            break
    else:
        print("   ❌ No Bitcoin data directory found")
        print("   💡 Using simulated data structure...")
        
        # Simulated file structure
        print(f"\n📁 Typical Bitcoin Core Data Structure:")
        print(f"   📂 .bitcoin/")
        print(f"     📂 blocks/")
        print(f"       📄 blk00000.dat (128 MB)")
        print(f"       📄 blk00001.dat (128 MB)")
        print(f"       📂 index/ (LevelDB)")
        print(f"     📂 chainstate/ (LevelDB)")
        print(f"       📄 CURRENT")
        print(f"       📄 *.ldb files")
        print(f"     📄 wallet.dat (Berkeley DB)")
        print(f"     📄 peers.dat")
        print(f"     📄 debug.log")
    
    # Explain storage concepts
    print(f"\n💡 Storage Concepts:")
    print(f"   🗂️  LevelDB: Key-value database for indexes")
    print(f"   📦 Block files: Raw block data in 128MB chunks")
    print(f"   ⚡ UTXO set: Fast lookup of spendable coins")
    print(f"   🔄 Pruning: Can delete old blocks to save space")

def simulate_network_propagation():
    """Simulate how transactions propagate through the network"""
    
    print("\n📡 NETWORK PROPAGATION SIMULATION")
    print("="*37)
    
    print("🎯 Let's simulate how a transaction spreads:")
    
    # Create a simulated network
    nodes = {
        "Alice": {"connections": ["Bob", "Charlie"], "has_tx": False},
        "Bob": {"connections": ["Alice", "Diana", "Eve"], "has_tx": False},
        "Charlie": {"connections": ["Alice", "Frank"], "has_tx": False},
        "Diana": {"connections": ["Bob", "Grace"], "has_tx": False},
        "Eve": {"connections": ["Bob", "Henry"], "has_tx": False},
        "Frank": {"connections": ["Charlie", "Grace"], "has_tx": False},
        "Grace": {"connections": ["Diana", "Frank"], "has_tx": False},
        "Henry": {"connections": ["Eve"], "has_tx": False}
    }
    
    print(f"🌐 Network topology:")
    for node, info in nodes.items():
        connections = ", ".join(info["connections"])
        print(f"   {node} ↔ {connections}")
    
    print(f"\n🚀 Alice creates a transaction...")
    nodes["Alice"]["has_tx"] = True
    
    # Simulate propagation rounds
    rounds = 0
    while True:
        rounds += 1
        print(f"\n📡 Round {rounds}:")
        
        new_propagations = []
        
        # Each node that has the transaction shares it with connected peers
        for node, info in nodes.items():
            if info["has_tx"]:
                for peer in info["connections"]:
                    if not nodes[peer]["has_tx"]:
                        new_propagations.append((node, peer))
        
        if not new_propagations:
            break
        
        # Apply propagations
        for sender, receiver in new_propagations:
            nodes[receiver]["has_tx"] = True
            print(f"   {sender} → {receiver}")
        
        # Show current state
        has_tx = [node for node, info in nodes.items() if info["has_tx"]]
        print(f"   📊 Nodes with transaction: {', '.join(has_tx)}")
        
        time.sleep(1)  # Dramatic pause
    
    print(f"\n🎉 Propagation complete in {rounds} rounds!")
    print(f"💡 In real Bitcoin:")
    print(f"   • Takes ~1-3 seconds to reach most nodes")
    print(f"   • Network has 10,000+ nodes worldwide")
    print(f"   • Uses optimized flooding algorithms")

def explore_node_synchronization():
    """Demonstrate how nodes stay synchronized"""
    
    print("\n🔄 NODE SYNCHRONIZATION")
    print("="*25)
    
    print("🎯 How Bitcoin nodes stay in sync:")
    print("   1. New node connects to network")
    print("   2. Downloads block headers first (fast)")
    print("   3. Downloads full blocks (slower)")
    print("   4. Validates each block")
    print("   5. Catches up to current height")
    
    rpc = BitcoinRPC()
    
    try:
        # Get blockchain info
        blockchain_info = rpc.call("getblockchaininfo")
        if blockchain_info:
            print(f"\n📊 Current Node Status:")
            print(f"   🏔️  Block height: {blockchain_info.get('blocks', 0):,}")
            print(f"   🔗 Headers: {blockchain_info.get('headers', 0):,}")
            print(f"   ✅ Verified: {blockchain_info.get('verificationprogress', 0):.1%}")
            print(f"   🌐 Chain: {blockchain_info.get('chain', 'unknown')}")
            
            # Check if node is synced
            blocks = blockchain_info.get('blocks', 0)
            headers = blockchain_info.get('headers', 0)
            
            if blocks == headers:
                print(f"   🎉 Node is fully synchronized!")
            else:
                print(f"   ⏳ Node is syncing ({blocks}/{headers} blocks)")
        
        # Show sync process simulation
        print(f"\n🎮 Simulate initial blockchain download?")
        simulate = input("Show sync simulation? (y/n): ") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...").lower().strip()
        
        if simulate == 'y':
            print(f"\n⏳ Simulating Initial Block Download...")
            
            total_blocks = 50  # Simulate small blockchain
            
            for height in range(0, total_blocks + 1, 5):
                progress = min(height / total_blocks, 1.0)
                blocks_left = max(0, total_blocks - height)
                
                print(f"   📦 Height: {height:3d}/{total_blocks} "
                      f"[{'█' * int(progress * 20):20s}] "
                      f"{progress:.1%} "
                      f"({blocks_left} blocks left)")
                
                time.sleep(0.3)
            
            print(f"   🎉 Sync complete! Node ready to use.")
    
    except Exception as e:
        print(f"❌ Error exploring synchronization: {e}")

def bitcoin_storage_quiz():
    """Interactive quiz about Bitcoin storage and networking"""
    
    print("\n🧠 NETWORK & STORAGE QUIZ")
    print("="*29)
    
    questions = [
        {
            "question": "Where do unconfirmed transactions wait?",
            "options": ["A) Blockchain", "B) Mempool", "C) Wallet", "D) Hard drive"],
            "answer": "B",
            "explanation": "The mempool (memory pool) holds unconfirmed transactions until they're included in a block."
        },
        {
            "question": "How long does transaction propagation typically take?",
            "options": ["A) 10 minutes", "B) 1 hour", "C) 1-3 seconds", "D) 1 day"],
            "answer": "C",
            "explanation": "Transactions propagate through the peer-to-peer network in just 1-3 seconds globally."
        },
        {
            "question": "What does the UTXO set contain?",
            "options": ["A) All transactions", "B) Private keys", "C) Spendable coins", "D) Block headers"],
            "answer": "C",
            "explanation": "The UTXO set contains all currently spendable transaction outputs (unspent coins)."
        },
        {
            "question": "How many peer connections does a typical Bitcoin node maintain?",
            "options": ["A) 1-2", "B) 8-10", "C) 50-100", "D) 1000+"],
            "answer": "B",
            "explanation": "Bitcoin nodes typically maintain 8-10 outbound connections and accept inbound connections."
        }
    ]
    
    score = 0
    
    for i, q in enumerate(questions, 1):
        print(f"\n❓ Question {i}: {q['question']}")
        for option in q['options']:
            print(f"   {option}")
        
        user_answer = input("\nYour answer (A/B/C/D): ") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...").upper().strip()
        
        if user_answer == q['answer']:
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Wrong. Correct answer: {q['answer']}")
        
        print(f"💡 Explanation: {q['explanation']}")
        input("Press Enter for next question...") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...")
    
    print(f"\n🎯 Final Score: {score}/{len(questions)}")
    
    if score == len(questions):
        print("🏆 Perfect! You understand Bitcoin networking!")
    elif score >= len(questions) * 0.7:
        print("👍 Great job! You've got the networking basics!")
    else:
        print("📚 Review the concepts and try again!")

def main():
    """Main lesson function"""
    
    print("🎓 BITCOIN FUNDAMENTALS: NETWORK & STORAGE")
    print("="*48)
    print("Understanding Bitcoin's P2P network and data storage")
    
    # Interactive lesson modules
    modules = [
        ("1. P2P Network", demonstrate_p2p_network),
        ("2. Mempool", demonstrate_mempool),
        ("3. Data Storage", demonstrate_data_storage),
        ("4. Network Propagation", simulate_network_propagation),
        ("5. Node Synchronization", explore_node_synchronization),
        ("6. Knowledge Quiz", bitcoin_storage_quiz)
    ]
    
    for title, function in modules:
        print(f"\n🎯 {title}")
        try:
            function()
        except KeyboardInterrupt:
            print("\n👋 Lesson interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error in {title}: {e}")
            
        input("\nPress Enter to continue to next module...") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...")
    
    print("\n🎉 LESSON COMPLETE!")
    print("💡 Key takeaways:")
    print("  • Bitcoin is a peer-to-peer network with no central servers")
    print("  • Transactions propagate globally in seconds via flooding")
    print("  • Mempool holds unconfirmed transactions waiting for mining")
    print("  • Nodes store blockchain data in efficient database formats")
    print("  • Network is self-healing and automatically synchronizes")

if __name__ == "__main__":
    main()