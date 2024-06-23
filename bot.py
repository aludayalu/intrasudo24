import discord # type: ignore
from discord.ext import commands # type: ignore
from secrets_parser import parse

TOKEN = parse("variables.txt")["discord"]

channel_id = {}

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

# Create an instance of the bot
bot = commands.Bot(command_prefix='', intents=intents)

# Event handler for when the bot has connected to the server
@bot.event
async def on_ready():
    print("Bot Started")

async def send_embed(ctx, participant_name, query, level):
    guild = ctx.guild
    if level not in channel_id.keys():
        channel = await guild.create_text_channel(name=f'Level {level}')
        channel_id[level] = channel.id
    else:
        channel = bot.get_channel(channel_id[level])
    
    embed = discord.Embed(title="Participant Info", color=discord.Color.blue())
    embed.add_field(name="Name", value=participant_name, inline=False)
    embed.add_field(name="Query", value=query, inline=False)
    embed.add_field(name="Level", value=level, inline=False)
    
    await channel.send(embed=embed)

@bot.command()
async def info(ctx, participant_name, query, level):
    await send_embed(ctx, participant_name, query, level)

# Run the bot with the specified token
bot.run(TOKEN)
