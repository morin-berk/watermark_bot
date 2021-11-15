# Watermark Bot
Telegram bot adds watermarks to images in messages.
The bot has the following functionality:
1. Start the bot.
2. Upload the watermark in png format as a document.
3. Forward the bot a message containing a picture.
4. The bot sends back the same message marked with watermark.

Watermark occupies 7% of the total area and is located in the lower right corner.

You can change the watermark.

__________________________________
# Instruction
Download the repository to your computer.
In the bot.py file, replace the token with your own, recieved from the BotFather.

To build docker container use **docker-compose build --no-cache**.
To run docker container **docker compose up** 
or in one command: **docker compose up --build**