from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random

TOKEN = "8764479094:AAEDODY1l2shXrDbA6BYzI9tFy93hAL_rOI"
ADMIN_ID = 6670244148
players = []

# ---------------- MENUS ----------------
def main_menu():
    return ReplyKeyboardMarkup(
        [["🏏 Team", "💎 Buy Access"],
         ["⚙ Set Players", "📄 Disclaimer"]],
        resize_keyboard=True
    )

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚠️ Welcome!\n\nTap Accept & Start using bot",
        reply_markup=main_menu()
    )

# ---------------- SET PLAYERS ----------------
async def setplayers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players
    try:
        data = update.message.text.replace("/setplayers ", "")
        players = []

        for p in data.split(","):
            name, ptype = p.strip().split(":")
            players.append({"name": name, "type": ptype})

        await update.message.reply_text("✅ Players Updated", reply_markup=main_menu())

    except:
        await update.message.reply_text("❌ Format:\n/setplayers name:type,name:type")

# ---------------- TEAM GENERATOR ----------------
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

# ---------------- HANDLER ----------------
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # TEAM
    if text == "🏏 Team":
        await update.message.reply_text(generate_team(), reply_markup=main_menu())

    # BUY
    elif text == "💎 Buy Access":
        await update.message.reply_text(
            "💰 Premium Access ₹49\nUPI: aman7800@airtel\nSend screenshot to admin",
            reply_markup=main_menu()
        )

    # DISCLAIMER
    elif text == "📄 Disclaimer":
        await update.message.reply_text(
            "⚠️ DISCLAIMER\n\n"
             "Ye bot AI sports insights, analysis aur data-driven suggestions provide karta hai jisse aap apne decisions ko better bana sako.\n\n"
        "Ye bot pitch report, venue, player form, aur previous data se team suggest krta hai, logical reasioning se risky team banata hai.\n\n"
        "Kisi bhi tarah ki guaranteed winning ya fixed result ka claim nahi kiya jata. Users ko apni samajh aur judgment use karke decision lena chahiye.\n\n"
        "Humara focus aapki selection strategy ko improve karna aur structured analysis ke through better performance ke chances ko enhance karna hai.\n\n"
        "Ye bot kisi bhi fantasy app ko promote nhi karta hai.",
            reply_markup=main_menu()
        )

    # SET PLAYERS HELP
    elif text == "⚙ Set Players":
        await update.message.reply_text(
            "Use format:\n/setplayers name:type,name:type\n\n"
            "Example:\n/setplayers Jaiswal:bat,Samson:wk,Archer:bowl"
        )

# ---------------- MAIN ----------------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setplayers", setplayers))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot Running...")
app.run_polling()
