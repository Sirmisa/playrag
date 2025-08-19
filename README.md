Of course. The `README.md` I provided should have been free of any citation tags, but I'm happy to provide the clean version again to ensure you have what you need.

Here is the complete, clean `README.md` file without any citations.

-----

# RAG Agent UI Evaluation Framework

This project provides an automated framework for testing and evaluating the responses of a Retrieval-Augmented Generation (RAG) agent through its web user interface. It uses Playwright to simulate user interactions and calculates a suite of metrics to compare the agent's actual responses against a predefined set of "ground truth" answers.

-----

## Features

  * **Automated UI Testing**: Uses Playwright to automatically open a browser, navigate to the RAG agent's UI, submit queries, and retrieve responses.
  * **Batch Processing**: Reads queries and expected responses from a CSV file, allowing for batch evaluation of multiple test cases.
  * **Comprehensive Evaluation Metrics**: Calculates a variety of metrics to provide a nuanced view of response quality:
      * **Exact Match**: Checks for a perfect match after text normalization.
      * **Lexical Similarity**:
          * String Similarity (SequenceMatcher)
          * Jaccard Similarity (word overlap)
          * Cosine Similarity (bag-of-words vector comparison)
      * **NLP-Based Metrics**:
          * **BLEU Score**: Measures fluency and n-gram precision.
          * **ROUGE-L Score**: Measures recall of the most important content.
  * **Detailed Reporting**: Generates a CSV report containing the query, expected response, actual response, and all calculated scores for each test case.
  * **Summary Statistics**: Prints a summary of the overall accuracy and average scores for all metrics to the console after the run is complete.

-----

## Prerequisites

  * Python 3.7+
  * pip (Python package installer)

-----

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

-----

## Configuration

Before running the script, you must update the configuration variables at the top of the Python file.

  * `RAG_UI_URL`: The URL of the web interface for your RAG agent.
  * `INPUT_SELECTOR`: The CSS selector for the text input field where queries are typed (e.g., `'textarea[id="prompt-input"]'`).
  * `SUBMIT_SELECTOR`: The CSS selector for the submit button to be clicked.
  * `RESPONSE_SELECTOR`: The CSS selector for the HTML element that contains the RAG agent's final response text.
  * `GROUND_TRUTH_FILE`: The name of the input CSV file (default is `'ground_truth.csv'`).
  * `REPORT_FILE`: The name of the output report file (default is `'evaluation_report.csv'`).
  * `headless`: In the `p.chromium.launch()` function, set `headless=True` to run the browser in the background or `headless=False` to watch it run in real-time.

-----

## Usage

### 1\. Create the Ground Truth File

Create a CSV file named `ground_truth.csv` (or the name you configured in `GROUND_TRUTH_FILE`). It must contain two columns: `query` and `expected_response`.

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

The script will print the progress for each query to the console.

-----

## Understanding the Output

### Console Output

After the script finishes, a summary of the results will be printed to your console:

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
| **query** | The original question sent to the agent. |
| **expected** | The ground truth answer from your CSV file. |
| **actual** | The raw response received from the agent. |
| **exact\_match** | `TRUE` or `FALSE` if the normalized responses are identical. |
| **string\_similarity** | Score (0-1) based on character-level similarity. |
| **jaccard\_similarity** | Score (0-1) based on the overlap of unique words. |
| **cosine\_similarity** | Score (0-1) based on word frequency vectors. |
| **bleu\_score** | Score (0-1) measuring response fluency and precision. |
| **rouge\_l\_score** | Score (0-1) measuring content recall (informational overlap). |
| **average\_similarity** | The average of string, jaccard, and cosine similarities. |
| **pass** | `TRUE` or `FALSE` based on whether `average_similarity` is above the defined threshold (e.g., 0.75). |
| **error** | Contains the error message if the script failed for a specific query. |
