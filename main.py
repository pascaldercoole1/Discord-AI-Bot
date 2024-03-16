import os
import requests
import json
import time
import re
import discord
from discord.ext import commands

from keep_alive import keep_alive

latest_message = "No message yet"
alreadysent3 = False

def GetConversationID():
    url = "https://huggingfaceh4-zephyr-7b-gemma-chat.hf.space/conversation"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept": "*/*",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://huggingfaceh4-zephyr-7b-gemma-chat.hf.space/",
        "Content-Type": "application/json",
        "Origin": "https://huggingfaceh4-zephyr-7b-gemma-chat.hf.space",
        "Connection": "keep-alive",
        "Cookie": "chat-ui=8f84c761-9726-47a4-8836-0dc63562372d",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    }

    data = {
        "model": "HuggingFaceH4/zephyr-7b-gemma-v0.1"
    }

    response = requests.post(url, json=data, headers=headers)
    return json.loads(response.text)["conversationId"]

def GetLink(ConversationID):
    url = f"https://huggingfaceh4-zephyr-7b-gemma-chat.hf.space/conversation/{ConversationID}/share"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept": "*/*",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": f"https://huggingfaceh4-zephyr-7b-gemma-chat.hf.space/conversation/{ConversationID}",
        "Content-Type": "application/json",
        "Origin": "https://huggingfaceh4-zephyr-7b-gemma-chat.hf.space",
        "Connection": "keep-alive",
        "Cookie": "chat-ui=8f84c761-9726-47a4-8836-0dc63562372d",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Content-Length": "0",
        "TE": "trailers"
    }

    response = requests.post(url, headers=headers)

    return response.text

def SendMessage(Message):
    print("SendMessage called")
    url = f"https://huggingfaceh4-zephyr-7b-gemma-chat.hf.space/conversation/{ConversationID}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept": "*/*",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": f"https://huggingfaceh4-zephyr-7b-gemma-chat.hf.space/conversation/{ConversationID}",
        "Content-Type": "application/json",
        "Origin": "https://huggingfaceh4-zephyr-7b-gemma-chat.hf.space",
        "Connection": "keep-alive",
        "Cookie": "chat-ui=8f84c761-9726-47a4-8836-0dc63562372d",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }

    Get_Values_responce = requests.get(Get_Values_url, headers=Get_Values_headers)
    latest_id = extract_latest_message_and_id(Get_Values_responce.text)
    print("latest_id:",latest_id)

    data = {
        "inputs": Message,
        "id": latest_id,
        "is_retry": False,
        "is_continue": False,
        "web_search": False,
        "files": []
        }

    response = requests.post(url, json=data, headers=headers)
    input_string = response.text
    lines = input_string.split('\n')

    final_answer = None

    # Iterate through each line
    for line in lines:
        # Find the line containing 'finalAnswer'
        if '"type":"finalAnswer"' in line:
            # Extract the text part
            final_answer = line.split('","text":"')[1][:-2]  # Extracting the text part
            break

    print(final_answer)
    return final_answer



ConversationID = GetConversationID()
print("ConversationID:",ConversationID)

Get_Values_url = f"https://huggingfaceh4-zephyr-7b-gemma-chat.hf.space/conversation/{ConversationID}/__data.json?x-sveltekit-invalidated=11"
Get_Values_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Accept": "*/*",
    "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://huggingfaceh4-zephyr-7b-gemma-chat.hf.space/conversation/65f5618aa8d4814d2568db9e",
    "Connection": "keep-alive",
    "Cookie": "chat-ui=8f84c761-9726-47a4-8836-0dc63562372d",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}



def extract_latest_message_and_id(data):
    latest_id = None

    global alreadysent3

    data = json.loads(data)
    
    # Loop through each node
    for node in data['nodes'][1]:
        datat = data['nodes'][1]["data"]
        # datatj = json.loads(str(data['nodes'][1]["data"]))
        # print(datat) ## 60

        for i, item in enumerate(datat): ## item in datat
          if type(item) == str and item.count('-') >= 4: ##item == '4789f7ec-97db-4475-b1bc-42768ca810a6':
              # print(item, type(item))
              latest_id = item
          else:
              index_ID = 10 ## 9
              string = datat[len(datat)-index_ID]
              #latest_message = datat[len(datat)-index_ID]
              try:
                  #json.loads(latest_message)
                  string = datat[len(datat)-15]
                  #latest_message = datat[len(datat)-15]
              except:
                  if type(string) == str:
                    stripped_string = string.strip()
                    # print("stripped_string:",stripped_string)
                    if not stripped_string:
                        # latest_message = "No Messages Yet!"
                        print(alreadysent3)
                        if alreadysent3 == False:
                            alreadysent3 = True
                            # SendMessage("Hello")


            
              #if type(item) == str:
                #print(i, datat[i], type(item))



    return latest_id

Get_Values_responce = requests.get(Get_Values_url, headers=Get_Values_headers)
latest_id = extract_latest_message_and_id(Get_Values_responce.text)

# SendMessage("Hello, please talk english only!")

intents = discord.Intents.default()
intents.messages = True  # Enable message-related events
intents.message_content = True

# Define bot's command prefix
bot = commands.Bot(command_prefix='/', intents=intents)

# Event listener for bot being ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    keep_alive()

@bot.command()
async def resetchat(ctx):
    ConversationID = GetConversationID()
    print("ConversationID:",ConversationID)
    await ctx.send("New ConversationID: ```" + str(ConversationID) + "```")

@bot.command()
async def promp(ctx, *, message):
    try:
        global ConversationID
        Get_Values_responce = requests.get(Get_Values_url, headers=Get_Values_headers)
        latest_id = extract_latest_message_and_id(Get_Values_responce.text)


        # MessageInput = input("What do you want to say: ")

        final_answer = SendMessage("NEVER USE NEW LINES! ALSO PLEASE DO NOT USE NEW LINES IN CODE MAKE ALL CODE 1 LINE! " + message)

        if final_answer == None:
            print(final_answer)

            latest_id = extract_latest_message_and_id(Get_Values_responce.text)

            Chat_Link = GetLink(ConversationID)
            Chat_LinkJ = json.loads(Chat_Link)
            FinalLink = Chat_LinkJ["url"]

            def remove_python_after_triple_backticks(input_string):
                a = re.sub(r'```python\b', '```', input_string)
                b = re.sub(r'```lua', '```', a)
                return b

            #await ctx.send("```latest_id: " + latest_id + "```")
            #await ctx.send("```GetLink: " + str(FinalLink) + "```")

            almostfinal_answer = final_answer.replace("lua\n", "").replace("python\n", "").replace("\\n", "").replace("\\", "")

            output_string = remove_python_after_triple_backticks(almostfinal_answer)
            print(output_string)

            print(GetLink(ConversationID))
            await ctx.send(output_string)
    except Exception as e:
        ConversationID = GetConversationID()
        print("ConversationID:",ConversationID)
        await ctx.send("Hey! The Bot ran into an Error please try sending the Command again: " + str(e))

token = os.environ.get("token")
bot.run(token)

