import chainlit as cl
import requests

@cl.on_chat_start
async def start_chat():
    await cl.Message(content="**Welcome to the Crypto Price Tracker!**\nType `Top 10` or a coin symbol like `BTCUSDT` to get live prices!").send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.strip().upper()

    if user_input == "TOP 10":
        url = "https://api.binance.com/api/v3/ticker/price" 
        try:
            response = requests.get(url)
            data = response.json()
            top_10 = "\n".join([f"{c['symbol']}: {c['price']} USDT" for c in data[:10]])
            await cl.Message(content=f"📊 **Top 10 Coins:**\n{top_10}").send()
        except Exception as e:
            await cl.Message(content="❌ Error fetching data from Binance API.").send()

    else:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={user_input}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                await cl.Message(content=f"💰 **Price of {user_input}**: {data['price']} USDT").send()
            else:
                await cl.Message(content="❗ Invalid symbol. Try `BTCUSDT`, `ETHUSDT`, etc.").send()
        except Exception as e:
            await cl.Message(content="⚠️ Error fetching data from Binance API.").send()
