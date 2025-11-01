import os, datetime, json, threading, asyncio
from flask import Flask, request
import nextcord
from nextcord.ext import commands

TOKEN   = os.environ["DISCORD_TOKEN"]
CHANNEL = int(os.environ["CHANNEL_ID"])

app  = Flask(__name__)
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"[BOT]  {bot.user} is online")

@app.route("/log", methods=["POST"])
def log_handler():
    data = request.get_json(force=True, silent=True) or {}
    embed = nextcord.Embed(
        title="🔥 Script executed",
        colour=0xff6600,
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="User",     value=data.get("user",    "?"), inline=True)
    embed.add_field(name="PlaceId",  value=data.get("placeId", "?"), inline=True)
    embed.add_field(name="JobId",    value=data.get("jobId",   "?"), inline=True)
    embed.add_field(name="Executor", value=data.get("executor","?"), inline=True)
    if data.get("note"):
        embed.add_field(name="Note", value=data["note"], inline=False)

    asyncio.run_coroutine_threadsafe(
        bot.get_channel(CHANNEL).send(embed=embed), bot.loop
    )
    return "ok", 200

def run_bot():
    bot.run(TOKEN)

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="User",    value=user,    inline=True)
    embed.add_field(name="PlaceId", value=placeId, inline=True)
    embed.add_field(name="JobId",   value=jobId,   inline=True)
    if note:
        embed.add_field(name="Note", value=note, inline=False)

    # send without blocking Flask
    asyncio.run_coroutine_threadsafe(
        bot.get_channel(CHANNEL).send(embed=embed),
        bot.loop
    )
    return "ok", 200

# ---------- BOT THREAD ----------
def run_bot():
    bot.run(TOKEN)

threading.Thread(target=run_bot, daemon=True).start()

# ---------- FLASK SERVER ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
