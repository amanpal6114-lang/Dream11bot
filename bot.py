from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import os

TOKEN = os.getenv("TOKEN")

players = []

# ---------------- SET PLAYERS ----------------

async def setplayers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players
    try:
        data = update.message.text.replace("/setplayers ", "")
        players = []

        for p in data.split(","):
            name, ptype = p.strip().split(":")
            players.append({"name": name.strip(), "type": ptype.strip()})

        await update.message.reply_text("✅ Players updated!")

    except:
        await update.message.reply_text("❌ Format error!\nUse:\n/setplayers name:type,name:type")

# ---------------- FORMAT ----------------

def format_team(team, label, c=None, vc=None):
    text = f"🔥 {label} TEAM\n\n"
    for p in team:
        text += f"- {p['name']}\n"

    if c:
        text += f"\n👑 C: {c['name']}\n⚡ VC: {vc['name']}"

    return text

# ---------------- BASIC TEAM ----------------

def random_team():
    if len(players) < 11:
        return None, None, None

    team = random.sample(players, 11)
    c = random.choice(team)
    vc = random.choice([p for p in team if p != c])
    return team, c, vc

# ---------------- MULTIPLE ----------------

def generate_multiple(n):
    if len(players) < 11:
        return "❌ Set players first"

    text = ""
    for i in range(1, n+1):
        team, c, vc = random_team()
        text += f"\n🔥 TEAM {i}\n"
        for p in team:
            text += f"- {p['name']}\n"
        text += f"👑 C: {c['name']}\n⚡ VC: {vc['name']}\n"

    return text

# ---------------- STRATEGY ----------------

def batting_team():
    bats = [p for p in players if p["type"] == "bat"]
    if len(bats) < 6:
        return None
    return random.sample(bats, 6) + random.sample(players, 5)

def bowling_team():
    bowls = [p for p in players if p["type"] == "bowl"]
    if len(bowls) < 6:
        return None
    return random.sample(bowls, 6) + random.sample(players, 5)

def balanced_team():
    if len(players) < 11:
        return None
    return random.sample(players, 11)

def impact_team():
    impact = [p for p in players if p["type"] in ["ar", "bowl"]]
    if len(impact) < 5:
        return None
    return random.sample(impact, 5) + random.sample(players, 6)

# ---------------- COMMANDS ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot Live! Use /setplayers first")

async def team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t, c, vc = random_team()
    if not t:
        await update.message.reply_text("❌ Set players first")
        return
    await update.message.reply_text(format_team(t, "Single", c, vc))

async def teams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(generate_multiple(10))

async def gl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(generate_multiple(40))

async def batting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = batting_team()
    if not t:
        await update.message.reply_text("❌ Not enough batsmen")
        return
    await update.message.reply_text(format_team(t, "Batting"))

async def bowling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = bowling_team()
    if not t:
        await update.message.reply_text("❌ Not enough bowlers")
        return
    await update.message.reply_text(format_team(t, "Bowling"))

async def balanced(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = balanced_team()
    if not t:
        await update.message.reply_text("❌ Set players first")
        return
    await update.message.reply_text(format_team(t, "Balanced"))

async def impact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = impact_team()
    if not t:
        await update.message.reply_text("❌ Not enough impact players")
        return
    await update.message.reply_text(format_team(t, "Impact"))

# ---------------- MAIN ----------------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setplayers", setplayers))
app.add_handler(CommandHandler("team", team))
app.add_handler(CommandHandler("teams", teams))
app.add_handler(CommandHandler("gl", gl))
app.add_handler(CommandHandler("batting", batting))
app.add_handler(CommandHandler("bowling", bowling))
app.add_handler(CommandHandler("balanced", balanced))
app.add_handler(CommandHandler("impact", impact))

print("Bot running...")
app.run_polling()
