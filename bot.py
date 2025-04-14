import discord
from discord.ext import commands
import os
import datetime
import subprocess
import asyncio

# ========================
# Botの初期化
# ========================
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ========================
# 録音関数（録音処理）
# ========================
async def record_audio(vc: discord.VoiceClient, channel: discord.VoiceChannel):
    if channel.name == "休憩室":
        print("🚫 休憩室なので録音をスキップします。")
        await vc.disconnect()
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{channel.name}_{timestamp}.wav".replace(" ", "_")
    filepath = os.path.join("recordings", filename)

    os.makedirs("recordings", exist_ok=True)

    print(f"🎙️ 録音開始: {filepath}")

    # ★ 今はダミー（録音は次ステップで）
    await asyncio.sleep(10)

    print(f"🎧 録音終了: {filepath}")
    await vc.disconnect()

# ========================
# イベント処理
# ========================
@bot.event
async def on_ready():
    print(f"🟢 Bot {bot.user} がログインしました。")

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and len(after.channel.members) >= 1:
        voice_channel = after.channel
        if voice_channel.name == "休憩室":
            print("🙅‍♂️ 休憩室は録音対象外です。")
            return
        if bot.voice_clients and any(vc.channel == voice_channel for vc in bot.voice_clients):
            return
        try:
            vc = await voice_channel.connect()
            print(f"🎤 {voice_channel.name} に接続しました。録音開始")
            await record_audio(vc, voice_channel)
        except Exception as e:
            print(f"接続エラー: {e}")

# ========================
# 起動処理
# ========================
bot.run(os.getenv("DISCORD_TOKEN"))
