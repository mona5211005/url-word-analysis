import jieba
from collections import Counter
from .config import STOP_WORDS

def analyze_text(text: str, min_freq: int = 1, extra_stop_words: set = None) -> dict:
    combined_stop_words = STOP_WORDS.copy()
    if extra_stop_words:
        combined_stop_words.update(extra_stop_words)
    
    words = jieba.lcut(text)
    filtered_words = [word for word in words if len(word) > 1 and word not in combined_stop_words]
    word_count = Counter(filtered_words)
    word_count = {word: count for word, count in word_count.items() if count >= min_freq}
    return dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True))

def get_top_words(word_count: dict, top_n: int = 20) -> list:
    return list(word_count.items())[:top_n]

def get_total_word_count(word_count: dict) -> int:
    return sum(word_count.values())

def get_unique_word_count(word_count: dict) -> int:
    return len(word_count)