from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random

# ================= SECURITY CONFIG =================
TOKEN = "8764479094:AAEDODY1l2shXrDbA6BYzI9tFy93hAL_rOI"
ADMIN_ID = 6670244148  

# paid users storage (simple secure runtime memory)
paid_users = {}

# ================= PLAYERS =================
players = []

# ================= MENUS =================
def main_menu():
    return ReplyKeyboardMarkup(
        [["🏏 Team", "💎 Buy Access"], ["⚙ Set Players"]],
        resize_keyboard=True
    )

def premium_menu():
    return ReplyKeyboardMarkup(
        [["🔥 Batting", "🎯 Bowling"],
         ["⚖ Balanced", "⚡ Impact"],
         ["💀 Risky", "🏆 GL"],
         ["🔙 Back"]],
        resize_keyboard=True
    )

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Bot Live\n\nFree + Paid system ready",
        reply_markup=main_menu()
    )

# ================= SET PLAYERS =================
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

# ================= SECURITY CHECK =================
def is_paid(user_id):
    return paid_users.get(user_id, False)

# ================= TEAM ENGINE =================
def build_team():
    team = random.sample(players, 11)
    c = random.choice(team)
    vc = random.choice([p for p in team if p != c])

    text = "🏏 TEAM\n\n"
    for p in team:
        text += f"- {p['name']}\n"

    text += f"\n👑 C: {c['name']}\n⚡ VC: {vc['name']}"
    return text

# ================= PREMIUM ENGINE =================
def premium_teams():
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

# ================= COMMAND HANDLERS =================
async def team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(build_team(), reply_markup=main_menu())

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "💰 PREMIUM ACCESS\n\n"
        "₹49 = 20 GL Teams\n\n"
        "Pay to UPI:\n"
        "yourupi@upi\n\n"
        "Payment ke baad screenshot send karo admin ko"
    )
    await update.message.reply_text(msg)

# ================= ADMIN APPROVAL =================
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(context.args[0])
        paid_users[user_id] = True

        await update.message.reply_text(f"✅ User {user_id} Approved")
    except:
        await update.message.reply_text("Usage: /approve user_id")

# ================= BUTTON HANDLER =================
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    # MAIN MENU
    if text == "🏏 Team":
        await update.message.reply_text(build_team(), reply_markup=main_menu())

    elif text == "💎 Buy Access":
        await update.message.reply_text(
            "💰 Pay ₹49 UPI\nSend screenshot to admin",
            reply_markup=main_menu()
        )

    elif text == "⚙ Set Players":
        await update.message.reply_text("Use:\n/setplayers name:type,name:type")

    # PREMIUM MENU (LOCKED)
    elif text in ["🔥 Batting","🎯 Bowling","⚖ Balanced","⚡ Impact","💀 Risky","🏆 GL"]:

        if not is_paid(user_id):
            await update.message.reply_text(
                "🔒 Locked Feature\n💰 Buy Access first",
                reply_markup=main_menu()
            )
            return

        if text == "🏆 GL":
            await update.message.reply_text(premium_teams(), reply_markup=premium_menu())
        else:
            await update.message.reply_text(build_team(), reply_markup=premium_menu())

    elif text == "🔙 Back":
        await update.message.reply_text("Main Menu", reply_markup=main_menu())

# ================= MAIN =================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setplayers", setplayers))
app.add_handler(CommandHandler("team", team))
app.add_handler(CommandHandler("buy", buy))
app.add_handler(CommandHandler("approve", approve))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot Running Securely...")
app.run_polling()
