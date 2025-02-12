# Snapshot bot
 Source code for generating fake discord message screenshots using pillow and discord.py

### Config.py
```py
# Bot Configuration
is_a_self_bot = False # Change this to True if you are using a self bot

# Bot Settings
default_background_color = "midnight" # midnight | white | dark
admin_id = 123456789123456789
default_status = "use v!help"
active_status = default_status
inactive_status = f"{default_status} [inactive]"

# Commands
prefix = "v!"
activation_command = prefix + "activate"
deactivation_command = prefix + "deactivate"
background_command = prefix + "bg"
snap_command = prefix + "snap"

# Bot Token
BOT_TOKEN = ""
```

## Usage
![image](https://i.postimg.cc/tCdSzbmv/image.png)
