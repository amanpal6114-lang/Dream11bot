from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random

TOKEN = "PASTE_YOUR_TOKEN_HERE"

players = []

# ---------- BUTTON MENU ----------
def get_menu():
    keyboard = [
        ["Team", "10 Teams"],
        ["Set Players"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot Live!\nUse button below 👇",
        reply_markup=get_menu()
    )

# ---------- SET PLAYERS ----------
async def setplayers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players
    try:
        data = update.message.text.replace("/setplayers ", "")
        players = []

        for p in data.split(","):
            name, ptype = p.strip().split(":")
            players.append({"name": name, "type": ptype})

        await update.message.reply_text("✅ Players Set!", reply_markup=get_menu())

    except:
        await update.message.reply_text("❌ Use:\n/setplayers name:type,name:type")

# ---------- GENERATE TEAM ----------
def generate_team():
    if len(players) < 11:
        return "❌ Set players first"

    team = random.sample(players, 11)
    c = random.choice(team)
    vc = random.choice([p for p in team if p != c])

    text = "🏏 TEAM\n\n"
    for p in team:
        text += f"- {p['name']}\n"

    text += f"\n👑 C: {c['name']}\n⚡ VC: {vc['name']}"
    return text

# ---------- MULTIPLE TEAMS ----------
def generate_multiple():
    if len(players) < 11:
        return "❌ Set players first"

    text = ""
    for i in range(1, 11):
        team = random.sample(players, 11)
        c = random.choice(team)
        vc = random.choice([p for p in team if p != c])

        text += f"\n🔥 TEAM {i}\n"
        for p in team:
            text += f"- {p['name']}\n"

        text += f"👑 C: {c['name']} | ⚡ VC: {vc['name']}\n"

    return text

# ---------- COMMAND ----------
async def team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(generate_team(), reply_markup=get_menu())

async def teams(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(generate_multiple(), reply_markup=get_menu())

# ---------- BUTTON HANDLER ----------
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Team":
        await update.message.reply_text(generate_team(), reply_markup=get_menu())

    elif text == "10 Teams":
        await update.message.reply_text(generate_multiple(), reply_markup=get_menu())

    elif text == "Set Players":
        await update.message.reply_text("Send:\n/setplayers name:type,name:type")

# ---------- MAIN ----------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setplayers", setplayers))
app.add_handler(CommandHandler("team", team))
app.add_handler(CommandHandler("teams", teams))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

print("Bot running...")
app.run_polling()
