import discord
import requests
import os
from bs4 import BeautifulSoup


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


#look up callsigns using the QRZ website to find an amateur radio operator
@client.event
async def on_message(message):
    if message.content.startswith('!lookup'):
        callsign = message.content[6:]
        response = requests.get(f'https://xmldata.qrz.com/xml/current/?s={callsign};callsign')
        xml_data = response.content.decode('utf-8')
        if '<Session>' in xml_data:
            name = xml_data.split('<fname>')[1].split('</fname>')[0]
            qth = xml_data.split('<addr2>')[1].split('</addr2>')[0]
            country = xml_data.split('<country>')[1].split('</country>')[0]
            grid = xml_data.split('<grid>')[1].split('</grid>')[0]
            url = xml_data.split('<bio_url>')[1].split('</bio_url>')[0]
            embed = discord.Embed(title=callsign.upper(), description=f'{name}\n{qth}\n{country}\n{grid}\n{url}', color=0x00ff00)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(f'{callsign} not found.')
    
# URL of the DX Watch page
url = 'https://dxwatch.com/'

# Read the callsigns from a file
with open('callsigns.txt', 'r') as file:
    callsigns = [line.strip() for line in file.readlines()]

# Event listener for when the bot is ready
@client.event
async def on_ready():
    print('Bot is ready')

    if message.content.startswith('!set_channel'):
        # Get the server ID and the channel ID from the command
        server_id, channel_id = message.content.split()[1:]
        channels[server_id] = channel_id
        await message.channel.send(f"DX spots will now be announced on channel <#{channel_id}>")

    # Event loop to check for DX Watch updates
    while True:
        # Get the HTML content of the DX Watch page
        response = requests.get(url)
        html = response.text

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Find the DX spots table
        table = soup.find('table', {'id': 'spot_table'})

        # Look for the callsigns in the DX spots
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if cols:
                spot_callsign = cols[1].text.strip()
                if spot_callsign in callsigns:
                    spot_frequency = cols[2].text.strip()
                    spot_comment = cols[3].text.strip()
                    # Send a message to the channel with the DX spot information
                    await client.get_channel(your_channel_id_here).send(f"**{spot_callsign}** spotted on {spot_frequency}: {spot_comment}")

        # Wait for an hour before checking again
        await asyncio.sleep(3600)


client.run('DISCORD BOT TOKEN')
