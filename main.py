# Import required libraries
import itertools
# Generate all possible combinations of a given iterable
import random
# Generate random numbers
from bitcoinlib.wallets import Wallet
# Handle bitcoin wallets
import tkinter as tk
# Create a Tkinter interface
from tkinter import ttk
# Create a ttk interface
from colorama import Fore, init
# Initialize colorama
# Colorama is a Python library for printing colored text and colored terminal
# It also provides autoreset feature which resets the color to default after
# each print
from flask import Flask, render_template_string, jsonify
# Flask is a web framework that allows you to create web applications
# It provides a set of functions and classes to handle requests and responses
# render_template_string is a function that renders a template string
# jsonify is a function that returns a json response
from flask.sansio.scaffold import F
# This is a module that provides a set of functions and classes to handle
# requests and responses
import matplotlib.pyplot as plt
# Matplotlib is a Python library for creating static, animated, and interactive
# visualizations in Python
import io
# This is a module that provides a set of functions and classes to handle
# input/output operations
import base64
# This is a module that provides a set of functions and classes to handle
# encoding and decoding of binary data into text
import time
# This is a module that provides a set of functions and classes to handle
# time-related operations
from colorama import Back, Style
# Colorama is a Python library for printing colored text and colored terminal
# It also provides autoreset feature which resets the color to default after
# each print
from random import randint
# This is a function that generates a random integer
from threading import Thread, Lock
# This is a module that provides a set of functions and classes to handle
# threading operations
# It provides a set of functions and classes to handle synchronization of
# threads

# Initialize colorama
init(autoreset=True)

# Global variables
found_wallets = []
# A list that stores all the wallets that have been found
found_wallets_no_balance = []
# A list that stores all the wallets that do not have any balance
money = 0
# A variable that stores the total amount of money in all the wallets
lock = Lock()
# A variable that stores a lock object to be used for synchronization
started_time = time.time()
# A variable that stores the time when the program started

# Global variables for Tkinter
root = None
# A variable that stores the root window of the Tkinter interface
right_frame_top = None
# A variable that stores the top right frame of the Tkinter interface
right_frame_bottom = None
# A variable that stores the bottom right frame of the Tkinter interface

# Flask app
app = Flask(__name__)


@app.route('/data')
def get_data():
  # This function returns a json response with the data of all the wallets
  # It is called when the user requests the /data endpoint
  with lock:
    # This is a context manager that acquires the lock before executing the
    # code and releases the lock after the code has been executed
    data = {
        "found_wallets": found_wallets,
        # A key that stores the list of all the wallets that have been found
        "found_wallets_no_balance": found_wallets_no_balance,
        # A key that stores the list of all the wallets that do not have any
        # balance
        "wallets_with_balance_count": len(found_wallets),
        # A key that stores the number of wallets that have any balance
        "wallets_no_balance_count": len(found_wallets_no_balance),
        # A key that stores the number of wallets that do not have any balance
        "money": money
        # A key that stores the total amount of money in all the wallets
    }
  return jsonify(data)


@app.route('/')
def index():
    # This function returns an html response with the interface of the
    # application
    # It is called when the user requests the / endpoint
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Metadata about the character encoding and viewport settings -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- Title of the web page -->
    <title>CryptoSentinel Dashboard</title>
    
    <!-- Including Chart.js library for rendering charts -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Internal CSS styles -->
    <style>
        /* Styling for the body of the page */
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 0;
        }}
        
        /* Styling for the header section */
        header {{
            background: #343a40;
            color: #fff;
            padding: 10px;
            text-align: center;
        }}
        
        /* Container styling for centralizing content */
        .container {{
            padding: 20px;
            max-width: 1200px;
            margin: auto;
        }}
        
        /* Flexbox styling for statistics section */
        .stats {{
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }}
        
        /* Card styling for individual statistics */
        .stat-card {{
            background: #fff;
            margin: 10px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            text-align: center;
            flex: 1 1 20%;
        }}
        
        /* Styling for titles within statistic cards */
        .stat-card h2 {{
            margin: 0;
            font-size: 1.2em;
        }}
        
        /* Styling for paragraph text in statistic cards */
        .stat-card p {{
            font-size: 1.8em;
            color: #17a2b8;
        }}
        
        /* Chart container styling for centralized chart display */
        .chart-container {{
            max-width: 800px;
            margin: 20px auto;
        }}
    </style>
</head>
<body>
    <!-- Header section with the main title -->
    <header>
        <h1>CryptoSentinel Dashboard</h1>
    </header>
    
    <!-- Main container for content -->
    <div class="container">
        <!-- Section for displaying wallet statistics -->
        <div class="stats">
            <!-- Card for wallets with balance -->
            <div class="stat-card">
                <h2>Wallets with Balance</h2>
                <p id="wallets-balance">Loading...</p>
            </div>

            <!-- Card for wallets without balance -->
            <div class="stat-card">
                <h2>Wallets with No Balance</h2>
                <p id="wallets-no-balance">Loading...</p>
            </div>

            <!-- Card for total money in BTC -->
            <div class="stat-card">
                <h2>Total Money (BTC)</h2>
                <p id="total-money">Loading...</p>
            </div>
        </div>
        
        <!-- Container for the doughnut chart -->
        <div class="chart-container">
            <canvas id="walletChart"></canvas>
        </div>
    </div>
    
    <!-- JavaScript section for dynamic data fetching and chart updates -->
    <script>
        // Function to fetch data from the server
        const fetchData = async () => {{
            const response = await fetch('/data');
            const data = await response.json();
            
            // Update the statistics on the page
            document.getElementById('wallets-balance').innerText = data.wallets_with_balance_count;
            document.getElementById('wallets-no-balance').innerText = data.wallets_no_balance_count;
            document.getElementById('total-money').innerText = data.money;
            
            // Update the doughnut chart with new data
            updateChart(data.wallets_with_balance_count, data.wallets_no_balance_count);
        }};

        // Function to update the chart
        const updateChart = (balance, noBalance) => {{
            const ctx = document.getElementById('walletChart').getContext('2d');
            // Create a new Chart.js doughnut chart
            new Chart(ctx, {{
                type: 'doughnut',
                data: {{
                    labels: ['With Balance', 'No Balance'],
                    datasets: [{{
                        data: [balance, noBalance],
                        backgroundColor: ['#007bff', '#6c757d']
                    }}]
                }},
                options: {{
                    responsive: true,
                }}
            }});
        }};

        // Set an interval to refresh data every 5 seconds
        setInterval(fetchData, 5000);

        // Initial data fetch when the page loads
        fetchData();
    </script>
</body>
</html>

    """
    return render_template_string(html)


# Flask thread
def start_flask_app():
  """
  Start the Flask web server in a separate thread
  """
  app.run(debug=False, host="127.0.0.1", port=8080)

flask_thread = Thread(target=start_flask_app)
flask_thread.daemon = True

# Function to add items to the boxes
def add_to_box(box, content):
  """
  Add a label to the given box with the given content
  """
  ttk.Label(box, text=content).pack(anchor="w", padx=5, pady=2)


def lostwallets(filename, r=24, num_combinations=1, visualize=False):
  """
  Generate random combinations of words and check for wallets with a balance

  :param filename: file containing words to generate combinations from
  :param r: number of words to use in each combination
  :param num_combinations: number of combinations to generate
  :param visualize: whether to display the results using Tkinter
  """
  # Read words from file
  # Open the file and read all the lines into a list
  with open(filename, 'r') as file:
    words = [line.strip() for line in file.readlines()]

  # Check if there are enough words to generate combinations from
  if len(words) < r:
    # If not, print an error message and return
    print(
        f"Error: Not enough words. The file contains only {len(words)} words.")
    return

  # Initialize visualization components if required
  for _ in range(num_combinations):
    # Generate a random combination of words
    random_combination = random.sample(words, r)
    # Join the words together with spaces to form a seed phrase
    seed_phrase = " ".join(random_combination)

    try:
      # Create a wallet using the seed phrase
      w = Wallet.create(f"Wallet_{_}", keys=seed_phrase, network='bitcoin')
      # Get the balance of the wallet
      balance = w.balance()

      # If the balance is 0, print a message and add it to the list
      if balance == 0:
        print(Fore.BLUE + "0.0 BTC - Wallet found")
        with open('found_wallets_no_balance.txt', 'a') as f:
          f.write(seed_phrase + '\n')
        if visualize:
          # Add the seed phrase to the top frame
          add_to_box(right_frame_top, seed_phrase)
          # Update the display
          root.update()
      else:
        # If the balance is not 0, print a message and add it to the list
        print(Fore.GREEN + f"{balance} BTC - Wallet found")
        with open('found_wallets.txt', 'a') as f:
          f.write(f"{seed_phrase}\n{balance} BTC\n")
        if visualize:
          # Add the seed phrase to the bottom frame
          add_to_box(right_frame_bottom, f"Wallet with balance: {balance} BTC")
          # Update the display
          root.update()
    except Exception as e:
      # If there is an exception, print the exception and continue
      pass
  # Start the Tkinter main loop if visualization is enabled
  if visualize:
    root.mainloop()



def create_scrollable_frame(parent, width, height):
  """
  Create a scrollable frame with the given width and height

  :param parent: parent widget
  :param width: width of the frame
  :param height: height of the frame
  """
  # Create a canvas and a scrollbar
  canvas = tk.Canvas(parent, width=width, height=height)
  scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)

  # Create a frame inside the canvas
  scrollable_frame = ttk.Frame(canvas)

  # Bind the configure event to update the scroll region
  scrollable_frame.bind(
      "<Configure>",
      lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

  # Create the window inside the canvas and add the frame to it
  canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

  # Configure the canvas and scrollbar
  canvas.configure(yscrollcommand=scrollbar.set)
  canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
  scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

  # Return the scrollable frame
  return scrollable_frame


def tkinterload():
  global root, right_frame_top, right_frame_bottom

  # Create the main window
  root = tk.Tk()
  root.title("Lost Crypto Wallets")
  root.geometry("600x400")

  # Create the left frame
  left_frame = ttk.Frame(root, width=200, height=400, relief=tk.RIDGE)
  # Create the right frame
  right_frame_top = ttk.Frame(root, width=200, height=200, relief=tk.RIDGE)
  right_frame_bottom = ttk.Frame(root, width=200, height=200, relief=tk.RIDGE)

  # Disable propagation for the frames
  left_frame.pack_propagate(False)
  right_frame_top.pack_propagate(False)
  right_frame_bottom.pack_propagate(False)

  # Pack the frames
  left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
  right_frame_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
  right_frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

  # Create scrollable frames
  create_scrollable_frame(left_frame, 200, 400)
  create_scrollable_frame(right_frame_top, 200, 200)
  create_scrollable_frame(right_frame_bottom, 200, 200)


def print_combinations(filename, r=24, visualize=False):
  # Open the file and read all the lines into a list
  with open(filename, 'r') as file:
    words = [line.strip() for line in file.readlines()]

  # Check if there are enough words to generate combinations from
  if len(words) < r:
    # If not, print an error message and return
    print(
        f"Error: Not enough words. The file contains only {len(words)} words.")
    return

  # Iterate over all combinations of words
  for combination in itertools.combinations(words, r):
    # Join the words together with spaces to form a seed phrase
    seed_phrase = " ".join(combination)

    try:
      # Create a wallet using the seed phrase
      w = Wallet.create(f"Wallet_{random.randint(0, 100000)}",
                        keys=seed_phrase,
                        network='bitcoin')
      # Get the balance of the wallet
      balance = w.balance()

      # If the balance is 0, print a message and add it to the list
      if balance == 0:
        print(Fore.BLUE + "0.0 BTC - Wallet found")
        found_wallets_no_balance.append(seed_phrase)
        flask_thread.start()
        with open('found_wallets_no_balance.txt', 'a') as f:
          f.write(seed_phrase + '\n')
        if visualize and right_frame_top:
          # Add the seed phrase to the top frame
          add_to_box(right_frame_top, seed_phrase)
      else:
        # If the balance is not 0, print a message and add it to the list
        money = money + balance
        print(Fore.GREEN + f"{balance} BTC - Wallet found")
        found_wallets.append(seed_phrase)
        with open('found_wallets.txt', 'a') as f:
          f.write(f"{seed_phrase}\n{balance} BTC\n")
        if visualize and right_frame_bottom:
          # Add the seed phrase to the bottom frame
          add_to_box(right_frame_bottom, f"Wallet with balance: {balance} BTC")
    except Exception:
      # If there is an exception, print the exception and continue
      pass


def search(visualize=True,
           r=24,
           num_combinations=10000000000,
           file=True,
           log=False,
           web=False):
    try:
        # Start the timer for the search
        start_time = time.time()

        # Start the Flask thread if web is enabled
        if web:
            flask_thread.start()

        # Load the Tkinter UI if visualization is enabled
        if visualize:
            tkinterload()

        # Print the combinations if log is enabled
        if log:
            print_combinations('words.txt', r=r, visualize=visualize)

        # Search for lost wallets if log is not enabled
        else:
            lostwallets('words.txt',
                        r=r,
                        num_combinations=num_combinations,
                        visualize=visualize)

        # Start the Tkinter main loop if visualization is enabled
        if visualize:
            if root is not None:  # Check to prevent null pointer exception
                root.mainloop()

    except Exception as e:
        # Print the exception if an error occurs
        print(f"An error occurred: {e}")


def checkhistory(filename):
  # Create an empty list to store the results
  empty = []
  number = 0

  # Read words from file and store them in a list (strip trailing newline)
  with open(filename, 'r') as file:
    wallets = [line.rstrip() for line in file]

  # Generate random combinations of words
  print(Fore.YELLOW + ("Checking for transactions..."))

  # Iterate over the wallets and check if there are any transactions
  for i in wallets:
    try:
      seed_phrase = i
      w = Wallet.create(
          str("Wwaalle" + seed_phrase[2] + seed_phrase[10] + seed_phrase[18] +
              "ett" + seed_phrase[randint(0, 24)] + str(randint(0, 100000))),
          keys=seed_phrase,
          network='bitcoin')
      number += 1
      # Check if the wallet has any transactions
      if len(w.transactions_export()) == 0:
        print(Fore.RESET + (str(number) + "/" + str(len(wallets))))
        empty.append(seed_phrase)
      else:
        print(Fore.GREEN + ("Transactions found in wallet"))
        with open('found_wallets_with_transactions.txt', 'a') as file:
          file.write(f"{seed_phrase}\n")
          file.close()
    except:
      pass

  # Print the results of the check
  print(Fore.YELLOW + ("Checking is complete..."))
  print()
  print(Fore.YELLOW + ("Saving empty wallets..."))
  for item in empty:
    with open('emptywallets.txt', 'a') as file2:
      file2.write(f"{item}\n")
  file2.close()
  print(Fore.CYAN + ("Check complete"))
  print(Fore.RESET)


def transfer_balance_to_master_wallet(master_wallet_address):
    # Read the file containing wallets with balance
    with open('wallets_with_balance.txt', 'r') as file:
        # Retrieve all lines, each representing a wallet
        wallets = file.readlines()

    # Iterate over each wallet in the list
    for wallet in wallets:
        # Remove any leading or trailing whitespace
        wallet = wallet.strip()
        # Split the wallet information into seed phrase and balance
        seed_phrase, balance = wallet.split('\n')
        # Extract the numeric value of the balance
        balance = float(balance.split(' ')[0])

        try:
            # Create a wallet object using the seed phrase
            w = Wallet.create(f"Wallet_{seed_phrase}", keys=seed_phrase, network='bitcoin')
            # Send the balance to the master wallet address
            w.send_to(master_wallet_address, balance)
            # Print a success message indicating the transfer details
            print(f"Transferred {balance} BTC from wallet {seed_phrase} to {master_wallet_address}")
        except Exception as e:
            # Print an error message if the transfer fails
            print(f"Error transferring balance from wallet {seed_phrase}: {e}")




#This is the section of the code that will be executed when the program is run
#This is the part you can modify to suit your needs
#Example usage of the functions
search(web=True, log=True)
checkhistory('found_wallets_nobalance.txt')
