#!/usr/bin/env python3
"""
Bitcoin Fundamentals Module 1: TRANSACTIONS
How Bitcoin moves value between addresses

Learning Goals:
- Understand UTXO (Unspent Transaction Output) model
- See how transactions are structured
- Create and analyze real Bitcoin transactions
- Understand inputs, outputs, and change
"""

import hashlib
import json
import requests
from dataclasses import dataclass
from typing import List, Dict, Any

# Bitcoin Core RPC connection (via Polar)
RPC_USER = "polaruser"
RPC_PASS = "polarpass" 
RPC_HOST = "localhost"
RPC_PORT = "18443"  # Polar's Bitcoin Core regtest port

class BitcoinRPC:
    """Simple Bitcoin Core RPC client for Polar"""
    
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
class TransactionInput:
    """Represents a transaction input (spending a UTXO)"""
    txid: str          # Previous transaction ID
    vout: int          # Output index in previous transaction  
    amount: float      # Amount being spent (for reference)
    address: str       # Address that owns this UTXO

@dataclass  
class TransactionOutput:
    """Represents a transaction output (creating new UTXO)"""
    address: str       # Recipient address
    amount: float      # Amount to send

class BitcoinTransaction:
    """Educational Bitcoin transaction class"""
    
    def __init__(self, rpc_client: BitcoinRPC):
        self.rpc = rpc_client
        self.inputs: List[TransactionInput] = []
        self.outputs: List[TransactionOutput] = []
        
    def add_input(self, txid: str, vout: int, amount: float, address: str):
        """Add an input to spend"""
        input_utxo = TransactionInput(txid, vout, amount, address)
        self.inputs.append(input_utxo)
        print(f"📥 Added input: {amount} BTC from {address}")
        
    def add_output(self, address: str, amount: float):
        """Add an output to create"""
        output = TransactionOutput(address, amount)
        self.outputs.append(output)
        print(f"📤 Added output: {amount} BTC to {address}")
        
    def get_total_input(self) -> float:
        """Calculate total input amount"""
        return sum(inp.amount for inp in self.inputs)
    
    def get_total_output(self) -> float:
        """Calculate total output amount"""
        return sum(out.amount for out in self.outputs)
        
    def get_fee(self) -> float:
        """Calculate transaction fee (input - output)"""
        return self.get_total_input() - self.get_total_output()
    
    def display_transaction(self):
        """Display transaction details in human-readable format"""
        print("\n" + "="*60)
        print("🧾 BITCOIN TRANSACTION ANALYSIS")
        print("="*60)
        
        print("\n📥 INPUTS (Money being spent):")
        for i, inp in enumerate(self.inputs):
            print(f"  {i+1}. {inp.amount:8.8f} BTC from {inp.address}")
            print(f"     └─ Previous TX: {inp.txid[:16]}...#{inp.vout}")
        
        print(f"\n📊 Total Input:  {self.get_total_input():8.8f} BTC")
        
        print("\n📤 OUTPUTS (New money destinations):")
        for i, out in enumerate(self.outputs):
            print(f"  {i+1}. {out.amount:8.8f} BTC to   {out.address}")
        
        print(f"\n📊 Total Output: {self.get_total_output():8.8f} BTC")
        print(f"💰 Transaction Fee: {self.get_fee():8.8f} BTC")
        
        # UTXO explanation
        print("\n🎯 EDUCATIONAL NOTES:")
        print("• Each input spends a complete UTXO (Unspent Transaction Output)")
        print("• You cannot spend 'part' of a UTXO - must spend the whole thing")
        print("• If you don't need all the money, send change back to yourself")
        print("• Fee = Total Input - Total Output (goes to miners)")
        print("="*60)

def demonstrate_utxo_model():
    """Interactive demonstration of Bitcoin's UTXO model"""
    
    print("\n🎯 UNDERSTANDING BITCOIN'S UTXO MODEL")
    print("="*50)
    print("Bitcoin doesn't have 'account balances' like banks.")
    print("Instead, it tracks individual 'coins' called UTXOs.")
    print("\nThink of UTXOs like physical cash bills:")
    print("- You have a $20 bill, $10 bill, $5 bill")
    print("- To pay $15, you might use the $20 bill and get $5 change")
    print("- You can't 'break' a $20 bill without a transaction")
    
    # Create example transaction
    rpc = BitcoinRPC()
    tx = BitcoinTransaction(rpc)
    
    print("\n💡 EXAMPLE: Alice wants to send 0.15 BTC to Bob")
    print("Alice has these UTXOs (unspent coins):")
    print("  • 0.1 BTC from previous transaction A") 
    print("  • 0.08 BTC from previous transaction B")
    print("  • 0.03 BTC from previous transaction C")
    
    # Alice needs to combine UTXOs to have enough
    tx.add_input("txA123...", 0, 0.1, "Alice's address")
    tx.add_input("txB456...", 1, 0.08, "Alice's address") 
    # Total input: 0.18 BTC (enough for 0.15 BTC payment)
    
    # Create outputs
    tx.add_output("Bob's address", 0.15)      # Payment to Bob
    tx.add_output("Alice's change address", 0.025)  # Change back to Alice
    # Fee: 0.18 - 0.15 - 0.025 = 0.005 BTC
    
    tx.display_transaction()
    
    print("\n🤔 STUDENT QUESTIONS:")
    print("1. Why did Alice need TWO inputs for this payment?")
    print("2. What happens to the 0.03 BTC UTXO she didn't use?") 
    print("3. Who gets the 0.005 BTC transaction fee?")

def analyze_real_transaction():
    """Analyze a real transaction from the Polar network"""
    
    print("\n🔍 ANALYZING REAL TRANSACTIONS")
    print("="*40)
    
    rpc = BitcoinRPC()
    
    # Get latest block
    try:
        best_block_hash = rpc.call("getbestblockhash")
        if not best_block_hash:
            print("❌ Cannot connect to Bitcoin Core. Is Polar running?")
            return
            
        block_info = rpc.call("getblock", [best_block_hash])
        print(f"📦 Latest Block: {block_info['height']}")
        print(f"🕐 Block Time: {block_info['time']}")
        print(f"📊 Transactions in block: {len(block_info['tx'])}")
        
        # Analyze first transaction (usually coinbase)
        if block_info['tx']:
            txid = block_info['tx'][0]
            tx_info = rpc.call("getrawtransaction", [txid, True])
            
            print(f"\n🧾 Transaction Analysis: {txid[:16]}...")
            print(f"📏 Size: {tx_info.get('size', 0)} bytes")
            print(f"💰 Fee: {tx_info.get('fee', 0)} BTC")
            
            print(f"\n📥 Inputs: {len(tx_info['vin'])}")
            for i, inp in enumerate(tx_info['vin']):
                if 'coinbase' in inp:
                    print(f"  {i+1}. COINBASE (mining reward)")
                else:
                    print(f"  {i+1}. From TX: {inp.get('txid', 'N/A')}")
            
            print(f"\n📤 Outputs: {len(tx_info['vout'])}")
            for i, out in enumerate(tx_info['vout']):
                amount = out['value']
                addresses = out['scriptPubKey'].get('addresses', ['Unknown'])
                print(f"  {i+1}. {amount:8.8f} BTC to {addresses[0] if addresses else 'Script'}")
                
    except Exception as e:
        print(f"❌ Error analyzing transactions: {e}")
        print("💡 Make sure Polar is running with Bitcoin Core node")

def transaction_puzzle():
    """Interactive puzzle for students to solve"""
    
    print("\n🧩 TRANSACTION PUZZLE")
    print("="*30)
    print("Help Charlie make a payment!")
    print("\nCharlie's UTXOs:")
    print("  A: 0.25 BTC")
    print("  B: 0.15 BTC") 
    print("  C: 0.05 BTC")
    print("  D: 0.03 BTC")
    
    print("\nCharlie wants to:")
    print("  • Send 0.2 BTC to Diana")
    print("  • Pay 0.01 BTC transaction fee")
    print("  • Get change back to himself")
    
    print("\n❓ QUESTIONS:")
    print("1. Which UTXOs should Charlie use as inputs?")
    print("2. What will be the change amount?")
    print("3. Design the complete transaction")
    
    # Wait for student input
    import os
    test_mode = os.environ.get('BITCOIN_TEST_MODE') == '1'
    
    if not test_mode:
        input("\nPress Enter when ready to see the solution...")
    else:
        print("\n🧪 Test mode: Showing solution...")
    
    print("\n✅ SOLUTION:")
    solution_tx = BitcoinTransaction(BitcoinRPC())
    solution_tx.add_input("utxo_A", 0, 0.25, "Charlie's address")
    solution_tx.add_output("Diana's address", 0.2)
    solution_tx.add_output("Charlie's change address", 0.04)  # 0.25 - 0.2 - 0.01 fee
    
    solution_tx.display_transaction()
    
    print("\n💡 Alternative solutions exist! Charlie could also use:")
    print("   • UTXOs B + C (0.15 + 0.05 = 0.2, exact amount)")
    print("   • UTXOs A + D, or other combinations")

def interactive_transaction_builder():
    """Let students build their own transaction"""
    
    print("\n🏗️ BUILD YOUR OWN TRANSACTION")
    print("="*35)
    
    tx = BitcoinTransaction(BitcoinRPC())
    
    # Check if in test mode
    import os
    test_mode = os.environ.get('BITCOIN_TEST_MODE') == '1'
    
    if test_mode:
        print("🧪 Test mode: Building demo transaction...")
        # Auto-build transaction for testing
        tx.add_input("demo_tx_1_abc123", 0, 0.1, "Alice's address")
        tx.add_input("demo_tx_2_def456", 1, 0.08, "Alice's address") 
        tx.add_output("Bob's address", 0.15)
        tx.add_output("Alice's change address", 0.025)
        tx.display_transaction()
        return
    
    print("Let's create a transaction step by step!")
    
    # Add inputs
    while True:
        print(f"\nCurrent inputs: {len(tx.inputs)}")
        add_input = input("Add an input? (y/n): ").lower().strip()
        
        if add_input != 'y':
            break
            
        try:
            txid = input("Previous transaction ID (or press Enter for demo): ").strip()
            if not txid:
                txid = f"demo_tx_{len(tx.inputs)}_" + "a"*56
                
            vout = int(input("Output index (0, 1, 2, etc.): ") or "0")
            amount = float(input("Amount in BTC: "))
            address = input("Your address (or press Enter for demo): ").strip()
            if not address:
                address = f"demo_address_{len(tx.inputs)}"
                
            tx.add_input(txid, vout, amount, address)
            
        except ValueError:
            print("❌ Invalid input, try again")
    
    # Add outputs  
    while True:
        print(f"\nCurrent outputs: {len(tx.outputs)}")
        add_output = input("Add an output? (y/n): ").lower().strip()
        
        if add_output != 'y':
            break
            
        try:
            address = input("Recipient address: ").strip() or f"recipient_{len(tx.outputs)}"
            amount = float(input("Amount to send: "))
            
            tx.add_output(address, amount)
            
        except ValueError:
            print("❌ Invalid amount, try again")
    
    # Show final transaction
    if tx.inputs and tx.outputs:
        tx.display_transaction()
        
        # Validate transaction
        if tx.get_fee() < 0:
            print("⚠️ WARNING: Negative fee! You're trying to spend more than you have.")
        elif tx.get_fee() == 0:
            print("⚠️ WARNING: Zero fee! Miners might not include this transaction.")
        elif tx.get_fee() > 0.01:
            print("⚠️ WARNING: Very high fee! Double-check your amounts.")
        else:
            print("✅ Transaction looks valid!")
    else:
        print("❌ Transaction needs at least one input and one output")

def main():
    """Main lesson function"""
    
    print("🎓 BITCOIN FUNDAMENTALS: TRANSACTIONS")
    print("="*45)
    print("Understanding how Bitcoin moves value")
    
    # Check if running in test mode
    import os
    test_mode = os.environ.get('BITCOIN_TEST_MODE') == '1'
    
    try:
        # Check connection to Polar
        rpc = BitcoinRPC()
        info = rpc.call("getblockchaininfo")
        if info:
            print(f"✅ Connected to Bitcoin Core (Block: {info.get('blocks', 0)})")
        else:
            print("❌ Cannot connect to Bitcoin Core")
            print("💡 Make sure Polar is running with Bitcoin Core node")
            if not test_mode:
                return
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("💡 Using demo mode for educational purposes")
    
    # Interactive lesson modules
    modules = [
        ("1. Understanding UTXOs", demonstrate_utxo_model),
        ("2. Real Transaction Analysis", analyze_real_transaction), 
        ("3. Transaction Puzzle", transaction_puzzle),
        ("4. Build Your Transaction", interactive_transaction_builder)
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
            
        if not test_mode:
            input("\nPress Enter to continue to next module...")
        else:
            print("🧪 Test mode: Skipping to next module...")
    
    print("\n🎉 LESSON COMPLETE!")
    print("💡 Key takeaways:")
    print("  • Bitcoin uses UTXOs, not account balances")
    print("  • Transactions have inputs (spending) and outputs (receiving)")
    print("  • You must spend entire UTXOs, use change for remainder")
    print("  • Fees = Total Input - Total Output")
    print("  • Every Bitcoin transaction follows these rules!")

if __name__ == "__main__":
    main()