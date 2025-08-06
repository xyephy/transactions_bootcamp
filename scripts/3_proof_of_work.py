#!/usr/bin/env python3
"""
Bitcoin Fundamentals Module 3: PROOF OF WORK
Understanding Bitcoin's consensus mechanism

Learning Goals:
- Understand what proof-of-work solves
- See how mining actually works  
- Experience the difficulty adjustment
- Understand why PoW secures Bitcoin
"""

import hashlib
import time
import random
import requests
from dataclasses import dataclass
from typing import Dict, Optional

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
class MiningCandidate:
    """Represents a block candidate for mining"""
    
    previous_hash: str
    merkle_root: str
    timestamp: int
    target: str          # Target hash (difficulty)
    nonce: int = 0
    
    def calculate_hash(self) -> str:
        """Calculate block hash with current nonce"""
        block_data = f"{self.previous_hash}{self.merkle_root}{self.timestamp}{self.nonce}"
        
        # Double SHA256 like Bitcoin
        hash1 = hashlib.sha256(block_data.encode()).digest()
        hash2 = hashlib.sha256(hash1).hexdigest()
        return hash2
    
    def meets_target(self) -> bool:
        """Check if current hash meets the target (difficulty)"""
        current_hash = self.calculate_hash()
        return current_hash <= self.target
    
    def display_attempt(self):
        """Display current mining attempt"""
        hash_value = self.calculate_hash()
        meets_target = "✅" if self.meets_target() else "❌"
        print(f"Nonce: {self.nonce:10d} | Hash: {hash_value} | Target: {meets_target}")

class SimpleMiner:
    """Educational Bitcoin miner"""
    
    def __init__(self, name: str = "Student Miner"):
        self.name = name
        self.hashes_calculated = 0
        self.blocks_found = 0
    
    def mine_block(self, candidate: MiningCandidate, max_attempts: int = 1000000) -> Optional[int]:
        """
        Mine a block by finding a valid nonce
        
        Returns:
            The winning nonce if found, None if not found within max_attempts
        """
        
        print(f"\n⛏️  {self.name} starting to mine...")
        print(f"🎯 Target: {candidate.target}")
        print(f"📊 Mining progress:")
        
        start_time = time.time()
        
        for attempt in range(max_attempts):
            candidate.nonce = attempt
            self.hashes_calculated += 1
            
            # Show progress every 10,000 attempts
            if attempt % 10000 == 0:
                candidate.display_attempt()
            
            # Check if we found a valid hash
            if candidate.meets_target():
                end_time = time.time()
                duration = end_time - start_time
                
                print(f"\n🎉 BLOCK FOUND!")
                print(f"✅ Winning nonce: {candidate.nonce}")
                print(f"🏆 Winning hash: {candidate.calculate_hash()}")
                print(f"⏱️  Time taken: {duration:.2f} seconds")
                print(f"💪 Hash rate: {self.hashes_calculated / duration:.0f} hashes/second")
                
                self.blocks_found += 1
                return candidate.nonce
        
        print(f"\n😞 No valid hash found in {max_attempts:,} attempts")
        print(f"💡 Try increasing max_attempts or reducing difficulty")
        return None

def demonstrate_hashing():
    """Show how small changes create completely different hashes"""
    
    print("\n🔬 CRYPTOGRAPHIC HASHING DEMO")
    print("="*38)
    
    print("🎯 Key property: Small input changes = Completely different output")
    
    # Original data
    data1 = "Block #1234: Alice sends 1 BTC to Bob"
    hash1 = hashlib.sha256(data1.encode()).hexdigest()
    
    # Tiny change
    data2 = "Block #1234: Alice sends 2 BTC to Bob"  # Changed 1 to 2
    hash2 = hashlib.sha256(data2.encode()).hexdigest()
    
    # Another tiny change  
    data3 = "Block #1235: Alice sends 1 BTC to Bob"  # Changed 1234 to 1235
    hash3 = hashlib.sha256(data3.encode()).hexdigest()
    
    print(f"\n📝 Original:  {data1}")
    print(f"🔗 Hash:      {hash1}")
    
    print(f"\n📝 Change #1: {data2}")
    print(f"🔗 Hash:      {hash2}")
    print(f"📊 Changed:   {''.join('X' if c1 != c2 else '.' for c1, c2 in zip(hash1, hash2))}")
    
    print(f"\n📝 Change #2: {data3}")
    print(f"🔗 Hash:      {hash3}")
    print(f"📊 Changed:   {''.join('X' if c1 != c3 else '.' for c1, c3 in zip(hash1, hash3))}")
    
    print(f"\n💡 Notice how tiny changes create completely different hashes!")
    print(f"   This makes it impossible to predict what input creates a specific hash")

def demonstrate_difficulty():
    """Show how mining difficulty works"""
    
    print("\n🎯 UNDERSTANDING MINING DIFFICULTY")
    print("="*37)
    
    print("🎲 Bitcoin mining is like a lottery:")
    print("   • Everyone guesses random numbers (nonces)")
    print("   • Winners must have hash starting with zeros")
    print("   • More zeros = harder to find = higher difficulty")
    
    difficulties = [
        ("Very Easy", "0fffffff" + "f" * 56),      # Hash must start with 0
        ("Easy", "00ffffff" + "f" * 54),           # Hash must start with 00  
        ("Medium", "000fffff" + "f" * 52),         # Hash must start with 000
        ("Hard", "0000ffff" + "f" * 50),           # Hash must start with 0000
    ]
    
    # Demo data
    demo_data = MiningCandidate(
        previous_hash="abc123" + "0" * 58,
        merkle_root="def456" + "0" * 58,
        timestamp=int(time.time()),
        target=""  # Will be set in loop
    )
    
    for difficulty_name, target in difficulties:
        print(f"\n⛏️  Mining with {difficulty_name} difficulty:")
        print(f"🎯 Target: {target}")
        print(f"💡 Hash must be ≤ {target}")
        
        demo_data.target = target
        demo_data.nonce = 0
        
        # Try to find a valid hash quickly
        miner = SimpleMiner(f"{difficulty_name} Miner")
        max_attempts = 50000 if difficulty_name == "Very Easy" else 10000
        
        winning_nonce = miner.mine_block(demo_data, max_attempts)
        
        if winning_nonce is not None:
            print(f"🏆 Success! Found valid hash: {demo_data.calculate_hash()}")
        else:
            print(f"😞 Didn't find valid hash in {max_attempts:,} attempts")
            print(f"💡 In real Bitcoin, miners would keep trying...")

def interactive_mining_race():
    """Let students experience competitive mining"""
    
    print("\n🏁 INTERACTIVE MINING RACE")
    print("="*30)
    
    print("🎮 You and your classmates are miners competing for a block!")
    print("🏆 First to find a valid hash wins the mining reward!")
    
    # Create mining candidate
    candidate = MiningCandidate(
        previous_hash="student_race_" + "0" * 52,
        merkle_root="class_transactions_" + "0" * 48,
        timestamp=int(time.time()),
        target="000fffff" + "f" * 52  # Medium difficulty
    )
    
    print(f"\n📊 Mining challenge:")
    print(f"   Target: {candidate.target}")
    print(f"   Goal: Find hash ≤ target")
    
    # Student miner
    student_name = input("\nEnter your miner name (or press Enter for 'Student'): ") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...").strip()
    if not student_name:
        student_name = "Student"
    
    student_miner = SimpleMiner(student_name)
    
    # Simulate other students mining
    competitor_miners = [
        SimpleMiner("Alice"),
        SimpleMiner("Bob"), 
        SimpleMiner("Charlie")
    ]
    
    print(f"\n⛏️  Starting mining race!")
    print(f"🏃 Competing against: {', '.join(m.name for m in competitor_miners)}")
    
    # Race simulation
    race_start = time.time()
    max_race_time = 10  # 10 second race
    
    winner = None
    winning_nonce = None
    
    # Student gets a head start (educational purposes)
    print(f"\n🎯 {student_name} mining...")
    start_nonce = random.randint(0, 50000)
    
    for nonce in range(start_nonce, start_nonce + 100000):
        candidate.nonce = nonce
        student_miner.hashes_calculated += 1
        
        # Show progress occasionally
        if nonce % 5000 == 0:
            elapsed = time.time() - race_start
            print(f"   Attempt {nonce}: {candidate.calculate_hash()[:16]}... ({elapsed:.1f}s)")
        
        # Check if student found it
        if candidate.meets_target():
            winner = student_miner
            winning_nonce = nonce
            break
        
        # Check if race time expired
        if time.time() - race_start > max_race_time:
            # Simulate competitor finding it
            competitor = random.choice(competitor_miners)
            winner = competitor
            winning_nonce = random.randint(nonce, nonce + 10000)
            break
    
    # Show race results
    race_time = time.time() - race_start
    
    if winner == student_miner:
        print(f"\n🎉 CONGRATULATIONS! {student_name} wins!")
        print(f"🏆 You found the winning nonce: {winning_nonce}")
        print(f"✅ Winning hash: {candidate.calculate_hash()}")
        print(f"⏱️  Time: {race_time:.2f} seconds")
        print(f"💰 You earn the mining reward!")
    else:
        print(f"\n😞 {winner.name} wins this round!")
        print(f"🏆 Winning nonce: {winning_nonce}")
        print(f"⏱️  Race time: {race_time:.2f} seconds")
        print(f"💡 Better luck next time!")
    
    print(f"\n📊 Race statistics:")
    print(f"   Your hash rate: {student_miner.hashes_calculated / race_time:.0f} hashes/sec")
    print(f"   Total attempts: {student_miner.hashes_calculated:,}")

def demonstrate_difficulty_adjustment():
    """Show how Bitcoin adjusts difficulty"""
    
    print("\n⚖️  DIFFICULTY ADJUSTMENT MECHANISM")
    print("="*40)
    
    print("🎯 Bitcoin targets 10-minute block times")
    print("📈 If blocks come too fast → increase difficulty")
    print("📉 If blocks come too slow → decrease difficulty")
    
    # Simulate different scenarios
    scenarios = [
        ("Normal Network", 10, "000fffff" + "f" * 52),      # 10 min target
        ("Network Growth", 5, "0000ffff" + "f" * 50),       # Too fast, increase difficulty
        ("Miners Leave", 20, "00ffffff" + "f" * 54),        # Too slow, decrease difficulty
    ]
    
    for scenario_name, avg_time, new_target in scenarios:
        print(f"\n📊 Scenario: {scenario_name}")
        print(f"   Recent average block time: {avg_time} minutes")
        print(f"   Target block time: 10 minutes")
        
        if avg_time < 10:
            print(f"   ⬆️  Blocks too fast! Increase difficulty")
            print(f"   🎯 New target: {new_target} (harder)")
        elif avg_time > 10:
            print(f"   ⬇️  Blocks too slow! Decrease difficulty")  
            print(f"   🎯 New target: {new_target} (easier)")
        else:
            print(f"   ✅ Perfect timing! Keep same difficulty")
            print(f"   🎯 Target unchanged: {new_target}")
    
    print(f"\n💡 This automatic adjustment ensures:")
    print(f"   • Blocks always come every ~10 minutes")
    print(f"   • Network adapts to changing hash power")
    print(f"   • Bitcoin remains predictable and stable")

def explore_real_mining():
    """Explore real mining data from Polar"""
    
    print("\n🌐 REAL BITCOIN MINING DATA")
    print("="*32)
    
    rpc = BitcoinRPC()
    
    try:
        # Get mining info
        mining_info = rpc.call("getmininginfo")
        if mining_info:
            print("⛏️  Current Mining Status:")
            print(f"   Network difficulty: {mining_info.get('difficulty', 'N/A')}")
            print(f"   Hash rate: {mining_info.get('networkhashps', 0):,.0f} hashes/second")
            print(f"   Blocks: {mining_info.get('blocks', 0)}")
            print(f"   Chain: {mining_info.get('chain', 'unknown')}")
        
        # Get latest block details
        best_hash = rpc.call("getbestblockhash")
        if best_hash:
            block_info = rpc.call("getblock", [best_hash])
            
            print(f"\n📦 Latest Block Analysis:")
            print(f"   Block hash: {block_info.get('hash')}")
            print(f"   Nonce: {block_info.get('nonce', 'N/A')}")
            print(f"   Difficulty: {block_info.get('difficulty', 'N/A')}")
            print(f"   Time: {time.ctime(block_info.get('time', 0))}")
            
            # Analyze the winning hash
            winning_hash = block_info.get('hash', '')
            leading_zeros = 0
            for char in winning_hash:
                if char == '0':
                    leading_zeros += 1
                else:
                    break
            
            print(f"   Leading zeros: {leading_zeros}")
            print(f"   💡 More zeros = harder to find = higher difficulty")
        
        # Generate some blocks for demonstration
        print(f"\n🎮 Want to see mining in action?")
        mine_demo = input("Generate some blocks? (y/n): ") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...").lower().strip()
        
        if mine_demo == 'y':
            print("⛏️  Mining 3 blocks...")
            
            for i in range(3):
                try:
                    # Mine a block (instant in regtest)
                    block_hashes = rpc.call("generatetoaddress", [1, "bcrt1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"])
                    
                    if block_hashes:
                        new_hash = block_hashes[0]
                        new_block = rpc.call("getblock", [new_hash])
                        
                        print(f"   Block #{new_block.get('height')}: {new_hash[:16]}... (nonce: {new_block.get('nonce')})")
                    
                    time.sleep(1)  # Dramatic pause
                    
                except Exception as e:
                    print(f"   Error mining block {i+1}: {e}")
    
    except Exception as e:
        print(f"❌ Cannot connect to Bitcoin Core: {e}")
        print("💡 Make sure Polar is running!")

def proof_of_work_quiz():
    """Interactive quiz about proof-of-work concepts"""
    
    print("\n🧠 PROOF-OF-WORK QUIZ")
    print("="*25)
    
    questions = [
        {
            "question": "What does a miner try to find?",
            "options": ["A) Private key", "B) Nonce that creates valid hash", "C) Transaction signature", "D) Wallet address"],
            "answer": "B",
            "explanation": "Miners search for a nonce (number used once) that makes the block hash meet the difficulty target."
        },
        {
            "question": "What happens if blocks are found too quickly?",
            "options": ["A) Nothing changes", "B) Difficulty decreases", "C) Difficulty increases", "D) Network stops"],
            "answer": "C", 
            "explanation": "Bitcoin increases difficulty every 2016 blocks to maintain 10-minute average block times."
        },
        {
            "question": "Why does Bitcoin use proof-of-work?",
            "options": ["A) To waste energy", "B) To secure the network", "C) To slow down transactions", "D) To confuse users"],
            "answer": "B",
            "explanation": "Proof-of-work makes it extremely expensive to attack Bitcoin, securing the network through economic incentives."
        },
        {
            "question": "What determines mining difficulty?",
            "options": ["A) Number of transactions", "B) Bitcoin price", "C) Recent block times", "D) Number of users"],
            "answer": "C",
            "explanation": "Difficulty adjusts based on how long recent blocks took to find, targeting 10-minute averages."
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
        print("🏆 Perfect! You understand proof-of-work!")
    elif score >= len(questions) * 0.7:
        print("👍 Great job! You've got the basics down!")
    else:
        print("📚 Review the concepts and try again!")

def main():
    """Main lesson function"""
    
    print("🎓 BITCOIN FUNDAMENTALS: PROOF OF WORK")
    print("="*45)
    print("Understanding Bitcoin's consensus mechanism")
    
    # Interactive lesson modules
    modules = [
        ("1. Cryptographic Hashing", demonstrate_hashing),
        ("2. Mining Difficulty", demonstrate_difficulty),
        ("3. Mining Race", interactive_mining_race),
        ("4. Difficulty Adjustment", demonstrate_difficulty_adjustment),
        ("5. Real Mining Data", explore_real_mining),
        ("6. Knowledge Quiz", proof_of_work_quiz)
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
        if not os.environ.get("BITCOIN_TEST_MODE") == "1":
            input("\nPress Enter to continue to next module...")
        else:
            print("🧪 Test mode: Skipping to next module...")
    
    print("\n🎉 LESSON COMPLETE!")
    print("💡 Key takeaways:")
    print("  • Proof-of-work is a lottery system based on hash calculations")
    print("  • Miners compete to find nonces that create valid block hashes")
    print("  • Difficulty adjusts to maintain 10-minute block times")
    print("  • PoW secures Bitcoin by making attacks economically costly")
    print("  • The system is self-regulating and trustless")

if __name__ == "__main__":
    main()