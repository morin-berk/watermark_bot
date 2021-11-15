# Watermark Bot
Telegram bot adds a watermarks to images in messages.
The bot has the following functionality:
1. Start the bot.
2. Upload the watermark in png format as a document.
3. Forward the bot a message containing a picture.
4. The bot sends back the same message marked with a watermark.

A watermark occupies 7% of the total area and is located in the lower right corner.

You can change a watermark.

__________________________________
# Instruction
Download the repository to your computer. Save your bot token to .env file.

To build docker container use **docker-compose build --no-cache**.
To run docker container **docker compose up** 
or in one command: **docker compose up --build**
