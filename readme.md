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


## Server Functionality for BrowseWeb

### Introduction
The BrowseWeb script now includes server functionality, allowing users to send search requests via HTTP and receive summarized information directly. This feature utilizes Flask, a lightweight WSGI web application framework, to handle HTTP requests.

### Setup
To enable the server functionality, ensure you have Flask installed alongside the other dependencies:
```sh
pip install Flask
```

### Running the Server
1. **Start the server** by running the server script:
   ```sh
   python server.py
   ```
   This script initializes a Flask server that listens for POST requests with search terms.

2. **Send a request** to the server using `curl` or any HTTP client:
   ```sh
   curl -X POST http://localhost:5000/search -H "Content-Type: application/json" -d "{\"search_term\":\"your search term here\"}"
   ```
   Replace `your search term here` with the term you wish to search for.

### Server Endpoints
- `/search` (POST): Accepts JSON payload with a `search_term` key. Returns a summarized response based on the search term provided.

### Example Request
```json
{
  "search_term": "example search term"
}
```

### Response
The server returns a JSON response containing the summarized information fetched and processed by the BrowseWeb script. The structure of the response may vary depending on the search results and summarization.

### Customization
You can customize the Flask server by modifying `server.py`. This includes changing the port, adding new endpoints, or altering request handling logic.

### Limitations
- The server relies on the proper configuration of the BrowseWeb script and its dependencies.
- Ensure your server environment is secure, especially if exposing the server to public networks.

### Disclaimer
The server functionality is intended for educational and research purposes. Ensure compliance with all applicable laws and regulations, including data protection and privacy laws.


## Limitations
- The script is heavily reliant on external services (OpenAI, Google CSE), and any changes to their APIs or rate limits may affect functionality.
- Web scraping with Selenium may break if the target websites update their layouts or implement measures to block automated browsing.

## Disclaimer
This script is intended for educational and research purposes. Ensure you comply with the terms of service of all utilized APIs and respect websites' `robots.txt` policies to avoid unauthorized data scraping.

## Contribution
Contributions are welcome. Please create an issue or pull request if you have suggestions for improvements or bug fixes.

## License
GPL