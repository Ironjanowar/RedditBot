import telebot
import praw

# Listener


def listener(messages):
    # When new messages arrive TeleBot will call this function.
    for m in messages:
        if m.content_type == 'text':
            # Prints the sent message to the console
            if m.chat.type == 'private':
                print("Chat -> " + str(m.chat.first_name) +
                      " [" + str(m.chat.id) + "]: " + m.text)
        else:
            print("Group -> " + str(m.chat.title) +
                  " [" + str(m.chat.id) + "]: " + m.text)

# Creamos el bot
with open('./bot.token', 'r') as TOKEN:
    bot = telebot.TeleBot(TOKEN.readline().strip())

# Inicializamos el listener
bot.set_update_listener(listener)

# Handlers


@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Hola @{}!\n\nEsto es un bot para coger posts de subreddits!\nUsa /help para ver como funciona.".format(m.from_user.username))


@bot.message_handler(commands=['help'])
def help(m):
    bot.send_message(m.chat.id, "Simplemente envia:\n`/r/subreddit [hot | new | rising | top]`\n\nEjemplo:\n`/r/gifs hot`", parse_mode="Markdown")


@bot.message_handler()
def send_subreddit(m):
    # Valid command?
    text = m.text
    if text.startswith("/r/"):
        # Extract the subreddit
        subreddit = text.split('/', 2)[2].split(' ', 1)[0].lower()

        # Select tab
        if len(text.split('/', 2)[2].split(' ', 1)) == 2:
            tab = text.split('/', 2)[2].split(' ', 1)[1].lower()
        else:
            tab = "hot"

        # Get the subreddit information
        r = praw.Reddit(user_agent='Reddit Tg Amazing App')
        try:
            if tab == "new":
                submissions = r.get_subreddit(subreddit, fetch=True).get_new(limit=10)
                # Format the information to send
                to_send = "New"
            elif tab == "hot":
                submissions = r.get_subreddit(subreddit, fetch=True).get_hot(limit=10)
                # Format the information to send
                to_send = "Hot"
            elif tab == "rising":
                submissions = r.get_subreddit(subreddit, fetch=True).get_rising(limit=10)
                # Format the information to send
                to_send = "Rising"
            elif tab == "top":
                submissions = r.get_subreddit(subreddit, fetch=True).get_top(limit=10)
                # Format the information to send
                to_send = "Top"
        except:
            bot.reply_to(m, "Ese subreddit no existe!")
            return

        to_send += " reddit posts in /r/{}\n\n".format(subreddit)

        for index, elem in enumerate(submissions):
            to_send += "{}. {}\n{}\n".format(index + 1, elem.title, elem.url)
            to_send += "---------------------------------------------------\n"

        # Send the message
        bot.send_message(m.chat.id, to_send, disable_web_page_preview=True)

# Ignore pending messages
bot.skip_pending = True

# Run the bot
print("Running...")
bot.polling()
