try:
    from config import *
except:
    print("Unable to find config.py")
    exit()
import discord
import string
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
from fontTools.ttLib import TTFont

if is_a_self_bot:
    bot = discord.Client()
else:
    bot = discord.Client(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name=default_status))

def get_characters(font_path: str) -> list[str]:
    """Extract characters from a font file."""
    font = TTFont(font_path)
    cmap = font.getBestCmap()
    return [chr(char_code) for char_code in cmap.keys()]

def check_characters(name: str) -> bool:
    """Check if all characters in the name are supported by the available fonts."""
    fonts = sorted(os.listdir('./font'))
    font_characters = []
    for font in fonts:
        characters = get_characters('./font/' + font)
        font_characters.extend(characters)
    return all(char in font_characters for char in name)

def get_font_for_character(character: str) -> str:
    """Get the font file path that supports the given character."""
    fonts = sorted(os.listdir('./font'))
    for font in fonts:
        characters = get_characters('./font/' + font)
        if character in characters:
            return './font/' + font

is_active = True
background_color = default_background_color

@bot.event
async def on_message(message: discord.Message):
    global is_active
    global background_color
    use_profile_picture = True
    custom_name = False
    if message.author == bot.user:
        return
    if message.content.lower().startswith(prefix + "help"):
        if is_a_self_bot:
            await message.reply("Help:\n"
                f"`{prefix}help` - Shows this help message.\n"
                f"`{activation_command}` - Activates the bot. (Admin only)\n"
                f"`{deactivation_command}` - Deactivates the bot. (Admin only)\n"
                f"`{background_command} <color>` - Changes the background color of the snapshot. Available colors: `midnight`, `white`, `dark`\n"
                f"`{snap_command} @user (message)` - Generates a snapshot of the user's message.")
            return
        embed = discord.Embed(title="Help", description="List of available commands:", color=0x00ff00)
        embed.add_field(name=f"{prefix}help", value="Shows this help message.", inline=False)
        embed.add_field(name=f"{activation_command}", value=f"Activates the bot. (Admin only)", inline=False)
        embed.add_field(name=f"{deactivation_command}", value=f"Deactivates the bot. (Admin only)", inline=False)
        embed.add_field(name=f"{background_command} <color>", value="Changes the background color of the snapshot.\nAvailable colors: `midnight`, `white`, `dark`", inline=False)
        embed.add_field(name=f"{snap_command} @user (message)", value="Generates a snapshot of the user's message.", inline=False)
        await message.reply(embed=embed)
        return
    if message.content.lower() == activation_command and message.author.id == admin_id:
        is_active = True
        await bot.change_presence(activity=discord.Game(name=active_status))
    elif message.content.lower() == deactivation_command and message.author.id == admin_id:
        is_active = False
        await bot.change_presence(activity=discord.Game(name=inactive_status))
    elif message.content.lower().startswith(background_command):
        if len(message.content.split()) == 1:
            await message.reply(f"`{background_command} <color>`\nmidnight\nwhite\ndark")
        else:
            new_color = message.content.split()[1]
            if new_color in ["midnight", "white", "dark"]:
                background_color = new_color
                await message.reply(f"Changed background color to **{new_color}**")
            else:
                await message.reply(f"`{background_command} <color>`\nmidnight\nwhite\ndark")
    elif message.content.lower().startswith(snap_command):
        if not is_active:
            return
        await message.channel.typing()
        content = message.content.split(' ', 2)
        if len(content) < 3:
            await message.reply(f"Use the command in the following format: `{snap_command} @user (message)`")
            return
        if not content[1].startswith("<@") and not content[1].endswith(">"):
            use_profile_picture = False
            custom_name = content[1]
        else:
            member = message.mentions[0]
        message_text = content[2].strip()
        if message.mentions[1:]:
            for user in message.mentions[1:]:
                mention = f"<@{user.id}>"
                name = user.nick or user.global_name or user.name
                if set(name).issubset(set(string.ascii_letters + string.digits + string.punctuation)):
                    message_text = message_text.replace(mention, f'@{name}')
                else:
                    message_text = message_text.replace(mention, f'@{user.name}')
        if background_color == 'white':
            colors = {
                "time": (36, 36, 36),
                "content": (0, 0, 0),
            }
        else:
            colors = {
                "time": (116, 127, 141),
                "content": (238, 239, 240),
            }

        font_sizes = {
            "title": 38,
            "time": 28
        }

        font_path = './font/ggsans-Medium.ttf'
        title_font_path = './font/ggsans-Semibold.ttf'
        text_font = ImageFont.truetype(font_path, font_sizes["title"])
        time_font = ImageFont.truetype(font_path, font_sizes["time"])
        title_font = ImageFont.truetype(title_font_path, font_sizes["title"])

        title_characters = get_characters("font/ggsans-Bold.ttf")

        def wrap_text(text: str, max_width: int) -> list[str]:
            """Wrap text to fit within a specified width."""
            wrapped_lines = []
            for line in text.splitlines():
                wrapped = textwrap.fill(line.strip(), width=max_width)
                wrapped_lines.extend(wrapped.splitlines())
            return wrapped_lines

        wrapped_message = wrap_text(message_text, 50)
        line_count = len(wrapped_message)
        image_height = 270 + ((line_count - 2) * 48)
        match background_color:
            case "white":
                image = Image.new('RGB', (1048, image_height), color=(242, 242, 242))
            case "dark":
                image = Image.new('RGB', (1048, image_height), color=(28, 29, 34))
            case _:
                image = Image.new('RGB', (1048, image_height), color=(0, 0, 0))

        draw = ImageDraw.Draw(image)
        if not custom_name:
            username = member.nick or member.display_name or member.name
            if not check_characters(username):
                username = member.name

            if len(member.roles) <= 1:
                color = (1, 2, 3) if background_color == 'white' else (248, 249, 250)
            else:
                r, g, b = member.top_role.color.to_rgb()
                color = (r, g, b)
        else:
            username = custom_name
            color = (248, 249, 250)

        x_position = 180
        for char in username:
            if char in title_characters:
                draw.text((x_position, 48), char, font=title_font, fill=color)
                char_size = title_font.getbbox(char)[2]
            else:
                font = ImageFont.truetype(get_font_for_character(char), font_sizes["title"])
                draw.text((x_position, 48), char, font=font, fill=color)
                char_size = font.getbbox(char)[2]
            x_position += char_size

        current_time = datetime.now().strftime("Today at %I:%M %p")
        draw.text((x_position + 20, 60), current_time, font=time_font, fill=colors["time"])

        padding_y = 0
        for line in wrapped_message:
            draw.text((180, 100 + padding_y), line, font=text_font, fill=colors["content"])
            padding_y += 54

        image.save('img.png')
        if use_profile_picture:
            try:
                await member.avatar.save('profile_picture.png')
                profile_picture = Image.open("profile_picture.png")
            except Exception:
                profile_picture = Image.open('default.png')
        else:
            profile_picture = Image.open('default.png')

        profile_picture.thumbnail((110, 110))
        profile_picture = profile_picture.convert("RGB")

        mask = Image.new("L", profile_picture.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, profile_picture.size[0], profile_picture.size[1]), fill=255)
        profile_picture.putalpha(mask)

        if not custom_name and member.avatar_decoration:
            await member.avatar_decoration.save('decoration.png')
            decoration = Image.open('decoration.png').convert("RGBA")
            decoration_size = (130, 130)
            decoration = decoration.resize(decoration_size, Image.Resampling.LANCZOS)
            final_image = Image.new("RGBA", decoration_size, (0, 0, 0, 0))
            x = (decoration_size[0] - profile_picture.size[0]) // 2
            y = (decoration_size[1] - profile_picture.size[1]) // 2
            final_image.paste(profile_picture, (x, y), profile_picture)
            final_image.paste(decoration, (0, 0), decoration)
            profile_picture = final_image

        final_image = image.copy()
        final_image.paste(profile_picture, (40, 40), profile_picture)
        final_image.save("img.png")
        file = discord.File("img.png")
        if is_a_self_bot:
            await message.reply(f"Snapshot by **{message.author.display_name or message.author.name}** ({message.author.name})", file=file)
        else:
            embed = discord.Embed(
                description=f"Snapshot by **{message.author.display_name or message.author.name}** ({message.author.name})",
                color=discord.Color.blurple()
            )
            embed.set_image(url="attachment://img.png")
            await message.reply(embed=embed, file=file)
        try:
            os.remove("profile_picture.png")
            os.remove("img.png")
            try:
                os.remove("decoration.png")
            except:
                pass
            return
        except Exception as e:
            print(e)
            return

if __name__ == "__main__":
    bot.run(BOT_TOKEN)