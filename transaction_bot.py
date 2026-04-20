import discord
from keep_alive import keep_alive
import asyncio
import random
import string
import os
import json
import aiohttp
from discord.ext import commands

# ── CONFIG ───────────────────────────────────────────────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
CONFIG_FILE = "config.json"
# ─────────────────────────────────────────────────────────────────────────────

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=",", intents=intents, help_command=None)

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
    ("RAGE | Alex",   "<@602276804025016525>"),
    ("RAGE | Jordan",   "<@808631930086875935>"),
    ("RAGE | Chris",   "<@868570220212633229>"),
    ("RAGE | Sam",   "<@661713965687203229>"),
    ("RAGE | Casey",   "<@098830890407714528>"),
    ("RAGE | Jamie",   "<@425723964512352206>"),
    ("RAGE | Taylor",   "<@298026219547810444>"),
    ("RAGE | Drew",   "<@769043821442294850>"),
    ("RAGE | Blake",   "<@989981424039274499>"),
    ("RAGE | Quinn",   "<@571295570558190156>"),
    ("RAGE | Avery",   "<@218256455927236237>"),
    ("RAGE | Logan",   "<@049902298831876960>"),
    ("RAGE | Skyler",   "<@826911152672624980>"),
    ("RAGE | Reese",   "<@420762754008958511>"),
    ("RAGE | Parker",   "<@387882217846198988>"),
    ("RAGE | Sage",   "<@073988827188284372>"),
    ("RAGE | Dylan",   "<@013892639591919214>"),
    ("RAGE | Cameron",   "<@736535270957763063>"),
    ("RAGE | Hayden",   "<@387334421496963502>"),
    ("RAGE | Peyton",   "<@456442497105638762>"),
    ("RAGE | Dakota",   "<@102480461642607714>"),
    ("RAGE | River",   "<@195028486959867585>"),
    ("RAGE | Phoenix",   "<@874226756202235126>"),
    ("RAGE | Rowan",   "<@704542495687303789>"),
    ("RAGE | Finley",   "<@475622403641416035>"),
    ("RAGE | Zion",   "<@676791011652671671>"),
    ("RAGE | Kai",   "<@891036937066178619>"),
    ("RAGE | Ash",   "<@734353881968747928>"),
    ("RAGE | Cruz",   "<@545473722111571247>"),
    ("RAGE | Dani",   "<@952112105295618485>"),
    ("RAGE | Eden",   "<@441094840601539176>"),
    ("RAGE | Flynn",   "<@725448936679226110>"),
    ("RAGE | Knox",   "<@541376725946196215>"),
    ("RAGE | Lane",   "<@509941847528925395>"),
    ("RAGE | Milo",   "<@882749582259415355>"),
    ("RAGE | Nash",   "<@431652707783689405>"),
    ("RAGE | Reed",   "<@072315571086291422>"),
    ("BLADE | Tyler",   "<@089614356428134255>"),
    ("BLADE | Jordan",   "<@929625670649276366>"),
    ("BLADE | Chris",   "<@676869634570271159>"),
    ("BLADE | Sam",   "<@598284873191987998>"),
    ("BLADE | Casey",   "<@846650721507228319>"),
    ("BLADE | Jamie",   "<@081121600723107574>"),
    ("BLADE | Taylor",   "<@751590785490446490>"),
    ("BLADE | Drew",   "<@060265395460786772>"),
    ("BLADE | Blake",   "<@423440463190800785>"),
    ("BLADE | Quinn",   "<@553136787963526218>"),
    ("BLADE | Avery",   "<@375889866098217330>"),
    ("BLADE | Logan",   "<@854160724337750016>"),
    ("BLADE | Skyler",   "<@626442714264603503>"),
    ("BLADE | Reese",   "<@212307137588080098>"),
    ("BLADE | Parker",   "<@557410386890825533>"),
    ("BLADE | Sage",   "<@331515937882116761>"),
    ("BLADE | Dylan",   "<@747749566861043205>"),
    ("BLADE | Cameron",   "<@340808865457848634>"),
    ("BLADE | Hayden",   "<@101837512445132435>"),
    ("BLADE | Peyton",   "<@760062769835139635>"),
    ("BLADE | Dakota",   "<@933786876564331294>"),
    ("BLADE | River",   "<@210817880371318781>"),
    ("BLADE | Phoenix",   "<@446242745384839942>"),
    ("BLADE | Rowan",   "<@359881268518827291>"),
    ("BLADE | Zion",   "<@419505214624609055>"),
    ("BLADE | Kai",   "<@953469207376773058>"),
    ("BLADE | Ash",   "<@174668074201095952>"),
    ("BLADE | Cruz",   "<@990638691670073356>"),
    ("BLADE | Dani",   "<@693755362174352249>"),
    ("BLADE | Eden",   "<@294184840683305887>"),
    ("BLADE | Flynn",   "<@967512170538560397>"),
    ("BLADE | Knox",   "<@342202362813537454>"),
    ("BLADE | Lane",   "<@309592304864584877>"),
    ("BLADE | Milo",   "<@345150572961937397>"),
    ("BLADE | Nash",   "<@155013446536197238>"),
    ("BLADE | Reed",   "<@701236531933776661>"),
    ("KING | Tyler",   "<@252922273397216398>"),
    ("KING | Alex",   "<@982273424259616526>"),
    ("KING | Chris",   "<@319472918374650193>"),
    ("KING | Sam",   "<@536290184756293848>"),
    ("KING | Casey",   "<@112830890407714528>"),
    ("KING | Jamie",   "<@525723964512352206>"),
    ("KING | Taylor",   "<@398026219547810444>"),
    ("KING | Drew",   "<@869043821442294850>"),
    ("KING | Blake",   "<@189981424039274499>"),
    ("KING | Quinn",   "<@671295570558190156>"),
    ("STORM | Alex",   "<@427381029473810294>"),
    ("STORM | Jordan",   "<@319472918374650194>"),
    ("STORM | Sam",   "<@536290184756293849>"),
    ("STORM | Casey",   "<@212830890407714528>"),
    ("STORM | Jamie",   "<@625723964512352206>"),
    ("STORM | Taylor",   "<@498026219547810444>"),
    ("NOVA | Alex",   "<@536290184756293850>"),
    ("NOVA | Jordan",   "<@319472918374650195>"),
    ("NOVA | Chris",   "<@427381029473810295>"),
    ("NOVA | Casey",   "<@312830890407714528>"),
    ("NOVA | Jamie",   "<@725723964512352206>"),
    ("WOLF | Tyler",   "<@147679767722314960>"),
    ("WOLF | Alex",   "<@238519204871345671>"),
    ("WOLF | Jordan",   "<@319472918374650196>"),
    ("HAWK | Tyler",   "<@147679767722314961>"),
    ("HAWK | Alex",   "<@238519204871345672>"),
    ("IRON | Tyler",   "<@147679767722314962>"),
    ("IRON | Alex",   "<@238519204871345673>"),
]


# ── Save/load channel ID ──────────────────────────────────────────────────────
def save_config(channel_id: int):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"channel_id": channel_id}, f)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("channel_id")
    return None


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

    try:
        if file:
            await channel.send(file=file, embed=embed)
        else:
            await channel.send(embed=embed)
        print(f"[BOT] Sent transaction #{order_counter}")
    except discord.errors.HTTPException as e:
        if e.status == 429:
            retry_after = e.retry_after if hasattr(e, 'retry_after') else 30
            print(f"[BOT] Rate limited! Waiting {retry_after}s before retrying...")
            await asyncio.sleep(retry_after)
            # Retry once after waiting
            if file:
                await channel.send(file=file, embed=embed)
            else:
                await channel.send(embed=embed)
            print(f"[BOT] Retried and sent transaction #{order_counter}")
        else:
            raise


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
    save_config(target_channel.id)
    await asyncio.sleep(1)  # small delay to avoid rate limit on reply
    embed = discord.Embed(
        description=f"✅ Transaction channel set to {target_channel.mention}!\nAll auto transactions will be sent there.",
        color=0x57F287
    )
    await ctx.send(embed=embed)
    print(f"[BOT] Channel set to: #{target_channel.name} (ID: {target_channel.id})")


# ── COMMAND: ,setimage ───────────────────────────────────────────────────────
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
    await asyncio.sleep(1)
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
    global target_channel
    await bot.wait_until_ready()
    await asyncio.sleep(5)  # Wait 5s after ready before starting loop

    # Load saved channel
    channel_id = load_config()
    if channel_id:
        target_channel = bot.get_channel(channel_id)
        if target_channel:
            print(f"[BOT] Restored channel: #{target_channel.name}")
        else:
            print(f"[BOT] Could not restore channel ID {channel_id}")

    while not bot.is_closed():
        if target_channel:
            try:
                await send_transaction(target_channel)
            except Exception as e:
                print(f"[BOT] Error sending transaction: {e}")
        else:
            print("[BOT] No channel set yet. Use ,setchannel to set one.")

        wait = random.randint(5 * 60, 30 * 60)
        print(f"[BOT] Next transaction in {wait // 60}m {wait % 60}s")
        await asyncio.sleep(wait)


@bot.event
async def on_ready():
    print(f"[BOT] Logged in as {bot.user} (ID: {bot.user.id})")
    bot.loop.create_task(transaction_loop())


keep_alive()
bot.run(BOT_TOKEN)
