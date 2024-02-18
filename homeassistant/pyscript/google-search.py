import requests
import yaml
import json

@service
def google_search(search_query, user_input):

    # Your API key and custom search engine ID
    google_cse_key = "google_cse_key"
    google_cse_id = "google_cse_id"
    
    # Construct the URL for the Google Custom Search JSON API
    search_url = f"https://customsearch.googleapis.com/customsearch/v1?key={google_cse_key}&cx={google_cse_id}&q={search_query}&num=3"
    
    # Make the request
    log.info(f"Searching Google ({search_query})...")
    response = task.executor(requests.get, search_url)

    # Check if the request was successful
    if response.status_code == 200:
        search_results = response.json().get('items', [])
        output = []
        for result in search_results:
            search_result_info = {
                "title": result.get('title'),
                "url": result.get('link'),
                "snippet": result.get('snippet'),
                "search_query": search_query,
                "user_input": user_input
            }
            json_str = json.dumps(search_result_info, ensure_ascii=False)
            todo.add_item(
                entity_id="todo.search_results", 
                item=result.get('title'),
                description=json_str
                )
    else:
        log.error("Failed to fetch search results")
