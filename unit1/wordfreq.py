import argparse
import json
import string
import constants
import synsets

from nltk.stem import WordNetLemmatizer
from nltk import FreqDist
from nltk import word_tokenize
from nltk.corpus import stopwords


def parse_arguments():
    """Parses command-line arguments.
    Returns:
    - args (argparse.Namespace): The parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='The path to the JSON file containing processed text.')
    parser.add_argument('-n', '--number', type=int, help='The numbers of words that this program will output.')
    return parser.parse_args()
# End of parse_arguments()


def load_records(file):
    """Loads the records from the JSON file. Also filters out empty records.
    Params:
    - file (str): The path to the JSON file
    Returns:
    - records (list<dict>): The contents of the JSON file
    """
    with open(file, 'r') as json_file:
        records = json_file.readlines()
    records = [json.loads(record) for record in records]
    records = list(filter(lambda record: record[constants.TEXT] != '', records))
    return records
# End of load_records()


def preprocess_freq(jsonarr):
    """
    from the given json object, convert into sentences and from there cleaned into a list of words
    :param jsonarr: a list of json data on the articles
    :return: a list of important words
    """
    # remove entries with empty sentences
    jsonarr = filter(lambda data: data[constants.TEXT], jsonarr)
    # change the array to just be a list of all the sentences and make them all lowercase
    sentences = map(lambda data: data[constants.TEXT].lower(), jsonarr)
    # punctuation and stopwords to remove
    stoplist = stopwords.words('english') + list(string.punctuation) \
        + constants.CONTRACTIONS + constants.MYSQL_STOPWORDS

    lemmatizer = WordNetLemmatizer()
    cleaned = []
    for sentence in sentences:
        # tokenize by words
        words = word_tokenize(sentence)
        # filter list of words to remove stop words and punctuation
        filtered = list(filter(lambda word: word not in stoplist, words))

        # lemmatize all words
        lemmatized = map(lambda word: lemmatizer.lemmatize(word), filtered)
        cleaned.extend(lemmatized)
    return cleaned
# End of preprocess_freq()


def get_freq(word_list, count=10):
    freq_dist = FreqDist(word_list)
    return freq_dist.most_common(count)
# End of get_freq


if __name__ == "__main__":
    args = parse_arguments()
    jsonFilePath = args.file
    num = args.number

    jsonArr = load_records(jsonFilePath)
    processed = preprocess_freq(jsonArr)

    freq_words = get_freq(processed, 500)
    no_count_freq_words = list(map(lambda tup: tup[0], freq_words))

    syns = synsets.generate_syn_set(freq_words)
    synsets.print_syn_set(syns)
# End main