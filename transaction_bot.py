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
    ("KING | Jordan",   "<@319472918374650192>"),
    ("STORM | Chris",   "<@427381029473810293>"),
    ("NOVA | Sam",   "<@536290184756293847>"),
    ("VIPER | Max",   "<@641029384756102938>"),
    ("GHOST | Riley",   "<@758392047561029384>"),
    ("APEX | Morgan",   "<@864729103847562019>"),
    ("RAGE | Alex",   "<@602276804025016525>"),
    ("RAGE | Jordan",   "<@808631930086875935>"),
    ("RAGE | Chris",   "<@868570220212633229>"),
    ("RAGE | Sam",   "<@661713965687203229>"),
    ("RAGE | Max",   "<@836394225258329500>"),
    ("RAGE | Riley",   "<@167403959807652614>"),
    ("RAGE | Morgan",   "<@498251982661757503>"),
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
    ("RAGE | Emery",   "<@061403237378200593>"),
    ("RAGE | Zion",   "<@676791011652671671>"),
    ("RAGE | Kai",   "<@891036937066178619>"),
    ("RAGE | Ash",   "<@734353881968747928>"),
    ("RAGE | Storm",   "<@544728808246308127>"),
    ("RAGE | Blaze",   "<@387209074766470263>"),
    ("RAGE | Cruz",   "<@545473722111571247>"),
    ("RAGE | Dani",   "<@952112105295618485>"),
    ("RAGE | Eden",   "<@441094840601539176>"),
    ("RAGE | Flynn",   "<@725448936679226110>"),
    ("RAGE | Gray",   "<@045227746976694569>"),
    ("RAGE | Haven",   "<@801375216695400432>"),
    ("RAGE | Indigo",   "<@098599620746915640>"),
    ("RAGE | Jett",   "<@336836298543394596>"),
    ("RAGE | Knox",   "<@541376725946196215>"),
    ("RAGE | Lane",   "<@509941847528925395>"),
    ("RAGE | Milo",   "<@882749582259415355>"),
    ("RAGE | Nash",   "<@431652707783689405>"),
    ("RAGE | Onyx",   "<@588454746149366888>"),
    ("RAGE | Pace",   "<@337780069974068469>"),
    ("RAGE | Reed",   "<@072315571086291422>"),
    ("BLADE | Tyler",   "<@089614356428134255>"),
    ("BLADE | Jordan",   "<@929625670649276366>"),
    ("BLADE | Chris",   "<@676869634570271159>"),
    ("BLADE | Sam",   "<@598284873191987998>"),
    ("BLADE | Max",   "<@370546658912085920>"),
    ("BLADE | Riley",   "<@893419340814679471>"),
    ("BLADE | Morgan",   "<@404490349806593311>"),
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
    ("BLADE | Finley",   "<@492430052930986712>"),
    ("BLADE | Emery",   "<@861740028575123047>"),
    ("BLADE | Zion",   "<@419505214624609055>"),
    ("BLADE | Kai",   "<@953469207376773058>"),
    ("BLADE | Ash",   "<@174668074201095952>"),
    ("BLADE | Storm",   "<@713783138783944958>"),
    ("BLADE | Blaze",   "<@706853063646308392>"),
    ("BLADE | Cruz",   "<@990638691670073356>"),
    ("BLADE | Dani",   "<@693755362174352249>"),
    ("BLADE | Eden",   "<@294184840683305887>"),
    ("BLADE | Flynn",   "<@967512170538560397>"),
    ("BLADE | Gray",   "<@578096463876194901>"),
    ("BLADE | Haven",   "<@113739882651355191>"),
    ("BLADE | Indigo",   "<@676858006567464629>"),
    ("BLADE | Jett",   "<@486200442637789135>"),
    ("BLADE | Knox",   "<@342202362813537454>"),
    ("BLADE | Lane",   "<@309592304864584877>"),
    ("BLADE | Milo",   "<@345150572961937397>"),
    ("BLADE | Nash",   "<@155013446536197238>"),
    ("BLADE | Onyx",   "<@572836957760497757>"),
    ("BLADE | Pace",   "<@516681609103164798>"),
    ("BLADE | Reed",   "<@701236531933776661>"),
    ("KING | Tyler",   "<@252922273397216398>"),
    ("KING | Alex",   "<@982273424259616526>"),
]


# ── Save/load channel ID so it survives restarts ─────────────────────────────
def save_config(channel_id: int):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"channel_id": channel_id}, f)

def load_config() -> int | None:
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
    save_config(target_channel.id)   # Save to file so it survives restarts
    embed = discord.Embed(
        description=f"✅ Transaction channel set to {target_channel.mention}!\nAll auto transactions will be sent there.",
        color=0x57F287
    )
    await ctx.send(embed=embed)
    print(f"[BOT] Channel set to: #{target_channel.name} (ID: {target_channel.id})")


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
    global target_channel
    await bot.wait_until_ready()

    # Load saved channel from file on startup
    channel_id = load_config()
    if channel_id:
        target_channel = bot.get_channel(channel_id)
        if target_channel:
            print(f"[BOT] Restored channel: #{target_channel.name}")
        else:
            print(f"[BOT] Could not restore channel ID {channel_id}")

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
    bot.loop.create_task(transaction_loop())


keep_alive()
bot.run(BOT_TOKEN)
