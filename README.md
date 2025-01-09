# CryptoSentinel 🪙 - README

## About ℹ️
Welcome to **CryptoSentinel**! This project is a multi-functional wallet monitoring tool designed to help you recover lost Bitcoin wallets. It employs various functionalities for comprehensive scanning and visualization. 🔍 (I did need to remake this project because one before lost unfortunately)

## Features ✨
- **Random Seed Generation:** Discovers potential wallets by generating random seed phrases. 🔑
- **Wallet Balance Tracking:** Identifies wallets with and without balances. 💰
- **Live Flask Dashboard:** Provides a dynamic web interface for visualizing wallet data (requires enabling the `web` parameter in the `search` function). 📊
- **Tkinter Visualization:** Offers an interactive desktop GUI for real-time monitoring (requires enabling the `visualize` parameter in the search function). 🖥️
- **Transaction History Check:** Scans wallets for existing transactions (uses the `checkhistory` function). 📜
- **Balance Transfer:** Transfers funds from discovered wallets to a specified master wallet address (uses the `transfer_balance_to_master_wallet` function). ➡️

## How to Use ⚙️
1. **Installation:** Install the required dependencies using pip: ⬇️
   ```
   pip install bitcoinlib flask tkinter colorama matplotlib
   ```

2. **Running the Script:** Execute your main script with the desired parameters (explained below). ▶️

   ### Function Parameters: 📝
   - **search(visualize=True, r=24, num_combinations=10000000000, file=True, log=False, web=False):**
     - `visualize (bool, default=True)`: Enables or disables the Tkinter visualization interface. 👁️
     - `r (int, default=24)`: Defines the word length for seed phrase generation. (Bitcoin seed phrases consist of 12 or 24 words) 🔢
     - `num_combinations (int, default=10000000000)`: Specifies the number of random seed phrases to generate. (A higher number increases the chance of finding lost wallets but requires more processing power) 💯
     - `file (bool, default=True)`: Enables or disables saving discovered wallets to a file. 💾
     - `log (bool, default=False)`: Enables or disables printing potential seed phrase combinations to the console for manual inspection. (Useful for debugging or targeted searches) 📃
     - `web (bool, default=False)`: Enables or disables the live Flask dashboard for web-based monitoring. 🌐

   ### Example Usage: 💡
   ```
   search(visualize=False, r=12, num_combinations=1000000, log=True, file=True)  # Search for lost wallets with 12-word seed phrases (faster)
   ```

3. **Checking Transaction History:** Use the `checkhistory` function to scan a file containing potential seed phrases and identify wallets with existing transactions. 🕵️
   ```
   checkhistory("potential_wallets.txt")
   ```
   This will create separate files (`emptywallets.txt` and `found_wallets_with_transactions.txt`) to categorize the scanned wallets. 📂

4. **Balance Transfer:** Utilize the `transfer_balance_to_master_wallet` function to transfer funds from discovered wallets with balances to a specified master wallet address. 💸
   ```
   transfer_balance_to_master_wallet("your_master_wallet_address")  # Replace with your actual master wallet address
   ```

## Technologies Used 🛠️
- **Python:** Main programming language for backend logic. 🐍
- **Flask:** Web framework for building the live dashboard (optional). 🌐
- **Tkinter:** Python's built-in GUI library for the desktop visualization interface (optional). 🖼️
- **Bitcoinlib:** Python library for interacting with the Bitcoin blockchain. 🔗
- **Colorama:** Enhances terminal text coloring for improved readability. 🌈
- **Matplotlib:** Python plotting library (potentially used for data visualization in the dashboard). 📈

## Custom License 📜
Exciting news! 🎉 A custom license for **CryptoSentinel** is found in `LICENSE.md`. This license is designed to empower you to explore, modify, and share this project while respecting the community and its values. 🌍✨

We encourage you to dive in, experiment, and contribute! Your creativity and passion can help shape the future of this project. Let's build something amazing together! 🚀💪

Developed with 💻 by Balogh Barnabás, MasterBros Developers.

## Disclaimer ⚠️
This project is for educational purposes only. Using it to scan random wallets or access Bitcoin funds without permission is **illegal** and unethical. Respect privacy and abide by the law. 🚨 I used AI for my English correcting both in README and on commenting.