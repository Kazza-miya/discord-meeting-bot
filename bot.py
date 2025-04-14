import discord
from discord.ext import commands
import os
import datetime
import asyncio
from discord.ext import audio

recorder = audio.Recorder()

@recorder.on_audio
async def on_audio_frame(sink, user, data):
    filename = f"recordings/{user.id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    with open(filename, "wb") as f:
        f.write(data.pcm)
    print(f"🎙️ {user.display_name} の音声を録音: {filename}")

# Botの初期化
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
        if voice_channel.name == "休憩室":
            print("🙅‍♂️ 休憩室は録音対象外です。")
            return
        if bot.voice_clients and any(vc.channel == voice_channel for vc in bot.voice_clients):
            return
        try:
            vc = await voice_channel.connect()
            recorder.attach_to(vc)
            print(f"🎤 {voice_channel.name} に接続しました。録音開始")
        except Exception as e:
            print(f"接続エラー: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
