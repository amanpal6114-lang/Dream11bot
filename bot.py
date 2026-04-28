from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

TOKEN = "8764479094:AAEDODY1l2shXrDbA6BYzI9tFy93hAL_rOI"

players = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot Live! Use /setplayers")

async def setplayers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players
    try:
        data = update.message.text.replace("/setplayers ", "")
        players = []

        for p in data.split(","):
            name, ptype = p.strip().split(":")
            players.append({"name": name, "type": ptype})

        await update.message.reply_text("✅ Players set!")

    except:
        await update.message.reply_text("❌ Format:\n/setplayers name:type,...")

def random_team():
    def generate_multiple(n):
    if len(players) < 11:
        return "❌ Set players first"

    text = ""
    for i in range(1, n+1):
        team = random.sample(players, 11)
        c = random.choice(team)
        vc = random.choice([p for p in team if p != c])

        text += f"\n🔥 TEAM {i}\n"
        for p in team:
            text += f"- {p['name']}\n"

        text += f"👑 C: {c['name']}\n⚡ VC: {vc['name']}\n"
async def teams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(generate_multiple(10))
    return text
    if len(players) < 11:
        return None, None, None

    team = random.sample(players, 11)
    c = random.choice(team)
    vc = random.choice([p for p in team if p != c])
    return team, c, vc

def format_team(team, c, vc):
    text = "🏏 TEAM\n\n"
    for p in team:
        text += f"- {p['name']}\n"
    text += f"\n👑 C: {c['name']}\n⚡ VC: {vc['name']}"
    return text

async def team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t, c, vc = random_team()
    if not t:
        await update.message.reply_text("❌ Set players first")
        return
    await update.message.reply_text(format_team(t, c, vc))

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setplayers", setplayers))
app.add_handler(CommandHandler("team", team))

print("Bot running...")
app.run_polling()
