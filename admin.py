import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

USERS_FILE = "users.json"

# Foydalanuvchilar ro‘yxatini yuklash
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Admin panel (faqat ommaviy xabar yuborish)
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📬 Ommaviy xabar yuborish", callback_data="broadcast")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("✉️ Ommaviy xabar yuborish paneli:", reply_markup=reply_markup)
    else:
        await update.callback_query.edit_message_text("✉️ Ommaviy xabar yuborish paneli:", reply_markup=reply_markup)

# Ommaviy xabar yuborishni boshlash
async def broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text("✍️ Yubormoqchi bo‘lgan xabaringizni kiriting:")
    context.user_data["awaiting_broadcast"] = True

# Ommaviy xabarni yuborish
async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_broadcast"):
        users = load_users()
        msg = update.message.text
        success = 0
        for user_id in users.keys():
            try:
                await context.bot.send_message(chat_id=int(user_id), text=msg)
                success += 1
            except:
                continue
        await update.message.reply_text(f"✅ {success} ta foydalanuvchiga yuborildi.")
        context.user_data["awaiting_broadcast"] = False
