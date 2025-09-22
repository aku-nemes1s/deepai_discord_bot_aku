import discord
import requests

# ---- Config ----
DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"
DEEP_AI_KEY = "YOUR_DEEPAI_API_KEY"

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # needed for reading messages

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Command trigger, e.g., !ai
    if message.content.startswith("!ai"):
        prompt = message.content[len("!ai "):]  # get text after !ai
        await message.channel.send("Thinking... 🤔")

        # Send request to DeepAI API
        response = requests.post(
            "https://api.deepai.org/api/text-generator",
            data={'text': prompt},
            headers={'api-key': DEEP_AI_KEY}
        )

        result = response.json()
        ai_text = result.get('output', 'No response from AI.')

        await message.channel.send(ai_text)

client.run(DISCORD_TOKEN)
