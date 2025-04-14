import discord
from discord.ext import commands
from discord.ext.audio import AudioClient
import os
import datetime

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
            audio = AudioClient(vc)

            # 録音ディレクトリ
            os.makedirs("recordings", exist_ok=True)

            # 音声データを保存
            @audio.on("data")
            async def on_audio_data(user, data):
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recordings/{user.id}_{timestamp}.pcm"
                with open(filename, "ab") as f:
                    f.write(data)
                print(f"🎙️ {user.display_name} の音声を録音中: {filename}")

            await audio.listen()  # 録音開始（イベントをトリガー）
        except Exception as e:
            print(f"接続エラー: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))
