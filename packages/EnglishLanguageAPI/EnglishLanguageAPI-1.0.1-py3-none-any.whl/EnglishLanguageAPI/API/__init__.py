#!/usr/bin/env python
from requests import get

from bs4 import BeautifulSoup

from logging import info
from logging import getLogger

# Call the logger if one is set.
try: getLogger(__name__)
except: pass


class EnglishVocabulary:
    def __init__(self):
        """
        Request a clean list of over 50,000 words from github,
        courtesy of Guyyatsu.Technomancer.
        """

        # Make the request and clean up the formatting as we read it into memory.
        info("Requesting 50,000 word list from Github.")
        wordlist = [ word.decode() for word in get( f"https://raw.githubusercontent.com/"
                                                    f"guyyatsu/EnglishLanguageAPI/master/"
                                                    f"src/EnglishLanguageAPI/wordlist.txt" ).content\
                                                                                            .split( "\n".encode() )\
                     if word.decode() != "" ]; info("Finished Request.")

        self.words = wordlist


class EnglishDictionary:
    """
    The EnglishLanguageAPI class accepts a single word and searches
    the dictionary for a matching description.
    """

    def __init__(self, word, dictionary=True):
        """
        The searchTag is a callers search request given as a
        raw text string which is then formatted to the dictionary.com
        built-in api standards.  By default the search tag is compared
        against the thesaurus unless explicitly told to check the dictionary.
        """


        # Set dictionary.com  api url.
        base_url = "https://dictionary.com/browse"

        # TODO: Handle multiple words.
        self.word = word.split()[0]\
                        .lower()

        # Request the `dictionary.com` webpage for our word.
        info(f"Requesting definition for: {self.word}")
        page = BeautifulSoup(
            get( f"{base_url}/{self.word.lower()}" ).content,
            "html.parser"
        )

        # Scrape the raw html for the single tag containing what we're looking for.
        description = \
            page.find("meta", {"name": "description"})\
                .get("content")

        # Clean up the text for presentability and make globally accessible.
        description = description.replace(f"{self.word.title()} definition: ", "")
        description = description.replace(" See more.", "")
        description = description.replace("..", ".")
        description = " ".join(description.split(".")[0:-2])

        self.description = f"{description.capitalize()}."

