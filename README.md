# exportDiscordChart

# Discord Channel Exporter (`export_discord.py`)

A Python script that exports the accessible message history of one Discord channel to a CSV file. It uses a **Discord bot token**, not a personal user token.

## What it does

- Connects to Discord using your bot account.
- Fetches one channel's message history, oldest message first.
- Writes a CSV containing `message_id`, `created_at_utc`, `author_id`, `author_name`, `content`, `attachment_urls`, `jump_url`, and `channel_id`.
- Saves the CSV to your Windows Desktop as `discord_channel_export.csv`.
- Uses UTF-8 with BOM (`utf-8-sig`) to help Excel display Chinese and other non-English text.

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer recommended
- A Discord application with a bot user
- The bot must be in the server and have permission to view the target channel and read its message history
- Message Content Intent enabled in the Discord Developer Portal and in the script

## 1. Create a Discord bot

1. Open the [Discord Developer Portal](https://discord.com/developers/applications).
2. Select **New Application**, name it (for example, `ChatExporter`), and create it.
3. Open **Bot** and create the bot user if prompted.
4. Under **Privileged Gateway Intents**, enable **Message Content Intent**.
5. Under **OAuth2 → URL Generator**, select the `bot` scope and generate an invite URL.
6. Invite the bot to your server.
7. Give the bot access to the target channel with **View Channel** and **Read Message History** permissions.

Do not grant Administrator unless you have a separate reason to do so.

## 2. Install Python and `discord.py`

Open PowerShell and check Python:

```powershell
py --version
```

If the command is unavailable, install Python from [python.org](https://www.python.org/downloads/) and reopen PowerShell.

Install the Discord library:

```powershell
py -m pip install -U discord.py
```

## 3. Save the script

Save the provided Python code as `export_discord.py`, for example in `C:\DiscordExporter\export_discord.py`.

## 4. Copy the channel ID

1. In Discord, open **User Settings → Advanced** and enable **Developer Mode**.
2. Right-click the channel you want to export.
3. Select **Copy Channel ID**.

Copy the channel ID, not the server ID or a message ID.

## 5. Run an export

Open PowerShell and run:

```powershell
cd C:\DiscordExporter
py .\export_discord.py
```

When prompted:

1. Paste the channel ID and press Enter.
2. Paste your **bot token** and press Enter. The token input is hidden while typing.

Do not share your token in chat, screenshots, public repositories, or command lines that may be saved in shell history. If exposed, reset it in the Developer Portal.

When finished, the CSV is saved to:

```text
C:\Users\<your Windows username>\Desktop\discord_channel_export.csv
```

Open it with Excel. Each run overwrites that filename, so rename or move the previous CSV first if you want to keep it.

## 6. CSV columns

| Column | Meaning |
|---|---|
| `message_id` | Discord message ID |
| `created_at_utc` | Message timestamp in UTC |
| `author_id` | ID of the message author |
| `author_name` | Author name returned by Discord |
| `content` | Message text available to the bot |
| `attachment_urls` | Newline-separated attachment URLs |
| `jump_url` | Direct link to the Discord message |
| `channel_id` | ID of the channel |

The script exports existing messages that are accessible to the bot. It cannot recover deleted messages. It does not automatically export other channels or every thread. It records attachment URLs but does not download attachment files.

## Troubleshooting

### `py` is not recognized

Install Python from [python.org](https://www.python.org/downloads/), then close and reopen PowerShell.

### `No module named 'discord'`

Run:

```powershell
py -m pip install -U discord.py
```

### `Access denied` / `Forbidden`

Check that the bot is in the server and has **View Channel** and **Read Message History** permissions in the target channel. Check category-level permission overrides too.

### `Channel not found`

Verify that you copied the channel ID and that the bot can access the channel.

### Message content is blank

Check **Developer Portal → Bot → Privileged Gateway Intents → Message Content Intent**, and verify that the script sets:

```python
intents.message_content = True
```

The bot must be authorized to use the intent. This script cannot bypass Discord's access controls.

### CSV has garbled characters in Excel

The script uses `utf-8-sig`, which usually helps Excel detect UTF-8. If needed, use Excel's **Data → From Text/CSV** import and choose UTF-8.

### Export takes a long time

Large channels can take a while to fetch. Leave the script running until it reports completion and avoid starting multiple exports simultaneously.

### Windows blocks a downloaded exporter executable

This Python project does not require the DiscordChatExporter CLI executable or changes to Windows security settings. Do not disable Smart App Control or replace blocked DLLs to run an unsigned executable.

## Security and privacy

- Use a **bot token**, never a personal user token.
- Keep the token private; anyone who obtains it may control the bot.
- Give the bot only the permissions it needs.
- Export only channels and conversations you are authorized to access.
- Store the CSV securely; it may contain private messages and attachment links.
- This script saves the CSV locally. It does not upload the CSV to Discord or a cloud host.

## Script versus command bot

`export_discord.py` is an interactive, one-time script. It asks for a channel ID and token in PowerShell, exports that channel, then exits.

It does **not** listen for commands such as `@ChatExporter export #general`. That requires a separate always-running bot implementation with a command handler and cloud hosting configuration.

## License

Use and modify this script for authorized Discord exports. Follow Discord's terms and your server's privacy rules.
