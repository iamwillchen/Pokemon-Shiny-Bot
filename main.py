import os
import discord
import numpy as np
import math
from keep_alive import keep_alive

client = discord.Client()

def Masuda(n):
  NonOdds = 100 * (681 / 682) ** n
  ShinyOdds = 100 - NonOdds
  P5 = np.round(np.ceil(((np.log(0.5) / np.log(681/682)) - n)), 0)
  P9 = np.round(np.ceil(((np.log(0.1) / np.log(681/682)) - n)), 0)
  return [NonOdds, ShinyOdds, P5, P9]

def SMasuda(n):
  NonOdds = 100 * (511 / 512) ** n
  ShinyOdds = 100 - NonOdds
  P5 = np.round(np.ceil(((np.log(0.5) / np.log(511/512)) - n)), 0)
  P9 = np.round(np.ceil(((np.log(0.1) / np.log(511/512)) - n)), 0)
  return [NonOdds, ShinyOdds, P5, P9]

SArray = np.array([4096, 3855, 3640, 3449, 3277, 3121, 2979, 2849, 2731, 2621, 2521, 2427, 2341, 2259, 2185, 2114, 2048, 1986, 1927, 1872, 1820, 1771, 1724, 1680, 1638, 1598, 1560, 1524, 1489, 1456, 1310, 1285, 1260, 1236, 1213, 1192, 993, 799, 400, 200, 99])

def Radar(n):
  n = int(n)
  n = n - 1

  u = 1

  if n <= 39:
    for i in range(n):
      u *= ((SArray[i] - 4) / (SArray[i]))

  if n >= 39:
    for i in  range(0, 39):
      u *= (SArray[i] - 4) / (SArray[i])
    u *= (95 / 99) ** (n - 39)
  
  Non = u * 100
  Shiny = 100 - Non

  return [Non, Shiny]

def RadarRepeat(n, x):
  n = int(n)
  x = int(x)

  n = n - 1

  u = 1

  if n <= 39:
    for i in range(n):
      u *= ((SArray[i] - 4) / (SArray[i]))

    if x == 0:
      Non = u * 100
      Shiny = 100 - Non
  
    elif x > 0:
      u *= ((SArray[n] - 4) / (SArray[n])) ** x
      Non = u * 100
      Shiny = 100 - Non

  if n >= 39:
    for i in  range(0, 39):
      u *= (SArray[i] - 4) / (SArray[i])
    u *= (95 / 99) ** (n - 39)
  
    if x == 0:
      Non = u * 100
      Shiny = 100 - Non
  
    elif x > 0:
      u = u * ((SArray[n] - 4) / (SArray[n])) ** x
      Non = u * 100
      Shiny = 100 - Non

  return [Non, Shiny]


@client.event
async def on_ready():
  print('I am logged in in as{0.user}'
  .format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('%help') or message.content.startswith('%h'):
    await message.channel.send('Masuda Odds, Command: %M (Encounters)\n'
    'Shiny Charm with Masuda Odds, Command: %SM (Encounters)\n'
    'PokeRadar Odds, Command: %Radar (Chain, Chain Repeat)\n')
    
  if message.content.startswith('%M') or message.content.startswith('%Masuda') or message.content.startswith('%masuda'):
    n = message.content.split(' ')[1]
    n = int(n)
    if n <= 0:
      await message.channel.send('Stop Breaking the Bot!  ')
    if n > 0:
      Shiny = np.round(Masuda(n)[1], 2)
      Non = np.round(Masuda(n)[0], 2)
      P5 = math.trunc(Masuda(n)[2])
      P9 = math.trunc(Masuda(n)[3])
      print(P9)
      print(P5)
      await message.channel.send('Shiny Odds: {}%'.format(Shiny))
      await message.channel.send('Non-Shiny Odds: {}%'.format(Non))
      if P5 > 0:
        await message.channel.send('For a 50% Odds, {} more eggs must hatch'.format(P5))
      if P9 > 0:
        await message.channel.send('For a 90% Odds, {} more eggs must hatch'.format(P9))

  if message.content.startswith('%SM') or message.content.startswith('%ShiningMasuda') or message.content.startswith('%Shiningmasuda') or message.content.startswith('%shiningmasuda'):
    n = message.content.split(' ')[1]
    n = int(n)
    if n <= 0:
      await message.channel.send('Stop Breaking the Bot!')
    if n > 0:
      Shiny = np.round(SMasuda(n)[1], 2)
      Non = np.round(SMasuda(n)[0], 2)
      P5 = math.trunc(SMasuda(n)[2])
      P9 = math.trunc(SMasuda(n)[3])
      await message.channel.send('Shiny Odds {}%'.format(Shiny))
      await message.channel.send('Non-Shiny Odds {}%'.format(Non))
      if P5 > 0:
       await message.channel.send('For a 50% Odds, {} more eggs must hatch'.format(P5))
      if P9 > 0:
        await message.channel.send('For a 90% Odds, {} more eggs must hatch'.format(P9))

  if message.content.startswith('%Radar') or message.content.startswith('%radar') or message.content.startswith('%r') or message.content.startswith('%R'):
    print(message.content.split(' '))
    n = message.content.split(' ')[1]
    x = 0

    lencheck = len(message.content.split(' '))
    
    if lencheck > 2:
     x = message.content.split(' ')[2]
     x = int(x)

    n = int(n)

    if n > 0 and x == 0:

      Shiny = np.round(Radar(n)[1], 2)
      Non = np.round(Radar(n)[0], 2)
      await message.channel.send('Shiny Odds {}%'.format(Shiny))
      await message.channel.send('Non-Shiny Odds {}%'.format(Non))

    if n > 0 and x != 0:
      Shiny = np.round(RadarRepeat(x, n)[1], 2)
      Non = np.round(RadarRepeat(x, n)[0], 2)
      await message.channel.send('Shiny Odds {}%'.format(Shiny))
      await message.channel.send('Non-Shiny Odds {}%'.format(Non))

    elif n <= 0 or x < 0:
      await message.channel.send('Stop Breaking the Bot!')

keep_alive()

client.run(os.environ['TOKEN'])