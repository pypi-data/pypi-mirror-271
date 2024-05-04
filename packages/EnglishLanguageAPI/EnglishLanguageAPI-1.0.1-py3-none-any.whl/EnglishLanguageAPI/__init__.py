from .API import EnglishDictionary
from .API import EnglishVocabulary

from argparse import ArgumentParser
from sqlite3 import connect
from random import choice
from time import sleep

from logging import basicConfig, info, INFO


utf8 = lambda string: string.encode("utf-8")


if __name__ == "__main__":

    arguments = ArgumentParser()


    # Heres a long block of arguments.
    arguments.add_argument("-W", "--word")

    arguments.add_argument("-Bw", "--build-wordlist", action="store_true")
    arguments.add_argument("-Dw", "--disposable-wordlist", default="/home/library/disposable-wordlist.txt")
    arguments.add_argument("-Wl", "--wordlist", default="/home/library/50000-wordlist.txt")
    arguments.add_argument("-R", "--resume", action="store_true")
    arguments.add_argument("-Db", "--database", action="store_true", default=False)
    arguments.add_argument("-Lf", "--logfile", default="/home/logs/EnglishLanguageAPI.log")
    arguments.add_argument(
        "-Df", "--database-file",
        default="/home/library/dictionary.db"
    )

    arguments = arguments.parse_args()

    basicConfig(filename=arguments.logfile, level=INFO)


    # Database functionality; for documenting every word.
    if arguments.database:
        
        database = connect(arguments.database_file)
        cursor = database.cursor()

        
        """ Request a source-file for local use if we need one. """

        # Request 50000 word list from github.
        if arguments.build_wordlist is True:
            english = EnglishVocabulary()
            wordlist = english.words

            with open(arguments.wordlist, "a") as source:
                for word in wordlist:
                    source.write(word)


        """ Select wordlist source from certain endpoints. """

        # Read from the consumable list to pick up where we left off.
        if arguments.resume is True:
            with open(arguments.disposable_wordlist, "r") as words:
                wordlist = words.readlines()

        # Read from the full list to avoid the overhead of writing our own list.
        else:
            # NOTE: Make sure we dont already have one in memory.
            try:
                if wordlist: pass

            except NameError:
                # NOTE: Check to see if we have our own if not in memory.
                try:
                    with open(arguments.wordlist, "r") as words:
                        wordlist = words.readlines()
                # NOTE: Request one from Github if we dont have our own.
                except:
                    english = EnglishVocabulary()
                    wordlist = english.words


        """ Begin iterating over the list of words. """

        try:
            while True:

                # Select a word to look up, and request its definition from the dictionary.
                word = choice(wordlist); info(f"Begin request for {word}.")
                request_attempt_count = 0
         
                while True:
                    try:
                        lookup = EnglishDictionary(word)
                        break
                    except:
                        request_attempt_count += 1
                        if request_attempt_count >= 3:
                            break
                        else:
                            sleep(3)

            
                # Record both to the database as utf8 encoded bytes.
                info("Writing {word} to dictionary database.")
                cursor.execute("""
                    INSERT OR IGNORE INTO english(
                        word, definition
                    ) VALUES ( ?, ? );""",
                    ( utf8(lookup.word),
                      utf8(lookup.description) )
                )
            
                # Save our change to the database and remove the word from the MEMORY list.
                database.commit(); wordlist.remove(word)


        except:
            """ Gracefully exit the program upon close. """
            info("Exception recieved; shutting down.")
            database.commit(); database.close()

            # NOTE: Save whats left of the consumable list, if we selected that one as our source.
            if arguments.resume is True:

                info("Saving progress to disposable wordlist.")

                # Clear the file by overwriting it with nothing.
                with open(arguments.disposable_wordlist, "w") as words:
                    words.write("")

                # Re-write the disposable wordlist with what we havent done yet.
                with open(arguments.disposable_wordlist, "a") as words:
                    for word in wordlist:
                        words.write(f"{word}")


    # Basic command-line functionality; just a word and no other arguments.
    else:

        lookup = EnglishDictionary(arguments.word)
        print(lookup.description)