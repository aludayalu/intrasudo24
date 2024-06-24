import discord
from discord.ext import commands
import time
from secrets_parser import parse
from flask import Flask, request
import threading
from database import get, set, delete
import asyncio

app=Flask(__name__)

bot_Token = parse("variables.txt")["discord"]
GUILD_ID = parse("variables.txt")["guild_id"]


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print("Bot Started")

async def create_channels(level):
    if get("level_channels", level)["Ok"]:
        return
    guild = bot.get_guild(int(GUILD_ID))
    levels_category = None
    hints_category = None
    for x in guild.categories:
        if x.name == "levels":
            levels_category = x
        if x.name == "hints":
            hints_category = x
    level_channel=await guild.create_text_channel(f"leads-{level}", category=levels_category)
    hint_channel=await guild.create_text_channel(f"hints-{level}", category=hints_category)
    set("level_channels", level, {"level":level_channel.id, "hint":hint_channel.id})

@app.get("/create_level")
async def create_channel():
    asyncio.run_coroutine_threadsafe(create_channels(request.args["level"]), bot.loop)
    return {"succes":"created channels"}

async def send_message(level, name, email, content):
    channel=bot.get_channel(get("level_channels", level)["Value"]["level"])
    message=await channel.send(f"`{name} {email} : {content}`\n")
    set("discord_messages", str(message.id), {"email":email})

@app.get("/send_message")
async def send_message_api():
    asyncio.run_coroutine_threadsafe(send_message(request.args["level"], request.args["name"], request.args["email"], request.args["content"]), bot.loop)
    return "hi"

@bot.event
async def on_message(message:discord.Message):
    if message.author==bot:
        return
    if message.reference!=None:
        id=message.reference.message_id
        database_message=get("discord_messages", str(id))
        if database_message["Ok"]:
            set("messages/"+database_message["Value"]["email"], str(message.id), {"author":"Exun Clan", "content":message.content})
            await message.channel.send("hello", reference=message)

@bot.event
async def on_message_delete(message:discord.Message):
    if message.reference!=None:
        id=message.reference.message_id
        database_message=get("discord_messages", str(id))
        if database_message["Ok"]:
            delete("messages/"+database_message["Value"]["email"], str(message.id))

# Run the bot with the specified token
threading.Thread(target=bot.run, args=(bot_Token, ), daemon=True).start()
app.run(host="0.0.0.0", port=5555)