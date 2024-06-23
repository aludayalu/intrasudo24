import discord  # type: ignore
from discord.ext import commands # type: ignore
from secrets_parser import parse

TOKEN = parse("variables.txt")["discord"]

channel_id = {}
prev_messages = {}

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print("Bot Started")

async def send_embed(ctx, participant_name, query, level):
    guild = ctx.guild
    if level not in channel_id:
        channel = await guild.create_text_channel(name=f'Level {level}')
        channel_id[level] = channel.id
    else:
        channel = bot.get_channel(channel_id[level])
    
    embed = discord.Embed(title="Participant Info", color=discord.Color.blue())
    embed.add_field(name="Name", value=participant_name, inline=False)
    embed.add_field(name="Query", value=query, inline=False)
    embed.add_field(name="Level", value=level, inline=False)
    
    msg = await channel.send(embed=embed)
    prev_messages[msg.id] = [participant_name, query, level]

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if message.reference and message.reference.message_id in prev_messages:
        print(message.content)

@bot.command()
async def info(ctx, participant_name, query, level):
    await send_embed(ctx, participant_name, query, level)

bot.run(TOKEN)
