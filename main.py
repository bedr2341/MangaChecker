import ezgmail
import feedparser
from datetime import datetime


def getUpdatedMangaFrom(url, lineNumber):
    mangaFeed = feedparser.parse(url).entries
    lines = open("lastUpdateDate.txt").read().splitlines()
    dateOfLastUpdate = lines[lineNumber - 1]

    for i in range(0, len(mangaFeed)):
        if mangaFeed[i].published != dateOfLastUpdate:
            mangaTitles.append(mangaFeed[i].title)
            mangaLinks.append(mangaFeed[i].link)
        else:
            break

    lines[lineNumber - 1] = mangaFeed[0].published
    with open("lastUpdateDate.txt", "w") as file:
        file.writelines("\n".join(lines))  # overwrites the date for future use


def formatText(listOfTitles, listOfLinks):
    formattedText = "The following Manga have been updated:"
    for i in range(0, len(listOfTitles)):
        formattedText += "\n\t- " + listOfTitles[i] + "\n\t" + listOfLinks[i] + "\n"

    return formattedText


if __name__ == '__main__':
    # they're global variables so that the getUpdatedMangaFrom appends to it when getting manga from different URL
    mangaTitles = []
    mangaLinks = []

    getUpdatedMangaFrom("rss url", 1)

    if mangaTitles:
        messageText = formatText(mangaTitles, mangaLinks)
        ezgmail.send('recipient', 'Manga Updates', messageText)
    else:
        print("No new manga :/ on ", datetime.now())

