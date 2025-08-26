import base64
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# States for conversation
WAITING_FOR_TEXT = "waiting_for_text"
WAITING_FOR_BASE64 = "waiting_for_base64"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Encode to Base64", callback_data="encode")],
        [InlineKeyboardButton("Decode from Base64", callback_data="decode")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome to Base64 Encoder/Decoder Bot!\nChoose an option:",
        reply_markup=reply_markup,
    )
    context.user_data.clear()

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "encode":
        context.user_data["mode"] = "encode"
        await query.edit_message_text("Send me the text you want to encode to Base64:")
    elif data == "decode":
        context.user_data["mode"] = "decode"
        await query.edit_message_text("Send me the Base64 string you want to decode:")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mode = context.user_data.get("mode")
    if not mode:
        await update.message.reply_text("Please start with /start and select encode or decode.")
        return

    user_text = update.message.text
    try:
        if mode == "encode":
            encoded_bytes = base64.b64encode(user_text.encode("utf-8"))
            encoded_str = encoded_bytes.decode("utf-8")
            await update.message.reply_text(f"Base64 Encoded:\n`{encoded_str}`", parse_mode="Markdown")
        else:  # decode
            decoded_bytes = base64.b64decode(user_text)
            decoded_str = decoded_bytes.decode("utf-8")
            await update.message.reply_text(f"Decoded Text:\n`{decoded_str}`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Error processing your input: {e}")

    # Clear the mode after operation to reset the flow
    context.user_data.clear()

def main():
    app = ApplicationBuilder().token("8377001447:AAEUZMLRP346KzuxLOpAVJdGzUTJ1g-KM9k").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Base64 Encoder/Decoder Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
