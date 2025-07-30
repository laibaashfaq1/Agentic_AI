<!-- Class Assignment -->
# Need to implement and Crypto Currency API that fetches that realtime data of Digital Coins

# API Endpoint: Get all coins: 
https://api.binance.com/api/v3/ticker

# Get coin by Symbol: 
https://api.binance.com/api/v3/ticker/price?symbol={currency}

# Submission Link: 
https://forms.gle/1TPU9hNtLWYDRsCo8


# own apis
api.binance.com/api/v3/ticker/price

api.binance.com/api/v3/ticker/price?symbol=B3CUSDTa





<!-- Required Installments -->
uv init .
uv venv
.venv\Scripts\activate
uv run main.py
uv pip install requests
uv add chainlit
chainlit run main.py
uv add openai-agents
uv add load_dotenv