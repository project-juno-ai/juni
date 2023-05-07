import discord
from datetime import datetime
import juni_core
import juni_vision
import juni_memory
import os
import prompts
import asyncio

BOT_TOKEN = os.environ.get('JUNI_BOT_TOKEN')
HOME_CHANNEL_NAME = "junis-room"
RECEIPTS_CHANNEL_NAME = 'receipts'

print(juni_memory.connection_string)

intents = discord.Intents.all()
intents.messages = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.name == RECEIPTS_CHANNEL_NAME:
        await receipt_skill(message)

async def send_message(message, channel_name=HOME_CHANNEL_NAME):
    if message is None or message.strip() == "":
        return

    channel = discord.utils.get(bot.get_all_channels(), name=channel_name)
    message_parts = [message[i:i + 1500] for i in range(0, len(message), 1500)]

    for part in message_parts:
        await channel.send(part)

current_receipt_chat = None

async def receipt_skill(message):
    global current_receipt_chat

    if len(message.attachments) == 1:
        attachment = message.attachments[0]
        if attachment.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            receipt = await asyncio.to_thread(lambda: juni_vision.see_receipt(attachment.url))
            if receipt != None:
                print(receipt)
                current_receipt_chat = juni_core.init_chat(prompts.receipt_prompt.format(receipt))
                await send_message(receipt, RECEIPTS_CHANNEL_NAME)

    if current_receipt_chat != None:
        juni_response = await asyncio.to_thread(lambda: juni_core.send_message_to_chat(message.content, current_receipt_chat)) 
        print(juni_response)

        if 'INSERT INTO' in juni_response:
            lines = juni_response.split('\n')
            text_message = '\n'.join([line for line in lines if not line.startswith('INSERT INTO')])
            sql_script = '\n'.join([line for line in lines if line.startswith('INSERT INTO')])

            print(text_message)
            print(sql_script)

            await send_message(text_message, RECEIPTS_CHANNEL_NAME)
            await send_message(sql_script, RECEIPTS_CHANNEL_NAME)

            await asyncio.to_thread(lambda: juni_memory.execute_sql_script(sql_script))

            juni_final_message = await asyncio.to_thread(lambda: juni_core.send_single_message(prompts.personality, "Let Juni say that we are done with the receipt (First person)", creative=True))
            await send_message(juni_final_message, RECEIPTS_CHANNEL_NAME)

            current_receipt_chat = None
        else:
            await send_message(juni_response, RECEIPTS_CHANNEL_NAME)
        

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
