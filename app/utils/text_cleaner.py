import re
import string
import unicodedata


from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def normalize_text(text: str) -> str:
    """Normalize unicode characters"""
    return unicodedata.normalize("NFKD", text)


def remove_urls(text: str) -> str:
    return re.sub(r"http\S+|www\S+", "", text)


def remove_html(text: str) -> str:
    return re.sub(r"<.*?>", "", text)


def remove_mentions_hashtags(text: str) -> str:
    return re.sub(r"@\w+|#\w+", "", text)


def remove_emojis(text: str) -> str:
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)


def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation))


def remove_numbers(text: str) -> str:
    return re.sub(r"\d+", "", text)


def remove_extra_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def reduce_repeated_chars(text: str) -> str:
    # gooooood -> good
    return re.sub(r"(.)\1{2,}", r"\1", text)


def remove_stopwords_func(text: str) -> str:
    words = text.split()
    filtered = [word for word in words if word not in stop_words]
    return " ".join(filtered)


def lemmatize_text(text: str) -> str:
    words = text.split()
    lemmas = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(lemmas)


def clean_text(text: str, remove_stopwords=True, lemmatize=True) -> str:
    """
    Full text cleaning pipeline
    """

    if not isinstance(text, str):
        return ""

    text = normalize_text(text)
    text = text.lower()

    text = remove_urls(text)
    text = remove_html(text)
    text = remove_mentions_hashtags(text)
    text = remove_emojis(text)

    text = reduce_repeated_chars(text)

    text = remove_punctuation(text)
    text = remove_numbers(text)

    text = remove_extra_spaces(text)

    if remove_stopwords:
        text = remove_stopwords_func(text)

    if lemmatize:
        text = lemmatize_text(text)

    return text