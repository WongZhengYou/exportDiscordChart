
import asyncio
import csv
import getpass
from pathlib import Path

import discord

CHANNEL_ID = int(input("Enter the Discord channel ID: ").strip())
OUTPUT_FILE = Path.home() / "Desktop" / "discord_channel_export.csv"

intents = discord.Intents.none()
intents.guilds = True
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    try:
        print(f"Connected as {client.user}")
        print("Fetching channel...")

        channel = await client.fetch_channel(CHANNEL_ID)

        if not hasattr(channel, "history"):
            print("Error: This channel does not support message history.")
            return

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        count = 0

        with OUTPUT_FILE.open(
            "w", newline="", encoding="utf-8-sig"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "message_id",
                    "created_at_utc",
                    "author_id",
                    "author_name",
                    "content",
                    "attachment_urls",
                    "jump_url",
                    "channel_id",
                ],
            )
            writer.writeheader()

            async for message in channel.history(
                limit=None, oldest_first=True
            ):
                writer.writerow({
                    "message_id": message.id,
                    "created_at_utc": message.created_at.isoformat(),
                    "author_id": message.author.id,
                    "author_name": str(message.author),
                    "content": message.content,
                    "attachment_urls": "\n".join(
                        attachment.url
                        for attachment in message.attachments
                    ),
                    "jump_url": message.jump_url,
                    "channel_id": message.channel.id,
                })

                count += 1
                if count % 500 == 0:
                    print(f"Exported {count} messages...")

        print(f"\nFinished! Exported {count} messages.")
        print(f"CSV saved to: {OUTPUT_FILE}")

    except discord.Forbidden:
        print("Access denied. Check the bot's channel permissions.")
    except discord.NotFound:
        print("Channel not found. Check the channel ID and bot access.")
    except Exception as error:
        print(f"Export failed: {type(error).__name__}: {error}")
    finally:
        await client.close()


async def main():
    token = getpass.getpass("Enter your Discord BOT token: ")
    if not token:
        print("No token entered.")
        return

    await client.start(token)


if __name__ == "__main__":
    asyncio.run(main())
