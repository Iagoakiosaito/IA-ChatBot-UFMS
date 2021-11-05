from token import set_token
from dicts import getDict_ent, getDict_price
from configs_chatbot import main_function


import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

global comanda

comanda = []
# Log
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:

    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}, o que deseja?',
        reply_markup=ForceReply(selective=True),
    )


def intention(update: Update, context: CallbackContext) -> None:
    global preco, msg_comanda, msg_comanda_fim
    detalhes= main_function(update.message.text)
    if detalhes[1] == "Saudação":

        user = update.effective_user
        update.message.reply_markdown_v2(
        fr'Olá {user.mention_markdown_v2()}, o que deseja?',
        reply_markup=ForceReply(selective=True),
        )

    if (detalhes[1] != "Finalizar" and detalhes[1] != "Saudação"):

        update.message.reply_text(detalhes[0])
        comanda.append(detalhes[2])

    elif detalhes[1] == "Finalizar":
        dict_prec = getDict_price()
        preco = 0
        msg_comanda = ("\nCerto! \nO pedido de: ")
        i = 1
        for pedido in comanda:
            for item in pedido:
                msg_comanda += ("\n• {} {}". format(item[0], item[1]))
                i += 1

        for pedido in comanda:
            for item in pedido:
                preco += item[0] * dict_prec[item[1]]
        
        msg_comanda_fim = ("Preço final: R${}".format(preco))
        
        update.message.reply_text(msg_comanda)
        update.message.reply_text(msg_comanda_fim)
    


def main() -> None:
    """Inicia o bot"""
    # instanciador do Updater com o token do bot
    updater = Updater(set_token)
    
    # dispatcher para registrar os handlers
    dispatcher = updater.dispatcher

    # comandos diferentes, com resposta no app
    dispatcher.add_handler(CommandHandler("start", start))

    # mensagem recebida do usuário, resposta no app
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, intention))

    # Inicia o bot
    updater.start_polling()

    # responsável para caso necessário, desligar o bot, com o comando ^C
    updater.idle()


if __name__ == '__main__':
    main()