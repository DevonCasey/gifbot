import discord
import requests
from moviepy.editor import *
from giphypop import upload
from config import discord_token, giphy_username, giphy_token
import os

client = discord.Client()  # Connect to Discord


@client.event
async def on_ready():  # Lets the server know that the bot is logged in and ready to be used
    print('{0.user} is ready'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:  # Lets the bot actually talk
        return

    if message.content.startswith('!gifhelp'):  # Listens for the !gifhelp command to display how to use this Bot
        await message.channel.send('If you want to convert a video to a gif upload the video normally and add '
                                   '"!convert" where it says "Add a comment"')

    if message.content.startswith('!convert'):  # Listens for the !convert command to an uploaded file attachment
        await message.channel.send('Lets get started!')
        url = message.attachments[0].url  # Gets the url of the uploaded file from the user
        request = requests.get(url, allow_redirects=True)  # Loads the url of the uploaded file

        if url.find('/'):  # Gets the original file name of the upload for consistency for the .gif name
            file_name = "tmp/" + url.rsplit('/', 1)[1]
            open(file_name, 'wb').write(request.content)  # Saves the uploaded file
            file_name_no_ext = file_name.split('.')[0]  # Sterilizes the the file_name String to not have the file
            # extension attached
            try:
                await message.channel.send('Your video is being processed...')
                video_file = (VideoFileClip(file_name))  # Reads the uploaded file
                gif_name = "%s.gif" % file_name_no_ext  # Adds .gif to the file name because the bot is nice like that
                video_file.write_gif(gif_name, fps=24, program='imageio')  # Saves the gif to the server
                await message.channel.send('Success! Uploading to Giphy...')  # Wouldn't you like to know that the
                # program is working?
                gif = upload(['discord', 'bot'], gif_name, username=giphy_username,
                             api_key=giphy_token)  # Uploads to giphy
                await message.channel.send('Upload complete, here is the link to your gif: %s' % gif)
                os.remove(file_name)  # Removes the files afterward to save some space
                os.remove(gif_name)
            except:  # Super broad try-catch for now, will do more testing for possible errors and update
                await message.channel.send('Something went wrong, are you sure this file is a video?')
                if file_name:
                    os.remove(file_name)
                if gif_name:
                    os.remove(gif_name)


client.run(discord_token)  # Runs the bot with its token
