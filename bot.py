import discord
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

client = discord.Client()

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

def create_room(url):
    chrome_options = Options()
    chrome_options.add_argument("window-size=1200x600")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH

    driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, options=chrome_options)

    driver.get("https://w2g.tv/")

    script = """var callback = arguments[arguments.length - 1]; // this is the callback to call when you are done
    var url = ""
    var item = "{0}"
    await fetch("https://w2g.tv/rooms/create", {{
    "method": "POST",
    }}).then(resp=>(url = resp.url))
    await fetch(url.replace('?lang=en', '') + "/sync_update", {{
    method: 'POST',
    headers: {{
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }},
    body: JSON.stringify({{
        "item_url" : item
    }})
    }});
    callback(url)
    """.format(url)
    
    value = driver.execute_async_script(script)
    
    return value

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    if message.content.startswith('!w2g'):
        message_list = message.content.split()
        if (len(message_list) == 1 or len(message_list) > 2):
            await message.channel.send('Invalid url! Please provide a youtube, twitch, vimeo, or soundcloud url.')
        elif (not('youtube.com' in message_list[1]) and not('twitch.tv' in message_list[1]) and not('vimeo.com' in message_list[1]) and not('soundcloud.com' in message_list[1])):
            await message.channel.send('Invalid url! Please provide a youtube, twitch, vimeo, or soundcloud url.')
        else:
            mention = message.author.mention
            room_url = create_room(message_list[1])
            await message.channel.send(f"Hey {mention}, your room is ready! {room_url}")
    if message.content.startswith('!w2ghelp'):
        await message.channel.send('To create a room, please type the command !w2g [insert link here]. The only supported links are youtube, vimeo, soundcloud, and twitch. ')

load_dotenv()
client.run(os.getenv('TOKEN'))


