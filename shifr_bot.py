import telebot
from cryptography.fernet import Fernet

bot_token = '7812447443:AAGiOSZ958ROAf-eqr8VI7AhfjpSFiYmBRA'
bot = telebot.TeleBot(bot_token)

# Хранение ключей в памяти (только для примера; на практике можно улучшить)
user_keys = {}

# Команда /start для приветствия и объяснения функций бота
@bot.message_handler(commands=['start'])
def start_message(message):
    start_text = (
        "Привет! Я бот для шифрования и дешифрования текстов. Вот что я умею:\n\n"
        "/generate_key - Сгенерировать новый ключ шифрования\n"
        "/encrypt - Зашифровать текст с помощью сгенерированного ключа\n"
        "/decrypt - Расшифровать текст с использованием указанного ключа\n"
        "/help - Показать список доступных команд"
    )
    bot.send_message(message.chat.id, start_text)

# Команда /help для отображения доступных команд
@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = (
        "Вот список доступных команд:\n\n"
        "/generate_key - Сгенерировать новый ключ шифрования\n"
        "/encrypt - Зашифровать текст с помощью сгенерированного ключа\n"
        "/decrypt - Расшифровать текст с использованием указанного ключа\n"
        "/help - Показать это сообщение с описанием команд"
    )
    bot.send_message(message.chat.id, help_text)

# Генерация случайного ключа
@bot.message_handler(commands=['generate_key'])
def generate_key(message):
    key = Fernet.generate_key()
    user_keys[message.chat.id] = key  # Сохраняем ключ для пользователя
    bot.send_message(message.chat.id, f"Сгенерированный ключ: {key.decode()} \nСохраните его, чтобы использовать для шифрования и дешифрования.")

# Шифрование текста
@bot.message_handler(commands=['encrypt'])
def ask_text_to_encrypt(message):
    bot.send_message(message.chat.id, "Отправьте текст, который хотите зашифровать.")
    bot.register_next_step_handler(message, encrypt_text)

def encrypt_text(message):
    if message.chat.id in user_keys:
        key = user_keys[message.chat.id]
        fernet = Fernet(key)
        encrypted_text = fernet.encrypt(message.text.encode())
        bot.send_message(message.chat.id, f"Зашифрованный текст: {encrypted_text.decode()}")
    else:
        bot.send_message(message.chat.id, "Сначала сгенерируйте ключ командой /generate_key.")

# Дешифрование текста
@bot.message_handler(commands=['decrypt'])
def ask_text_to_decrypt(message):
    bot.send_message(message.chat.id, "Отправьте зашифрованный текст, который хотите расшифровать.")
    bot.register_next_step_handler(message, ask_key_for_decryption)

def ask_key_for_decryption(message):
    encrypted_text = message.text
    bot.send_message(message.chat.id, "Отправьте ключ для расшифровки.")
    bot.register_next_step_handler(message, lambda msg: decrypt_text(msg, encrypted_text))

def decrypt_text(message, encrypted_text):
    try:
        key = message.text.encode()
        fernet = Fernet(key)
        decrypted_text = fernet.decrypt(encrypted_text.encode()).decode()
        bot.send_message(message.chat.id, f"Расшифрованный текст: {decrypted_text}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка расшифровки: {str(e)}\nУбедитесь, что ключ и текст верны.")

bot.polling()
