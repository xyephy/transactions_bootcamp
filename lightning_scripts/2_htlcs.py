#!/usr/bin/env python3
"""
Lightning Network: HTLCs (Hash Time-Locked Contracts)
=====================================================

This script demonstrates Hash Time-Locked Contracts (HTLCs), the building blocks of Lightning payments:
- How HTLCs enable trustless payments
- Hash preimages and secrets
- Time locks and expiration
- Multi-hop payment routing
- Atomic payments across multiple channels

Key Learning Objectives:
- Understand how HTLCs work
- See the hash preimage mechanism
- Learn about time locks
- Experience atomic multi-hop payments
"""

import hashlib
import secrets
import time
import os
import json
from typing import Dict, List, Optional, Tuple

class HTLCDemo:
    """HTLC (Hash Time-Locked Contract) demonstrations"""
    
    def __init__(self):
        self.htlcs = {}  # Store active HTLCs for demo
        self.secrets = {}  # Store secrets for demo
        
    def generate_secret_and_hash(self) -> Tuple[bytes, str]:
        """Generate a random secret and its SHA256 hash"""
        secret = secrets.token_bytes(32)  # 32 random bytes
        hash_hex = hashlib.sha256(secret).hexdigest()
        return secret, hash_hex
    
    def create_htlc(self, amount: int, payment_hash: str, expiry_blocks: int = 144) -> Dict:
        """Create an HTLC (conceptual representation)"""
        htlc = {
            "amount": amount,
            "payment_hash": payment_hash,
            "expiry_blocks": expiry_blocks,
            "created_at": int(time.time()),
            "status": "pending"
        }
        return htlc
    
    def demonstrate_htlc_basics(self):
        """Demonstrate basic HTLC concepts"""
        print("\n🔐 HTLC BASICS DEMONSTRATION")
        print("=" * 45)
        print("HTLCs are the magic behind Lightning payments!")
        print("\n📚 What makes HTLCs special:")
        print("• Hash Lock: Payment requires a secret")
        print("• Time Lock: Automatic refund after timeout")
        print("• Atomic: Either complete or fully revert")
        print("• Trustless: No need to trust intermediaries")
        
        print("\n🎯 Let's create an HTLC step by step...")
        
        # Step 1: Generate secret and hash
        print("\n1️⃣ GENERATING SECRET AND HASH")
        secret, payment_hash = self.generate_secret_and_hash()
        print(f"🔑 Secret: {secret.hex()}")
        print(f"🔒 Hash (SHA256): {payment_hash}")
        print("💡 The hash is public, but the secret is kept private!")
        
        # Step 2: Create HTLC
        print("\n2️⃣ CREATING HTLC")
        amount = 1000  # sats
        htlc = self.create_htlc(amount, payment_hash, 144)
        print(f"⚡ HTLC created for {amount} sats")
        print(f"🔒 Payment Hash: {payment_hash}")
        print(f"⏰ Expires in: {htlc['expiry_blocks']} blocks")
        print("💰 Funds are now locked!")
        
        # Step 3: Show HTLC conditions
        print("\n3️⃣ HTLC CONDITIONS")
        print("The HTLC can be claimed if:")
        print(f"  ✅ Correct secret is provided (preimage of {payment_hash[:16]}...)")
        print(f"  ✅ Before block timeout ({htlc['expiry_blocks']} blocks)")
        print("\nOtherwise:")
        print("  🔄 Funds automatically return to sender after timeout")
        
        if os.environ.get("BITCOIN_TEST_MODE") == "1":
            print("🧪 Test mode: Auto-completing HTLC...")
            return self.resolve_htlc_demo(htlc, secret, payment_hash)
        
        # Interactive resolution
        print("\n🤔 What should we do with this HTLC?")
        print("1. Claim with correct secret")
        print("2. Try to claim with wrong secret")
        print("3. Let it timeout")
        
        try:
            choice = input("Enter choice (1-3): ").strip()
            if choice == "1":
                return self.resolve_htlc_demo(htlc, secret, payment_hash)
            elif choice == "2":
                return self.resolve_htlc_demo(htlc, secrets.token_bytes(32), payment_hash)
            elif choice == "3":
                return self.timeout_htlc_demo(htlc)
            else:
                print("Invalid choice")
        except KeyboardInterrupt:
            print("\n👋 HTLC demo interrupted")
    
    def resolve_htlc_demo(self, htlc: Dict, secret: bytes, expected_hash: str):
        """Demonstrate HTLC resolution with secret"""
        print("\n4️⃣ HTLC RESOLUTION")
        print("=" * 25)
        
        # Verify the secret
        provided_hash = hashlib.sha256(secret).hexdigest()
        print(f"🔑 Provided secret: {secret.hex()}")
        print(f"🔒 Hash of secret: {provided_hash}")
        print(f"🎯 Expected hash: {expected_hash}")
        
        if provided_hash == expected_hash:
            print("✅ HTLC CLAIMED SUCCESSFULLY!")
            print("💰 Payment complete - funds released!")
            print("🎉 This is how Lightning payments work atomically!")
            htlc["status"] = "claimed"
        else:
            print("❌ WRONG SECRET!")
            print("🔒 HTLC remains locked")
            print("💡 This prevents theft - only the right secret works!")
            htlc["status"] = "failed"
        
        return htlc
    
    def timeout_htlc_demo(self, htlc: Dict):
        """Demonstrate HTLC timeout scenario"""
        print("\n4️⃣ HTLC TIMEOUT")
        print("=" * 20)
        print("⏰ Time has passed... HTLC expired!")
        print("🔄 Funds automatically return to sender")
        print("💡 This prevents funds from being locked forever!")
        htlc["status"] = "timeout"
        return htlc
    
    def demonstrate_multi_hop_htlcs(self):
        """Demonstrate how HTLCs enable multi-hop payments"""
        print("\n🔗 MULTI-HOP HTLC DEMONSTRATION")
        print("=" * 45)
        print("How payments route through multiple channels...")
        
        # Setup the scenario
        print("\n📋 SCENARIO:")
        print("Alice wants to pay Dave 1000 sats")
        print("Route: Alice → Bob → Charlie → Dave")
        print("Each hop uses the SAME payment hash!")
        
        # Generate payment details
        secret, payment_hash = self.generate_secret_and_hash()
        amount = 1000
        
        print(f"\n🎯 Payment Details:")
        print(f"💰 Amount: {amount} sats")
        print(f"🔒 Payment Hash: {payment_hash}")
        print(f"🔑 Secret (only Dave knows): {secret.hex()}")
        
        # Create HTLCs for each hop
        hops = [
            {"from": "Alice", "to": "Bob", "amount": 1003},    # +3 sats fee
            {"from": "Bob", "to": "Charlie", "amount": 1002},  # +2 sats fee  
            {"from": "Charlie", "to": "Dave", "amount": 1000}, # final amount
        ]
        
        print("\n⚡ CREATING HTLCs FOR EACH HOP:")
        hop_htlcs = []
        for i, hop in enumerate(hops, 1):
            htlc = self.create_htlc(hop["amount"], payment_hash, 144-i*6)  # Decreasing timeouts
            hop_htlcs.append(htlc)
            print(f"{i}. {hop['from']} → {hop['to']}: {hop['amount']} sats (timeout: {htlc['expiry_blocks']} blocks)")
        
        print("\n🔒 All HTLCs use the SAME payment hash!")
        print("💡 This ensures atomicity - either all succeed or all fail!")
        
        if os.environ.get("BITCOIN_TEST_MODE") == "1":
            print("🧪 Test mode: Auto-completing multi-hop payment...")
            return self.complete_multi_hop_demo(hop_htlcs, hops, secret, payment_hash)
        
        print("\n🤔 What happens next?")
        print("1. Dave claims payment (reveals secret)")
        print("2. Payment fails (wrong secret)")
        
        try:
            choice = input("Enter choice (1-2): ").strip()
            if choice == "1":
                return self.complete_multi_hop_demo(hop_htlcs, hops, secret, payment_hash)
            elif choice == "2":
                return self.fail_multi_hop_demo(hop_htlcs, hops)
        except KeyboardInterrupt:
            print("\n👋 Multi-hop demo interrupted")
    
    def complete_multi_hop_demo(self, hop_htlcs: List[Dict], hops: List[Dict], secret: bytes, payment_hash: str):
        """Demonstrate successful multi-hop payment completion"""
        print("\n✅ MULTI-HOP PAYMENT SUCCESS!")
        print("=" * 35)
        
        # Dave claims the payment
        print("1️⃣ Dave receives payment and reveals secret:")
        provided_hash = hashlib.sha256(secret).hexdigest()
        print(f"   🔑 Secret revealed: {secret.hex()}")
        print(f"   ✅ Hash matches: {provided_hash == payment_hash}")
        print("   💰 Dave receives 1000 sats")
        
        # Backward propagation
        print("\n2️⃣ Secret propagates backward through route:")
        for i in reversed(range(len(hops))):
            hop = hops[i]
            htlc = hop_htlcs[i]
            print(f"   {hop['to']} → {hop['from']}: Claims {htlc['amount']} sats with secret")
            htlc["status"] = "claimed"
            time.sleep(0.5)  # Dramatic effect
        
        print("\n🎉 PAYMENT COMPLETE!")
        print("✨ All HTLCs resolved atomically")
        print("💰 Everyone got paid their fees")
        print("🔒 The secret enabled trustless routing!")
        
        return hop_htlcs
    
    def fail_multi_hop_demo(self, hop_htlcs: List[Dict], hops: List[Dict]):
        """Demonstrate multi-hop payment failure"""
        print("\n❌ MULTI-HOP PAYMENT FAILURE!")
        print("=" * 35)
        
        print("Dave doesn't claim the payment (wrong secret/timeout)")
        print("\n🔄 HTLCs timeout in reverse order:")
        
        for i in reversed(range(len(hops))):
            hop = hops[i]
            htlc = hop_htlcs[i]
            print(f"   {hop['from']} → {hop['to']}: HTLC expires, funds return to {hop['from']}")
            htlc["status"] = "timeout"
            time.sleep(0.5)
        
        print("\n💡 KEY INSIGHT:")
        print("🔒 No one lost money!")
        print("🔄 All funds returned safely")
        print("⚛️ Atomicity protects everyone!")
        
        return hop_htlcs
    
    def demonstrate_htlc_security(self):
        """Demonstrate HTLC security properties"""
        print("\n🛡️ HTLC SECURITY DEMONSTRATION")
        print("=" * 45)
        
        scenarios = [
            {
                "name": "Honest Payment",
                "description": "Receiver provides correct secret",
                "action": "success"
            },
            {
                "name": "Wrong Secret Attack",
                "description": "Attacker tries random secret",
                "action": "fail_wrong_secret"
            },
            {
                "name": "Timeout Protection",
                "description": "What if receiver doesn't claim?",
                "action": "timeout"
            },
            {
                "name": "Double Spend Attempt", 
                "description": "Can the same secret be used twice?",
                "action": "explain_reuse"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{i}️⃣ SCENARIO: {scenario['name']}")
            print(f"📝 {scenario['description']}")
            
            if scenario['action'] == 'success':
                secret, payment_hash = self.generate_secret_and_hash()
                htlc = self.create_htlc(1000, payment_hash)
                print("✅ Correct secret provided → Payment succeeds")
                
            elif scenario['action'] == 'fail_wrong_secret':
                secret, payment_hash = self.generate_secret_and_hash()
                wrong_secret = secrets.token_bytes(32)
                wrong_hash = hashlib.sha256(wrong_secret).hexdigest()
                print(f"❌ Wrong hash: {wrong_hash}")
                print(f"🎯 Expected: {payment_hash}")
                print("🔒 Payment fails - funds stay locked")
                
            elif scenario['action'] == 'timeout':
                print("⏰ Time expires → Funds return to sender")
                print("🛡️ No money lost, just delayed")
                
            elif scenario['action'] == 'explain_reuse':
                print("🔄 Each payment uses a unique hash")
                print("🆔 Secret reuse would reveal payment correlation")
                print("🔒 Fresh secrets ensure privacy")
            
            if not os.environ.get("BITCOIN_TEST_MODE") == "1":
                input("   Press Enter to continue...")
    
    def htlc_quiz(self):
        """Interactive quiz about HTLC concepts"""
        print("\n🧠 HTLC CONCEPTS QUIZ")
        print("=" * 30)
        
        questions = [
            {
                "question": "What are the two locks in an HTLC?",
                "options": [
                    "A. Hash lock and amount lock",
                    "B. Hash lock and time lock", 
                    "C. Time lock and signature lock",
                    "D. Address lock and time lock"
                ],
                "answer": "B",
                "explanation": "HTLCs have a hash lock (requires secret) and time lock (automatic timeout)."
            },
            {
                "question": "Why do multi-hop payments use the SAME payment hash?",
                "options": [
                    "A. To save bandwidth",
                    "B. To ensure atomicity",
                    "C. To reduce fees", 
                    "D. To increase speed"
                ],
                "answer": "B",
                "explanation": "The same hash ensures all HTLCs succeed or fail together - atomic payments!"
            },
            {
                "question": "What happens if an HTLC times out?",
                "options": [
                    "A. Funds are lost forever",
                    "B. Funds go to miners",
                    "C. Funds return to sender",
                    "D. Payment succeeds anyway"
                ],
                "answer": "C", 
                "explanation": "Timeouts protect senders - funds automatically return if not claimed."
            },
            {
                "question": "Who generates the payment hash?",
                "options": [
                    "A. The sender",
                    "B. The receiver", 
                    "C. A random router",
                    "D. The Lightning Network"
                ],
                "answer": "B",
                "explanation": "The receiver creates a secret, hashes it, and shares only the hash in the invoice."
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
            print("🏆 Perfect! You're an HTLC expert!")
        elif score >= len(questions) * 0.7:
            print("👍 Great job! You understand HTLCs well!")
        else:
            print("📚 Keep studying! HTLCs are the heart of Lightning.")
    
    def interactive_htlc_builder(self):
        """Interactive HTLC creation and management"""
        print("\n🔨 INTERACTIVE HTLC BUILDER")
        print("=" * 40)
        
        if os.environ.get("BITCOIN_TEST_MODE") == "1":
            print("🧪 Test mode: Building demo HTLC...")
            secret, payment_hash = self.generate_secret_and_hash()
            htlc = self.create_htlc(5000, payment_hash, 100)
            print(f"🔒 Demo HTLC: {htlc['amount']} sats, hash: {payment_hash[:16]}...")
            return
        
        print("Let's build your own HTLC!")
        
        try:
            # Get HTLC parameters
            amount = int(input("Enter amount in sats: "))
            timeout = int(input("Enter timeout in blocks (default 144): ") or "144")
            
            # Generate or provide hash
            hash_choice = input("Generate new secret (g) or provide hash (h)? ").lower().strip()
            
            if hash_choice == 'g':
                secret, payment_hash = self.generate_secret_and_hash()
                print(f"🔑 Generated secret: {secret.hex()}")
                print(f"🔒 Payment hash: {payment_hash}")
            else:
                payment_hash = input("Enter payment hash (hex): ").strip()
                secret = None
            
            # Create HTLC
            htlc = self.create_htlc(amount, payment_hash, timeout)
            htlc_id = len(self.htlcs)
            self.htlcs[htlc_id] = htlc
            if secret:
                self.secrets[htlc_id] = secret
            
            print(f"\n✅ HTLC #{htlc_id} created!")
            print(f"💰 Amount: {amount} sats")
            print(f"🔒 Hash: {payment_hash}")
            print(f"⏰ Timeout: {timeout} blocks")
            
            # Offer to resolve it
            if secret:
                resolve = input("\nResolve this HTLC now? (y/n): ").lower().strip()
                if resolve == 'y':
                    self.resolve_htlc_demo(htlc, secret, payment_hash)
                    
        except ValueError:
            print("❌ Invalid input")
        except KeyboardInterrupt:
            print("\n👋 HTLC builder interrupted")

def main():
    """Main function for HTLC demo"""
    print("🔐 Welcome to Lightning Network HTLCs!")
    print("Hash Time-Locked Contracts - The Magic Behind Lightning")
    
    demo = HTLCDemo()
    
    try:
        # Basic HTLC demonstration
        demo.demonstrate_htlc_basics()
        
        # Multi-hop routing
        print("\n" + "="*60)
        demo.demonstrate_multi_hop_htlcs()
        
        # Security properties
        print("\n" + "="*60)
        demo.demonstrate_htlc_security()
        
        # Interactive elements
        if os.environ.get("BITCOIN_TEST_MODE") != "1":
            print("\n" + "="*60)
            print("🛠️ Want to build your own HTLC?")
            build_choice = input("Try the interactive HTLC builder? (y/n): ").lower().strip()
            if build_choice == 'y':
                demo.interactive_htlc_builder()
            
            print("\n🎓 Ready for the HTLC quiz?")
            quiz_choice = input("Test your knowledge? (y/n): ").lower().strip()
            if quiz_choice == 'y':
                demo.htlc_quiz()
        else:
            demo.interactive_htlc_builder()
            demo.htlc_quiz()
            
        print("\n🎉 HTLC Demo Complete!")
        print("💡 You now understand the building blocks of Lightning payments!")
        
    except KeyboardInterrupt:
        print("\n👋 HTLC demo ended")
    except Exception as e:
        print(f"\n❌ Error in demo: {e}")

if __name__ == "__main__":
    main()