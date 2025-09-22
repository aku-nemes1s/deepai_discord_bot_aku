import os
import discord
import requests
from discord.ext import commands

# ----------------- CONFIG -----------------
# Use environment variables for security
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
DEEP_AI_KEY = os.environ.get("DEEP_AI_KEY")

if not DISCORD_TOKEN or not DEEP_AI_KEY:
    raise ValueError("Missing DISCORD_TOKEN or DEEP_AI_KEY in environment variables.")

# ----------------- INTENTS -----------------
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Needed to read message content

# ----------------- BOT SETUP -----------------
bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------- EVENTS -----------------
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# ----------------- COMMANDS -----------------
@bot.command(name="ai", help="Generate AI text using DeepAI. Usage: !ai your prompt")
async def ai(ctx, *, prompt: str):
    await ctx.send("Thinking... 🤔")

    try:
        response = requests.post(
            "https://api.deepai.org/api/text-generator",
            data={"text": prompt},
            headers={"api-key": DEEP_AI_KEY},
            timeout=15
        )
        data = response.json()
        ai_text = data.get("output", "No response from DeepAI.")
    except Exception as e:
        ai_text = f"Error contacting DeepAI API: {e}"

    # Discord messages have a max length of 2000 chars
    if len(ai_text) > 2000:
        ai_text = ai_text[:1997] + "..."

    await ctx.send(ai_text)

# ----------------- RUN BOT -----------------
bot.run(DISCORD_TOKEN)
