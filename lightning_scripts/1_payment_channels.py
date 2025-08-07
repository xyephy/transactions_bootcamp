#!/usr/bin/env python3
"""
Lightning Network: Payment Channels
====================================

This script demonstrates the fundamental concept of Lightning Network payment channels:
- How payment channels work
- Channel opening and closing
- Off-chain transactions
- Channel states and balances
- Commitment transactions

Key Learning Objectives:
- Understand bidirectional payment channels
- See how off-chain transactions work
- Learn about channel capacity and routing
- Experience real Lightning operations
"""

import requests
import json
import time
import os
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class ChannelInfo:
    """Information about a Lightning channel"""
    channel_id: str
    node1: str
    node2: str
    capacity: int
    local_balance: int
    remote_balance: int
    active: bool
    private: bool

class LightningChannelDemo:
    """Lightning Network payment channel demonstrations"""
    
    def __init__(self):
        # Polar Lightning Node configurations
                self.nodes = {
            "alice": {
                "rpc_host": "localhost",
                "rpc_port": "8081",  # REST API port
                "name": "Alice",
                "pubkey": None
            },
            "bob": {
                "rpc_host": "localhost", 
                "rpc_port": "8082",  # REST API port
                "name": "Bob",
                "pubkey": None
            },
            "carol": {
                "rpc_host": "localhost",
                "rpc_port": "8083",  # REST API port
                "name": "Carol",
                "pubkey": None
            }
        }
        
    def lnd_request(self, node: str, endpoint: str, data=None, method="GET"):
        """Make REST API request to LND node"""
        base_url = f"https://{self.nodes[node]['rpc_host']}:{self.nodes[node]['rpc_port']}"
        url = f"{base_url}{endpoint}"
        
        # Read macaroon for authentication (Polar setup)
        try:
            # Use the active network 17 that's currently running
            macaroon_path = f"/Users/{os.getenv('USER')}/.polar/networks/17/volumes/lnd/{node}/data/chain/bitcoin/regtest/admin.macaroon"
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
                print(f"❌ Request failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error connecting to {node}: {e}")
            return None
    
    def get_node_info(self, node: str):
        """Get basic node information"""
        info = self.lnd_request(node, "/v1/getinfo")
        if info:
            self.nodes[node]["pubkey"] = info.get("identity_pubkey")
            return info
        return None
    
    def get_wallet_balance(self, node: str):
        """Get node's on-chain wallet balance"""
        balance = self.lnd_request(node, "/v1/balance/blockchain")
        return balance
    
    def get_channel_balance(self, node: str):
        """Get node's Lightning channel balance"""
        balance = self.lnd_request(node, "/v1/balance/channels")
        return balance
    
    def list_channels(self, node: str):
        """List all channels for a node"""
        channels = self.lnd_request(node, "/v1/channels")
        return channels.get("channels", []) if channels else []
    
    def get_pending_channels(self, node: str):
        """Get pending channels (opening/closing)"""
        pending = self.lnd_request(node, "/v1/channels/pending")
        return pending if pending else {}
    
    def open_channel(self, from_node: str, to_node: str, amount_sats: int):
        """Open a payment channel between two nodes"""
        if not self.nodes[to_node]["pubkey"]:
            self.get_node_info(to_node)
            
        to_pubkey = self.nodes[to_node]["pubkey"]
        if not to_pubkey:
            print(f"❌ Could not get pubkey for {to_node}")
            return None
            
        data = {
            "node_pubkey_string": to_pubkey,
            "local_funding_amount": str(amount_sats),
            "push_sat": "0",
            "target_conf": 3,
            "sat_per_byte": "1"
        }
        
        result = self.lnd_request(from_node, "/v1/channels", data, "POST")
        return result
    
    def close_channel(self, node: str, channel_point: str):
        """Close a payment channel"""
        funding_txid, output_index = channel_point.split(":")
        endpoint = f"/v1/channels/{funding_txid}/{output_index}"
        
        # Use DELETE method for closing
        try:
            base_url = f"https://{self.nodes[node]['rpc_host']}:{self.nodes[node]['rpc_port']}"
            url = f"{base_url}{endpoint}"
            
            macaroon_path = f"/Users/{os.getenv('USER')}/.polar/networks/1/volumes/lnd/{node}/data/chain/bitcoin/regtest/admin.macaroon"
            with open(macaroon_path, 'rb') as f:
                macaroon = f.read().hex()
                
            headers = {
                'Grpc-Metadata-macaroon': macaroon,
                'Content-Type': 'application/json'
            }
            
            response = requests.delete(url, headers=headers, verify=False, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Close failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error closing channel: {e}")
            return None
    
    def send_payment(self, from_node: str, to_node: str, amount_sats: int, memo: str = ""):
        """Send a Lightning payment"""
        # First, create an invoice on the receiving node
        invoice_data = {
            "value": str(amount_sats),
            "memo": memo,
            "expiry": "3600"
        }
        
        invoice = self.lnd_request(to_node, "/v1/invoices", invoice_data, "POST")
        if not invoice:
            return None
            
        payment_request = invoice.get("payment_request")
        if not payment_request:
            print("❌ Could not create invoice")
            return None
            
        # Now send payment from the sending node
        payment_data = {
            "payment_request": payment_request
        }
        
        result = self.lnd_request(from_node, "/v1/channels/transactions", payment_data, "POST")
        return result
    
    def demonstrate_channel_lifecycle(self):
        """Demonstrate complete channel lifecycle"""
        print("\n🔗 LIGHTNING PAYMENT CHANNELS DEMO")
        print("=" * 50)
        print("Learning about:")
        print("• How payment channels work")
        print("• Channel opening and funding")
        print("• Off-chain transactions")
        print("• Channel closing")
        
        # Get node info
        print("\n📡 Getting node information...")
        for node in ["alice", "bob"]:
            info = self.get_node_info(node)
            if info:
                print(f"✅ {self.nodes[node]['name']}: {info['identity_pubkey'][:20]}...")
                print(f"   Synced: {info.get('synced_to_chain', False)}")
                print(f"   Blocks: {info.get('block_height', 0)}")
            else:
                print(f"❌ Could not connect to {node}")
                return
        
        # Check wallet balances
        print("\n💰 Checking on-chain balances...")
        for node in ["alice", "bob"]:
            balance = self.get_wallet_balance(node)
            if balance:
                total = int(balance.get("total_balance", 0))
                confirmed = int(balance.get("confirmed_balance", 0))
                print(f"💳 {self.nodes[node]['name']}: {confirmed:,} sats confirmed, {total:,} sats total")
        
        # List existing channels
        print("\n📋 Current channels:")
        alice_channels = self.list_channels("alice")
        bob_channels = self.list_channels("bob")
        
        if alice_channels or bob_channels:
            for channel in alice_channels:
                print(f"⚡ Alice channel: {channel['capacity']} sats, active: {channel['active']}")
            for channel in bob_channels:
                print(f"⚡ Bob channel: {channel['capacity']} sats, active: {channel['active']}")
        else:
            print("📭 No existing channels found")
        
        # Interactive channel operations
        if os.environ.get("BITCOIN_TEST_MODE") == "1":
            print("🧪 Test mode: Skipping interactive channel operations...")
            return
            
        print("\n🤔 What would you like to do?")
        print("1. Open a new channel")
        print("2. Send a Lightning payment")
        print("3. Close a channel")
        print("4. Show channel details")
        
        try:
            choice = input("Enter choice (1-4): ").strip()
            
            if choice == "1":
                self.interactive_channel_opening()
            elif choice == "2":
                self.interactive_payment()
            elif choice == "3":
                self.interactive_channel_closing()
            elif choice == "4":
                self.show_detailed_channel_info()
            else:
                print("Invalid choice")
                
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted")
    
    def interactive_channel_opening(self):
        """Interactive channel opening demonstration"""
        print("\n🔨 OPENING A PAYMENT CHANNEL")
        print("=" * 40)
        
        print("📚 Channel Opening Process:")
        print("1. Choose funding amount")
        print("2. Create funding transaction")
        print("3. Wait for confirmations")
        print("4. Channel becomes active")
        
        try:
            amount = input("Enter funding amount in sats (e.g., 1000000): ")
            amount_sats = int(amount)
            
            if amount_sats < 20000:
                print("❌ Minimum channel size is 20,000 sats")
                return
                
            print(f"\n⏳ Opening channel from Alice to Bob with {amount_sats:,} sats...")
            result = self.open_channel("alice", "bob", amount_sats)
            
            if result:
                funding_txid = result.get("funding_txid_str", "")
                print(f"✅ Channel opening initiated!")
                print(f"📄 Funding transaction: {funding_txid}")
                print(f"⏰ Waiting for confirmations...")
                
                # Check pending channels
                time.sleep(2)
                pending = self.get_pending_channels("alice")
                if pending.get("pending_open_channels"):
                    channel = pending["pending_open_channels"][0]
                    print(f"📊 Pending channel capacity: {channel['channel']['capacity']} sats")
                    print(f"🔗 Channel point: {channel['channel']['channel_point']}")
            else:
                print("❌ Failed to open channel")
                
        except ValueError:
            print("❌ Invalid amount")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def interactive_payment(self):
        """Interactive Lightning payment demonstration"""
        print("\n⚡ LIGHTNING PAYMENT")
        print("=" * 30)
        
        print("📚 Lightning Payment Process:")
        print("1. Recipient creates invoice")
        print("2. Sender pays invoice")
        print("3. Payment routes through channels")
        print("4. Balances update instantly")
        
        try:
            amount = input("Enter payment amount in sats: ")
            amount_sats = int(amount)
            memo = input("Enter payment memo (optional): ")
            
            print(f"\n💸 Sending {amount_sats} sats from Alice to Bob...")
            result = self.send_payment("alice", "bob", amount_sats, memo)
            
            if result:
                if result.get("payment_error"):
                    print(f"❌ Payment failed: {result['payment_error']}")
                else:
                    print("✅ Payment sent successfully!")
                    print("⚡ This was an off-chain transaction - instant and cheap!")
            else:
                print("❌ Payment failed")
                
        except ValueError:
            print("❌ Invalid amount")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def interactive_channel_closing(self):
        """Interactive channel closing demonstration"""
        print("\n🔒 CLOSING A PAYMENT CHANNEL")
        print("=" * 40)
        
        # List available channels
        channels = self.list_channels("alice")
        if not channels:
            print("❌ No channels to close")
            return
            
        print("Available channels:")
        for i, channel in enumerate(channels):
            print(f"{i+1}. Capacity: {channel['capacity']} sats, Remote: {channel['remote_pubkey'][:20]}...")
        
        try:
            choice = int(input("Enter channel number to close: ")) - 1
            if 0 <= choice < len(channels):
                channel = channels[choice]
                channel_point = channel["channel_point"]
                
                print(f"\n⏳ Closing channel {channel_point}...")
                result = self.close_channel("alice", channel_point)
                
                if result:
                    print("✅ Channel close initiated!")
                    print("⏰ Waiting for closing transaction to confirm...")
                else:
                    print("❌ Failed to close channel")
            else:
                print("❌ Invalid choice")
                
        except ValueError:
            print("❌ Invalid input")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def show_detailed_channel_info(self):
        """Show detailed channel information"""
        print("\n📊 DETAILED CHANNEL INFORMATION")
        print("=" * 45)
        
        for node in ["alice", "bob"]:
            print(f"\n👤 {self.nodes[node]['name']}'s channels:")
            channels = self.list_channels(node)
            
            if not channels:
                print("   📭 No channels")
                continue
                
            for channel in channels:
                print(f"   ⚡ Channel ID: {channel['chan_id']}")
                print(f"   💰 Capacity: {int(channel['capacity']):,} sats")
                print(f"   📈 Local Balance: {int(channel['local_balance']):,} sats")
                print(f"   📉 Remote Balance: {int(channel['remote_balance']):,} sats")
                print(f"   🟢 Active: {channel['active']}")
                print(f"   🔒 Private: {channel['private']}")
                print(f"   📍 Remote Node: {channel['remote_pubkey'][:20]}...")
                print(f"   🔗 Channel Point: {channel['channel_point']}")
                print("   " + "-" * 40)
    
    def channel_concepts_quiz(self):
        """Interactive quiz about payment channel concepts"""
        print("\n🧠 PAYMENT CHANNEL CONCEPTS QUIZ")
        print("=" * 45)
        
        questions = [
            {
                "question": "What happens when you send a Lightning payment?",
                "options": [
                    "A. A new Bitcoin transaction is broadcast",
                    "B. Channel balances are updated off-chain",
                    "C. The payment goes through the mempool",
                    "D. Miners need to confirm it"
                ],
                "answer": "B",
                "explanation": "Lightning payments update channel balances off-chain instantly, without needing blockchain confirmations!"
            },
            {
                "question": "Why do channels need to be funded on-chain?",
                "options": [
                    "A. To pay Lightning Network fees",
                    "B. To secure the channel with real Bitcoin",
                    "C. To register with Lightning routers",
                    "D. To create payment invoices"
                ],
                "answer": "B", 
                "explanation": "Channels are secured by real Bitcoin locked in a 2-of-2 multisig transaction on the blockchain."
            },
            {
                "question": "What is channel capacity?",
                "options": [
                    "A. Maximum number of payments per second",
                    "B. Total Bitcoin locked in the channel",
                    "C. Number of HTLCs allowed",
                    "D. Channel connection speed"
                ],
                "answer": "B",
                "explanation": "Channel capacity is the total amount of Bitcoin locked in the channel, which can be sent back and forth."
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
            print("🏆 Perfect! You understand payment channels!")
        elif score >= len(questions) * 0.7:
            print("👍 Great job! You have a good grasp of the concepts!")
        else:
            print("📚 Keep learning! Payment channels are fundamental to Lightning.")

def main():
    """Main function for payment channels demo"""
    print("🚀 Welcome to Lightning Network Payment Channels!")
    
    demo = LightningChannelDemo()
    
    try:
        demo.demonstrate_channel_lifecycle()
        
        if os.environ.get("BITCOIN_TEST_MODE") != "1":
            print("\n🎓 Ready for a quick quiz?")
            quiz_choice = input("Take the payment channels quiz? (y/n): ").lower().strip()
            if quiz_choice == 'y':
                demo.channel_concepts_quiz()
        else:
            demo.channel_concepts_quiz()
            
    except KeyboardInterrupt:
        print("\n👋 Payment channels demo ended")
    except Exception as e:
        print(f"\n❌ Error in demo: {e}")

if __name__ == "__main__":
    main()