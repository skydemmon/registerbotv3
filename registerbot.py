import sys
import time
import traceback
import discord
from os import getenv
from discord import Game, File
from discord.ext import commands
from discord.utils import get
import logging
import re
from urllib.parse import urlparse
from collections import defaultdict
from sqlalchemy import create_engine, func, update, sql
from sqlalchemy.orm import sessionmaker
from models import Base, Battles, Participants
from datetime import datetime, timezone, timedelta
import math as m
import pandas as pd
import numpy as np




# Server IDs
FRICKS_SERVER_ID = "Placeholder"
CLAP_SERVER_ID = "Placeholder"
KINGSMEN_SERVER_ID = "Placeholder"
OOV_SERVER_ID ="Placeholder"
PING_SERVER_ID ="Placeholder"
FAME_SERVER_ID = "Placeholder"
TEST_SERVER_ID ="Placeholder"
MC_SERVER_ID = "Placeholder"


# User IDs
PUPPYBOT_ID = "Placeholder"

# Channel IDs
BOT_TESTING_CHANNEL_ID = "Placeholder"
GENERAL_CHANNEL_ID = "Placeholder"
SCREENSHOT_APPROVAL_CHANNEL_ID = "Placeholder"
SCREENSHOT_LOG_CHANNEL_ID = "Placeholder"
FUNDS_TRACKING_CHANNEL_ID = "Placeholder"
RECRUITMENT_CHANNEL_ID = "Placeholder"
LOGS_CHANNEL_ID = "Placeholder"
LOOT_SPLIT_CHANNEL_ID = "Placeholder"
# Role IDs
FRICKS_ROLE_ID =  "Placeholder"
KINGSMEN_ROLE_ID = "Placeholder"
SOLDIER_ROLE_ID = "Placeholder"
OOV_ROLE_ID = "Placeholder"
PING_ROLE_ID =  "Placeholder"
FAME_ROLE_ID = "Placeholder"
NKC_ROLE_ID = "Placeholder"
NKC_RECRUIT_ROLE_ID = "Placeholder"
NKC_RED_ROLE_ID = "Placeholder"
NKC_GREEN_ROLE_ID = "Placeholder"
NKC_BLUE_ROLE_ID = "Placeholder"
AK_ROLE_ID = "Placeholder"
AK_RECRUIT_ROLE_ID = "Placeholder"
DARK_ROLE_ID = "Placeholder"
MC_ROLE_ID = "Placeholder"
MC_ROLE_ELITE_ID = "Placeholder"
# Role CLAP id's
FRICKLING_ROLE_ID = "Placeholder"
FRICKS_CLAP_ROLE_ID = "Placeholder"
KINGSMEN_CLAP_ROLE_ID = "Placeholder"
OOV_CLAP_ROLE_ID = "Placeholder"
PING_CLAP_ROLE_ID = "Placeholder"
FAME_CLAP_ROLE_ID = "Placeholder"
ROYAL_CLAP_ROLE_ID = "Placeholder"
AK_CLAP_ROLE_ID = "Placeholder"
DARK_CLAP_ROLE_ID = "Placeholder"
GUEST_CLAP_ROLE_ID = "Placeholder"
ROYAL_SERVER_ID = "Placeholder"
AK_SERVER_ID = "Placeholder"
DARK_SERVER_ID = "Placeholder"
MC_CLAP_ROLE_ID = "Placeholder"

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='%', case_insensitive=True, chunk_guilds_at_startup = True, intents=intents)

engine = create_engine('sqlite:///register.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def is_url(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    filename="fricksbot.log",
    filemode='a'
)

# Discord Logger
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)


def role_check(user, roles):
    role_list = []

    for role in user.roles:
        role_list.append(role.id)

    return any(i in roles for i in role_list)


def find_between(s, first, last):
    try:
        start_idx = s.index(first) + len(first)
        end_idx = s.index(last, start_idx)
        return s[start_idx:end_idx]
    except ValueError:
        return ""

def getBattleTimer(time):
    hour = time.hour

    if hour in (23, 0, 1):
        return 0
    elif hour in (2,3):
        return 3
    elif hour in (4,5,6):
        return 5
    if hour in (11, 12, 13):
        return 12
    if hour in (14,15,16):
        return 15
    if hour in (17, 18, 19):
        return 18
    elif hour in (20,21,22):
        return 21

@client.event
async def on_ready():
    channel = client.get_channel(BOT_TESTING_CHANNEL_ID)
    await client.change_presence(activity=Game('Granting permissions, 24/7'))

@client.command()
async def mc(ctx):
    message = ctx.message
    if ctx.guild and ctx.guild.id == TEST_SERVER_ID:
        mc_server = client.get_guild(MC_SERVER_ID)
        mc_member = mc_server.get_member(message.author.id)

        if mc_member is None:
            await message.channel.send("You are not in MC guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🗡️')
            return

        roles = [MC_ROLE_ID, MC_ROLE_ELITE_ID]
        if role_check(mc_member, roles):
            role = get(message.guild.roles, id=MC_CLAP_ROLE_ID)
            rrole = get(message.guild.roles, id=GUEST_CLAP_ROLE_ID)
            await message.author.add_roles(role)
            await message.channel.send("You are in MC guild granting permissions")
            await message.add_reaction('👌')
            await message.author.remove_roles(rrole)
        else:
            await message.channel.send("You are not in MC guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🕵️')
            await message.add_reaction('❌')
    else:
        await message.channel.send("Wrong server, bud. You can only use this command in the CLAP discord.")

@client.command()
async def nkc(ctx):
    message = ctx.message
    if ctx.guild and ctx.guild.id == TEST_SERVER_ID:
        royal_server = client.get_guild(ROYAL_SERVER_ID)
        royal_member = royal_server.get_member(message.author.id)

        if royal_member is None:
            await message.channel.send("You are not in NKC guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🗡️')
            return

        roles = [NKC_ROLE_ID, NKC_RECRUIT_ROLE_ID, NKC_RED_ROLE_ID, NKC_GREEN_ROLE_ID, NKC_BLUE_ROLE_ID]
        if role_check(royal_member, roles):
            role = get(message.guild.roles, id=ROYAL_CLAP_ROLE_ID)
            rrole = get(message.guild.roles, id=GUEST_CLAP_ROLE_ID)
            await message.author.add_roles(role)
            await message.channel.send("You are in NKC guild granting permissions")
            await message.add_reaction('👌')
            await message.author.remove_roles(rrole)
        else:
            await message.channel.send("You are not in NKC guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🕵️')
            await message.add_reaction('❌')
    else:
        await message.channel.send("Wrong server, bud. You can only use this command in the CLAP discord.")


@client.command()
async def dark(ctx):
    message = ctx.message
    if ctx.guild and ctx.guild.id == TEST_SERVER_ID:
        dark_server = client.get_guild(DARK_SERVER_ID)
        dark_member = dark_server.get_member(message.author.id)

        if dark_member is None:
            await message.channel.send("You are not in TheDarkClan guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🗡️')
            return

        roles = [DARK_ROLE_ID]
        if role_check(dark_member, roles):
            role = get(message.guild.roles, id=DARK_CLAP_ROLE_ID)
            rrole = get(message.guild.roles, id=GUEST_CLAP_ROLE_ID)
            await message.author.add_roles(role)
            await message.channel.send("You are in TheDarkClan guild granting permissions")
            await message.add_reaction('👌')
            await message.author.remove_roles(rrole)
        else:
            await message.channel.send("You are not in TheDarkClan guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🕵️')
            await message.add_reaction('❌')
    else:
        await message.channel.send("Wrong server, bud. You can only use this command in the CLAP discord.")

@client.command()
async def ak(ctx):
    message = ctx.message
    if ctx.guild and ctx.guild.id == TEST_SERVER_ID:
        ak_server = client.get_guild(AK_SERVER_ID)
        ak_member = ak_server.get_member(message.author.id)

        if ak_member is None:
            await message.channel.send("You are not in AK7 guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🗡️')
            return

        roles = [AK_ROLE_ID, AK_RECRUIT_ROLE_ID]
        if role_check(ak_member, roles):
            role = get(message.guild.roles, id=AK_CLAP_ROLE_ID)
            rrole = get(message.guild.roles, id=GUEST_CLAP_ROLE_ID)
            await message.author.add_roles(role)
            await message.channel.send("You are in AK7 guild granting permissions")
            await message.author.remove_roles(rrole)
            await message.add_reaction('👌')
        else:
            await message.channel.send("You are not in AK7 guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🕵️')
            await message.add_reaction('❌')
    else:
        await message.channel.send("Wrong server, bud. You can only use this command in the CLAP discord.")

@client.command()
async def oov(ctx):
    message = ctx.message
    if ctx.guild and ctx.guild.id == TEST_SERVER_ID:
        oov_server = client.get_guild(OOV_SERVER_ID)
        oov_member = oov_server.get_member(message.author.id)

        if oov_member is None:
            await message.channel.send("You are not in Oath of Vengeance guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🗡️')
            return

        roles = [OOV_ROLE_ID]
        if role_check(oov_member, roles):
            role = get(message.guild.roles, id=OOV_CLAP_ROLE_ID)
            rrole = get(message.guild.roles, id=GUEST_CLAP_ROLE_ID)
            await message.author.add_roles(role)
            await message.author.remove_roles(rrole)
            await message.channel.send("You are in Oath of Vengeance guild granting permissions")
            await message.add_reaction('👌')
        else:
            await message.channel.send("You are not in Oath of Vengeance guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🕵️')
            await message.add_reaction('❌')
    else:
        await message.channel.send("Wrong server, bud. You can only use this command in the CLAP discord.")

@client.command()
async def fricks(ctx):
    message = ctx.message
    if ctx.guild and ctx.guild.id == TEST_SERVER_ID:
        fricks_server = client.get_guild(FRICKS_SERVER_ID)
        fricks_member = fricks_server.get_member(message.author.id)

        if fricks_member is None:
            await message.channel.send("You are not in Fricks guild, permission not granted")
            return

        roles = [FRICKS_ROLE_ID, FRICKLING_ROLE_ID]
        if role_check(fricks_member, roles):
            role = get(message.guild.roles, id=FRICKS_CLAP_ROLE_ID)
            rrole = get(message.guild.roles, id=GUEST_CLAP_ROLE_ID)
            await message.channel.send("You are in Fricks guild, permission granted")
            await message.author.add_roles(role)
            await message.author.remove_roles(rrole)
        else:
            await message.channel.send("You are not in Fricks guild, permission not granted")

    else:
        await message.channel.send("Wrong server, bud. You can only use this command in the CLAP discord.")


@client.command()
async def kingsmen(ctx):
    message = ctx.message
    if ctx.guild and ctx.guild.id == TEST_SERVER_ID:
        kingsmen_server = client.get_guild(KINGSMEN_SERVER_ID)
        kingsmen_member = kingsmen_server.get_member(message.author.id)

        if kingsmen_member is None:
            await message.channel.send("You are not in TheKingsmen guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🗡️')
            return

        roles = [KINGSMEN_ROLE_ID, SOLDIER_ROLE_ID]
        if role_check(kingsmen_member, roles):
            role = get(message.guild.roles, id=KINGSMEN_CLAP_ROLE_ID)
            rrole = get(message.guild.roles, id=GUEST_CLAP_ROLE_ID)
            await message.author.add_roles(role)
            await message.channel.send("You are in TheKingsmen guild granting permissions")
            await message.author.remove_roles(rrole)
            await message.add_reaction('👌')
        else:
            await message.channel.send("You are not in TheKingsmen guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🕵️')
            await message.add_reaction('❌')
    else:
        await message.channel.send("Wrong server, bud. You can only use this command in the CLAP discord.")

@client.command()
async def ping(ctx):
    message = ctx.message
    if ctx.guild and ctx.guild.id == TEST_SERVER_ID:
        ping_server = client.get_guild(PING_SERVER_ID)
        ping_member = ping_server.get_member(message.author.id)

        if ping_member is None:
            await message.channel.send("You are not in Always350PinG guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🗡️')
            return

        roles = [PING_ROLE_ID]
        if role_check(ping_member, roles):
            role = get(message.guild.roles, id=PING_CLAP_ROLE_ID)
            rrole = get(message.guild.roles, id=GUEST_CLAP_ROLE_ID)
            await message.author.add_roles(role)
            await message.channel.send("You are in Always350PinG guild granting permissions")
            await message.author.remove_roles(rrole)
            await message.add_reaction('👌')
        else:
            await message.channel.send("You are not in Always350PinG guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🕵️')
            await message.add_reaction('❌')
    else:
        await message.channel.send("Wrong server, bud. You can only use this command in the CLAP discord.")

@client.command()
async def fame(ctx):
    message = ctx.message
    if ctx.guild and ctx.guild.id == TEST_SERVER_ID:
        fame_server = client.get_guild(FAME_SERVER_ID)
        fame_member = fame_server.get_member(message.author.id)

        if fame_member is None:
            await message.channel.send("You are not in F A M E L E S S guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🗡️')
            return

        roles = [FAME_ROLE_ID]
        if role_check(fame_member, roles):
            role = get(message.guild.roles, id=FAME_CLAP_ROLE_ID)
            rrole = get(message.guild.roles, id=GUEST_CLAP_ROLE_ID)
            await message.author.add_roles(role)
            await message.channel.send("You are in F A M E L E S S guild granting permissions")
            await message.add_reaction('👌')
            await message.author.remove_roles(rrole)
        else:
            await message.channel.send("You are not in F A M E L E S S guild, permission not granted")
            await message.add_reaction('🐀')
            await message.add_reaction('🕵️')
            await message.add_reaction('❌')
    else:
        await message.channel.send("Wrong server, bud. You can only use this command in the CLAP discord.")

client.run("Placeholder_BOT_TOKEN_HERE")
