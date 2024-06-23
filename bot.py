import discord # type: ignore
from discord.ext import commands # type: ignore
import time
from secrets_parser import parse

TOKEN = parse("variables.txt")["discord"]
GUILD_ID = parse("variables.txt")["guild_id"]

channel_id = {}
replies = {}


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print("Bot Started")

async def send_embed(participant_email, participant_name, query, level):
    guild = bot.get_guild(int(GUILD_ID))
    if not guild:
        print(f"Guild with ID {GUILD_ID} not found.")
        return

    if level not in channel_id:
        channel = await guild.create_text_channel(name=f'Level {level}')
        channel_id[level] = channel.id
    else:
        channel = bot.get_channel(channel_id[level])
 
    embed = discord.Embed(title="Participant Info", color=discord.Color.blue())
    embed.add_field(name="Email", value=participant_email, inline=False)
    embed.add_field(name="Name", value=participant_name, inline=False)
    embed.add_field(name="Query", value=query, inline=False)
    embed.add_field(name="Level", value=level, inline=False)
    
    msg = await channel.send(embed=embed)
    replies[msg.id] = [participant_email, participant_name, query, level]

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if message.reference and message.reference.message_id in replies:
        temp_list = replies[message.reference.message_id]
        temp_list.extend([message.content, message.id])
        replies[message.reference.message_id] = temp_list
        print(replies)

@bot.event
async def on_message_delete(message):
    print('test')
    for keys,values in replies.items():
       if message.id == values[5]:
            temp_list = replies[keys]
            print(temp_list)
            del temp_list[-2:]
            print(temp_list)
            replies[keys] = temp_list
            print(replies)

@bot.command()
async def info(ctx, participant_email, participant_name, query, level):
    await send_embed(participant_email, participant_name, query, level)

# Run the bot with the specified token
bot.run(TOKEN)
