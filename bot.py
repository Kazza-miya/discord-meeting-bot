import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🟢 Bot {bot.user} がログインしました。")

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and len(after.channel.members) >= 1:
        voice_channel = after.channel
        if bot.voice_clients and any(vc.channel == voice_channel for vc in bot.voice_clients):
            return
        try:
            vc = await voice_channel.connect()
            print(f"🎤 {voice_channel.name} に接続しました。録音開始（仮）。")
            await vc.disconnect()
        except Exception as e:
            print(f"接続エラー: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
