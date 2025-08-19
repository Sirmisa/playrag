import csv
import string
from collections import Counter
from playwright.sync_api import sync_playwright
import difflib
import numpy as np
import pandas as pd
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize
from rouge_score import rouge_scorer

# --- Configuration ---
RAG_UI_URL = 'https://your-rag-agent-ui.com'
INPUT_SELECTOR = 'textarea[id="prompt-input"]'
SUBMIT_SELECTOR = 'button[type="submit"]'
RESPONSE_SELECTOR = 'div[class="response-output"]'
GROUND_TRUTH_FILE = 'ground_truth.csv'
REPORT_FILE = 'evaluation_report.csv'

# --- Text Processing and Similarity Metrics ---

def normalize_text(text):
    """Simple normalization: lowercase, remove punctuation."""
    text = text.lower()
    return text.translate(str.maketrans('', '', string.punctuation))

def jaccard_similarity(text1, text2):
    """Jaccard similarity: intersection over union of unique words."""
    words1 = set(normalize_text(text1).split())
    words2 = set(normalize_text(text2).split())
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union) if union else 0.0

def bag_of_words_cosine(text1, text2):
    """Cosine similarity on bag-of-words vectors using numpy."""
    norm_text1 = normalize_text(text1)
    norm_text2 = normalize_text(text2)
    words = list(set(norm_text1.split() + norm_text2.split()))
    if not words:
        return 0.0
    vec1 = np.array([Counter(norm_text1.split())[w] for w in words])
    vec2 = np.array([Counter(norm_text2.split())[w] for w in words])
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2) if norm1 and norm2 else 0.0

# --- NLTK/ROUGE Evaluation Metrics ---

def calculate_bleu(actual, expected):
    """Calculates BLEU score."""
    reference = [word_tokenize(normalize_text(expected))]
    candidate = word_tokenize(normalize_text(actual))
    chencherry = SmoothingFunction()
    return sentence_bleu(reference, candidate, smoothing_function=chencherry.method1)

def calculate_rouge(actual, expected):
    """Calculates ROUGE-L score."""
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = scorer.score(normalize_text(expected), normalize_text(actual))
    return scores['rougeL'].fmeasure

# --- Core Evaluation Logic ---

def evaluate_response(actual, expected):
    """Evaluates the response using a suite of metrics."""
    norm_actual = normalize_text(actual)
    norm_expected = normalize_text(expected)
    
    exact_match = norm_actual == norm_expected
    string_sim = difflib.SequenceMatcher(None, norm_actual, norm_expected).ratio()
    jaccard_sim = jaccard_similarity(actual, expected)
    cosine_sim = bag_of_words_cosine(actual, expected)
    bleu_score = calculate_bleu(actual, expected)
    rouge_l_score = calculate_rouge(actual, expected)

    avg_sim = (string_sim + jaccard_sim + cosine_sim) / 3
    return {
        'exact_match': exact_match,
        'string_similarity': string_sim,
        'jaccard_similarity': jaccard_sim,
        'cosine_similarity': cosine_sim,
        'bleu_score': bleu_score,
        'rouge_l_score': rouge_l_score,
        'average_similarity': avg_sim,
        'pass': avg_sim > 0.75
    }

# --- Main Execution Block ---

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    results = []
    with open(GROUND_TRUTH_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            query = row['query']
            expected = row['expected_response']
            
            try:
                page.goto(RAG_UI_URL)
                page.wait_for_selector(INPUT_SELECTOR)
                page.fill(INPUT_SELECTOR, query)
                page.click(SUBMIT_SELECTOR)
                
                page.wait_for_selector(RESPONSE_SELECTOR, timeout=30000)
                actual = page.locator(RESPONSE_SELECTOR).inner_text().strip()
                
                eval_metrics = evaluate_response(actual, expected)
                results.append({
                    'query': query,
                    'expected': expected,
                    'actual': actual,
                    **eval_metrics
                })
                print(f"Processed: {query} - Pass: {eval_metrics['pass']} - Avg Sim: {eval_metrics['average_similarity']:.2f}")
            
            except Exception as e:
                print(f"Error on {query}: {e}")
                results.append({'query': query, 'error': str(e)})
    
    browser.close()

# --- Reporting ---

df = pd.DataFrame(results)
df.to_csv(REPORT_FILE, index=False)
print(f"\nReport saved to {REPORT_FILE}")

if not df.empty:
    accuracy = df['pass'].mean() * 100 if 'pass' in df else 0
    avg_string_sim = df['string_similarity'].mean()
    avg_jaccard = df['jaccard_similarity'].mean()
    avg_cosine = df['cosine_similarity'].mean()
    avg_bleu = df['bleu_score'].mean()
    avg_rouge = df['rouge_l_score'].mean()

    print(f"\n--- Evaluation Summary ---")
    print(f"Overall Accuracy (based on threshold): {accuracy:.2f}%")
    print(f"Average String Similarity: {avg_string_sim:.2f}")
    print(f"Average Jaccard Similarity: {avg_jaccard:.2f}")
    print(f"Average Cosine Similarity: {avg_cosine:.2f}")
    print(f"Average BLEU Score: {avg_bleu:.2f}")
    print(f"Average ROUGE-L Score: {avg_rouge:.2f}")
