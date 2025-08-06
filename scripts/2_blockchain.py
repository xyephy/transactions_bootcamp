#!/usr/bin/env python3
"""
Bitcoin Fundamentals Module 2: BLOCKCHAIN
Understanding the distributed ledger structure

Learning Goals:
- Understand how blocks are linked together
- See how cryptographic hashing secures the chain
- Explore block structure and contents
- Understand immutability and verification
"""

import hashlib
import json
import time
import requests
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

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
class SimpleBlock:
    """Educational representation of a Bitcoin block"""
    
    height: int                    # Block number in the chain
    hash: str                     # Block's unique identifier
    previous_hash: str            # Previous block's hash (creates the chain)
    merkle_root: str             # Root of transaction tree
    timestamp: int               # When block was created
    nonce: int                   # Proof-of-work number
    transactions: List[str]      # List of transaction IDs
    
    def __post_init__(self):
        """Calculate block hash after initialization"""
        if not self.hash:
            self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate block hash from its contents"""
        # Simplified version of how Bitcoin calculates block hash
        block_string = f"{self.previous_hash}{self.merkle_root}{self.timestamp}{self.nonce}"
        for tx in self.transactions:
            block_string += tx
            
        # Double SHA256 (like Bitcoin)
        hash1 = hashlib.sha256(block_string.encode()).hexdigest()
        hash2 = hashlib.sha256(hash1.encode()).hexdigest()
        return hash2
    
    def display_block(self):
        """Display block in human-readable format"""
        print(f"\n📦 BLOCK #{self.height}")
        print("="*50)
        print(f"🔗 Block Hash:     {self.hash}")
        print(f"🔙 Previous Hash:  {self.previous_hash}")
        print(f"🌳 Merkle Root:    {self.merkle_root}")
        print(f"🕐 Timestamp:      {time.ctime(self.timestamp)}")
        print(f"🎯 Nonce:          {self.nonce}")
        print(f"📊 Transactions:   {len(self.transactions)}")
        
        if self.transactions:
            print("   Transaction IDs:")
            for i, tx in enumerate(self.transactions[:3]):  # Show first 3
                print(f"     {i+1}. {tx[:16]}...")
            if len(self.transactions) > 3:
                print(f"     ... and {len(self.transactions) - 3} more")
        print("="*50)

class SimpleBlockchain:
    """Educational blockchain implementation"""
    
    def __init__(self):
        self.chain: List[SimpleBlock] = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis = SimpleBlock(
            height=0,
            hash="",  # Will be calculated
            previous_hash="0" * 64,  # Genesis has no previous block
            merkle_root="genesis_merkle_root",
            timestamp=int(time.time()),
            nonce=0,
            transactions=["genesis_coinbase_tx"]
        )
        self.chain.append(genesis)
        print("🌱 Genesis block created!")
    
    def add_block(self, transactions: List[str]) -> SimpleBlock:
        """Add a new block to the chain"""
        if not self.chain:
            raise Exception("No genesis block found!")
        
        previous_block = self.chain[-1]
        
        new_block = SimpleBlock(
            height=len(self.chain),
            hash="",  # Will be calculated
            previous_hash=previous_block.hash,
            merkle_root=self.calculate_merkle_root(transactions),
            timestamp=int(time.time()),
            nonce=0,  # In real Bitcoin, this would be found through mining
            transactions=transactions
        )
        
        self.chain.append(new_block)
        print(f"✅ Block #{new_block.height} added to chain!")
        return new_block
    
    def calculate_merkle_root(self, transactions: List[str]) -> str:
        """Simplified Merkle tree calculation"""
        if not transactions:
            return "empty_merkle_root"
        
        # In real Bitcoin, this is more complex
        # Here we just hash all transactions together
        combined = "".join(transactions)
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def validate_chain(self) -> bool:
        """Verify the entire blockchain is valid"""
        print("\n🔍 VALIDATING BLOCKCHAIN...")
        
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block points to previous block
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ Block #{i} has invalid previous hash!")
                return False
            
            # Check if block hash is correct
            calculated_hash = current_block.calculate_hash()
            if current_block.hash != calculated_hash:
                print(f"❌ Block #{i} has invalid hash!")
                return False
            
            print(f"✅ Block #{i} is valid")
        
        print("🎉 Entire blockchain is valid!")
        return True
    
    def display_chain(self):
        """Display the entire blockchain"""
        print(f"\n⛓️  BLOCKCHAIN OVERVIEW")
        print(f"📊 Total blocks: {len(self.chain)}")
        print(f"🔗 Chain structure:")
        
        for i, block in enumerate(self.chain):
            if i == 0:
                print(f"   🌱 Genesis → {block.hash[:8]}...")
            else:
                prev_hash = block.previous_hash[:8]
                curr_hash = block.hash[:8]
                print(f"   📦 Block #{i} → {prev_hash}... → {curr_hash}...")
    
    def find_block_by_hash(self, block_hash: str) -> Optional[SimpleBlock]:
        """Find a block by its hash"""
        for block in self.chain:
            if block.hash == block_hash:
                return block
        return None

def demonstrate_block_structure():
    """Show the anatomy of a Bitcoin block"""
    
    print("\n🔬 BITCOIN BLOCK ANATOMY")
    print("="*40)
    
    rpc = BitcoinRPC()
    
    try:
        # Get latest block from Polar
        best_hash = rpc.call("getbestblockhash")
        if best_hash:
            block_info = rpc.call("getblock", [best_hash])
            
            print("📦 REAL BITCOIN BLOCK STRUCTURE:")
            print(f"   🔢 Height: {block_info.get('height')}")
            print(f"   🔗 Hash: {block_info.get('hash')}")
            print(f"   🔙 Previous: {block_info.get('previousblockhash', 'N/A')}")
            print(f"   🌳 Merkle Root: {block_info.get('merkleroot')}")
            print(f"   🕐 Time: {time.ctime(block_info.get('time', 0))}")
            print(f"   🎯 Nonce: {block_info.get('nonce')}")
            print(f"   📊 Transactions: {len(block_info.get('tx', []))}")
            print(f"   📏 Size: {block_info.get('size')} bytes")
            print(f"   💪 Difficulty: {block_info.get('difficulty')}")
            
    except Exception as e:
        print(f"❌ Cannot connect to Bitcoin Core: {e}")
        print("💡 Using demo block instead...")
        
        # Create demo block
        demo_block = SimpleBlock(
            height=750000,
            hash="",
            previous_hash="0000000000000000000a1b2c3d4e5f6789abcdef" + "0" * 24,
            merkle_root="abc123def456789abc123def456789abc123def456789abc123def456789",
            timestamp=int(time.time()),
            nonce=1234567890,
            transactions=[
                "tx1_coinbase_reward",
                "tx2_alice_to_bob", 
                "tx3_charlie_to_diana",
                "tx4_exchange_deposit"
            ]
        )
        demo_block.display_block()

def demonstrate_chain_linking():
    """Show how blocks link together to form a chain"""
    
    print("\n🔗 HOW BLOCKS LINK TOGETHER")
    print("="*35)
    
    # Create a mini blockchain
    blockchain = SimpleBlockchain()
    
    print("\n1️⃣ Starting with Genesis block:")
    blockchain.chain[0].display_block()
    
    print("\n2️⃣ Adding Block #1:")
    block1_txs = ["tx_alice_pays_bob", "tx_charlie_pays_eve"]
    block1 = blockchain.add_block(block1_txs)
    block1.display_block()
    
    print(f"\n🔍 Notice how Block #1's 'Previous Hash' matches Genesis block's hash!")
    print(f"   Genesis Hash:  {blockchain.chain[0].hash}")
    print(f"   Block #1 Prev: {block1.previous_hash}")
    print(f"   Match? {'✅ YES' if blockchain.chain[0].hash == block1.previous_hash else '❌ NO'}")
    
    print("\n3️⃣ Adding Block #2:")
    block2_txs = ["tx_diana_pays_frank", "tx_mining_reward"]
    block2 = blockchain.add_block(block2_txs)
    block2.display_block()
    
    print("\n📊 Complete chain structure:")
    blockchain.display_chain()
    
    # Validate the chain
    blockchain.validate_chain()

def demonstrate_immutability():
    """Show why blockchain is immutable"""
    
    print("\n🛡️ BLOCKCHAIN IMMUTABILITY")
    print("="*30)
    
    # Create blockchain with some blocks
    blockchain = SimpleBlockchain()
    blockchain.add_block(["tx_legitimate_1", "tx_legitimate_2"])
    blockchain.add_block(["tx_legitimate_3", "tx_legitimate_4"])
    
    print("Original blockchain:")
    blockchain.display_chain()
    blockchain.validate_chain()
    
    print("\n😈 ATTACK SIMULATION: Let's try to tamper with Block #1")
    
    # Tamper with a transaction in the middle block
    print("   Changing transaction in Block #1...")
    blockchain.chain[1].transactions[0] = "tx_HACKED_steal_money"
    
    print("   Blockchain after tampering:")
    blockchain.display_chain()
    
    # Show that validation fails
    print("\n🔍 Validation after tampering:")
    is_valid = blockchain.validate_chain()
    
    if not is_valid:
        print("\n💡 KEY INSIGHT:")
        print("   • Changing ANY data in a block changes its hash")
        print("   • This breaks the link to the next block")
        print("   • The entire chain becomes invalid!")
        print("   • Everyone on the network would reject this chain")
    
    print("\n🛡️ This is why Bitcoin is tamper-proof!")
    print("   To change history, you'd need to:")
    print("   1. Recalculate the tampered block's hash")
    print("   2. Recalculate ALL subsequent blocks")
    print("   3. Do this faster than the honest network")
    print("   4. Convince majority of nodes to accept your version")

def blockchain_puzzle():
    """Interactive puzzle about blockchain mechanics"""
    
    print("\n🧩 BLOCKCHAIN DETECTIVE PUZZLE")
    print("="*35)
    
    # Create a blockchain with a problem
    blockchain = SimpleBlockchain()
    blockchain.add_block(["tx_alice_100", "tx_bob_200"])
    blockchain.add_block(["tx_charlie_150", "tx_diana_300"])
    blockchain.add_block(["tx_eve_250", "tx_frank_400"])
    
    # Introduce an error
    blockchain.chain[2].previous_hash = "corrupted_hash_12345"
    
    print("🔍 You are a Bitcoin node operator.")
    print("📦 You received a blockchain with 4 blocks.")
    print("🤔 Something seems wrong...")
    
    blockchain.display_chain()
    
    print("\n❓ QUESTIONS:")
    print("1. Which block has a problem?")
    print("2. What specifically is wrong?")
    print("3. How would you detect this automatically?")
    
    # Check if in test mode
    import os
    test_mode = os.environ.get('BITCOIN_TEST_MODE') == '1'
    
    if not test_mode:
        input("\nPress Enter to run validation...")
    else:
        print("\n🧪 Test mode: Running validation...")
    
    print("\n🤖 AUTOMATIC VALIDATION:")
    blockchain.validate_chain()
    
    print("\n💡 LESSON:")
    print("   • Every Bitcoin node validates every block")
    print("   • Invalid blocks are immediately rejected")
    print("   • The network only accepts the longest VALID chain")
    print("   • This prevents tampering and ensures consensus")

def explore_real_blockchain():
    """Explore the real Bitcoin blockchain via Polar"""
    
    print("\n🌐 EXPLORING REAL BLOCKCHAIN")
    print("="*32)
    
    rpc = BitcoinRPC()
    
    try:
        # Get blockchain info
        info = rpc.call("getblockchaininfo")
        if not info:
            print("❌ Cannot connect to Bitcoin Core")
            return
        
        print(f"📊 Current blockchain height: {info.get('blocks')}")
        print(f"🌐 Network: {info.get('chain')} (regtest for education)")
        print(f"💾 Chain size: {info.get('size_on_disk', 0) / 1024 / 1024:.2f} MB")
        
        # Show last few blocks
        current_height = info.get('blocks', 0)
        
        print(f"\n🔗 Last 5 blocks in the chain:")
        for i in range(max(0, current_height - 4), current_height + 1):
            try:
                block_hash = rpc.call("getblockhash", [i])
                block_info = rpc.call("getblock", [block_hash])
                
                print(f"   Block #{i}: {block_hash[:16]}... ({len(block_info.get('tx', []))} txs)")
                
                if i > 0:
                    # Verify this block points to previous
                    prev_hash = rpc.call("getblockhash", [i-1])
                    points_to_prev = block_info.get('previousblockhash') == prev_hash
                    print(f"      ↳ Links to previous: {'✅' if points_to_prev else '❌'}")
                    
            except Exception as e:
                print(f"   Block #{i}: Error - {e}")
        
        # Interactive exploration
        import os
        test_mode = os.environ.get('BITCOIN_TEST_MODE') == '1'
        
        if not test_mode:
            print(f"\n🔍 Want to explore a specific block?")
            try:
                height = input(f"Enter block height (0-{current_height}) or press Enter to skip: ").strip()
                if height:
                    height = int(height)
                    block_hash = rpc.call("getblockhash", [height])
                    block_info = rpc.call("getblock", [block_hash])
                    
                    print(f"\n📦 BLOCK #{height} DETAILS:")
                    print(f"   Hash: {block_info.get('hash')}")
                    print(f"   Previous: {block_info.get('previousblockhash', 'N/A')}")
                    print(f"   Merkle Root: {block_info.get('merkleroot')}")
                    print(f"   Time: {time.ctime(block_info.get('time', 0))}")
                    print(f"   Nonce: {block_info.get('nonce')}")
                    print(f"   Difficulty: {block_info.get('difficulty')}")
                    print(f"   Transactions: {len(block_info.get('tx', []))}")
                    
            except (ValueError, Exception) as e:
                print("Skipping block exploration")
        else:
            print(f"\n🧪 Test mode: Skipping interactive block exploration")
        
    except Exception as e:
        print(f"❌ Error exploring blockchain: {e}")

def main():
    """Main lesson function"""
    
    print("🎓 BITCOIN FUNDAMENTALS: BLOCKCHAIN")
    print("="*42)
    print("Understanding the distributed ledger structure")
    
    # Check if running in test mode
    import os
    test_mode = os.environ.get('BITCOIN_TEST_MODE') == '1'
    
    # Interactive lesson modules
    modules = [
        ("1. Block Structure", demonstrate_block_structure),
        ("2. Chain Linking", demonstrate_chain_linking),
        ("3. Immutability Demo", demonstrate_immutability),
        ("4. Blockchain Puzzle", blockchain_puzzle),
        ("5. Real Blockchain", explore_real_blockchain)
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
            
        # Check if in test mode
        import os
        test_mode = os.environ.get('BITCOIN_TEST_MODE') == '1'
        
        if not test_mode:
            input("\nPress Enter to continue to next module...")
        else:
            print("🧪 Test mode: Skipping to next module...")
    
    print("\n🎉 LESSON COMPLETE!")
    print("💡 Key takeaways:")
    print("  • Blocks contain transactions and link to previous blocks")
    print("  • Cryptographic hashes secure the chain structure")
    print("  • Changing any data breaks the chain (immutability)")
    print("  • Every node validates the entire blockchain")
    print("  • The longest valid chain is accepted as truth")

if __name__ == "__main__":
    main()