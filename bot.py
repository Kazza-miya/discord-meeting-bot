import discord
from discord.ext import commands
from discord.ext import voice_recv
import os

intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

class MySink(voice_recv.AudioSink):
    def __init__(self):
        super().__init__()
        self.audio_data = []

    def write(self, user, data):
        if data.pcm:
            self.audio_data.append(data.pcm)

    def cleanup(self):
        os.makedirs("recordings", exist_ok=True)
        with open("recordings/output.pcm", "wb") as f:
            for chunk in self.audio_data:
                f.write(chunk)

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        vc = await ctx.author.voice.channel.connect(cls=voice_recv.VoiceRecvClient)
        sink = MySink()
        vc.listen(sink)
        await ctx.send("録音を開始しました。")
    else:
        await ctx.send("ボイスチャンネルに接続してください。")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("切断しました。")
    else:
        await ctx.send("ボイスチャンネルに接続していません。")

from dotenv import load_dotenv

load_dotenv()
bot.run(os.getenv("DISCORD_TOKEN"))

