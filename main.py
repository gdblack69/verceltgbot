from telethon import TelegramClient, events
import os
import asyncio

source_api_id = 26697231  # Replace with your first API ID
source_api_hash = '35f2769c773534c6ebf24c9d0731703a'  # Replace with your first API Hash
source_chat_id = -4564401074  # Replace with the chat ID to listen to

destination_api_id = 14135677  # Replace with your second API ID
destination_api_hash = 'edbecdc187df07fddb10bcff89964a8e'  # Replace with your second API Hash
destination_bot_username = '@gpt3_unlim_chatbot'  # Replace with the bot's username

source_session_file = "source_session.session"
destination_session_file = "destination_session.session"

source_client = TelegramClient(source_session_file, source_api_id, source_api_hash)
destination_client = TelegramClient(destination_session_file, destination_api_id, destination_api_hash)

async def handle_disconnection():
    while True:
        try:
            await source_client.run_until_disconnected()
        except Exception as e:
            print(f"Error: {e}. Reconnecting...")
            await asyncio.sleep(5)
            await source_client.start()

@source_client.on(events.NewMessage(chats=source_chat_id))
async def forward_message(event):
    source_id_message = event.raw_text
    custom_message = f"""
"{source_id_message}"
 
If the quoted text within double quotation marks is not a trading signal, respond with "Processing your question....". If it is a trading signal, extract the necessary information and fill out the form below.
Symbol: 
Price: 
Stop Loss: 
Take Profit: 
"""
    async with destination_client:
        try:
            await destination_client.send_message(destination_bot_username, custom_message)
            print("Custom message forwarded.")
        except Exception as e:
            print(f"Error: {e}")

async def main():
    print("Starting both clients...")
    await source_client.start()
    await destination_client.start()
    print("Bot is running... Waiting for messages...")
    await handle_disconnection()

def handler(request):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())  # Start the bot on request
    return "Bot is running", 200  # A simple response
