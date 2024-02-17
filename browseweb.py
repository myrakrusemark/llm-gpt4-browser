import logging
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from openai import OpenAI
import yaml
import requests

logging.getLogger('selenium').setLevel(logging.ERROR)
logging.getLogger('webdriver').setLevel(logging.ERROR)

class BrowseWeb:
    def __init__(self):
        # Initialize Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')

        # Add other options to mimic human behavior
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        self.secrets = self.load_secrets('secrets.yaml')

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.openai_client = OpenAI(api_key=self.secrets['openai_api_key'])

    def main(self, search_results, query="None"):
        if len(search_results) and query != "None":

            passage_summaries = []
            for i, passage in enumerate(search_results):
                url = search_results[i]['url']
                label = f"\n-------------------------\n({i+1} of {len(search_results)}) - Browsing {search_results[i]['title']}({url}) - {search_results[i]['snippet']}\n"
                passages, _ = self.get_webpage_content(url)

                relevant_passages = []
                for j, passage in enumerate(passages, start=1):
                    relevant_content = self.find_relevant_content(passage, query)
                    if relevant_content:
                        print(f"Analyzing passage {j} of {len(passages)}. {len(relevant_content)} relevant passages found.")
                        relevant_passages.append(relevant_content)  # Append all relevant sections
                    else:
                        print(f"Analyzing passage {j} of {len(passages)}. No relevant passages found.")

                if not relevant_passages:
                    return "Server error: No relevant passages found. Try a different query maybe?"
            
                # Format the prompt as a single user message
                print("\nGenerating output(s)...")
                #If returned passages are too long for the context window, split them up and summarize them separately.
                parts = self.split_text(passage)
                for part in parts:
                    print("...")
                    prompt = f"Relevant text:\n{part}\nSearch term: {query}\n"
                    prompt += "Please provide output in context of the search term."
                    prompt += "The output may be in the form of a summary, or more detailed data. Let the context of the search term dictate how detailed your output should be."
                    response_text = self.make_openai_request(prompt, "plain_text", "gpt-4")
                    passage_summaries.append(label+response_text)

            print("\nGenerating final output...\n")
            passage_summaries_string = "\n".join(passage_summaries)
            prompt = f"Website outputs in context of the search term:\n"
            prompt += passage_summaries_string+"\n\n"
            prompt += "-------------------------"
            prompt += "\nSearch term: "+query
            prompt += "\nThe passages above are outputs from the associated web pages in context of the search term."
            prompt += "\nPlease combine the outputs into a single response that satisfies the context of the search term."

            response_text = self.make_openai_request(prompt, "plain_text", "gpt-4")
            print(response_text)
            return response_text
        else:
            return "Server error: Missing Information. Search Results: "+len(search_results)+" Query: "+query
    
    def load_secrets(self, file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    
    def google_search(self, query):
        # Your API key and custom search engine ID
        google_cse_key = self.secrets['google_cse_key']
        google_cse_id = self.secrets['google_cse_id']
        
        # Construct the URL for the Google Custom Search JSON API
        search_url = f"https://customsearch.googleapis.com/customsearch/v1?key={google_cse_key}&cx={google_cse_id}&q={query}&num=3"
        
        # Make the request
        print(f"Searching Google ({query})...")
        response = requests.get(search_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            search_results = response.json().get('items', [])
            output = []
            for result in search_results:
                output.append({
                    "title": result.get('title'),
                    "url": result.get('link'),
                    "snippet": result.get('snippet')
                })
            
            # Convert the list to a JSON string and print it
            #print(output)
            return output
        else:
            print("Failed to fetch search results")
            return None

    def split_text(self, text, max_length=3000):
        # Splits the text into parts no longer than max_length
        parts = []
        while len(text) > max_length:
            part = text[:max_length]
            last_space = part.rfind(' ')
            if last_space != -1:
                parts.append(text[:last_space])
                text = text[last_space+1:]
            else:  # No spaces found, force split
                parts.append(text[:max_length])
                text = text[max_length:]
        parts.append(text)  # Add the remaining part
        return parts

    def get_webpage_content(self, url):
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            full_text = self.driver.find_element(By.TAG_NAME, "body").text
            # Tokenization placeholder - actual tokenization to define passage size
            passages = self.chunk_text(full_text, 1500)
            return passages, full_text
        except Exception as e:
            return [], ""

    def chunk_text(self, text, chunk_size):
        # Simple placeholder for chunking text into passages
        words = text.split()
        passages = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
        return passages

    def find_relevant_content(self, passage, query):
        # Format the prompt as a single user message
        prompt = f"Passage: \"{passage}\"\n"
        prompt += f"Search term: \"{query}\"\n"
        prompt += "Identify the relevant sections. Return start and end excerpts that match the start and end of the relevant sections, about 30 characters long.\n"
        prompt += "Keep the start and end excerpts concise and short! Only about 30 characters long! They are only used for matching purposes.\n"
        prompt += "JSON format:\n"
        prompt += "{sections:[{'start': 'copy of start text', 'end': 'copy of end text'}]}"
        prompt += "Sections can have as many list items as you need."

        response_text = self.make_openai_request(prompt, "json_object", "gpt-3.5-turbo-0125")
        try:
            return self.extract_relevant_parts(json.loads(response_text), passage)
        except Exception as e:
            print(f"Error extracting relevant parts: {e}")
            return None

    def make_openai_request(self, prompt, response_format='json_object', model="gpt-3.5-turbo-0125"):
        context = [
            {
                "role": "system",
                "content": "You are a highly intelligent assistant who can understand and analyze text passages."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        try:
            if response_format == "json_object":
                response = self.openai_client.chat.completions.create(
                    model=model,
                    response_format={ "type": "json_object" },
                    messages=context,
                    temperature=0.3,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
            else:
                response = self.openai_client.chat.completions.create(
                    model=model,
                    messages=context,
                    temperature=0.3,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
            # Assuming the response will contain the JSON string directly in the message content
            # Extract the JSON string from the last message of the response
            if response.choices:
                #print(response.choices[0].message.content)
                return response.choices[0].message.content
            else:
                print("No content in response message.")
                return None
        except Exception as e:
            print(f"Error during OpenAI API call: {e}")
            return None

    def extract_relevant_parts(self, response_data, passage):
        try:
            relevant_sections = []
            for section in response_data['sections']:
                start_text, end_text = section['start'], section['end']
                start_index = passage.find(start_text)
                end_index = passage.find(end_text) + len(end_text)
                if start_index != -1 and end_index != -1:
                    relevant_section = passage[start_index:end_index]
                    #print(relevant_section)
                    relevant_sections.append(relevant_section)
            return relevant_sections
        except Exception as e:
            print(f"Error extracting relevant parts: {e}")
            return None


if __name__ == "__main__":
    query = "aldi deals"

    browser = BrowseWeb()
    search_results = browser.google_search(query)
    output = browser.main(search_results, query)