#!/usr/bin/env python3
"""
Lightning Network: Economics and Incentives
===========================================

This script demonstrates Lightning Network economic concepts:
- Fee structures and routing economics
- Liquidity markets and capital efficiency
- Economic incentives for node operators
- Fee optimization strategies
- Economic security models

Key Learning Objectives:
- Understand Lightning fee mechanics
- Learn about liquidity as a service
- See economic incentives for participation
- Experience fee optimization strategies
"""

import requests
import json
import time
import os
import random
import math
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class FeePolicy:
    """Lightning Network fee policy"""
    base_fee_msat: int
    fee_rate_ppm: int  # parts per million
    min_htlc_msat: int
    max_htlc_msat: int

@dataclass
class LiquidityPosition:
    """Represents liquidity position in a channel"""
    channel_id: str
    capacity: int
    local_balance: int
    remote_balance: int
    fee_revenue: int
    routing_volume: int

class LightningEconomicsDemo:
    """Lightning Network economics demonstrations"""
    
    def __init__(self):
        self.nodes = {
            "alice": {
                "rpc_host": "localhost",
                "rpc_port": "8081",
                "name": "Alice",
                "pubkey": None
            },
            "bob": {
                "rpc_host": "localhost", 
                "rpc_port": "8082",
                "name": "Bob",
                "pubkey": None
            },
            "carol": {
                "rpc_host": "localhost",
                "rpc_port": "8083",
                "name": "Carol", 
                "pubkey": None
            }
        }
        
        self.fee_data = {}
        self.routing_stats = {}
    
    def calculate_routing_fee(self, amount_msat: int, base_fee_msat: int, fee_rate_ppm: int) -> int:
        """Calculate routing fee for a payment"""
        return base_fee_msat + (amount_msat * fee_rate_ppm // 1000000)
    
    def demonstrate_fee_structure(self):
        """Demonstrate Lightning Network fee structure"""
        print("\n💰 LIGHTNING NETWORK FEE STRUCTURE")
        print("=" * 45)
        print("Understanding how fees work in Lightning...")
        
        print("\n📚 FEE COMPONENTS:")
        print("🔹 Base Fee: Fixed cost per payment (typically 1-1000 msat)")
        print("🔹 Fee Rate: Proportional to payment amount (ppm = parts per million)")
        print("🔹 Example: 1000 ppm = 0.1% fee rate")
        
        # Demonstrate fee calculation
        print(f"\n🧮 FEE CALCULATION EXAMPLES:")
        print(f"=" * 35)
        
        scenarios = [
            {"amount": 100000, "base": 1000, "rate": 1000, "description": "Small payment"},
            {"amount": 1000000, "base": 1000, "rate": 1000, "description": "Medium payment"}, 
            {"amount": 10000000, "base": 1000, "rate": 1000, "description": "Large payment"},
            {"amount": 100000000, "base": 1000, "rate": 1000, "description": "Very large payment"}
        ]
        
        for scenario in scenarios:
            amount_sats = scenario["amount"] // 1000
            fee_msat = self.calculate_routing_fee(scenario["amount"], scenario["base"], scenario["rate"])
            fee_sats = fee_msat / 1000
            fee_percentage = (fee_msat / scenario["amount"]) * 100
            
            print(f"\n💸 {scenario['description']}:")
            print(f"   Amount: {amount_sats:,} sats")
            print(f"   Base fee: {scenario['base']} msat")
            print(f"   Rate: {scenario['rate']} ppm (0.1%)")
            print(f"   Total fee: {fee_msat:,} msat ({fee_sats:.3f} sats)")
            print(f"   Effective rate: {fee_percentage:.4f}%")
        
        print(f"\n💡 KEY INSIGHTS:")
        print(f"📊 Base fee dominates for small payments")
        print(f"📈 Fee rate dominates for large payments")
        print(f"💼 Node operators balance both to optimize revenue")
        
        if os.environ.get("BITCOIN_TEST_MODE") != "1":
            input("\nPress Enter to continue...")
    
    def demonstrate_liquidity_economics(self):
        """Demonstrate liquidity economics and capital efficiency"""
        print("\n💧 LIQUIDITY ECONOMICS")
        print("=" * 30)
        print("How liquidity generates returns...")
        
        # Simulate liquidity positions
        channels = [
            {
                "name": "High Volume Route",
                "capacity": 10000000,  # 10M sats
                "daily_volume": 50000000,  # 50M sats per day
                "avg_fee_rate": 500,  # 0.05%
                "utilization": 0.8
            },
            {
                "name": "Medium Volume Route",
                "capacity": 5000000,   # 5M sats
                "daily_volume": 10000000,  # 10M sats per day
                "avg_fee_rate": 1000,  # 0.1%
                "utilization": 0.6
            },
            {
                "name": "Low Volume Route", 
                "capacity": 2000000,   # 2M sats
                "daily_volume": 1000000,   # 1M sats per day
                "avg_fee_rate": 2000,  # 0.2%
                "utilization": 0.3
            }
        ]
        
        print(f"\n📊 LIQUIDITY PERFORMANCE ANALYSIS:")
        print(f"=" * 40)
        
        total_capital = 0
        total_daily_revenue = 0
        
        for channel in channels:
            # Calculate daily revenue
            daily_fee_revenue = (channel["daily_volume"] * channel["avg_fee_rate"]) // 1000000
            
            # Calculate capital efficiency 
            capital_deployed = channel["capacity"] * channel["utilization"]
            daily_yield = (daily_fee_revenue / capital_deployed) * 100 if capital_deployed > 0 else 0
            annual_yield = daily_yield * 365
            
            total_capital += capital_deployed
            total_daily_revenue += daily_fee_revenue
            
            print(f"\n⚡ {channel['name']}:")
            print(f"   💰 Capacity: {channel['capacity']:,} sats")
            print(f"   📊 Daily Volume: {channel['daily_volume']:,} sats")
            print(f"   💸 Avg Fee Rate: {channel['avg_fee_rate']} ppm")
            print(f"   🔄 Utilization: {channel['utilization']*100:.0f}%")
            print(f"   💵 Daily Revenue: {daily_fee_revenue:,} sats")
            print(f"   📈 Annual Yield: {annual_yield:.2f}%")
        
        # Portfolio analysis
        portfolio_yield = (total_daily_revenue / total_capital) * 365 * 100 if total_capital > 0 else 0
        
        print(f"\n📋 PORTFOLIO SUMMARY:")
        print(f"💰 Total Capital: {total_capital:,} sats")
        print(f"💵 Daily Revenue: {total_daily_revenue:,} sats")
        print(f"📈 Portfolio Yield: {portfolio_yield:.2f}% annually")
        
        # Compare to alternatives
        print(f"\n⚖️ ALTERNATIVE INVESTMENTS:")
        print(f"🏦 Traditional savings: ~0.5% annually")
        print(f"📈 Stock market: ~7% annually (historical)")
        print(f"₿ Bitcoin holding: Volatile, no yield")
        print(f"⚡ Lightning routing: {portfolio_yield:.2f}% + network utility")
        
        print(f"\n💡 LIQUIDITY INSIGHTS:")
        print(f"🎯 Higher volume routes = better returns")
        print(f"⚖️ Balance yield vs liquidity risk") 
        print(f"🔄 Rebalancing costs affect profitability")
        print(f"📊 Diversification reduces risk")
    
    def demonstrate_fee_optimization(self):
        """Demonstrate fee optimization strategies"""
        print("\n⚖️ FEE OPTIMIZATION STRATEGIES")
        print("=" * 45)
        print("How to maximize routing revenue...")
        
        # Market research simulation
        print(f"\n🔍 MARKET RESEARCH:")
        print(f"Analyzing competing routes...")
        
        competing_routes = [
            {"node": "CompetitorA", "base": 1000, "rate": 800, "reliability": 0.95},
            {"node": "CompetitorB", "base": 500, "rate": 1200, "reliability": 0.90},
            {"node": "CompetitorC", "base": 2000, "rate": 600, "reliability": 0.98},
            {"node": "YourNode", "base": 1000, "rate": 1000, "reliability": 0.92}
        ]
        
        print(f"\n📊 COMPETITIVE ANALYSIS:")
        for route in competing_routes:
            # Calculate fee for 1M sat payment
            sample_amount = 1000000000  # 1M sats in msat
            total_fee = self.calculate_routing_fee(sample_amount, route["base"], route["rate"])
            fee_sats = total_fee / 1000
            
            indicator = "👈 YOU" if route["node"] == "YourNode" else ""
            print(f"   {route['node']}: {fee_sats:.1f} sats fee, {route['reliability']*100:.0f}% uptime {indicator}")
        
        # Optimization strategies
        print(f"\n🎯 OPTIMIZATION STRATEGIES:")
        
        strategies = [
            {
                "name": "Undercut Competition",
                "description": "Set fees slightly below competitors",
                "pros": ["Higher volume", "Market share growth"],
                "cons": ["Lower margins", "Race to bottom"]
            },
            {
                "name": "Premium Pricing",
                "description": "Charge higher fees for better service",
                "pros": ["Higher margins", "Quality positioning"],
                "cons": ["Lower volume", "Need excellent uptime"]
            },
            {
                "name": "Dynamic Pricing",
                "description": "Adjust fees based on demand/liquidity",
                "pros": ["Optimized revenue", "Automatic balancing"],
                "cons": ["Complexity", "May discourage usage"]
            },
            {
                "name": "Value-Based Pricing",
                "description": "Different fees for different routes",
                "pros": ["Route optimization", "Higher overall revenue"],
                "cons": ["Management overhead", "Market knowledge needed"]
            }
        ]
        
        for i, strategy in enumerate(strategies, 1):
            print(f"\n{i}️⃣ {strategy['name']}")
            print(f"   📝 {strategy['description']}")
            print(f"   ✅ Pros: {', '.join(strategy['pros'])}")
            print(f"   ❌ Cons: {', '.join(strategy['cons'])}")
        
        # Interactive fee setting
        if os.environ.get("BITCOIN_TEST_MODE") == "1":
            print("🧪 Test mode: Using optimal fee strategy...")
            self.show_optimal_fees()
        else:
            print(f"\n🤔 Which strategy appeals to you?")
            try:
                choice = int(input("Enter strategy number (1-4): "))
                if 1 <= choice <= len(strategies):
                    chosen = strategies[choice - 1]
                    print(f"\n✅ You chose: {chosen['name']}")
                    self.implement_fee_strategy(chosen)
            except (ValueError, KeyboardInterrupt):
                print("\n👋 Fee optimization interrupted")
    
    def implement_fee_strategy(self, strategy: Dict):
        """Implement chosen fee strategy"""
        print(f"\n🔧 IMPLEMENTING {strategy['name'].upper()}")
        print(f"=" * (len(strategy['name']) + 15))
        
        if strategy['name'] == "Undercut Competition":
            print("💡 Setting fees 10% below lowest competitor...")
            print("   Base fee: 900 msat (was 1000)")
            print("   Fee rate: 720 ppm (was 1000)")
            print("📈 Expected: +40% volume, -15% margin")
            
        elif strategy['name'] == "Premium Pricing":
            print("💡 Setting premium fees with reliability guarantee...")
            print("   Base fee: 1500 msat (was 1000)")
            print("   Fee rate: 1200 ppm (was 1000)")
            print("📈 Expected: -20% volume, +35% margin")
            
        elif strategy['name'] == "Dynamic Pricing":
            print("💡 Implementing dynamic fee adjustments...")
            print("   Low liquidity: Higher fees (discourage usage)")
            print("   High liquidity: Lower fees (encourage usage)")
            print("📈 Expected: Optimized revenue, balanced channels")
            
        elif strategy['name'] == "Value-Based Pricing":
            print("💡 Setting different fees per route...")
            print("   Popular routes: Higher fees")
            print("   Underutilized routes: Lower fees")
            print("📈 Expected: Better capital allocation")
        
        print(f"\n⏰ Remember to monitor results and adjust!")
    
    def show_optimal_fees(self):
        """Show optimal fee calculation for test mode"""
        print("🎯 Optimal Fee Calculation:")
        print("Market analysis suggests:")
        print("   Base fee: 800-1200 msat")
        print("   Fee rate: 500-1500 ppm")
        print("🧪 Recommended: 1000 msat base, 800 ppm rate")
        print("📊 Balance of competitiveness and profitability")
    
    def demonstrate_economic_security(self):
        """Demonstrate economic security model"""
        print("\n🛡️ ECONOMIC SECURITY MODEL")
        print("=" * 35)
        print("How economics secure the Lightning Network...")
        
        print(f"\n💼 CAPITAL REQUIREMENTS:")
        print(f"🔹 Node operators lock real Bitcoin in channels")
        print(f"🔹 Capital is at risk if misbehavior is detected")
        print(f"🔹 Economic incentive to behave honestly")
        
        # Security scenarios
        security_scenarios = [
            {
                "scenario": "Honest Routing",
                "capital": 10000000,  # 10M sats
                "daily_revenue": 5000,  # 5k sats/day
                "risk": "None",
                "outcome": "Steady income"
            },
            {
                "scenario": "Failed Payment Routing",
                "capital": 10000000,
                "daily_revenue": -1000,  # Lost reputation
                "risk": "Reputation damage",
                "outcome": "Reduced future volume"
            },
            {
                "scenario": "Channel Force Close",
                "capital": 10000000,
                "daily_revenue": -50000,  # On-chain fees
                "risk": "High on-chain fees",
                "outcome": "Significant cost"
            },
            {
                "scenario": "Attempted Fraud",
                "capital": 10000000,
                "daily_revenue": -10000000,  # Lose all capital
                "risk": "Total capital loss", 
                "outcome": "Complete financial loss"
            }
        ]
        
        print(f"\n📊 ECONOMIC INCENTIVE ANALYSIS:")
        for scenario in security_scenarios:
            capital_sats = scenario["capital"] // 1000
            revenue_sats = scenario["daily_revenue"] // 1000 if scenario["daily_revenue"] > 0 else scenario["daily_revenue"] // 1000
            
            print(f"\n🎭 {scenario['scenario']}:")
            print(f"   💰 Capital at stake: {capital_sats:,} sats")
            if scenario["daily_revenue"] > 0:
                print(f"   📈 Daily revenue: +{revenue_sats:,} sats")
            else:
                print(f"   📉 Daily cost: {revenue_sats:,} sats")
            print(f"   ⚠️ Risk: {scenario['risk']}")
            print(f"   🎯 Outcome: {scenario['outcome']}")
        
        print(f"\n🔒 SECURITY MECHANISMS:")
        print(f"⚡ HTLCs ensure atomic payments")
        print(f"⏰ Time locks prevent fund lockup")
        print(f"🔑 Cryptographic proofs prevent fraud")
        print(f"💰 Economic penalties discourage attacks")
        print(f"🌐 Network effects reward honest behavior")
        
        print(f"\n💡 KEY INSIGHT:")
        print(f"Lightning security comes from economic rationality:")
        print(f"   It's more profitable to be honest than dishonest!")
    
    def economics_quiz(self):
        """Interactive quiz about Lightning economics"""
        print("\n🧠 LIGHTNING ECONOMICS QUIZ")
        print("=" * 35)
        
        questions = [
            {
                "question": "What are the two components of Lightning routing fees?",
                "options": [
                    "A. Mining fee and network fee",
                    "B. Base fee and fee rate",
                    "C. Channel fee and routing fee", 
                    "D. Fixed fee and variable fee"
                ],
                "answer": "B",
                "explanation": "Lightning fees have a base fee (fixed per payment) and fee rate (proportional to amount)."
            },
            {
                "question": "What determines Lightning Network security?",
                "options": [
                    "A. Mining power",
                    "B. Number of nodes",
                    "C. Economic incentives",
                    "D. Government regulation"
                ],
                "answer": "C",
                "explanation": "Lightning security relies on economic incentives - it's more profitable to be honest."
            },
            {
                "question": "How do node operators earn revenue?",
                "options": [
                    "A. Mining Bitcoin blocks",
                    "B. Routing payment fees",
                    "C. Selling lightning bolts",
                    "D. Government subsidies"
                ],
                "answer": "B", 
                "explanation": "Node operators earn fees by routing payments through their channels."
            },
            {
                "question": "What affects Lightning routing profitability?",
                "options": [
                    "A. Channel capacity only",
                    "B. Fee rates only",
                    "C. Volume, fees, and capital efficiency",
                    "D. Bitcoin price only"
                ],
                "answer": "C",
                "explanation": "Profitability depends on routing volume, competitive fees, and efficient capital use."
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
            print("🏆 Perfect! You understand Lightning economics!")
        elif score >= len(questions) * 0.7:
            print("👍 Great job! You grasp the economic model!")
        else:
            print("📚 Keep learning! Economics drive the network.")
    
    def interactive_business_calculator(self):
        """Interactive Lightning business calculator"""
        print("\n💼 LIGHTNING BUSINESS CALCULATOR")
        print("=" * 45)
        
        if os.environ.get("BITCOIN_TEST_MODE") == "1":
            print("🧪 Test mode: Showing business calculation example...")
            self.show_business_example()
            return
        
        print("🎯 Calculate potential Lightning routing revenue!")
        
        try:
            print("\n📝 Enter your parameters:")
            capital = int(input("Total capital to deploy (sats): "))
            avg_fee_rate = int(input("Average fee rate (ppm, e.g., 1000 = 0.1%): "))
            daily_volume_multiple = float(input("Daily volume as multiple of capital (e.g., 0.5 = 50%): "))
            
            # Calculate projections
            daily_volume = capital * daily_volume_multiple
            daily_revenue = (daily_volume * avg_fee_rate) // 1000000
            monthly_revenue = daily_revenue * 30
            annual_revenue = daily_revenue * 365
            annual_yield = (annual_revenue / capital) * 100
            
            print(f"\n📊 BUSINESS PROJECTIONS:")
            print(f"=" * 30)
            print(f"💰 Capital Deployed: {capital:,} sats")
            print(f"📊 Daily Volume: {daily_volume:,.0f} sats")
            print(f"💵 Daily Revenue: {daily_revenue:,} sats")
            print(f"📅 Monthly Revenue: {monthly_revenue:,} sats")
            print(f"🗓️ Annual Revenue: {annual_revenue:,} sats")
            print(f"📈 Annual Yield: {annual_yield:.2f}%")
            
            # Risk analysis
            print(f"\n⚠️ RISK CONSIDERATIONS:")
            print(f"🔄 Rebalancing costs: ~10-20% of revenue")
            print(f"⚡ Channel closure costs: ~0.1-1% of capital")
            print(f"📉 Volume volatility: Revenue can vary ±50%")
            print(f"🏦 Opportunity cost: Compare to other investments")
            
            # Break-even analysis
            monthly_btc_price = 50000  # Assume $50k BTC for calculation
            monthly_revenue_usd = (monthly_revenue / 100000000) * monthly_btc_price
            print(f"\n💲 USD Equivalent (assuming $50k BTC):")
            print(f"📅 Monthly Revenue: ~${monthly_revenue_usd:.2f}")
            
            if monthly_revenue_usd > 100:
                print("✅ Potentially viable business!")
            elif monthly_revenue_usd > 20:
                print("⚖️ Marginal business case")
            else:
                print("❌ Likely not profitable as primary business")
                
        except (ValueError, KeyboardInterrupt):
            print("\n👋 Calculator interrupted")
    
    def show_business_example(self):
        """Show business calculation example for test mode"""
        print("💼 Lightning Business Example:")
        print("Capital: 50,000,000 sats (0.5 BTC)")
        print("Fee rate: 1000 ppm (0.1%)")
        print("Daily volume: 25,000,000 sats (50% of capital)")
        print("\nProjections:")
        print("   Daily revenue: 25,000 sats")
        print("   Monthly revenue: 750,000 sats")
        print("   Annual yield: 18.25%")
        print("🧪 Attractive returns but requires active management!")

def main():
    """Main function for economics demo"""
    print("💰 Welcome to Lightning Network Economics!")
    print("Understanding the business model and incentives")
    
    demo = LightningEconomicsDemo()
    
    try:
        # Fee structure
        demo.demonstrate_fee_structure()
        
        # Liquidity economics
        print("\n" + "="*60)
        demo.demonstrate_liquidity_economics()
        
        # Fee optimization
        print("\n" + "="*60)
        demo.demonstrate_fee_optimization()
        
        # Economic security
        print("\n" + "="*60)
        demo.demonstrate_economic_security()
        
        # Interactive elements
        if os.environ.get("BITCOIN_TEST_MODE") != "1":
            print("\n" + "="*60)
            print("🛠️ Want to calculate Lightning business potential?")
            calc_choice = input("Try the business calculator? (y/n): ").lower().strip()
            if calc_choice == 'y':
                demo.interactive_business_calculator()
            
            print("\n🎓 Ready for the economics quiz?")
            quiz_choice = input("Test your knowledge? (y/n): ").lower().strip()
            if quiz_choice == 'y':
                demo.economics_quiz()
        else:
            demo.interactive_business_calculator()
            demo.economics_quiz()
            
        print("\n🎉 Economics Demo Complete!")
        print("💡 You now understand Lightning's economic model!")
        
    except KeyboardInterrupt:
        print("\n👋 Economics demo ended")
    except Exception as e:
        print(f"\n❌ Error in demo: {e}")

if __name__ == "__main__":
    main()