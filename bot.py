from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random

TOKEN = "8764479094:AAEDODY1l2shXrDbA6BYzI9tFy93hAL_rOI"

players = []

# ---------- MENUS ----------
def main_menu():
    return ReplyKeyboardMarkup([["Team", "Set Players"]], resize_keyboard=True)

def team_menu():
    return ReplyKeyboardMarkup([
        ["Batting", "Bowling"],
        ["Balanced", "Impact"],
        ["Risky", "GL"],
        ["Back"]
    ], resize_keyboard=True)

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot Live!", reply_markup=main_menu())

# ---------- SET PLAYERS ----------
async def setplayers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players
    try:
        data = update.message.text.replace("/setplayers ", "")
        players = []

        for p in data.split(","):
            name, ptype = p.strip().split(":")
            players.append({"name": name, "type": ptype})

        await update.message.reply_text("✅ Players Set!", reply_markup=main_menu())

    except:
        await update.message.reply_text("❌ Format:\n/setplayers name:type,name:type")

# ---------- TEAM GENERATORS ----------

def pick_team(base_players):
    team = random.sample(base_players, 11)
    c = random.choice(team)
    vc = random.choice([p for p in team if p != c])

    text = "🏏 TEAM\n\n"
    for p in team:
        text += f"- {p['name']}\n"

    text += f"\n👑 C: {c['name']}\n⚡ VC: {vc['name']}"
    return text

def batting_team():
    bats = [p for p in players if p["type"] == "bat"]
    if len(bats) < 6:
        return "❌ Not enough batsmen"
    return pick_team(bats + players)

def bowling_team():
    bowls = [p for p in players if p["type"] == "bowl"]
    if len(bowls) < 6:
        return "❌ Not enough bowlers"
    return pick_team(bowls + players)

def balanced_team():
    if len(players) < 11:
        return "❌ Set players first"
    return pick_team(players)

def impact_team():
    impact = [p for p in players if p["type"] in ["ar", "bowl"]]
    if len(impact) < 5:
        return "❌ Not enough impact players"
    return pick_team(impact + players)

def risky_team():
    if len(players) < 11:
        return "❌ Set players first"
    return pick_team(players)

def gl_teams():
    if len(players) < 11:
        return "❌ Set players first"

    text = ""
    for i in range(1, 21):
        team = random.sample(players, 11)
        c = random.choice(team)
        vc = random.choice([p for p in team if p != c])

        text += f"\n🔥 TEAM {i}\n"
        for p in team:
            text += f"- {p['name']}\n"
        text += f"👑 {c['name']} | ⚡ {vc['name']}\n"

    return text

# ---------- BUTTON HANDLER ----------
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Team":
        await update.message.reply_text("Select Type 👇", reply_markup=team_menu())

    elif text == "Back":
        await update.message.reply_text("Main Menu", reply_markup=main_menu())

    elif text == "Batting":
        await update.message.reply_text(batting_team(), reply_markup=team_menu())

    elif text == "Bowling":
        await update.message.reply_text(bowling_team(), reply_markup=team_menu())

    elif text == "Balanced":
        await update.message.reply_text(balanced_team(), reply_markup=team_menu())

    elif text == "Impact":
        await update.message.reply_text(impact_team(), reply_markup=team_menu())

    elif text == "Risky":
        await update.message.reply_text(risky_team(), reply_markup=team_menu())

    elif text == "GL":
        await update.message.reply_text(gl_teams(), reply_markup=team_menu())

    elif text == "Set Players":
        await update.message.reply_text("Send:\n/setplayers name:type,name:type")

# ---------- MAIN ----------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setplayers", setplayers))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot running...")
app.run_polling()
