# Bitcoin Transactions Bootcamp

A hands-on educational program designed to teach Bitcoin fundamentals through interactive Python scripts and practical demonstrations using Polar Lightning Network.

## Overview

This bootcamp provides students with a comprehensive understanding of how Bitcoin works at the implementation level. Through six interactive modules, participants will explore Bitcoin's core mechanisms including transactions, blockchain structure, proof-of-work consensus, network architecture, mining economics, and modern development tools.

## Prerequisites

- **Polar Lightning Network** - Local Bitcoin development environment
- **Python 3.7+** - Programming language for scripts
- **Docker** - Required for Polar
- Basic programming knowledge (helpful but not required)

## Course Structure

### Module 1: Transactions & UTXO Model (45 minutes)
Learn how Bitcoin moves value through the Unspent Transaction Output (UTXO) model.
- Understanding inputs, outputs, and transaction fees
- Hands-on transaction building and analysis
- Real Bitcoin transaction exploration

### Module 2: Blockchain Structure (45 minutes)
Explore Bitcoin's tamper-proof distributed ledger.
- Block anatomy and cryptographic linking
- Immutability demonstrations
- Blockchain validation mechanisms

### Module 3: Proof of Work & Mining (45 minutes)
Experience Bitcoin's consensus mechanism through interactive mining simulations.
- Mining competitions and difficulty adjustment
- Hash rate and energy considerations
- Real mining data analysis

### Module 4: Network & Storage (30 minutes)
Understand Bitcoin's peer-to-peer architecture and data management.
- Transaction propagation simulation
- Mempool monitoring
- Data storage optimization

### Module 5: Mining Economics (45 minutes)
Analyze Bitcoin's economic incentive system.
- Halving events and supply schedule
- Fee markets and transaction priority
- Mining profitability calculations

### Module 6: Modern Bitcoin Development (30 minutes)
Introduction to contemporary Bitcoin development tools.
- Bitcoin Development Kit (BDK)
- Key and address generation
- Transaction building with modern APIs

## Getting Started

### 1. Environment Setup
```bash
# Install Polar Lightning Network
# Download from: https://lightningpolar.com

# Create Python virtual environment
python3 -m venv bitcoin_bootcamp_env
source bitcoin_bootcamp_env/bin/activate
pip install requests
```

### 2. Network Configuration
1. Launch Polar application
2. Create new network with 1 Bitcoin Core node
3. Start the network and mine 110+ blocks
4. Verify connection with test script

### 3. Running the Bootcamp
```bash
# Test your setup
python test_scripts.py

# Run individual modules
python scripts/1_transactions.py
python scripts/2_blockchain.py
python scripts/3_proof_of_work.py
python scripts/4_network_and_storage.py
python scripts/5_mining_and_incentives.py
python scripts/bdk_bitcoin_demo.py
```

## Key Features

- **Real Bitcoin Network Interaction** - Uses actual Bitcoin Core via Polar's regtest environment
- **Interactive Learning** - Hands-on exercises, competitions, and real-time demonstrations
- **Progressive Complexity** - Builds understanding from basic concepts to advanced topics
- **Practical Application** - Students build actual Bitcoin transactions and applications
- **Modern Tools** - Introduction to professional Bitcoin development frameworks

## Learning Outcomes

Upon completion, students will be able to:
- Explain the UTXO model and how it differs from traditional account systems
- Analyze and construct Bitcoin transactions
- Understand blockchain immutability and cryptographic security
- Describe proof-of-work consensus and mining economics
- Navigate Bitcoin's peer-to-peer network architecture
- Use modern Bitcoin development tools and APIs

## Technical Architecture

The bootcamp leverages:
- **Polar Lightning Network** for local Bitcoin Core node management
- **Python scripts** for interactive demonstrations and exercises
- **Bitcoin Core RPC API** for real blockchain interaction
- **Bitcoin Development Kit (BDK)** for modern development practices

## File Structure

```
transactions_bootcamp/
├── README.md                    # This file
├── test_scripts.py             # Pre-bootcamp environment testing
├── scripts/                    # Educational modules
│   ├── 1_transactions.py       # UTXO model and transaction mechanics
│   ├── 2_blockchain.py         # Blockchain structure and security
│   ├── 3_proof_of_work.py      # Mining and consensus mechanisms
│   ├── 4_network_and_storage.py # P2P network and data management
│   ├── 5_mining_and_incentives.py # Economic incentives and halving
│   └── bdk_bitcoin_demo.py     # Modern Bitcoin development tools
└── .gitignore                  # Version control exclusions
```

## Contributing

This is an educational project designed for Bitcoin fundamentals instruction. Contributions that enhance learning outcomes or fix technical issues are welcome.

## License

This project is intended for educational use. Please respect Bitcoin's open-source ecosystem and the tools that make this education possible.

---

**Transform theoretical Bitcoin knowledge into practical understanding through hands-on experience.**