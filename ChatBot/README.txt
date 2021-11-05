Bibliotecas necessárias:

    •pip install text2num
    •pip install python-telegram-bot
    •pip install sklearn
    •pip install nltk
        -será instalado algumas dependências na execução também
    •pip install numpy
    •pip install pandas

----•-Funcionamento-•----

O sistema possui duas alternativas de execução, uma sem a implementação da rede social "telegram" ("trabalho_chatbot_WHITOUT_telegram.py"),
já a outra, com essa implementação ("telegram_bot.py"), disponível no link "t.me/Papelaria_bot", o bot DEVE ser hospedado em máquina local para funcionar.

----•-Execução-•----

-trabalho_chatbot_WHITOUT_telegram.py:

    A entrada e saída será TOTALMENTE via cmd, com a entrada tendo uma mensagem "Usuário: " seguida para a entrada de dados do usuário.
    Após isso, a frase de entrada passa por um split simples e seguido para aplicação de um "stem" e normalização nessas palavras. Após a tratativa no input,
    é verificado a intenção dessa frase, entre as classes:
        "Saudação"  - quando uma conversa é iniciada;
        "Produtos"  - quando é requisitada uma listagem de produtos;
        "Pedido"    - quando um produto é pedido;
        "Finalizar" - quando é requisitado o fechamendo do pedido.
    Após a intenção ser definida, ela entrada em uma estrutura condicional para cada intenção, com suas devidas ações a serem tomadas.

    Um exemplo de execução está disponível no link "https://snipboard.io/n9F4tN.jpg".

-telegram_bot.py:

    Possui a mesma base do "trabalho_chatbot_WHITOUT_telegram.py", porém a execução se passa em uma inteface gráfica, que neste caso é o Telegram.
    Um exemplo de execução está disponível no link "https://snipboard.io/BKJyCd.jpg".


**Obrigado pela atenção**