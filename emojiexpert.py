#!/usr/bin/env python3
import requests
import config
import atexit
import time
import sys
import csv
import urllib.parse

import persistence


class emojiexpert:
    def __init__(self):
        self.storage = persistence.Persistence()
        self.last_update_id = 0

        self.startupMessage()
        atexit.register(self.shutdownMessage)

        self.server_retry = config.SERVER_RETRY_TIMEOUT

        self.emojiChars = self.load_unicode_data()
        self.emojiChars.update(self.load_emoji_data())


        # lower case versions of hello's
        self.HELLO = ["hi", "hello", "hallo"]

    def _load_emoji_data_file(self, filename, url):
        try:
            csvfile = open(filename, newline='')
        except Exception as a:
            print(a)
            print("Failed to open '{}'.\nMake sure to download it e.g. from {}".format(filename,url))
            sys.exit(1)

        emojiChars = {}
        unicodeReader = csv.reader(csvfile, delimiter=';')
        for row in unicodeReader:
            if len(row) != 3:
                continue
            if row[1] == 'Basic_Emoji':
                continue
            if '..' in row[0]:
                continue
            codes=row[0].strip()
            typ=row[1].strip()
            name=row[2].strip().split('#')[0]

            emojiChars[codes] = { 'name': name, 'type': typ }
            # add optional representation without the VARIATION SELECTOR-16
            codes2 = codes.replace('FE0F', '').replace('  ',' ').strip()
            emojiChars[codes2] = { 'name': name, 'type': typ }
        return emojiChars

    def load_emoji_data(self):

        emojiChars = self._load_emoji_data_file("emoji-sequences.txt", "https://unicode.org/Public/emoji/12.0/emoji-sequences.txt")
        emojiChars.update(self._load_emoji_data_file("emoji-zwj-sequences.txt", "https://unicode.org/Public/emoji/12.0/emoji-zwj-sequences.txt"))
        emojiChars.update(self._load_emoji_data_file("emoji-data.txt", "https://unicode.org/Public/emoji/12.0/emoji-data.txt"))
        emojiChars.update(self._load_emoji_data_file("emoji-test.txt", "https://unicode.org/Public/emoji/12.0/emoji-test.txt"))

        return emojiChars

    def load_unicode_data(self):
        try:
            csvfile = open('UnicodeData.txt', newline='')
        except Exception as a:
            print(a)
            print("Failed to open 'UnicodeData.txt'.\nMake sure to download the current version e.g. from ftp://ftp.unicode.org/Public/UNIDATA/UnicodeData.txt")
            sys.exit(1)

        unicodeChars = {}
        unicodeReader = csv.reader(csvfile, delimiter=';')
        # columns implemented according to ftp://ftp.unicode.org/Public/3.0-Update/UnicodeData-3.0.0.html
        CODE_VALUE=0
        CHAR_NAME=1
        OLD_NAME=10
        for row in unicodeReader:
            name=row[CHAR_NAME]
            if not name or name == "<control>":
                name = row[OLD_NAME]
            if not name:
                name = "Char code 0x{} has no name :-(".format(row[CODE_VALUE])
            unicodeChars[row[CODE_VALUE]] = { 'name': name }
        return unicodeChars

    def startupMessage(self):
        for id in self.storage.allUsers():
            self.sendTextMessage(id, "Hi! I'm online again!")

    def shutdownMessage(self):
        for id in self.storage.allUsers():
            self.sendTextMessage(id, "I'm going to sleep for some maintenace.")

    def _sendMessage(self, chat_id, text, parse_mode=None):
        j = {
            "chat_id" : chat_id,
            "text" : text
        }

        if parse_mode is not None:
            j["parse_mode"] = parse_mode

        r = requests.post(config.API_URL + "sendMessage", json=j)

        result = r.json()
        if not result["ok"]:
            print(result)

    def sendTextMessage(self, chat_id, text):
        self._sendMessage(chat_id, text)



    def processTextMessage(self, message):
        text = message["text"]

        chat_id = message["chat"]["id"]
        if not self.storage.isUser(chat_id):
            self.sendTextMessage(chat_id, "Hi {}, ".format(message["from"]["first_name"]) + config.GREETING + config.STATEMENT)
            self.storage.createUser(chat_id)

        if text.startswith("/"):
            #processCommandMessage(message)
            self.sendTextMessage(chat_id, "I don't know any command for now" + config.STATEMENT)
        elif any(x in text.lower() for x in self.HELLO):
            self.sendTextMessage(chat_id, config.GREETING)
        else:
            code = ' '.join(["%X" % ord(x) for x in text]).replace('FE0F', '').strip()
            code_raw = ' '.join(["%X" % ord(x) for x in text])

            e = self.emojiChars.get(code)
            if e:
                url = "https://emojipedia.org/emoji/"+urllib.parse.quote(text)+"\n"
                meaning = url + e.get('name')
                self.storage.countSearch(chat_id)
            else:
                meaning = '… unknown to me!\nPlease only submit one emoji at a time \U0001F612\nor my data needs an update \U0001f616\n' + config.STATEMENT

            self.sendTextMessage(chat_id, "'{}' ({}) is:\n{}".format(text, code_raw, meaning))

    def processMessage(self, message):
        if "text" in message:
            self.processTextMessage(message)
        if "group_chat_created" in message:
            chat_id = message["chat"]["id"]
            self.sendTextMessage(chat_id, "Hi! I don't like group chats, sorry!")

    def run_bot(self):

        while True:

            print("Make request: {0}".format(self.last_update_id))
            try:
                r = requests.post( config.API_URL + "getUpdates"
                                 , json={ "offset" : self.last_update_id + 1
                                        , "timeout" : config.TIMEOUT
                                        }
                                 , timeout=config.TIMEOUT + 5
                                 )
                result = r.json()
                print(result)

                if result["ok"]:
                    limit = 10
                    if (len(result["result"]) == 0):
                        print("No result, {}".format(result))

                    for update in result["result"]:
                        print("update {}: {}".format(11-limit,update))
                        limit-=1
                        if limit <= 0: break
                        update_id = update["update_id"]
                        if update_id > self.last_update_id:
                            self.last_update_id = update_id

                        try:
                            self.processMessage(update["message"])
                        except Exception as e:
                            print(e)
                    server_retry = config.SERVER_RETRY_TIMEOUT
                else:
                # TODO error handling
                    print(result)
            except (ValueError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as err:
                print("Connection Error {0}\nRetrying in {1} seconds".format(err, server_retry))
                time.sleep(server_retry)
                server_retry *= 2

            #print(result)

if __name__ == "__main__":
    b = emojiexpert()
    b.run_bot()
