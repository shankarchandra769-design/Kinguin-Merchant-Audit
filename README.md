# 💸 Transaction Bot

A Discord bot that auto-sends fake transaction embeds at random intervals (every 5–30 minutes), styled like a real marketplace receipt.

---

## 📁 File Structure

```
transaction_bot.py   ← Main bot file
requirements.txt     ← Python dependencies
.env                 ← Your secret bot token (never share/commit this)
.gitignore           ← Keeps .env and other files out of Git
README.md            ← This file
```

---

## ⚙️ Local Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your bot token
Edit the `.env` file:
```
BOT_TOKEN=your_discord_bot_token_here
```

### 3. Run the bot
```bash
python transaction_bot.py
```

---

## 🚀 Deploy on Render

1. Push your project to a **GitHub repo** (make sure `.env` is in `.gitignore`)
2. Go to [render.com](https://render.com) → **New → Background Worker**
3. Connect your GitHub repo
4. Set these fields:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python transaction_bot.py`
5. Go to **Environment** tab → Add variable:
   - Key: `BOT_TOKEN`
   - Value: your actual Discord bot token
6. Click **Deploy** ✅

> ⚠️ Never put your real token in `.env` before pushing to GitHub. Always use Render's Environment Variables panel.

---

## 🤖 Bot Commands

| Command | Description |
|---|---|
| `,setchannel [#channel]` | Set which channel transactions are sent to. Uses current channel if none mentioned. |
| `,setimage` + attach file | Attach a PNG/JPG to set the embed thumbnail. Saved locally, never expires. |
| `,sendnow` | Manually trigger a transaction embed instantly. |
| `,help` | Show all commands in Discord. |

---

## 📋 Notes

- The bot won't auto-send until you run `,setchannel`
- Images set with `,setimage` are saved as `stored.png` locally on the server
- On Render free tier, the bot may restart occasionally — use `,setimage` again after a restart if the image is lost
