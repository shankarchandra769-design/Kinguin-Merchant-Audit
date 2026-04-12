import discord
from keep_alive import keep_alive
import asyncio
import random
import string
import os
import aiohttp
from discord.ext import commands

# ── CONFIG (loaded from environment variables for Render) ────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
# ────────────────────────────────────────────────────────────────────────────

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=",", intents=intents)

order_counter  = 2980
thumbnail_url  = None
stored_image   = "stored.png"
target_channel = None

PAYMENT_METHODS = ["Zelle", "PayPal", "CashApp", "Venmo", "Crypto"]

FAKE_USERS = [
    ("RAGE | Tyler",   "<@147679767722314959>"),
    ("BLADE | Alex",   "<@238519204871345670>"),
    ("KING | Jordan",  "<@319472918374650192>"),
    ("STORM | Chris",  "<@427381029473810293>"),
    ("NOVA | Sam",     "<@536290184756293847>"),
    ("VIPER | Max",    "<@641029384756102938>"),
    ("GHOST | Riley",  "<@758392047561029384>"),
    ("APEX | Morgan",  "<@864729103847562019>"),
]


def random_transaction_id() -> str:
    return "".join(random.choices(string.digits, k=18))


def star_rating(rating: float) -> str:
    full  = int(rating)
    half  = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + "½" * half + "☆" * empty


async def build_and_send(channel, file=None, thumb_url=None):
    global order_counter
    order_counter += 1

    user_name, user_mention = random.choice(FAKE_USERS)
    payment  = random.choice(PAYMENT_METHODS)
    euro_val = round(random.uniform(5.00, 200.00), 2)
    rating   = round(random.choice([4.0, 4.5, 5.0]), 1)
    txn_id   = random_transaction_id()
    stars    = star_rating(rating)

    embed = discord.Embed(title="Transaction Completed", color=0x2b2d31)

    if thumb_url:
        embed.set_thumbnail(url=thumb_url)

    embed.add_field(name="Order",          value=f"#{order_counter}",            inline=True)
    embed.add_field(name="\u200b",         value="\u200b",                       inline=True)
    embed.add_field(name="\u200b",         value="\u200b",                       inline=True)
    embed.add_field(name="User",           value=f"{user_name}\n{user_mention}", inline=False)
    embed.add_field(name="Payment Method", value=payment,                        inline=False)
    embed.add_field(name="EURO Value",     value=f"€{euro_val:.2f}",             inline=False)
    embed.add_field(name="Rating",         value=f"{stars} ({rating}/5)",        inline=False)
    embed.add_field(name="Transaction ID", value=txn_id,                         inline=False)
    embed.set_footer(text="Powered by kinguin.net")

    if file:
        await channel.send(file=file, embed=embed)
    else:
        await channel.send(embed=embed)

    print(f"[BOT] Sent transaction #{order_counter}")


async def send_transaction(channel):
    global thumbnail_url

    if thumbnail_url:
        await build_and_send(channel, thumb_url=thumbnail_url)
    elif os.path.exists(stored_image):
        file = discord.File(stored_image, filename="thumb.png")
        await build_and_send(channel, file=file, thumb_url="attachment://thumb.png")
    else:
        await build_and_send(channel)


# ── COMMAND: ,setchannel ─────────────────────────────────────────────────────
@bot.command(name="setchannel")
async def set_channel(ctx, channel: discord.TextChannel = None):
    global target_channel
    target_channel = channel or ctx.channel
    embed = discord.Embed(
        description=f"✅ Transaction channel set to {target_channel.mention}!\nAll auto transactions will be sent there.",
        color=0x57F287
    )
    await ctx.send(embed=embed)
    print(f"[BOT] Channel set to: #{target_channel.name}")


# ── COMMAND: ,setimage (attach image) ────────────────────────────────────────
@bot.command(name="setimage")
async def set_image(ctx):
    global thumbnail_url

    if not ctx.message.attachments:
        await ctx.send(
            "❌ Please **attach an image** to the command.\n"
            "Example: type `,setimage` and attach your PNG/JPG file."
        )
        return

    attachment = ctx.message.attachments[0]
    if not attachment.content_type or not attachment.content_type.startswith("image/"):
        await ctx.send("❌ That doesn't look like an image. Please attach a PNG or JPG.")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(attachment.url) as resp:
            if resp.status == 200:
                data = await resp.read()
                with open(stored_image, "wb") as f:
                    f.write(data)
                thumbnail_url = None
                embed = discord.Embed(
                    description=(
                        "✅ Image **saved & set**!\n"
                        "It will appear top-right in all future transactions and will **never expire**."
                    ),
                    color=0x57F287
                )
                embed.set_thumbnail(url=attachment.url)
                await ctx.send(embed=embed)
                print(f"[BOT] Image saved locally as '{stored_image}'")
            else:
                await ctx.send("❌ Failed to download the image. Please try again.")


# ── COMMAND: ,sendnow ────────────────────────────────────────────────────────
@bot.command(name="sendnow")
async def send_now(ctx):
    channel = target_channel or ctx.channel
    await send_transaction(channel)
    await ctx.send("✅ Transaction sent!", delete_after=3)


# ── COMMAND: ,help ───────────────────────────────────────────────────────────
@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(
        title="📋 Bot Commands",
        description="Prefix: `,`  |  All commands listed below",
        color=0x5865F2
    )
    embed.add_field(
        name=",setchannel [#channel]",
        value=(
            "Set which channel the auto transactions will be sent to.\n"
            "If no channel is mentioned, uses the current channel.\n"
            "Example: `,setchannel #sales`"
        ),
        inline=False
    )
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(
        name=",setimage  [attach image]",
        value=(
            "Attach a PNG/JPG to set the thumbnail (top-right of embed).\n"
            "Image is saved locally so it **never expires**.\n"
            "Example: type `,setimage` and attach your PNG/JPG file."
        ),
        inline=False
    )
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.add_field(
        name=",sendnow",
        value=(
            "Manually send a transaction embed instantly.\n"
            "Sends to the channel set by `,setchannel` or current channel."
        ),
        inline=False
    )
    embed.add_field(name="\u200b", value="\u200b", inline=False)
    embed.set_footer(text="Auto transactions send every 5–30 minutes randomly.")
    await ctx.send(embed=embed)


async def transaction_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        if target_channel:
            await send_transaction(target_channel)
        else:
            print("[BOT] No channel set yet. Use ,setchannel to set one.")
        wait = random.randint(5 * 60, 30 * 60)
        print(f"[BOT] Next transaction in {wait // 60}m {wait % 60}s")
        await asyncio.sleep(wait)


@bot.event
async def on_ready():
    print(f"[BOT] Logged in as {bot.user} (ID: {bot.user.id})")
    print("[BOT] Use ,setchannel in your Discord to start sending transactions.")
    bot.loop.create_task(transaction_loop())


keep_alive()
bot.run(BOT_TOKEN)
