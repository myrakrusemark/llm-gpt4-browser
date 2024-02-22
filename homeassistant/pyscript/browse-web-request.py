import json
import requests
from datetime import datetime
import time

server = "http://basement-server:5000/browseweb"

@service
def browse_web_request(
    search_results_entity="todo.search_results", 
    browsing_results_entity="todo.browsing_results",
    title="Empty",
    search_query="Empty",
    user_input="Empty"
    ):
        
    # Create Browsing output todo item
    todo.add_item(
        entity_id=browsing_results_entity, 
        item=title,
        description="Sending request..."
        )
    
    # Get the to-do item service response
    search_results_todo_list = todo.get_items(
        entity_id=search_results_entity,
        status="needs_action",
        return_response=True
        )

    # Get the search result items. The last one in the list is the latest
    #Format the payload
    for item in search_results_todo_list["todo.search_results"]["items"]:
        if item["summary"] == title:
            search_results_todo_items = {
                "search_results": json.loads(item["description"]),
                "title": title,
                "search_query": search_query,
                "user_input": user_input
                }
                
    headers = {'Content-Type': 'application/json'}
    max_retries = 10
    attempt = 0

    while attempt < max_retries:
        try:
            response = task.executor(requests.post,
                server, json=search_results_todo_items, headers=headers,
                timeout=5
                )
            if response.status_code == 202:
                service.call(
                    "todo", "update_item", 
                    entity_id=browsing_results_entity, 
                    item=title,
                    description="Request sent successfully. Processing..."
                    )
                break
            elif response.status_code == 500:
                #Update item with failure
                service.call(
                    "todo", "update_item", 
                    entity_id=browsing_results_entity, 
                    item=title,
                    description="Attempt #"+str(attempt+1) + "Server error 500."
                    )
                if attempt == max_retries:
                    # Update item with failure after max retries
                    service.call(
                        "todo", "update_item", 
                        entity_id=browsing_results_entity, 
                        item=title,
                        description="Failed after maximum retries. Server error 500."
                        )
                    log.error("Failed after maximum retries. Server error 500.")
                    return {"error": "Failed after maximum retries. Server error 500."}
                continue
            else:
                # Update Browsing Results todo item with different error
                service.call(
                    "todo", "update_item", 
                    entity_id=browsing_results_entity, 
                    item=title,
                    description="Attempt #" + str(attempt+1) + "Failed to get output. Status code: " + str(response.status_code)
                    )
                log.error("Failed to fetch search results. Status code: " + str(response.status_code))
                return {"error": "Unexpected status code: " + str(response.status_code)}
        except Exception as e:
            attempt += 1
            if attempt == max_retries:
                # Update item with failure after max retries due to exception
                service.call(
                    "todo", "update_item", 
                    entity_id=browsing_results_entity, 
                    item=title,
                    description="Attempt #" + str(attempt+1) + " - Exception: " + str(e)
                    )
                log.error("Failed after maximum retries due to exception: " + str(e))
                return {"error": "Failed after maximum retries due to exception: " + str(e)}
        attempt += 1
