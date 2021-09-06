import discord
from discord.ext import commands
from config import *

bot = commands.Bot(command_prefix=prefix, self_bot=True, intents=discord.Intents.all(), help_command=None)

bot.sniped_messages = {}
bot.editsniped_messages = {}

@bot.event
async def on_ready():
  print(bot.user)
  print(discord.__version__)
  print("--------------")
  await bot.change_presence(activity=discord.Game(name=status))

@bot.command()
async def help(ctx):
  await ctx.message.delete()
  await ctx.send(f"There is only 1 command and that is **{prefix}snipe** `<index>`.")

@bot.event
async def on_message_delete(message):
  if message.content == f"{prefix}snipe":
    return
  try:
    if message.content.split(f"{prefix}snipe ")[1].isnumeric() is True:
      return
  except:
    pass

  try:
    guild = str(message.guild.name)
  except:
    guild = "dm channel or a group chat"

  try:
    key = str(message.guild.id)
  except:
    key = "dm channel or a group chat"
  
  try:
    deleted_in = '#' + message.channel.name
  except:
    deleted_in = "dm channel or a group chat"
  
  gd = f"{', sniped in ' + guild if str(message.guild) is not None else ''}"

  if len(message.attachments) != 0:
    if key not in list(bot.sniped_messages.keys()):
      bot.sniped_messages[key] = []
    bot.sniped_messages[key].append(
          {
            "author" : str(message.author), 
            "author_icon" : str(message.author.avatar_url), 
            "attachments" : [f"{message.attachments[x].filename}: [Download]({message.attachments[x].proxy_url})" for x in range(len(message.attachments))],
            "content" : message.content if message.content != '' else "Empty message",
            "footer" : f"Deleted in {deleted_in} {gd}",
            "img" : str(message.attachments[0].url)
          }
        )
  else:
    if key not in list(bot.sniped_messages.keys()):
      bot.sniped_messages[key] = []
    bot.sniped_messages[key].append(
          {
            "author" : str(message.author), 
            "author_icon" : str(message.author.avatar_url), 
            "content" : message.content if message.content != '' else "Empty message",
            "footer" : f"Deleted in {deleted_in} {gd}"
          }
        )

@bot.command()
async def snipe(ctx, snipe_index='1'):
  await ctx.message.delete()
  if snipe_index.isnumeric() is False:
    snipe_index=1
  else:
    snipe_index=int(snipe_index)
  try:
    key = str(ctx.guild.id)
  except:
    key = "dm channel or a group chat"
  try:
    sniped = list(reversed(bot.sniped_messages[key]))
  except KeyError:
    await ctx.send('Theres nothing to snipe!')
    return
  index = snipe_index - 1
  try:
    embed_data = sniped[index]
  except IndexError:
    if index != 0:
      await ctx.send('No message to snipe that far back.')
    return
  if "img" in list(embed_data.keys()):
    embed = discord.Embed(description='\n'.join(embed_data["attachments"])+"\n"+embed_data["content"], color=123456).set_author(name=embed_data["author"], icon_url=embed_data["author_icon"]).set_footer(text=embed_data["footer"]).set_image(url=embed_data["img"])
  else:
    embed = discord.Embed(description=embed_data["content"], color=123456).set_author(name=embed_data["author"], icon_url=embed_data["author_icon"]).set_footer(text=embed_data["footer"])
  try:
    await ctx.send(embed=embed)
  except:
    await ctx.send("you are missing permissions to send embed messages.")

bot.run(token, bot=False)
