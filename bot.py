from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random
TOKEN = "8764479094:AAEDODY1l2shXrDbA6BYzI9tFy93hAL_rOI"
ADMIN_ID = 6670244148

players = []

# ================= MENUS =================
def main_menu():
    return ReplyKeyboardMarkup(
        [["🏏 Team", "💰 Buy"], ["⚙ Set Players"]],
        resize_keyboard=True
    )

def team_menu():
    return ReplyKeyboardMarkup([
        ["🔥 Batting", "🎯 Bowling"],
        ["⚖ Balanced", "⚡ Impact"],
        ["💀 Risky", "🏆 GL"],
        ["🔙 Back"]
    ], resize_keyboard=True)

# ================= DISCLAIMER =================
DISCLAIMER = """
🤖 AI Fantasy Team Bot

⚠️ Disclaimer:
This bot uses AI-based analysis like pitch report, venue data, player form, and historical performance to generate fantasy combinations.

👉 It does NOT guarantee any win or rank.
👉 It is for educational & analytical purpose only.
👉 Users must play responsibly on any fantasy platform.

💡 How to use:
- Add players list
- Select team type
- Get AI-generated combinations in seconds

🏏 Types:
Batting | Bowling | Balanced | Impact | Risky | GL

💰 Premium: 16 teams = ₹49 | 4-5 teams = ₹25
"""

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(DISCLAIMER)
    msg = await update.message.reply_text("👇 Main Menu", reply_markup=main_menu())

    # PIN MESSAGE (Telegram feature)
    try:
        await msg.pin()
    except:
        pass

# ================= SET PLAYERS =================
async def setplayers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players
    try:
        data = update.message.text.replace("/setplayers ", "")
        players = []

        for p in data.split(","):
            name, role = p.strip().split(":")
            players.append({"name": name, "role": role})

        await update.message.reply_text("✅ Players Set", reply_markup=main_menu())

    except:
        await update.message.reply_text("❌ Format:\n/setplayers name:type,name:type")

# ================= TEAM ENGINE =================
def make_team():
    team = random.sample(players, 11)
    c = random.choice(team)
    vc = random.choice([p for p in team if p != c])

    text = "🏏 TEAM\n\n"
    for p in team:
        text += f"- {p['name']}\n"

    text += f"\n👑 C: {c['name']}\n⚡ VC: {vc['name']}"
    return text

# ================= BUTTON HANDLER =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # MAIN
    if text == "🏏 Team":
        await update.message.reply_text("Select Type 👇", reply_markup=team_menu())

    elif text == "🔙 Back":
        await update.message.reply_text("Main Menu", reply_markup=main_menu())

    elif text == "⚙ Set Players":
        await update.message.reply_text("Use:\n/setplayers name:type,name:type")
elif text == "📄 Disclaimer":
    await update.message.reply_text(
        "⚠️ DISCLAIMER\n\n"
        "Ye bot AI sports insights, analysis aur data-driven suggestions provide karta hai jisse aap apne decisions ko better bana sako.\n\n"
        "Ye bot pitch report, venue, player form, aur previous data se team suggest krta hai, logical reasioning se risky team banata hai.\n\n"
        "Kisi bhi tarah ki guaranteed winning ya fixed result ka claim nahi kiya jata. Users ko apni samajh aur judgment use karke decision lena chahiye.\n\n"
        "Humara focus aapki selection strategy ko improve karna aur structured analysis ke through better performance ke chances ko enhance karna hai.\n\n"
        "Ye bot kisi bhi fantasy app ko promote nhi karta hai."
    )
    elif text == "💰 Buy":
        await update.message.reply_text(
            "💰 Premium:\n₹49 = 16 Teams\n₹25 = 4-5 Teams\n\nUPI: aman7800@airtel"
        )

    # TEAM TYPES
    elif text in ["🔥 Batting", "🎯 Bowling", "⚖ Balanced", "⚡ Impact", "💀 Risky", "🏆 GL"]:
        if len(players) < 11:
            await update.message.reply_text("❌ Set players first")
            return

        await update.message.reply_text(make_team(), reply_markup=team_menu())

# ================= MAIN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setplayers", setplayers))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot Running...")
app.run_polling()
