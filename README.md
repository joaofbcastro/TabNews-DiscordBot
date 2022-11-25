# TabNews-DiscordBot

## Sobre

Esse projeto tem como base a API do site [TabNews](https://www.tabnews.com.br). seu repositório pode ser encontrado em [filipedeschamps/tabnews.com.br](https://github.com/filipedeschamps/tabnews.com.br).

## Instalar e rodas o projeto

Rodar o bot em uma máquina local é bastante simples

### Dependências globais

Você precisa ter duas principais dependências:
 
 - Python LTS v3.7 (ou qualquer versão superior)
 - Token de acesso à uma aplicação Discord

Você pode criar e obter o token de acesso da sua aplicação no [Discord Developer Portal](https://discord.com/developers/applications).

### Dependências locais

Então após baixar o repositório, não se esqueça de instalar as dependências locais do projeto:

```bash
pip install -r requirements.txt
```

### Inserindo token do bot

Dentro do arquivo `bot.py` você precisará substituir na linha 130 a palavra TOKEN por seu token de acesso.

### Rodar o projeto

Para rodar o projeto localmente, basta rodar o comando abaixo:

```py
py bot.py
```
Observação:

 - A depender do ambiente que você esteja utilizando o `py` deve ser substituído por `python` ou `python3`.

### Sincronizando comandos

É necessário primeiro sincronizar os comandos antes de conseguir os utilizar.

Estando num servidor juntamente com o bot, use o comando de texto`@NOME_DO_SEU_BOT sync` da seguinte maneira:

![Usando o comando no Discord](https://i.imgur.com/16TAOyE.gif)

### Definindo canal

Bem após os comandos serem sincronizados será necessário definir o canal onde as novas notificações de conteúdos serão enviadas. Para isso, use o comando `/enable`:

![Usando o comando /enable no Discord](https://i.imgur.com/GjebNcq.gif)

## Concluindo

Com isso, é apenas questão de tempo até que as novas mensagens sejam enviadas no canal escolhido.

![Nova publicação](https://i.imgur.com/u9g4Rfy.gif)
