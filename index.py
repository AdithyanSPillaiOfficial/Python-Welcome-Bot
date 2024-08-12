import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import os
import asyncio
from dotenv import load_dotenv
import datetime
from collections import defaultdict


load_dotenv()

# Enable intents
intents = discord.Intents.default()
intents.members = True  # Make sure the bot can receive member-related events
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='welcome')
    if not channel:
        return

    # Load the background image
    bg_image = Image.open('bg.jpg')

    # Create a drawing context
    draw = ImageDraw.Draw(bg_image)

    # Load fonts with larger sizes
    try:
        font_large = ImageFont.truetype('arial.ttf', 50)  # Size for "Welcome" and "to GTA MALLU FAMILY"
        font_extra_large = ImageFont.truetype('arial.ttf', 75)  # Size for the name
    except IOError:
        # Fallback to a default font if Arial is not available
        font_large = ImageFont.load_default()
        font_extra_large = ImageFont.load_default()

    # Define the text
    welcome_text = "Welcome"
    name_text = member.display_name
    family_text = "to GTA MALLU FAMILY"

    # Line spacing factor
    line_spacing = 20  # Adjust this value to increase/decrease space between lines

    # Calculate the bounding box for the text to center it
    welcome_bbox = draw.textbbox((0, 0), welcome_text, font=font_large)
    name_bbox = draw.textbbox((0, 0), name_text, font=font_extra_large)
    family_bbox = draw.textbbox((0, 0), family_text, font=font_large)

    # Get image dimensions
    img_width, img_height = bg_image.size

    # Calculate text dimensions
    welcome_width, welcome_height = welcome_bbox[2] - welcome_bbox[0], welcome_bbox[3] - welcome_bbox[1]
    name_width, name_height = name_bbox[2] - name_bbox[0], name_bbox[3] - name_bbox[1]
    family_width, family_height = family_bbox[2] - family_bbox[0], family_bbox[3] - family_bbox[1]

    # Calculate positions for centering with line spacing
    total_text_height = welcome_height + line_spacing + name_height + line_spacing + family_height
    welcome_position = (((img_width - welcome_width) // 2) + 80, (img_height - total_text_height) // 2)
    name_position = (((img_width - name_width) // 2) + 80, welcome_position[1] + welcome_height + line_spacing)
    family_position = (((img_width - family_width) // 2) + 80, name_position[1] + name_height + line_spacing)

    # Draw the text onto the image
    draw.text(welcome_position, welcome_text, font=font_large, fill=(255, 255, 255))
    draw.text(name_position, name_text, font=font_extra_large, fill=(255, 255, 255))
    draw.text(family_position, family_text, font=font_large, fill=(255, 255, 255))

    # Save the image
    bg_image.save('welcome.png')

    # Send the image in the welcome channel
    with open('welcome.png', 'rb') as f:
        picture = discord.File(f)
        await channel.send(f'Welcome to the server, {member.mention}!', file=picture)


#TIME OUT SPAMMING USERS
# Track message timestamps
message_times = defaultdict(list)
SPAM_THRESHOLD = 5  # Number of messages in a short period considered as spam
TIME_WINDOW = 10  # Time window in seconds to check for spam

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = message.author.id
    now = discord.utils.utcnow()

    # Update message timestamps
    message_times[user_id].append(now)
    message_times[user_id] = [timestamp for timestamp in message_times[user_id] if (now - timestamp).total_seconds() < TIME_WINDOW]

    if len(message_times[user_id]) > SPAM_THRESHOLD:
        # User is spamming
        try:
            #await message.author.timeout_for(minutes=10)
            duration = datetime.timedelta(seconds=0, minutes=10, hours= 0, days=0)
            await message.author.timeout(duration, reason="Spamming")
            await message.channel.send(f"{message.author.mention}, you have been put in timeout for spamming.")
        except discord.Forbidden:
            await message.channel.send("I don't have permission to timeout users.")
        except discord.HTTPException as e:
            await message.channel.send(f"An error occurred: {e}")

    await bot.process_commands(message)


# Running the bot
async def main():
    from keep_alive import keep_alive
    keep_alive()
    bot_token = os.getenv('BOT_TOKEN')  # Ensure this environment variable is set
    await bot.start(bot_token)

# Use asyncio.run to execute the async function
if __name__ == "__main__":
    asyncio.run(main())
