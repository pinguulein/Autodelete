import discord
from discord.ext import commands
global channels

prefix = "%" # Dein Prefix
bot = commands.Bot(command_prefix=prefix)
client = discord.Client()
channels = []
token = "Token" # Token

def notPinned(message):
    if not message.pinned:
        return True
    

class AutoChannel:
    def __init__(self, channelId, limit):
        self.channelId = channelId
        self.limit = limit
        self.messages = []

    def addMessage(self, messageId):
        self.messages.append(messageId)

    def getFirst(self):
        s = self.messages[0]
        del(self.messages[0])
        return s

    def timeToDelet(self):
        if len(self.messages) > self.limit:
            return True
        else:
            return False

    async def delet(self, link):
        try:
            channel = bot.get_channel(self.channelId)
            toDelet = await channel.fetch_message(link)
            if not toDelet.pinned:
                await channel.delete_messages([toDelet])
        except:
            print("Ein Fehler ist aufgetreten")
@bot.command()
async def ping(ctx):
    await ctx.channel.send("Pong!")

@bot.command()
@commands.has_any_role("Mod", "Autodeleteperms")
async def disableauto(ctx):
    for ch in channels:
        if ch.channelId == ctx.channel.id:
            del(ch)
            return await ctx.channel.send("Autodelete wurde abgeschaltet.")
        else:
            return await ctx.channel.send("Dieser Channel hat kein AutoDelete!")

@bot.command()
@commands.has_any_role("Mod", "Autodeleteperms")
async def enableauto(ctx, limit):
    for ch in channels:
        if ch.channelId == ctx.channel.id:
            if ch.limit == int(limit):
                return await ctx.channel.send("Das Limit was du setzen möchtest ist schon gesetzt.")
            else:
                ch.limit = int(limit)
    channels.append(AutoChannel(ctx.channel.id, int(limit)))
    await ctx.channel.send("AutoDelete eingestellt mit " + str(limit))

@bot.event
async def on_message(message):
    if message.content.startswith(prefix):
        return await bot.process_commands(message)
    for c in channels:
        if message.channel.id == c.channelId:
            c.addMessage(message.id)
            if c.timeToDelet():
                a = c.getFirst()
                await c.delet(a)
            

@bot.event
async def on_ready():
    print("Client logged in...")


bot.run(token)
