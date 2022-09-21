import os
import random

import asyncio as asyncio
import discord
import requests
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=intents  # Set up basic permissions
)
bot.author_id = 0000000  # Change to your discord id
BOT_ROLE_NAME = 'nlpf td 1'


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


@bot.command(name="name")
async def say_my_name(ctx):
    await ctx.channel.send(ctx.author.name)


@bot.command(name="d6")
async def say_my_name(ctx):
    await ctx.channel.send(random.randint(1, 6))


@bot.command(name="admin")
async def give_admin(ctx, arg):
    # Check the validity of 'arg'
    if len(ctx.message.mentions) == 0:
        await ctx.channel.send(f'No user mentioned')
        return
    member = ctx.message.mentions[0]
    if member is None:
        await ctx.channel.send(f'User {arg} not found')
        return

    role = next(
        filter(lambda role: role.permissions.administrator is True and role.name != BOT_ROLE_NAME, ctx.guild.roles),
        None)  # The bot role is excluded because of missing permissions
    if role is None:
        role = await ctx.guild.create_role(name='Admin', permissions=discord.Permissions(administrator=True))
        await ctx.channel.send(f'Role {role.name} created')
    await member.add_roles(role)


@bot.command(name="ban")
async def ban_member(ctx, arg):
    # Check the validity of 'arg'
    if len(ctx.message.mentions) == 0:
        await ctx.channel.send(f'No user mentioned')
        return
    member = ctx.message.mentions[0]
    if member is None:
        await ctx.channel.send(f'User {arg} not found')
        return

    if member.id == author_id:
        await ctx.channel.send("You is crazy to ban the manager of the server !!!!!!")
        return
    await ctx.guild.ban(member)


@bot.command(name="count")
async def count_member_status(ctx):
    status = {
        "online": [],
        "offline": [],
        "idle": [],
        "dnd": []
    }
    for member in ctx.guild.members:
        status[str(member.status)].append(member.name)

    for key in status:
        status[key].sort()

    message = "```"
    for key in status:
        if len(status[key]) > 0:
            message += f"{key}: \n"
            for member in status[key]:
                message += f"\t- {member}\n"
    message += "\n```"
    await ctx.channel.send(message)


@bot.command(name="xkcd")
async def get_image_from_xkcd(ctx):
    async with ctx.channel.typing():
        response = requests.get(url=f"https://xkcd.com/{random.randint(1, 2000)}/info.0.json")
        if response.status_code == 200:
            data = response.json()
            await ctx.channel.send(data["img"])


@bot.command(name="poll")
async def poll(ctx, *, args):
    await ctx.channel.send("@here" + " " + args)
    question = await ctx.channel.send(args)
    await question.add_reaction("👍")
    await question.add_reaction("👎")
    await asyncio.sleep(4)
    question = await ctx.channel.fetch_message(question.id)
    await ctx.channel.send(
        f"The results are...:\n👍 {question.reactions[0].count - 1} 👎 {question.reactions[1].count - 1}")
    await question.delete()


@bot.event
async def on_message(message):
    if message.author.id == bot.author_id:
        return
    if message.content == "Salut tout le monde":
        await message.channel.send(f"Salut tout seul {message.author.mention}")
        return
    await bot.process_commands(message)


token = os.environ["TOKEN"]
# token = "bonésoiré"
author_id = 220230614740238336

bot.run(token)
