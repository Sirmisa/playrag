Of course. Here is a `README.md` file that explains the program, its setup, configuration, and usage, based on the provided source code.

-----

# RAG Agent UI Evaluation Framework

This project provides an automated framework for testing and evaluating the responses of a Retrieval-Augmented Generation (RAG) agent through its web user interface. It uses Playwright to simulate user interactions and calculates a suite of metrics to compare the agent's actual responses against a predefined set of "ground truth" answers.

## Features

  * [cite\_start]**Automated UI Testing**: Uses Playwright to automatically open a browser, navigate to the RAG agent's UI, submit queries, and retrieve responses[cite: 5, 6, 7].
  * [cite\_start]**Batch Processing**: Reads queries and expected responses from a CSV file, allowing for batch evaluation of multiple test cases[cite: 5].
  * **Comprehensive Evaluation Metrics**: Calculates a variety of metrics to provide a nuanced view of response quality:
      * [cite\_start]**Exact Match**: Checks for a perfect match after text normalization[cite: 3].
      * **Lexical Similarity**:
          * [cite\_start]String Similarity (SequenceMatcher) [cite: 3]
          * [cite\_start]Jaccard Similarity (word overlap) [cite: 1, 4]
          * [cite\_start]Cosine Similarity (bag-of-words vector comparison) [cite: 2, 4]
      * **NLP-Based Metrics**:
          * **BLEU Score**: Measures fluency and n-gram precision.
          * **ROUGE-L Score**: Measures recall of the most important content.
  * [cite\_start]**Detailed Reporting**: Generates a CSV report containing the query, expected response, actual response, and all calculated scores for each test case[cite: 10].
  * [cite\_start]**Summary Statistics**: Prints a summary of the overall accuracy and average scores for all metrics to the console after the run is complete[cite: 10, 11].

## Prerequisites

  * Python 3.7+
  * pip (Python package installer)

## Installation

1.  **Install Python Libraries**:
    Open your terminal and run the following command to install all necessary packages:

    ```bash
    pip install playwright pandas numpy nltk rouge-score
    ```

2.  **Install Playwright Browsers**:
    Playwright requires browser binaries for automation. Install them with this command:

    ```bash
    playwright install
    ```

3.  **Download NLTK Data**:
    The script uses the 'punkt' tokenizer from NLTK. Download it with this command:

    ```bash
    python -m nltk.downloader punkt
    ```

## Configuration

Before running the script, you must update the configuration variables at the top of the Python file.

  * [cite\_start]`RAG_UI_URL`: The URL of the web interface for your RAG agent[cite: 1].
  * [cite\_start]`INPUT_SELECTOR`: The CSS selector for the text input field where queries are typed (e.g., `'textarea[id="prompt-input"]'`)[cite: 1].
  * [cite\_start]`SUBMIT_SELECTOR`: The CSS selector for the submit button to be clicked[cite: 1].
  * [cite\_start]`RESPONSE_SELECTOR`: The CSS selector for the HTML element that contains the RAG agent's final response text[cite: 1].
  * [cite\_start]`GROUND_TRUTH_FILE`: The name of the input CSV file (default is `'ground_truth.csv'`)[cite: 1].
  * [cite\_start]`REPORT_FILE`: The name of the output report file (default is `'evaluation_report.csv'`)[cite: 1].
  * [cite\_start]`headless`: In the `p.chromium.launch()` function, set `headless=True` to run the browser in the background or `headless=False` to watch it run in real-time[cite: 5].

## Usage

### 1\. Create the Ground Truth File

Create a CSV file named `ground_truth.csv` (or the name you configured in `GROUND_TRUTH_FILE`). [cite\_start]It must contain two columns: `query` and `expected_response`[cite: 1, 5].

**Example `ground_truth.csv`:**

```csv
query,expected_response
"What is the capital of Japan?","The capital of Japan is Tokyo."
"Explain the process of photosynthesis.","Photosynthesis is the process used by plants, algae, and certain bacteria to harness energy from sunlight and turn it into chemical energy."
"Who wrote 'To Kill a Mockingbird'?","'To Kill a Mockingbird' was written by Harper Lee."
```

### 2\. Run the Evaluation Script

Execute the script from your terminal:

```bash
python your_script_name.py
```

[cite\_start]The script will print the progress for each query to the console[cite: 9].

## Understanding the Output

### Console Output

[cite\_start]After the script finishes, a summary of the results will be printed to your console[cite: 11]:

```
--- Evaluation Summary ---
Overall Accuracy (based on threshold): 85.50%
Average String Similarity: 0.88
Average Jaccard Similarity: 0.82
Average Cosine Similarity: 0.86
Average BLEU Score: 0.78
Average ROUGE-L Score: 0.89
```

### Report File

The script generates a detailed CSV file (e.g., `evaluation_report.csv`) with the following columns:

| Column | Description |
| :--- | :--- |
| **query** | [cite\_start]The original question sent to the agent[cite: 8]. |
| **expected** | [cite\_start]The ground truth answer from your CSV file[cite: 9]. |
| **actual** | [cite\_start]The raw response received from the agent[cite: 9]. |
| **exact\_match** | [cite\_start]`TRUE` or `FALSE` if the normalized responses are identical[cite: 4]. |
| **string\_similarity** | [cite\_start]Score (0-1) based on character-level similarity[cite: 4]. |
| **jaccard\_similarity** | [cite\_start]Score (0-1) based on the overlap of unique words[cite: 4]. |
| **cosine\_similarity** | [cite\_start]Score (0-1) based on word frequency vectors[cite: 4]. |
| **bleu\_score** | Score (0-1) measuring response fluency and precision. |
| **rouge\_l\_score** | Score (0-1) measuring content recall (informational overlap). |
| **average\_similarity** | [cite\_start]The average of string, jaccard, and cosine similarities[cite: 5]. |
| **pass** | [cite\_start]`TRUE` or `FALSE` based on whether `average_similarity` is above the defined threshold (e.g., 0.75)[cite: 5]. |
| **error** | [cite\_start]Contains the error message if the script failed for a specific query[cite: 10]. |
