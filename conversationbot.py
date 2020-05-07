#!/usr/bin/env python

import logging
import sys
import csv
import time
import telegram
from telegram import (ReplyKeyboardMarkup, KeyboardButton,
                      ReplyKeyboardRemove, Update, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackContext,CallbackQueryHandler)
from apiKey import apiKey

exit() if  __name__ != "__main__" else None
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO, PROCEED, EDIT, LIKE, SECOND = range(8)



def start(update, context: CallbackContext):
    val = None
    user = update.message.from_user
    reply_keyboard = [['Boy', 'Girl', 'Other', 'Prostitute']]
    reply_keyboard1 = [['Proceed', 'Edit Info']]
    logger.info(user.id)
    userDict.update(user_id=str(user.id), name=user.full_name)
    with open('userdet.csv', newline='') as csv_file_r:
        csv_reader = csv.reader(csv_file_r)
        csv_list = list(csv_reader)
        for row in csv_list:
            if str(user.id) in row:
                val = True
                break
            else:
                val = False
        if val == False:
            update.message.reply_text(
                'Hi! My name is ORgYNiZER Bot. You seem new here. '
                'Send /cancel to stop talking to me.\n\n'
                'Are you a boy or a girl?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))
            return GENDER
        else:
            update.message.reply_text(
                'Hi! My name is ORgYNiZER Bot. I remember you from the last time. '
                'Send /edit to change your info.'
                'Send /continue to move along @vote',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True, resize_keyboard=True))
            return PROCEED


def like(update, context):

    if len(users_dic) == 0:
        return
    i = users_dic.pop(0)
    photo = "photos\\" + str(i[1]) + "'s_photo_" + str(i[2]) + ".jpg"
    keyboard = [[InlineKeyboardButton(
        u"chat " + str(i[1]) + " for 100 coin 💸", callback_data=str(SECOND))]]
    reply_keyboard = [['👎🏻', '👍🏻']]
    res =  update.message.reply_text(
                text='. . .',
                reply_markup=ReplyKeyboardRemove())
    context.bot. delete_message(chat_id=update.message.chat.id, message_id=res.message_id)
    res = context.bot.sendPhoto(
        disable_web_page_preview=True,
        chat_id=update.message.chat.id,
        photo=open(photo, 'rb'),
        selective=True,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        text=str(i[1]),
        reply_markup=reply_markup,
        chat_id=update.message.chat.id,
    )



def proceed(update, context):

    login_user_location = False
    users_location = []
    gender = False
    with open('userdet.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for i in reader:
            # print(i)
            if i['user_id'] == str(update['_effective_user']['id']):
                gender = i['gender']
                login_user_location = [
                    float(i['latitude']),  float(i['longitude'])]
            else:
                users_location.append([float(i['latitude']), float(
                    i['longitude']), i['gender'], i['name'], i['user_id']])
    for i in users_location:
        if i[2] != gender:
            users_dic.append(((abs(i[0] - login_user_location[0]) ** 2) +
                              (abs(i[1] - login_user_location[1])) ** 0.5, i[3], i[4]))
    users_dic.sort(key=lambda i: i[0])
    return LIKE




def edit(update, context):
    # work under progress
    print('this section can be used to edit / update you current info..')
    # ...
    # ...


def gender(update, context):
    user = update.message.from_user
    userDict.update(gender=update.message.text)
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    print(update.message)
    update.message.reply_text('I see! Please send me a photo of yourself, '
                              'so I know what you look like, or send /skip if you don\'t want to.',
                              reply_markup=ReplyKeyboardRemove())

    return PHOTO


def photo(update, context):

    location_keyboard = telegram.KeyboardButton(
        text="send_location", request_location=True)
    reply_keyboard = [[location_keyboard]]

    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(user.first_name+'\'s_photo_'+str(user.id)+'.jpg')
    logger.info("Photo of %s: %s", user.first_name,
                user.full_name+'_photo_'+str(user.id)+'.jpg')
    update.message.reply_text('Gorgeous! Now, send me your location please, '
                              'or send /skip if you don\'t want to.', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return LOCATION


def skip_photo(update, context):
    location_keyboard = telegram.KeyboardButton(
        text="send location", request_location=True)
    reply_keyboard = [[location_keyboard]]
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, and turn on your location please '
                              'or send /skip. ', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True))

    return LOCATION


def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    userDict.update(latitude=user_location.latitude,
                    longitude=user_location.longitude)
    logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text('Maybe I can visit you sometime! '
                              'At last, tell me something about yourself.', reply_markup=ReplyKeyboardRemove())

    return BIO


def skip_location(update, context):
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text('You seem a bit paranoid! '
                              'At last, tell me something about yourself.', reply_markup=ReplyKeyboardRemove())

    return BIO


def bio(update, context):
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    userDict.update(bio=update.message.text)
    update.message.reply_text('you seem like a very nice person!!')
    logger.info(userDict)
    objlist = []
    with open('userdet.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            objlist.append(row)

    with open('userdet.csv', 'w', newline='') as csv_file_w:
        fieldnames = ['user_id', 'name', 'gender',
                      'latitude', 'longitude', 'bio']
        writer = csv.DictWriter(csv_file_w, fieldnames=fieldnames)
        writer.writeheader()
        for i in objlist:
            writer.writerow(i)
        # writer.writerow({'user_id': '000000000', 'name': 'anonymous', 'gender': 'Other',
        #                  'latitude': '31.774171', 'longitude': '34.683293', 'bio': 'bjhbh'})
    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error ========>>> "%s"',
                   update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        apiKey, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other|Prostitute)$'), gender)],

            EDIT: [CommandHandler('edit', edit)],

            PROCEED: [
                CommandHandler('continue', proceed)],
            # MessageHandler(Filters.text,proceed),

            LIKE: [MessageHandler(Filters.text, like)],

            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],

            LOCATION: [MessageHandler(Filters.location, location),
                       CommandHandler('skip', skip_location)],

            BIO: [MessageHandler(Filters.text, bio)],

            # SECOND: [CallbackQueryHandler(second) ] # for test
            # OTHERQUES: [MessageHandler(Filters.text, otherques)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    # next(csv_reader, None)
    # csv_writer = csv.DictWriter(csv_file, fieldnames=csv_fields)
    # header = next(csv.reader(csv_file))
    users_dic = []
    userDict = {}
    main()
