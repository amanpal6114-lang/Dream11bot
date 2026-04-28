from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import random

TOKEN = "8764479094:AAEDODY1l2shXrDbA6BYzI9tFy93hAL_rOI"

players = [
    "Rohit", "Kohli", "Hardik", "Bumrah",
    "Surya", "Rinku", "Gill", "Jadeja",
    "Siraj", "Rahul", "Pant"
]

def generate_team():
    team = random.sample(players, 11)
    captain = random.choice(team)
    vice = random.choice([p for p in team if p != captain])

    text = "🏏 TEAM:\n\n"
    for p in team:
        text += f"- {p}\n"

    text += f"\n👑 C: {captain}\n⚡ VC: {vice}"
    return text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot Live! Use /team")

async def team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = generate_team()
    await update.message.reply_text(t)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("team", team))
print("Bot successfully started...")
app.run_polling()