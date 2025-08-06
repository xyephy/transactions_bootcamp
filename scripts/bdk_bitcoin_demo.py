#!/usr/bin/env python3
"""
Bitcoin Development Kit (BDK) Educational Demo
Practical demonstration of Bitcoin keys, addresses, and transactions using BDK

Learning Goals:
- Generate and manage Bitcoin keys with BDK
- Create different types of Bitcoin addresses
- Build and analyze transactions
- Connect to Bitcoin networks (testnet/regtest)
- Understand wallet functionality
"""

try:
    import bdkpython as bdk
    BDK_AVAILABLE = True
except ImportError:
    BDK_AVAILABLE = False
    print("⚠️  BDK Python not available. Install with: pip install bdkpython")

import hashlib
import json
import secrets
from typing import Dict, List, Optional
import time

class BitcoinEducationalWallet:
    """Educational Bitcoin wallet using BDK"""
    
    def __init__(self, network_type: str = "regtest"):
        """
        Initialize wallet for educational purposes
        
        Args:
            network_type: "bitcoin", "testnet", or "regtest"
        """
        if not BDK_AVAILABLE:
            print("❌ BDK not available - using simulation mode")
            self.simulation_mode = True
            return
            
        self.simulation_mode = False
        
        # Set network
        if network_type == "bitcoin":
            self.network = bdk.Network.BITCOIN
        elif network_type == "testnet":
            self.network = bdk.Network.TESTNET
        else:  # regtest
            self.network = bdk.Network.REGTEST
        
        print(f"✅ BDK wallet initialized for {network_type}")
        
        # Generate mnemonic and keys
        self.mnemonic = None
        self.wallet = None
        self.blockchain = None
        
    def generate_mnemonic(self, word_count: int = 12) -> str:
        """Generate a BIP39 mnemonic phrase"""
        
        if self.simulation_mode:
            # Simulated mnemonic for demo
            demo_words = [
                "abandon", "ability", "able", "about", "above", "absent",
                "absorb", "abstract", "absurd", "abuse", "access", "accident"
            ]
            return " ".join(demo_words[:word_count])
        
        try:
            # Generate entropy and create mnemonic
            entropy_bits = 128 if word_count == 12 else 256
            entropy = secrets.token_bytes(entropy_bits // 8)
            self.mnemonic = bdk.Mnemonic.from_entropy(entropy)
            
            print(f"🔑 Generated {word_count}-word mnemonic")
            return str(self.mnemonic)
            
        except Exception as e:
            print(f"❌ Error generating mnemonic: {e}")
            return ""
    
    def create_wallet_from_mnemonic(self, mnemonic_str: str, passphrase: str = ""):
        """Create wallet from mnemonic phrase"""
        
        if self.simulation_mode:
            print("🎭 Simulating wallet creation...")
            return
        
        try:
            # Create mnemonic object
            mnemonic = bdk.Mnemonic.from_string(mnemonic_str)
            
            # Create descriptor for receiving addresses (BIP84 - native segwit)
            descriptor_secret_key = bdk.DescriptorSecretKey.from_string(
                f"wpkh({mnemonic}/84'/1'/0'/0/*)"  # testnet path
            )
            
            # Create wallet descriptor
            external_descriptor = bdk.Descriptor.new_bip84(
                descriptor_secret_key,
                bdk.KeychainKind.EXTERNAL,
                self.network
            )
            
            internal_descriptor = bdk.Descriptor.new_bip84(
                descriptor_secret_key,
                bdk.KeychainKind.INTERNAL,
                self.network
            )
            
            # Create wallet
            self.wallet = bdk.Wallet(
                external_descriptor,
                internal_descriptor,
                self.network,
                bdk.DatabaseConfig.MEMORY()
            )
            
            print("✅ Wallet created successfully")
            
        except Exception as e:
            print(f"❌ Error creating wallet: {e}")
    
    def demonstrate_key_generation(self):
        """Show different ways to generate Bitcoin keys"""
        
        print("\n🔐 BITCOIN KEY GENERATION WITH BDK")
        print("="*42)
        
        # Method 1: Generate mnemonic
        print("1️⃣ Generating BIP39 Mnemonic:")
        mnemonic = self.generate_mnemonic(12)
        print(f"   📝 Mnemonic: {mnemonic}")
        print(f"   💡 This is your wallet backup - keep it safe!")
        
        if not self.simulation_mode:
            # Method 2: Extended keys
            print("\n2️⃣ Deriving Extended Keys:")
            try:
                mnemonic_obj = bdk.Mnemonic.from_string(mnemonic)
                
                # Create extended private key
                extended_private_key = bdk.DescriptorSecretKey.from_string(
                    f"[fingerprint]/84'/1'/0'"  # BIP84 testnet path
                )
                
                print(f"   🔑 Extended Private Key derived")
                print(f"   🔓 Can generate unlimited child keys")
                
            except Exception as e:
                print(f"   ❌ Error with extended keys: {e}")
        
        # Method 3: Individual key pairs (simulated)
        print("\n3️⃣ Individual Key Pairs:")
        print("   🎲 Private Key: da2d9c7c7c3b8e4a5f9e1c8d7b6a5d4c3b2a1e9f8d7c6b5a4d3c2b1a9e8d7c6b")
        print("   🔓 Public Key:  03f4d8e2c1b7a3f9e8d2c1b7a6f5d4c3b2a1f0e9d8c7b6a5f4d3c2b1a0f9e8d7")
        print("   📍 Address:     bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh")
        
        return mnemonic
    
    def demonstrate_address_types(self):
        """Show different Bitcoin address types"""
        
        print("\n📍 BITCOIN ADDRESS TYPES")
        print("="*28)
        
        if self.simulation_mode:
            # Demo addresses for each type
            addresses = {
                "Legacy (P2PKH)": "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2",
                "Script Hash (P2SH)": "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy", 
                "Native SegWit (P2WPKH)": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
                "Taproot (P2TR)": "bc1p5cyxnuxmeuwuvkwfem96lqzszd02n6xdcjrs20cac6yqjjwudpxqkedrcr"
            }
            
            for addr_type, address in addresses.items():
                print(f"\n🏷️  {addr_type}:")
                print(f"   Address: {address}")
                print(f"   Starts with: '{address[:2]}'")
                
                # Explain each type
                if "Legacy" in addr_type:
                    print(f"   💡 Original Bitcoin address format")
                    print(f"   📊 Higher transaction fees")
                elif "Script" in addr_type:
                    print(f"   💡 Can represent complex spending conditions")
                    print(f"   🔗 Multisig and other scripts")
                elif "SegWit" in addr_type:
                    print(f"   💡 Lower fees, witness data separate")
                    print(f"   ⚡ Most commonly used today")
                elif "Taproot" in addr_type:
                    print(f"   💡 Most private and efficient")
                    print(f"   🌳 Advanced scripting capabilities")
        
        else:
            try:
                # Generate real addresses if BDK available
                if self.wallet:
                    address_info = self.wallet.get_address(bdk.AddressIndex.NEW())
                    print(f"🏠 Your new address: {address_info.address}")
                    print(f"📍 Address index: {address_info.index}")
                    print(f"🏷️  Type: Native SegWit (bech32)")
                    
            except Exception as e:
                print(f"❌ Error generating address: {e}")
    
    def demonstrate_transaction_building(self):
        """Show how to build Bitcoin transactions with BDK"""
        
        print("\n🧾 BUILDING BITCOIN TRANSACTIONS")
        print("="*36)
        
        if self.simulation_mode:
            print("🎭 Transaction Building Simulation:")
            print("\n📝 Step 1: Create transaction builder")
            print("   builder = TxBuilder()")
            
            print("\n📝 Step 2: Add recipient")
            print("   builder.add_recipient(address, amount)")
            print("   📍 To: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh")
            print("   💰 Amount: 50,000 sats")
            
            print("\n📝 Step 3: Set fee rate")
            print("   builder.fee_rate(10 sat/vB)")
            
            print("\n📝 Step 4: Build transaction")
            print("   (tx, details) = builder.finish(wallet)")
            
            print("\n📊 Transaction Details:")
            print("   📏 Size: 141 vBytes")
            print("   💰 Fee: 1,410 sats")
            print("   ⚖️  Fee rate: 10 sat/vB")
            print("   📥 Inputs: 1")
            print("   📤 Outputs: 2 (payment + change)")
            
            return
        
        try:
            if not self.wallet:
                print("❌ No wallet available")
                return
            
            # Create transaction builder
            tx_builder = bdk.TxBuilder()
            
            # Demo recipient (testnet faucet address)
            recipient_address = "tb1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
            amount_sats = 50000
            
            print(f"📝 Building transaction:")
            print(f"   💰 Amount: {amount_sats:,} sats")
            print(f"   📍 To: {recipient_address}")
            
            # Add recipient to transaction
            tx_builder = tx_builder.add_recipient(
                bdk.Script.from_str(recipient_address),
                amount_sats
            )
            
            # Set fee rate (sats per vbyte)
            fee_rate = 10.0
            tx_builder = tx_builder.fee_rate(fee_rate)
            
            print(f"   ⚖️  Fee rate: {fee_rate} sat/vB")
            
            # Build the transaction
            tx_details = tx_builder.finish(self.wallet)
            
            print(f"\n✅ Transaction built successfully!")
            print(f"   📏 Size: {tx_details.transaction.vsize()} vBytes")
            print(f"   💰 Fee: {tx_details.fee:,} sats")
            print(f"   📥 Inputs: {len(tx_details.transaction.input())}")
            print(f"   📤 Outputs: {len(tx_details.transaction.output())}")
            
            return tx_details
            
        except Exception as e:
            print(f"❌ Error building transaction: {e}")
            return None
    
    def analyze_transaction_details(self, tx_details=None):
        """Analyze transaction inputs and outputs"""
        
        print("\n🔍 TRANSACTION ANALYSIS")
        print("="*25)
        
        if self.simulation_mode or not tx_details:
            print("🎭 Simulated Transaction Analysis:")
            
            print("\n📥 INPUTS:")
            print("   Input #1:")
            print("     🆔 TXID: a1b2c3d4e5f6...9876543210")
            print("     📍 Output Index: 0")
            print("     💰 Amount: 75,000 sats")
            print("     🔐 Unlocking Script: <signature> <pubkey>")
            
            print("\n📤 OUTPUTS:")
            print("   Output #1 (Payment):")
            print("     📍 Address: bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh")
            print("     💰 Amount: 50,000 sats")
            print("     🔒 Locking Script: OP_0 <pubkey_hash>")
            
            print("   Output #2 (Change):")
            print("     📍 Address: bc1q9x8y7z6w5v4u3t2s1r0q9p8o7n6m5l4k3j2h1g0")
            print("     💰 Amount: 23,590 sats")
            print("     🔒 Locking Script: OP_0 <pubkey_hash>")
            
            print("\n📊 Transaction Summary:")
            print("   💰 Total Input:  75,000 sats")
            print("   💰 Total Output: 73,590 sats") 
            print("   💰 Fee Paid:     1,410 sats")
            
            return
        
        try:
            transaction = tx_details.transaction
            
            print("📥 INPUTS:")
            for i, tx_input in enumerate(transaction.input()):
                print(f"   Input #{i+1}:")
                print(f"     🆔 Previous TXID: {tx_input.previous_output.txid}")
                print(f"     📍 Output Index: {tx_input.previous_output.vout}")
                # Note: Amount not directly available in PSBT without UTXO data
            
            print("\n📤 OUTPUTS:")
            for i, tx_output in enumerate(transaction.output()):
                print(f"   Output #{i+1}:")
                print(f"     💰 Amount: {tx_output.value:,} sats")
                print(f"     🔒 Script: {tx_output.script_pubkey}")
            
            print(f"\n📊 Transaction Summary:")
            print(f"   💰 Fee: {tx_details.fee:,} sats")
            print(f"   📏 Virtual Size: {transaction.vsize()} vBytes")
            print(f"   ⚖️  Fee Rate: {tx_details.fee / transaction.vsize():.1f} sat/vB")
            
        except Exception as e:
            print(f"❌ Error analyzing transaction: {e}")
    
    def demonstrate_wallet_sync(self):
        """Show wallet synchronization with blockchain"""
        
        print("\n🔄 WALLET SYNCHRONIZATION")
        print("="*28)
        
        if self.simulation_mode:
            print("🎭 Simulating wallet sync...")
            print("   🔍 Scanning blockchain for transactions...")
            print("   📦 Checked 25,000 blocks")
            print("   🧾 Found 3 transactions")
            print("   💰 Balance: 125,000 sats")
            print("   ⏳ Sync completed in 2.3 seconds")
            return
        
        try:
            if not self.wallet:
                print("❌ No wallet to sync")
                return
            
            # In a real application, you'd connect to a blockchain backend
            print("🔍 Scanning for wallet transactions...")
            print("💡 In real app, this would connect to:")
            print("   • Bitcoin Core node")
            print("   • Electrum server")
            print("   • Block explorer API")
            
            # Get wallet balance
            balance = self.wallet.get_balance()
            print(f"\n💰 Wallet Balance:")
            print(f"   Confirmed: {balance.confirmed:,} sats")
            print(f"   Unconfirmed: {balance.untrusted_pending:,} sats")
            print(f"   Immature: {balance.immature:,} sats")
            
        except Exception as e:
            print(f"❌ Error syncing wallet: {e}")
    
    def interactive_wallet_demo(self):
        """Interactive demonstration of wallet features"""
        
        print("\n🎮 INTERACTIVE WALLET DEMO")
        print("="*30)
        
        # Generate new wallet
        print("🔑 Creating new wallet...")
        mnemonic = self.generate_mnemonic(12)
        
        if not self.simulation_mode:
            self.create_wallet_from_mnemonic(mnemonic)
        
        print(f"✅ Wallet created!")
        print(f"📝 Backup phrase: {mnemonic[:50]}...")
        
        # Show addresses
        print(f"\n📍 Generating receiving addresses:")
        if self.simulation_mode:
            addresses = [
                "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
                "bc1q9x8y7z6w5v4u3t2s1r0q9p8o7n6m5l4k3j2h1g0",
                "bc1qabcdefghijklmnopqrstuvwxyz1234567890abcd"
            ]
            for i, addr in enumerate(addresses):
                print(f"   Address #{i+1}: {addr}")
        else:
            try:
                for i in range(3):
                    if self.wallet:
                        addr_info = self.wallet.get_address(bdk.AddressIndex.NEW())
                        print(f"   Address #{i+1}: {addr_info.address}")
            except Exception as e:
                print(f"   ❌ Error generating addresses: {e}")
        
        # Simulate receiving funds
        print(f"\n💰 Simulating received payments:")
        print(f"   📥 Received 50,000 sats")
        print(f"   📥 Received 25,000 sats") 
        print(f"   📥 Received 100,000 sats")
        print(f"   💼 Total balance: 175,000 sats")
        
        # Show transaction building
        print(f"\n🧾 Building a payment transaction:")
        tx_details = self.demonstrate_transaction_building()
        
        if tx_details or self.simulation_mode:
            self.analyze_transaction_details(tx_details)

def main():
    """Main BDK demonstration"""
    
    print("🎓 BITCOIN DEVELOPMENT KIT (BDK) DEMO")
    print("="*44)
    print("Practical Bitcoin development with BDK")
    
    # Check if BDK is available
    if not BDK_AVAILABLE:
        print("\n⚠️  BDK Python not installed")
        print("📦 Install with: pip install bdkpython")
        print("🎭 Running in simulation mode for educational purposes\n")
    
    # Create educational wallet
    wallet = BitcoinEducationalWallet("regtest")
    
    # Interactive demonstrations
    demos = [
        ("1. Key Generation", wallet.demonstrate_key_generation),
        ("2. Address Types", wallet.demonstrate_address_types),
        ("3. Transaction Building", wallet.demonstrate_transaction_building),
        ("4. Wallet Synchronization", wallet.demonstrate_wallet_sync),
        ("5. Interactive Demo", wallet.interactive_wallet_demo)
    ]
    
    for title, demo_function in demos:
        print(f"\n🎯 {title}")
        try:
            demo_function()
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error in {title}: {e}")
            
        input("\nPress Enter to continue to next demo...") if not os.environ.get("BITCOIN_TEST_MODE") == "1" else print("🧪 Test mode: Skipping input...")
    
    print("\n🎉 BDK DEMO COMPLETE!")
    print("💡 Key takeaways:")
    print("  • BDK simplifies Bitcoin development")
    print("  • Handles key management, addresses, and transactions")
    print("  • Supports all modern Bitcoin features")
    print("  • Great for building Bitcoin applications")
    print("  • Cross-platform and well-documented")
    
    if not BDK_AVAILABLE:
        print("\n📚 To use BDK in real projects:")
        print("  pip install bdkpython")
        print("  https://bitcoindevkit.org/")

if __name__ == "__main__":
    main()