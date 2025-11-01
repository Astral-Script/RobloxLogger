import os
import datetime
import json
import threading
import asyncio
from flask import Flask, request
import nextcord
from nextcord.ext import commands

# ---------- CONFIG ----------
TOKEN   = os.environ["MTQzNDA3ODU0ODQ3MzI4MjYzMA.G0Ejiu.w_VR7wuW0wL8zzSElTzPo1q_bpMwL-3qFvIZvY"]     # set in Render dashboard
CHANNEL = int(os.environ["1434084772031762482"])   # set in Render dashboard
# ----------------------------

app  = Flask(__name__)
intents = nextcord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ---------- DISCORD READY ----------
@bot.event
async def on_ready():
    print(f"[BOT]  {bot.user} is online")

# ---------- WEB ENDPOINT ----------
@app.route("/log", methods=["POST"])
def log_script_run():
    data = request.get_json(force=True, silent=True) or {}
    user    = data.get("user",    "Unknown")
    placeId = data.get("placeId", "N/A")
    jobId   = data.get("jobId",   "N/A")
    note    = data.get("note",    "")

    embed = nextcord.Embed(
        title="🔥 Script executed",
        colour=0xff6600,
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
