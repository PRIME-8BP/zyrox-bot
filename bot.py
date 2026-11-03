import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ---------------- CONFIGURATION ----------------
TOKEN = "8946984052:AAGdyU4rOVKnsFVRqx1Ub8FPDmMnPBNIE"
ADMIN_CHAT_ID = "8986662222"  # Your Telegram ID

# Templates Catalog Data
TEMPLATES = {
    "tpl_1": {
        "name": "🔥 Premium Store Landing Page",
        "price_usd": "15",
        "price_pkr": "4200",
        "price_inr": "1250",
        "price_bdt": "1800",
        "desc": "High-speed, modern responsive HTML/CSS/JS template with dark theme and animations.",
        "demo": "https://example.com/demo1",
    },
    "tpl_2": {
        "name": "🤖 Telegram Auto-Shop Bot Code",
        "price_usd": "25",
        "price_pkr": "7000",
        "price_inr": "2100",
        "price_bdt": "3000",
        "desc": "Full Python backend code for an automated Telegram shop bot with inline menu systems.",
        "demo": "https://example.com/demo2",
    },
    "tpl_3": {
        "name": "⚡️ Agency & Portfolio Web Suite",
        "price_usd": "20",
        "price_pkr": "5600",
        "price_inr": "1650",
        "price_bdt": "2400",
        "desc": "Sleek agency template to showcase web development services & capture client leads.",
        "demo": "https://example.com/demo3",
    },
}

# Payment Details
PAYMENT_INFO = """
💳 **Select your preferred payment method:**

🇵🇰 **Pakistan:**
▫️ **EasyPaisa:** `03473441249` (Title: Aziza bano)

🇮🇳 **India (UPI / GPay / FamPay):**
▫️ **UPI ID:** `paytm.s3h85g1@pty`
*(Name: Biswajit Choudhury)*[span_0](start_span)[span_0](end_span)

🇧🇩 **Bangladesh:**
▫️ **bKash / Nagad:** `01854576246`

🌐 **International:**
▫️ **Binance Pay ID:** `1269457012`[span_1](start_span)[span_1](end_span)

---
⚠️ **After sending payment, reply to this message with your Payment Screenshot or Transaction ID (TxID).**
"""

# ---------------- HANDLERS ----------------

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "⚡️ **Welcome to ZYROX STORE Template Bot!** 🚀\n\n"
        "Browse high-quality, pre-built website templates and bot source codes. "
        "Get 100% full source code ownership instantly after purchase.\n\n"
        "👇 Tap **Explore Templates** to view the catalog!"
    )
    
    keyboard = [
        [InlineKeyboardButton("📦 Explore Templates", callback_data="catalog")],
        [InlineKeyboardButton("💳 Payment Methods", callback_data="payment_methods")],
        [InlineKeyboardButton("❓ Need Help / Support", url="https://t.me/ZYROX")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# Catalog View
async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = "📁 **ZYROX STORE Catalog**\n\nChoose a template below to view details and pricing:"
    
    keyboard = []
    for key, item in TEMPLATES.items():
        keyboard.append([InlineKeyboardButton(f"{item['name']} - ${item['price_usd']}", callback_data=f"view_{key}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# Detail View for Specific Template
async def view_template(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    tpl_id = query.data.replace("view_", "")
    tpl = TEMPLATES.get(tpl_id)
    
    if not tpl:
        await query.edit_message_text("Template not found.")
        return

    text = (
        f"✨ **{tpl['name']}**\n\n"
        f"📝 **Description:** {tpl['desc']}\n\n"
        f"💰 **Pricing:**\n"
        f"▫️ **USD:** ${tpl['price_usd']} (Binance USDT)\n"
        f"▫️ **PKR:** Rs. {tpl['price_pkr']} (EasyPaisa)\n"
        f"▫️ **INR:** ₹{tpl['price_inr']} (UPI / GPay / FamPay)\n"
        f"▫️ **BDT:** ৳{tpl['price_bdt']} (bKash / Nagad)\n\n"
        f"🔗 [Click Here to View Live Demo]({tpl['demo']})"
    )
    
    keyboard = [
        [InlineKeyboardButton("💳 Buy This Source Code", callback_data=f"buy_{tpl_id}")],
        [InlineKeyboardButton("🔙 Back to Catalog", callback_data="catalog")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown", disable_web_page_preview=True)

# Buy Screen with Instructions
async def buy_template(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    tpl_id = query.data.replace("buy_", "")
    tpl = TEMPLATES.get(tpl_id)
    
    context.user_data["pending_order"] = tpl['name']
    
    text = (
        f"🛍 **Order Initiation: {tpl['name']}**\n\n"
        f"Price: **${tpl['price_usd']} USD** | **Rs. {tpl['price_pkr']} PKR** | **₹{tpl['price_inr']} INR** | **৳{tpl['price_bdt']} BDT**\n\n"
        f"{PAYMENT_INFO}"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Cancel / Back", callback_data="catalog")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

# Payment Methods Info Button
async def payment_methods_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(PAYMENT_INFO, reply_markup=reply_markup, parse_mode="Markdown")

# Forward Payment Proofs to Admin
async def handle_payment_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    pending_item = context.user_data.get("pending_order", "General Inquiry / Proof")
    
    admin_notification = (
        f"🚨 **NEW PAYMENT PROOF RECEIVED!** 🚨\n\n"
        f"👤 **User:** {user.full_name} (@{user.username or 'No Username'})\n"
        f"🆔 **User ID:** `{user.id}`\n"
        f"📦 **Selected Item:** {pending_item}\n"
    )

    # Forward Photo or Text Proof to Admin
    if update.message.photo:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_notification, parse_mode="Markdown")
        await context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=update.message.photo[-1].file_id, caption="📸 Payment Receipt")
    elif update.message.text:
        admin_notification += f"💬 **TxID / Message:** {update.message.text}"
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_notification, parse_mode="Markdown")

    await update.message.reply_text(
        "✅ **Thank you! Your payment proof has been submitted.**\n\n"
        "Our team is verifying your payment. Once confirmed, your source code file link will be sent to you here shortly!",
        parse_mode="Markdown"
    )

# Callback Router
async def button_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data == "main_menu":
        await start(update, context)
    elif data == "catalog":
        await show_catalog(update, context)
    elif data == "payment_methods":
        await payment_methods_info(update, context)
    elif data.startswith("view_"):
        await view_template(update, context)
    elif data.startswith("buy_"):
        await buy_template(update, context)

# Main Application Entry Point
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_router))
    app.add_handler(MessageHandler(filters.PHOTO | filters.TEXT & ~filters.COMMAND, handle_payment_proof))

    print("⚡️ ZYROX STORE Bot is live and running...")
    app.run_polling()

if __name__ == "__main__":
    main()
      
