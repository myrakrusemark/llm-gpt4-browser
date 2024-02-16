# GPT4 Powered Web Browser for LLMs

## Overview
The BrowseWeb script is a Python script designed to automate the process of searching the web, retrieving, and summarizing information based on a specific search term. It integrates several technologies, including Selenium for web automation, OpenAI's GPT models for text analysis and summarization, and Google Custom Search Engine (CSE) for fetching relevant web pages. This script is particularly useful for processing large amounts of textual information and condensing it into actionable insights.

## Features
- **Automated Web Browsing**: Uses Selenium with a headless Chrome browser to navigate the web.
- **Dynamic Content Handling**: Capable of interacting with JavaScript-rendered content thanks to Selenium.
- **Intelligent Text Analysis**: Leverages OpenAI's GPT models to analyze and summarize the content.
- **Google Custom Search**: Incorporates Google CSE to perform targeted web searches.
- **Configurable**: Allows customization through `secrets.yaml` for API keys and other sensitive information.

## Prerequisites
Before running the BrowseWeb script, ensure you have the following installed and configured:
- Python 3.8 or higher
- Selenium WebDriver
- `webdriver-manager` for automatic driver management
- OpenAI Python library
- `requests` for making HTTP requests
- `pyyaml` for YAML file handling

Additionally, you need:
- An OpenAI API key for accessing GPT models.
- A Google Cloud Platform (GCP) account with Custom Search Engine (CSE) setup and an API key.

## Installation
1. **Clone the repository**:
   ```sh
   git clone <repository-url>
   ```
2. **Install required Python packages**:
   ```sh
   pip install selenium webdriver-manager openai requests pyyaml
   ```
3. **Configure your secrets**:
   Create a `secrets.yaml` file in the root directory of the script with the following structure:
   ```yaml
   openai_api_key: "YOUR_OPENAI_API_KEY"
   google_cse_key: "YOUR_GOOGLE_CSE_API_KEY"
   google_cse_id: "YOUR_GOOGLE_CSE_ID"
   ```
   Replace the placeholders with your actual API keys.

## Usage
To use the BrowseWeb script, navigate to the script's directory and run:
```sh
python browse_web.py
```
You can modify the `request` variable inside the `if __name__ == "__main__":` block to search for different terms.

## Limitations
- The script is heavily reliant on external services (OpenAI, Google CSE), and any changes to their APIs or rate limits may affect functionality.
- Web scraping with Selenium may break if the target websites update their layouts or implement measures to block automated browsing.

## Disclaimer
This script is intended for educational and research purposes. Ensure you comply with the terms of service of all utilized APIs and respect websites' `robots.txt` policies to avoid unauthorized data scraping.

## Contribution
Contributions are welcome. Please create an issue or pull request if you have suggestions for improvements or bug fixes.

## License
GPL