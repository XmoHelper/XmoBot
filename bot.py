from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai
import yfinance as yf

# ========== GANTI BAGIAN INI ==========

TOKEN = "7789757370:AAEyw4AefA4SewPn8113Z2Y_0DSDUhFG9zg"
OPENROUTER_API_KEY = "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"

# ========== SETTING OPENROUTER (AI GRATIS) ==========
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

# ========== COMMAND /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Halo! Aku SahamBot buatan Massimo!\n"
        "Ketik /pantau BBRI untuk melihat harga saham dan saran dari AI! 🤖"
    )

# ========== COMMAND /pantau BBRI ==========
async def pantau(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Contoh: /pantau BBRI")
        return

    kode_saham = context.args[0].upper()
    await update.message.reply_text(f"🔍 Mengambil data saham {kode_saham}...")

    try:
        saham = yf.Ticker(f"{kode_saham}.JK")
        data = saham.history(period="1d")

        if data.empty:
            await update.message.reply_text("⚠️ Data tidak tersedia. Coba kode saham lain.")
            return

        harga = round(data["Close"][-1], 2)
        await update.message.reply_text(f"💵 Harga saham {kode_saham}: Rp {harga:,}")

        # 🔗 Minta saran dari AI
        prompt = f"Harga saham {kode_saham} adalah Rp {harga}. Apakah ini saat yang baik untuk beli atau jual? Jawab singkat seperti analis saham."

        gpt_response = openai.ChatCompletion.create(
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        jawaban = gpt_response["choices"][0]["message"]["content"]
        await update.message.reply_text(f"🤖 Saran AI:\n{jawaban}")

    except Exception as e:
        await update.message.reply_text(f"❌ Gagal ambil data: {e}")

# ========== JALANKAN BOT ==========
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pantau", pantau))
    print("🚀 Bot Saham Massimo sedang berjalan...")
    app.run_polling()
