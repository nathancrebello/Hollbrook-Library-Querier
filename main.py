from isbntools.app import *
import isbnlib
from isbnlib import meta
from isbnlib import meta, NotValidISBNError
from isbnlib.dev._exceptions import DataNotFoundAtServiceError
from fuzzywuzzy import fuzz
import pandas as pd
import math
from termcolor import colored

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkgZN8wCAoo4S_vaxHqLU-Cc1uyadaYud6fdTTF9hrJx6irwyaBLpT36z5JxaopHXpGSq3PqEeZ_Pf/pub?gid=0&single=true&output=csv"
df = pd.read_csv(url)
print(
  "\n\nWelcome to the Hollbrook Library Searching Catalaog! When you search for a book, the top results will appear based on the similarity to\nthe title. When you return the book, please put it back in the same shelf. Enjoy!\n"
)

while True:

  response = input(
    colored(
      "\n\n\nEnter the book you are searching for (or type 'q' to quit): ",
      'green'))

  if response == 'q':
    break

  if (len(response) > 0 and response.isspace() != True):

    title = response

    matches = []

    for i, item in enumerate(df["ISBN"]):

      if (math.isnan(item)):
        break
      else:

        if (len(str(int(item))) == 9):
          try:
            metadata = meta(str(int(item)), service='openl')
          except NotValidISBNError:
            try:
              metadata = meta("0" + str(int(item)), service='openl')
            except NotValidISBNError:

              metadata = None

          if metadata is not None:
            if 'Title' in metadata:
              title1 = metadata['Title']

            else:
              print("No title found in the metadata for this book.")
              print(item)

        else:
          metadata = meta(str(int(item)), service='openl')

          if not metadata:
            print("Invalid or unrecognized ISBN")
            print(item)
          else:
            title1 = metadata['Title']

        fuzz_ratio = fuzz.partial_ratio(title.lower(), title1.lower())
        if (fuzz_ratio > 80):
          matches.append((fuzz_ratio, item, i))

    if matches:
      matches = sorted(matches, reverse=True)

      for match in matches:
        print(
          "\n-------------------------------------------------------------")
        print("\nHere's some information about your book: \n")

        if (len(str(int(match[1]))) == 9):
          metadata = meta("0" + str(int(match[1])), service='openl')

        else:
          metadata = meta(str(int(match[1])), service='openl')

        if (metadata is not None):
          print(metadata)

        else:
          print("The metadata is empty. Book needs to be updated")
        print("\n")

        print("The book is located in shelf", df["Shelf"][match[2]])
        print("Fuzz ratio: ", match[0])

    else:
      print("\nSorry, we could not find a match for your search.\n")
  else:
    print("Sorry that is an invalid response")

print("\nThank you for using the book searching program!")
