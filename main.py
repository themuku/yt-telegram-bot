import os
from typing import Final
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from pytube import YouTube

TOKEN: Final = "7426971938:AAEHyUM94loJbJOt4Eu4WwPWFRhS2AmNYyw"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("For starting paste the video link.")


async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    yt_link = update.message.text

    try:
        yt = YouTube(yt_link)

        downloaded_file = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
        if downloaded_file:
            await update.message.reply_video(downloaded_file)
            for file in os.listdir():
                if file.endswith(".mp4"):
                    os.remove(file)
        else:
            await update.message.reply_text("Unable to download video")
    except:
        print("Something went wrong!")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT, download_command))

    app.run_polling()
