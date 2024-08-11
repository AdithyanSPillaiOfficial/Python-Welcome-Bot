import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

# Enable intents
intents = discord.Intents.default()
intents.members = True  # Make sure the bot can receive member-related events

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
        font_large = ImageFont.truetype('arial.ttf', 50)  # Increased size for "Welcome" and "to GTA MALLU FAMILY"
        font_extra_large = ImageFont.truetype('arial.ttf', 75)  # Increased size for the name
    except IOError:
        # Fallback to a default font if Arial is not available
        font_large = ImageFont.load_default()
        font_extra_large = ImageFont.load_default()

    # Define the text
    welcome_text = "Welcome"
    name_text = member.display_name
    family_text = "to GTA MALLU FAMILY"

    # Calculate the width and height of the text to center it
    welcome_width, welcome_height = draw.textsize(welcome_text, font=font_large)
    name_width, name_height = draw.textsize(name_text, font=font_extra_large)
    family_width, family_height = draw.textsize(family_text, font=font_large)

    # Get image dimensions
    img_width, img_height = bg_image.size

    # Calculate positions for centering
    welcome_position = (((img_width - welcome_width) // 2)+80, (img_height - welcome_height - name_height - family_height) // 2)
    name_position = (((img_width - name_width) // 2)+80, welcome_position[1] + welcome_height)
    family_position = (((img_width - family_width) // 2)+80, name_position[1] + name_height)

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


# Running the bot
bot_token = os.getenv('BOT_TOKEN')

async def main():
    async with bot:
        await bot.start(bot_token)

# If running in a Colab/Jupyter environment
await main()
