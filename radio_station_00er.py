import discord
import asyncio
import os
import subprocess

TOKEN = "####"
CHANNEL_ID = "####"
AUDIO_URL = "####"
STATUS_TEXT = "####"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"[INFO] Eingeloggt als {client.user}")
    await client.change_presence(activity=discord.Game(name=STATUS_TEXT))

    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"[ERROR] Kanal mit ID {CHANNEL_ID} nicht gefunden.")
        return

    try:
        print(f"[INFO] Versuche Verbindung zu Sprachkanal: {channel.name}")
        vc = await channel.connect()

        ffmpeg_options = {
            "options": "-loglevel debug -filter:a volume=0.6"
        }

        print(f"[INFO] Starte Stream von: {AUDIO_URL}")
        vc.play(discord.FFmpegPCMAudio(AUDIO_URL, **ffmpeg_options))

        while vc.is_playing():
            await asyncio.sleep(1)

        print("[INFO] Audio-Stream beendet.")
        await vc.disconnect()

    except Exception as e:
        print(f"[EXCEPTION] Fehler beim Abspielen: {e}")

@client.event
async def on_error(event, *args, **kwargs):
    print(f"[ERROR] Event-Fehler: {event}")
    raise

client.run(TOKEN)
