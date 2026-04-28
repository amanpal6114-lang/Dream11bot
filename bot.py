from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random
import os

TOKEN = os.getenv("TOKEN")

players = []

# ------------------ PLAYER SET ------------------

async def setplayers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players
    try:
        data = update.message.text.replace("/setplayers ", "")
        players = []

        for p in data.split(","):
            name, ptype = p.strip().split(":")
            players.append({"name": name.strip(), "type": ptype.strip()})

        await update.message.reply_text("✅ Players updated successfully!")

    except:
        await update.message.reply_text(
            "❌ Format error!\nUse:\n/setplayers name:type,name:type\nExample:\n/setplayers Jaiswal:bat,Stoinis:ar,Archer:bowl"
        )

# ------------------ TEAM FORMAT ------------------

def format_team(team, label, c=None, vc=None):
    text = f"🔥 {label} TEAM\n\n"

    for p in team:
        text += f"- {p['name']}\n"

    if c:
        text += f"\n👑 C: {c['name']}\n⚡ VC: {vc['name']}"

    return text

# ------------------ BASE GENERATION ------------------

def random_team():
    if len(players) < 11:
        return None

    team = random.sample(players, 11)
    c = random.choice(team)
    vc = random.choice([p for p in team if p != c])
    return team, c, vc

# ------------------ MULTI TEAM ------------------

def generate_multiple(n):
    if len(players) < 11:
        return "❌ Set players first using /setplayers"

    output = "🏏 MATCH TEAMS\n"

    for i in range(1, n+1):
        team, c, vc = random_team()
        output += f"\n🔥 TEAM {i}\n"

        for p in team:
            output += f"- {p['name']}\n"

        output += f"👑 C: {c['name']}\n⚡ VC: {vc['name']}\n"

    return output

# ------------------ STRATEGIES ------------------

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
    return random.sample(players, 11)

def impact_team():
    impact = [p for p in players if p["type"] in ["ar", "bowl"]]
    if len(impact) < 5:
        return None
    return random.sample(impact, 5) + random.sample(players, 6)

def risky_team():
    return random_team()

# ------------------ COMMANDS ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot Live!\n\nCommands:\n"
        "/setplayers name:type,...\n"
        "/team\n/teams\n/gl\n"
        "/batting\n/bowling\n/balanced\n/impact\n/risky"
    )

async def team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(players) < 11:
        await update.message.reply_text("❌ Set players first")
        return

    t, c, vc = random_team()
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
    await update.message.reply_text(format_team(t, "Batting Heavy"))

async def bowling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = bowling_team()
    if not t:
        await update.message.reply_text("❌ Not enough bowlers")
        return
    await update.message.reply_text(format_team(t, "Bowling Heavy"))

async def balanced(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = balanced_team()
    await update.message.reply_text(format_team(t, "Balanced"))

async def impact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = impact_team()
    if not t:
        await update.message.reply_text("❌ Not enough impact players")
        return
    await update.message.reply_text(format_team(t, "Impact"))

async def risky(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t, c, vc = risky_team()
    await update.message.reply_text(format_team(t, "Risky", c, vc))

# ------------------ MAIN ------------------

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
app.add_handler(CommandHandler("risky", risky))

print("✅ Bot running...")
app.run_polling()