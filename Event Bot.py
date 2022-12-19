import discord
import os
from os import system
import random
import requests
import json
from discord.ext import commands, tasks
from dotenv import load_dotenv
from online import online


TOKEN = "TOKEN"

events = []
class Event:
    def __init__(self, name, date, who):
      self.name = name
      self.date = date
      self.who = who.split()
      
      
    def __repr__(self):
      return f"|**EVENT**: {self.name}|\n**DATE**: {self.date}|\n**ATTENDING**: {self.who}|"

    def __str__(self):
      return f"|**EVENT**: {self.name}|\n**|DATE**: {self.date}|\n**|ATTENDING**: {self.who}|"

    def add_who(self, name):
      self.who.append(name)
      return f"ALL ATTENDING: {self.who}"

    def change_date(self, new_date):
      self.date = new_date
      return f"Event date changed to: {self.date}"

    def change_name(self, new_name):
      self.name = new_name
      return f"Event name changed to: {self.name}"
      #use .delete to delete() object
    def delete_event(self):
      self.name = ""
      self.date = ""
      self.who  = []
        


class MyClient(discord.Client):
  #bot = commands.self(command_prefix='$') FIX
  #================================================================================================#
  async def on_ready(self):
    print(f'Logged on as {self.user}!')
    #await channel.send("Type $help for list of commands")

  #================================================================================================#
  async def on_guild_join(guild):
    await guild.text_channels[0].send("Thanks for having me!")

  #===================================================================================================#
  async def on_message(self, message):
    print(f'Message from {message.author}: {message.content}')

    if message.content.startswith("$help"):
      await message.channel.send(
        "**EVENTS:**\n"
        "\n**|**$event.make**, name,date,people**: Create's a new event (enter people param with spaces betwen names)\n"
        "\n**|**$event.find**, name_of_event**: display's details of specified event\n"
        "\n**|**$event.change_name**, old_name, new_name**: Changes the name of the event\n"
        "\n**|**$event.change_date**, new_date**: Changes the date of the event\n"
        "\n**|**$event.names: Lists all events\n"
        "\n**|**$event.add_guest**, name,name...**: add's names to guest list\n"
        "\n**|**$event.delete**, event_name**: delete event details"
                                         
      )

    #===================================================================================================#    
    if message.content.startswith("$event.make"):
      param = message.content.split(",")
      len_p = len(param)
      check = 0

      for i in range(len(events)):
        if events[i].name == param[1]:
          await message.channel.send(f"**This event already exists**\n{events[i]}")
          check = 1

      if check == 1:
        return 
      
      new_event = Event(param[1].lstrip(), param[2].lstrip(), param[3].lstrip())
      events.append(new_event)
      await message.channel.send(f"{new_event}")
    #===================================================================================================#
    if message.content.startswith("$event.names"):     
      all = ""
      for i in range(len(events)):
        all += events[i].name + "\n"
    
      await message.channel.send(f"**All Events:**\n{all}")
    #===================================================================================================#
    if message.content.startswith("$event.delete"):
      param = message.content.split(",")
      len_p = len(param)

      for i in range(len(events)):
        if (events[i].name == param[1].lstrip()):
            events.pop(i)
            
                
      await message.channel.send(f"Event **{param[1].lstrip()}** deleted !")
    #===================================================================================================#
    if message.content.startswith("$event.find"):
      param = message.content.split(",")

      for i in range(len(events)):
        if (events[i].name == param[1].lstrip()):
            await message.channel.send(f"{events[i]}")
  #===================================================================================================# 
    if message.content.startswith("$event.change_name"):
      param = message.content.split(",")
      len_p = len(param)
        
      for i in range(len(events)):
        if (events[i].name == param[1].lstrip()):
          events[i].change_name(param[2].lstrip())  
          await message.channel.send(f"Event named: **{param[1].lstrip()}** changed to {param[2].lstrip()}")
  #===================================================================================================#
    if message.content.startswith("$event.change_date"):
      param = message.content.split(",")
      len_p = len(param)
      
      for i in range(len(events)):
        if (events[i].name == param[1].lstrip()):
          events[i].change_date(param[2].lstrip())  
          await message.channel.send(f"Event **{events[i].name}'s**' date: **{param[1].lstrip()}** changed to date{param[2].lstrip()}")
  #===================================================================================================#
    if message.content.startswith("$event.add_guest"):
      param = message.content.split(",")
      len_p = len(param)
      cur_event = []
      for i in range(len(events)):
        if (events[i].name == param[1].lstrip()):
          cur_event = events[i]
      
      for i in range(2,len_p):
        cur_event.add_who(param[i].lstrip())

        await message.channel.send(f"{param[1].lstrip()}")
  #===================================================================================================#
      

          
def main():
  intents = discord.Intents.default()
  intents.message_content = True
  client = MyClient(intents=intents)

  
  try:
    online()
    client.run(TOKEN)

  except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    system('kill 1')

main()