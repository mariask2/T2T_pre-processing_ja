# These files are used for adding sentiment mark-up in the texts, as well as for producing a json-format file which is used by Topics2Themes for adding static labels to the texts

# The format should be as follows:

# The first element in each tuple is the file name that contains the dictionary
# The second element is the name of the static label
# If the name of the static label is "negative", a word included in the dictionary receives the markup "negative" in the text (red colour).
# If the name of the static label is "positive", a word included in the dictionary receives the markup "negative" in the text (green colour).

# The dictionary should be in the following format (a JSON list):
# ["good", "splendid"]

# If this file contains no label_dictionary_files variable, no dictionaries will be used.

label_dictionary_files = [
                          ("dictionaries/anger.json", "anger"),
                          ("dictionaries/dislike.json", "dislike"),
                          ("dictionaries/positive.json", "positive"),
                          ("dictionaries/negative.json", "negative"),
                          ]


