from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# बॉट का टोकन (अपना टोकन यहां डालें)
TOKEN = '7034919230:AAFs4AiMivV2BNuy3VxHBkE8CHm0F2sFC8c'

# गेम्स की सूची (वेब ऐप्स के URL)
color_trading_games = {
    "IPL.WIN ₹117🇮🇳": {
        "url": "https://www.iplinvip.com/?dl=$arr9f7$INR$4",
        "description": "Great Choice 🙂 Signup And Get ₹117"
    },
    "Lottery 7 ₹77🇮🇳": {
        "url": "https://lottery7y.com/#/register?invitationCode=2653612802163",
        "description": "Great Choice 🙂 Signup And Get ₹77"
    },
    "BDG.WIN ₹58🇮🇳": {
        "url": "https://www.bigdaddygame.co//#/register?invitationCode=224112998604",
        "description": "Great Choice 🙂 Signup And Get ₹58"
    },
    "BBGO ₹58🇮🇳": {
        "url": "https://www.bbgo01.vip/#/register?invitationCode=688571020981",
        "description": "Great Choice 🙂 Signup And Get ₹58 This App Lounch In 2025"
    },
    "51 Game ₹51🇮🇳": {
        "url": "https://51game7.in/#/register?invitationCode=582181716687",
        "description": "Great Choice 🙂 Signup And Get ₹51"
    },
    "66 Lottery ₹66🇮🇳": {
        "url": "https://www.66lotterybkhn.com/#/pages/login/register?invitationCode=0946849507",
        "description": "Great Choice 🙂 Signup And Get ₹66"
    },
    "Raja Game ₹38🇮🇳": {
        "url": "https://www.rajalucky.in/#/register?invitationCode=45463988437",
        "description": "Great Choice 🙂 Signup And Get ₹38"
    },
    "6 Club ₹58🇮🇳": {
        "url": "https://www.6club11.com/#/register?invitationCode=75715118183",
        "description": "Great Choice 🙂 Signup And Get ₹58"
    },
    "DiuWin ₹57🇮🇳": {
        "url": "https://diuwinapp.club/#/register?invitationCode=46458365419",
        "description": "Great Choice 🙂 Signup And Get ₹57"
    },
    "RajaLuck ₹28🇮🇳": {
        "url": "https://rajaluck.world/#/register?invitationCode=LHgTB38426",
        "description": "Great Choice 🙂 Signup And Get ₹28"
    },
    "Z65.Win ₹58🇮🇳": {
        "url": "https://z65win.com/#/register?invitationCode=815269998682",
        "description": "Great Choice 🙂 Signup And Get ₹58 This App Lounch In 1 Jan 2025"
    },
    "Ok Win ₹28🇮🇳": {
        "url": "https://okwin9.in/#/register?invitationCode=78466476960",
        "description": "Great Choice 🙂 Signup And Get ₹28"
    }
}

slots_games = {
    # Slots games की सूची यहाँ जोड़ें (यदि आवश्यक हो)
}

# /start कमांड का हैंडलर
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_first_name = update.message.from_user.first_name
    keyboard = [
        [InlineKeyboardButton("Color Trading", callback_data='color_trading')],
        [InlineKeyboardButton("Slots Game", callback_data='slots')],
        [InlineKeyboardButton("Join Our Channel", url='https://t.me/yourchannel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Welcome {user_first_name}! आप किस तरह के गेम खेलना चाहते हैं?",
        reply_markup=reply_markup
    )

# गेम प्रकार चयन का हैंडलर
async def select_game_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    selected_type = query.data
    if selected_type == 'color_trading':
        games = color_trading_games
        context.user_data['selected_type'] = 'color_trading'
    elif selected_type == 'slots':
        games = slots_games
        context.user_data['selected_type'] = 'slots'
    else:
        return

    keyboard = [
        [InlineKeyboardButton(game, callback_data=f"game_{game}")] for game in games.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="Great Choice! कृपया एक गेम चुनें जिसे आप खेलना चाहते हैं:",
        reply_markup=reply_markup
    )

# गेम चयन का हैंडलर
async def select_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    selected_game = query.data[len("game_"):]
    selected_type = context.user_data.get('selected_type')
    if selected_type == 'color_trading':
        game_info = color_trading_games.get(selected_game)
    elif selected_type == 'slots':
        game_info = slots_games.get(selected_game)
    else:
        game_info = None

    if not game_info:
        return

    game_url = game_info["url"]
    game_description = game_info["description"]

    await query.edit_message_text(
        text=f"{selected_game}\n\n{game_description}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Play Now", url=game_url)],
            [InlineKeyboardButton("Back to Games", callback_data=selected_type)]
        ])
    )

# मुख्य कार्य जो बॉट को शुरू करता है
def main() -> None:
    # Application को सेट करें
    application = Application.builder().token(TOKEN).build()

    # हैंडलर्स जोड़ें
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(select_game_type, pattern='^(color_trading|slots)$'))
    application.add_handler(CallbackQueryHandler(select_game, pattern='^game_'))

    # बॉट को पोलिंग मोड में चलाना
    application.run_polling()

if __name__ == '__main__':
    main()