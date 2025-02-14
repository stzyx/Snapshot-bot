# Snapshot bot
Source code for generating fake discord message screenshots using pillow and discord.py

## Setup
### Cloning the source
```sh
git clone https://github.com/stzyx/SnapshotBot
cd SnapshotBot
```

### Requirements
- Python 3.8+
- Packages:
  ```sh
  python -m pip install -r requirements.txt
  ```

## Running the Bot
1. Extract font files:
   ```sh
   unzip font.zip
   ```
   **IMPORTANT:** unzip `font.zip` before running the bot.
2. Configure `config.py` with your bot token
3. Run the bot:
   ```sh
   python bot.py
   ```
   or
   ```sh
   python3 bot.py
   ```
## Commands
- `v!help` - Show help message
- `v!activate` - Activate the bot
- `v!deactivate` - Deactivate the bot
- `v!snap @user <message>` - Generate screenshot from text and user mention
- `v!bg <theme>` - Change background theme (midnight/white/dark)

 `You can change the prefix(v!) in config.py`
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
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

## Usage
![image](https://i.postimg.cc/tCdSzbmv/image.png)

