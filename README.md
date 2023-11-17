[![Typing SVG](https://readme-typing-svg.herokuapp.com?color=%2336BCF7&lines=OKX-Whitelist)](https://git.io/typing-svg)

Скрипт для добавления адресов в OKX Whitelist.

Принцип работы - запускаешь скрипт, открывается selenium, заходишь в аккаунт руками, дальше софт сам все делает: заполняет кошельки, парсит почту на получение кода, смотрит 2FA код, подтверждает и так далее. 1 цикл = 20 кошельков = 1.5 минуты.

# Настройка
1. Переименовываем `config_EXAMPLE.py` на `config.py`
2. Настраиваем `config.py`
3. Вставляем адреса кошельков в `wallets.txt`
4. Запускаем `main.py`

# Настройка `config.py`
1. `OKX_2FA` - сюда вставляем 2FA от okx аккаунта
2. `EMAIL_LOGIN` - сюда вставляем логин от почты okx аккаунта
3. `EMAIL_2FA` - сюда вставляем пароль приложений от почты. Вот как его получить: https://support.google.com/accounts/answer/185833?sjid=2552998692219979507-EU. 
[Пример пароля](https://github.com/zaivanza/okx-whitelist/blob/main/email_2fa_example.jpg)
4. `CHROME_VERSION` - сюда записываем версию своего хрома. Сейчас стоит 119, если будет ошибка при запуске, тогда меняй версию на свою.

Устанавливаем библиотеки : `pip install -r requirements.txt`

## Донаты (EVM): 
- `0xb7415DB78c886c67DBfB25D3Eb7fcd496dAf9021`
- `donates-for-hodlmod.eth`

## Links:
- https://t.me/links_hodlmodeth
- Code chat: [[ code ]](https://t.me/code_hodlmodeth)
- Ультимативный гайд по запуску скриптов на python : https://teletype.in/@hodlmod.eth/how-to-run-scripts