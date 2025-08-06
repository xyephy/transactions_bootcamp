#!/usr/bin/env python3
"""
Bitcoin Fundamentals Module 5: MINING & INCENTIVES
Understanding Bitcoin's economic incentive system

Learning Goals:
- Understand why miners mine (economic incentives)
- See how mining rewards work
- Explore halving events and supply schedule
- Understand fee markets and priority
- Experience mining economics simulation
"""

import time
import random
import json
import requests
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# Optional plotting (not required for core functionality)
try:
    import matplotlib.pyplot as plt
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False

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
class MiningReward:
    """Represents a mining reward"""
    
    block_height: int
    coinbase_reward: float     # Block subsidy
    transaction_fees: float    # Fees from transactions
    total_reward: float        # coinbase_reward + transaction_fees
    
    def display(self):
        """Display reward information"""
        print(f"   🏆 Block #{self.block_height}:")
        print(f"     💰 Coinbase reward: {self.coinbase_reward:.8f} BTC")
        print(f"     💸 Transaction fees: {self.transaction_fees:.8f} BTC")
        print(f"     💎 Total reward: {self.total_reward:.8f} BTC")

class MiningSimulator:
    """Educational mining simulator"""
    
    def __init__(self):
        self.current_height = 0
        self.total_supply = 0.0
        self.halvings = 0
        self.mining_history = []
    
    def get_block_reward(self, height: int) -> float:
        """Calculate block reward at given height"""
        initial_reward = 50.0  # Initial Bitcoin reward
        halvings = height // 210000  # Halving every 210,000 blocks
        
        if halvings >= 33:  # After ~33 halvings, reward becomes 0
            return 0.0
        
        return initial_reward / (2 ** halvings)
    
    def simulate_mining_economics(self, num_blocks: int = 10):
        """Simulate mining economics over multiple blocks"""
        
        print(f"\n⛏️  MINING ECONOMICS SIMULATION")
        print(f"="*35)
        print(f"🎯 Simulating {num_blocks} blocks of mining...")
        
        total_rewards = 0.0
        total_fees = 0.0
        
        for i in range(num_blocks):
            height = self.current_height + i
            
            # Calculate coinbase reward
            coinbase = self.get_block_reward(height)
            
            # Simulate transaction fees (random for demo)
            fees = random.uniform(0.001, 0.1)
            
            # Create mining reward
            reward = MiningReward(
                block_height=height,
                coinbase_reward=coinbase,
                transaction_fees=fees,
                total_reward=coinbase + fees
            )
            
            reward.display()
            
            total_rewards += coinbase
            total_fees += fees
            self.mining_history.append(reward)
            
            time.sleep(0.5)  # Dramatic pause
        
        print(f"\n📊 Simulation Summary:")
        print(f"   💰 Total coinbase: {total_rewards:.8f} BTC")
        print(f"   💸 Total fees: {total_fees:.8f} BTC")
        print(f"   💎 Total earned: {total_rewards + total_fees:.8f} BTC")
        print(f"   📈 Average per block: {(total_rewards + total_fees) / num_blocks:.8f} BTC")

def demonstrate_bitcoin_supply_schedule():
    """Show Bitcoin's predetermined supply schedule"""
    
    print("\n📈 BITCOIN SUPPLY SCHEDULE")
    print("="*30)
    
    print("🎯 Bitcoin has a fixed supply schedule:")
    print("   • 21 million BTC maximum supply")
    print("   • Block reward halves every 210,000 blocks (~4 years)")
    print("   • Final bitcoin mined around year 2140")
    
    # Calculate key halving events
    halvings = [
        (0, 50.0, "2009-01-03", "Genesis"),
        (210000, 25.0, "2012-11-28", "1st Halving"),
        (420000, 12.5, "2016-07-09", "2nd Halving"),
        (630000, 6.25, "2020-05-11", "3rd Halving"),
        (840000, 3.125, "2024-04-19", "4th Halving (estimated)"),
        (1050000, 1.5625, "2028", "5th Halving (estimated)"),
    ]
    
    print(f"\n📅 Historical and Future Halvings:")
    cumulative_supply = 0.0
    
    for height, reward, date, event in halvings:
        # Calculate supply at this point
        if height == 0:
            blocks_in_period = 210000
        else:
            blocks_in_period = 210000
        
        supply_in_period = blocks_in_period * reward
        cumulative_supply += supply_in_period
        
        print(f"\n   {event}:")
        print(f"     📦 Block height: {height:,}")
        print(f"     📅 Date: {date}")
        print(f"     💰 Block reward: {reward} BTC")
        print(f"     📊 Supply at point: {cumulative_supply:,.0f} BTC")
        print(f"     📈 % of total supply: {(cumulative_supply / 21000000) * 100:.1f}%")
    
    print(f"\n💡 Key insights:")
    print(f"   • 50% of all Bitcoin mined in first 4 years")
    print(f"   • 75% mined in first 8 years")
    print(f"   • Last 25% takes over 100 years to mine")
    print(f"   • Scarcity increases over time")

def analyze_transaction_fees():
    """Analyze transaction fees and priority"""
    
    print("\n💸 TRANSACTION FEES & PRIORITY")
    print("="*34)
    
    print("🎯 Transaction fees serve multiple purposes:")
    print("   • Compensate miners for including transactions")
    print("   • Prevent spam attacks (costs money)")
    print("   • Create priority system (higher fee = faster confirmation)")
    print("   • Become more important as block rewards decrease")
    
    rpc = BitcoinRPC()
    
    try:
        # Get current fee estimates
        fee_estimates = {}
        
        for blocks in [1, 3, 6, 10]:
            try:
                estimate = rpc.call("estimatesmartfee", [blocks])
                if estimate and 'feerate' in estimate:
                    fee_estimates[blocks] = estimate['feerate']
            except:
                # Fallback for regtest
                fee_estimates[blocks] = 0.00001 * blocks
        
        print(f"\n📊 Current Fee Estimates (BTC/KB):")
        for blocks, fee in fee_estimates.items():
            urgency = "🚀 Urgent" if blocks == 1 else "⏰ Normal" if blocks <= 6 else "🐌 Low priority"
            print(f"   {blocks:2d} blocks: {fee:.8f} BTC/KB ({urgency})")
        
        # Demonstrate fee calculation
        print(f"\n🧮 Fee calculation example:")
        print(f"   📏 Transaction size: 250 bytes")
        print(f"   ⚖️  Fee rate: 20 sat/byte")
        print(f"   💰 Total fee: 250 × 20 = 5,000 sats")
        print(f"   💵 In BTC: 0.00005000 BTC")
        
        # Show mempool and fee market
        mempool_info = rpc.call("getmempoolinfo")
        if mempool_info:
            print(f"\n🏊 Current Mempool Status:")
            print(f"   🧾 Pending transactions: {mempool_info.get('size', 0):,}")
            print(f"   💰 Total fees waiting: {mempool_info.get('total_fee', 0):.8f} BTC")
            
            if mempool_info.get('size', 0) > 0:
                print(f"   🔥 Fee market is active!")
            else:
                print(f"   😴 Low congestion, minimal fees needed")
        
    except Exception as e:
        print(f"❌ Error analyzing fees: {e}")
        print("💡 Using simulated fee data...")
        
        # Simulated fee market during congestion
        print(f"\n🌋 Simulated High Congestion Scenario:")
        print(f"   🧾 Mempool size: 50,000 transactions")
        print(f"   ⚖️  Low priority: 1 sat/byte (12+ hour wait)")
        print(f"   ⚖️  Normal: 10 sat/byte (1-3 hour wait)")
        print(f"   ⚖️  High priority: 50 sat/byte (next block)")
        print(f"   ⚖️  Urgent: 100+ sat/byte (definitely next block)")

def mining_profitability_calculator():
    """Interactive mining profitability calculator"""
    
    print("\n🧮 MINING PROFITABILITY CALCULATOR")
    print("="*38)
    
    print("💡 Let's calculate if mining is profitable!")
    
    # Get user inputs
    try:
        print(f"\n📝 Enter your mining setup:")
        hash_rate = float(input("Hash rate (TH/s): ") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...") or "100")
        power_consumption = float(input("Power consumption (watts): ") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...") or "3000")
        electricity_cost = float(input("Electricity cost ($/kWh): ") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...") or "0.10")
        hardware_cost = float(input("Hardware cost ($): ") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...") or "5000")
        
        # Bitcoin parameters (use current estimates)
        btc_price = float(input("Bitcoin price ($): ") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...") or "30000")
        network_hashrate = float(input("Network hash rate (EH/s): ") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...") or "400")
        block_reward = 6.25  # Current reward
        
        print(f"\n📊 Calculating profitability...")
        
        # Calculate daily earnings
        hash_rate_eh = hash_rate / 1_000_000  # Convert TH/s to EH/s
        probability_per_block = hash_rate_eh / network_hashrate
        blocks_per_day = 144  # ~6 blocks per hour × 24 hours
        daily_blocks_mined = probability_per_block * blocks_per_day
        daily_btc_earned = daily_blocks_mined * block_reward
        daily_usd_earned = daily_btc_earned * btc_price
        
        # Calculate daily costs
        daily_power_kwh = (power_consumption * 24) / 1000
        daily_electricity_cost = daily_power_kwh * electricity_cost
        
        # Calculate net profit
        daily_profit = daily_usd_earned - daily_electricity_cost
        monthly_profit = daily_profit * 30
        
        # Calculate return on investment
        if daily_profit > 0:
            payback_days = hardware_cost / daily_profit
        else:
            payback_days = float('inf')
        
        print(f"\n💰 PROFITABILITY RESULTS:")
        print(f"   📈 Daily BTC earned: {daily_btc_earned:.8f} BTC")
        print(f"   💵 Daily USD earned: ${daily_usd_earned:.2f}")
        print(f"   ⚡ Daily electricity cost: ${daily_electricity_cost:.2f}")
        print(f"   💎 Daily net profit: ${daily_profit:.2f}")
        print(f"   📅 Monthly profit: ${monthly_profit:.2f}")
        
        if payback_days < 365:
            print(f"   🏆 Hardware payback: {payback_days:.0f} days")
            print(f"   ✅ Mining appears profitable!")
        elif payback_days < float('inf'):
            print(f"   ⏰ Hardware payback: {payback_days:.0f} days ({payback_days/365:.1f} years)")
            print(f"   ⚠️  Long payback period")
        else:
            print(f"   ❌ Mining is not profitable with these parameters")
        
        # Sensitivity analysis
        print(f"\n📊 Sensitivity Analysis:")
        scenarios = [
            ("Bitcoin +50%", btc_price * 1.5),
            ("Bitcoin -50%", btc_price * 0.5),
            ("Electricity half cost", electricity_cost * 0.5),
            ("Electricity double cost", electricity_cost * 2.0)
        ]
        
        for scenario_name, new_value in scenarios:
            if "Bitcoin" in scenario_name:
                new_daily_usd = daily_btc_earned * new_value
                new_profit = new_daily_usd - daily_electricity_cost
            else:  # Electricity scenarios
                new_daily_cost = daily_power_kwh * new_value
                new_profit = daily_usd_earned - new_daily_cost
            
            print(f"   {scenario_name}: ${new_profit:.2f}/day")
    
    except ValueError:
        print("❌ Invalid input. Using default values for demo...")
        print("📊 Example calculation with default values:")
        print("   💰 Daily profit: $15.50")
        print("   📅 Monthly profit: $465")
        print("   🏆 Hardware payback: 323 days")

def demonstrate_mining_pools():
    """Explain mining pools and variance"""
    
    print("\n🏊 MINING POOLS & VARIANCE")
    print("="*29)
    
    print("🎯 Why miners join pools:")
    print("   • Solo mining has high variance (all-or-nothing)")
    print("   • Pools provide steady, predictable income")
    print("   • Share rewards proportionally to contributed work")
    print("   • Reduce risk for individual miners")
    
    # Simulate solo vs pool mining
    print(f"\n🎲 Solo Mining Simulation (10 days):")
    solo_earnings = []
    
    for day in range(1, 11):
        # 0.1% chance to find a block per day (example small miner)
        if random.random() < 0.001:
            earnings = 6.25  # Found a block!
            solo_earnings.append(earnings)
            print(f"   Day {day:2d}: 🎉 FOUND BLOCK! +{earnings} BTC")
        else:
            solo_earnings.append(0)
            print(f"   Day {day:2d}: 😞 No block found +0 BTC")
    
    solo_total = sum(solo_earnings)
    
    print(f"\n🏊 Pool Mining Simulation (10 days):")
    pool_daily = 6.25 * 0.001 * 0.98  # Expected daily × pool fee (2%)
    pool_earnings = [pool_daily] * 10
    
    for day in range(1, 11):
        print(f"   Day {day:2d}: ⚖️  Steady payout +{pool_daily:.6f} BTC")
    
    pool_total = sum(pool_earnings)
    
    print(f"\n📊 10-Day Comparison:")
    print(f"   🎲 Solo mining total: {solo_total:.6f} BTC")
    print(f"   🏊 Pool mining total: {pool_total:.6f} BTC")
    print(f"   📈 Solo variance: {'High' if max(solo_earnings) > 0 else 'Zero income'}")
    print(f"   📉 Pool variance: Very low (steady income)")
    
    print(f"\n💡 Pool benefits:")
    print(f"   • Predictable income for budgeting")
    print(f"   • Lower risk for miners")
    print(f"   • Can mine with smaller operations")
    print(f"   • Pool handles technical infrastructure")

def halving_event_simulation():
    """Simulate a Bitcoin halving event"""
    
    print("\n✂️  BITCOIN HALVING EVENT SIMULATION")
    print("="*40)
    
    print("🎯 Let's simulate what happens during a halving:")
    
    # Pre-halving state
    print(f"\n📊 Pre-Halving State:")
    current_reward = 6.25
    current_height = 839999  # Just before next halving
    miners_profit = 1000  # USD per day (example)
    
    print(f"   📦 Block height: {current_height:,}")
    print(f"   💰 Block reward: {current_reward} BTC")
    print(f"   ⛏️  Miner daily profit: ${miners_profit}")
    print(f"   📈 Network hash rate: Stable")
    
    input("\nPress Enter for halving event...") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...")
    
    # Halving occurs
    print(f"\n🎉 HALVING EVENT OCCURS!")
    new_reward = current_reward / 2
    new_height = current_height + 1
    
    print(f"   📦 Block height: {new_height:,}")
    print(f"   💰 New block reward: {new_reward} BTC")
    print(f"   📉 Reward reduced by 50%!")
    
    input("\nPress Enter to see immediate effects...") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...")
    
    # Immediate effects
    print(f"\n⚡ Immediate Effects:")
    new_profit = miners_profit * 0.5  # Assuming price stays same
    
    print(f"   💰 Miner revenue: Cut in half")
    print(f"   ⛏️  Miner profit: ${new_profit:.0f}/day (down 50%)")
    print(f"   🔴 Some miners become unprofitable")
    print(f"   📉 Mining difficulty: Unchanged (for now)")
    
    input("\nPress Enter for market adjustment...") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...")
    
    # Market adjustment phase
    print(f"\n🔄 Market Adjustment Phase (weeks 1-4):")
    
    adjustments = [
        "Week 1: Inefficient miners shut down (-15% hash rate)",
        "Week 2: Remaining miners more profitable (+30% individual profit)",
        "Week 3: Difficulty adjustment algorithm activates",
        "Week 4: New equilibrium reached"
    ]
    
    for adjustment in adjustments:
        print(f"   {adjustment}")
        time.sleep(1)
    
    print(f"\n📊 Post-Halving Equilibrium:")
    print(f"   💰 Block reward: {new_reward} BTC (permanent)")
    print(f"   📉 Hash rate: 85% of pre-halving (stabilized)")
    print(f"   ⚖️  Difficulty: Adjusted down 15%")
    print(f"   💎 Bitcoin scarcity: Doubled!")
    print(f"   📈 Long-term price pressure: Upward")
    
    print(f"\n💡 Historical halving effects:")
    print(f"   • 2012: BTC $12 → $1,000+ (1 year later)")
    print(f"   • 2016: BTC $650 → $20,000 (1.5 years later)")
    print(f"   • 2020: BTC $8,500 → $69,000 (1.5 years later)")
    print(f"   • Pattern: Short-term volatility, long-term appreciation")

def incentive_alignment_demo():
    """Demonstrate how Bitcoin aligns incentives"""
    
    print("\n🎯 BITCOIN INCENTIVE ALIGNMENT")
    print("="*34)
    
    print("💡 Bitcoin's genius: Aligning selfish interests with network security")
    
    participants = {
        "Miners": {
            "goal": "Maximize profit",
            "actions": ["Find valid blocks", "Include high-fee transactions", "Follow consensus rules"],
            "result": "Secure the network while earning money"
        },
        "Users": {
            "goal": "Send/receive Bitcoin",
            "actions": ["Pay transaction fees", "Run full nodes", "Follow protocol"],
            "result": "Contribute to decentralization"
        },
        "Hodlers": {
            "goal": "Preserve value",
            "actions": ["Reject bad protocol changes", "Support good upgrades"],
            "result": "Maintain Bitcoin's integrity"
        },
        "Developers": {
            "goal": "Improve Bitcoin",
            "actions": ["Write better code", "Fix bugs", "Propose upgrades"],
            "result": "Strengthen the system"
        }
    }
    
    for participant, details in participants.items():
        print(f"\n👥 {participant}:")
        print(f"   🎯 Goal: {details['goal']}")
        print(f"   ⚡ Actions:")
        for action in details['actions']:
            print(f"     • {action}")
        print(f"   🏆 Result: {details['result']}")
    
    print(f"\n🎪 The Beautiful Equilibrium:")
    print(f"   • Everyone acts in self-interest")
    print(f"   • Yet the system becomes more secure")
    print(f"   • No central coordination needed")
    print(f"   • Game theory makes cooperation profitable")
    print(f"   • Attacks become economically irrational")
    
    print(f"\n💰 Economic Security:")
    print(f"   • Attack cost: Millions of dollars per hour")
    print(f"   • Honest mining profit: Thousands per hour")
    print(f"   • Attacking costs more than honest participation")
    print(f"   • Therefore: Rational actors choose honesty")

def main():
    """Main lesson function"""
    
    print("🎓 BITCOIN FUNDAMENTALS: MINING & INCENTIVES")
    print("="*51)
    print("Understanding Bitcoin's economic incentive system")
    
    # Check if matplotlib is available for plotting
    try:
        import matplotlib.pyplot as plt
        plotting_available = True
    except ImportError:
        plotting_available = False
        print("📊 Note: matplotlib not available for plotting")
    
    # Interactive lesson modules
    modules = [
        ("1. Supply Schedule", demonstrate_bitcoin_supply_schedule),
        ("2. Transaction Fees", analyze_transaction_fees),
        ("3. Mining Economics", lambda: MiningSimulator().simulate_mining_economics(5)),
        ("4. Profitability Calculator", mining_profitability_calculator),
        ("5. Mining Pools", demonstrate_mining_pools),
        ("6. Halving Simulation", halving_event_simulation),
        ("7. Incentive Alignment", incentive_alignment_demo)
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
    print("  • Mining rewards incentivize network security")
    print("  • Block rewards decrease over time (halvings)")
    print("  • Transaction fees become increasingly important")
    print("  • Economic incentives align individual and network interests")
    print("  • Bitcoin's scarcity is programmatically enforced")

if __name__ == "__main__":
    main()