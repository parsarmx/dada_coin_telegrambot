from SafeTrade import bot
from SafeTrade.logs import LOGGER

LOGGER(__name__).info("client successfully initiated....")
if __name__ == "__main__":
    bot.run()
