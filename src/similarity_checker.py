import ast
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def parse_code_to_ast(code, language):
    if language == "Python":
        try:
            tree = ast.parse(code)
            return tree
        except SyntaxError:
            return None
    elif language == "C":
        # Tokenize C code by meaningful constructs
        tokens = re.findall(r'\b\w+\b', code)  # Extract words as tokens
        return tokens


def ast_to_tokens(tree, language):
    if language == "Python":
        return [node.__class__.__name__ for node in ast.walk(tree)]
    elif language == "C":
        return tree  # Already tokenized for C


def calculate_structural_similarity(tokens1, tokens2):
    # Jaccard similarity (set-based)
    set1, set2 = set(tokens1), set(tokens2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    if not union:  # Avoid division by zero
        return 0
    return len(intersection) / len(union)


def calculate_lexical_similarity(code1, code2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([code1, code2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]


def calculate_highest_similarity(language, input_code, code_samples, filenames):
    input_tree = parse_code_to_ast(input_code, language)
    if not input_tree:
        return 0, None  # Invalid input code

    input_tokens = ast_to_tokens(input_tree, language)
    max_similarity = 0
    most_similar_file = None

    for code, filename in zip(code_samples, filenames):
        sample_tree = parse_code_to_ast(code, language)
        if not sample_tree:
            continue

        sample_tokens = ast_to_tokens(sample_tree, language)
        structural_similarity = calculate_structural_similarity(input_tokens, sample_tokens)
        lexical_similarity = calculate_lexical_similarity(input_code, code)
        combined_score = 0.7 * structural_similarity + 0.3 * lexical_similarity

        if combined_score > max_similarity:
            max_similarity = combined_score
            most_similar_file = filename

    return max_similarity, most_similar_file
