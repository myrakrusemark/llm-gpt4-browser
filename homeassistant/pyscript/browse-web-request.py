import json
import requests
from datetime import datetime

server = "http://basement-server:5000/browseweb"

@service(supports_response = "optional")
def browse_web_request(search_results_entity="todo.search_results", browsing_results_entity="todo.browsing_results"):
    
    # Get the to-do item service response
    search_results_todo_list = todo.get_items(
        entity_id=search_results_entity,
        status="needs_action",
        return_response=True
        )
    
    # Put items in an iterable list
    search_results_todo_items = search_results_todo_list["todo.search_results"]["items"]
        
    search_results = []
    for search_results_todo_item in search_results_todo_items:
        search_results.append(json.loads(search_results_todo_item["description"]))
    search_results = {"search_results": search_results}
    
    #Create Browsing output todo item
    timestamp = datetime.now()
    clean_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    query = search_results["search_results"][0]["query"]
    todo.add_item(
        entity_id=browsing_results_entity, 
        item=query,
        description="Processing. Please wait..."
        )

    headers = {'Content-Type': 'application/json'}

    response = task.executor(requests.post,
        server, json=search_results, headers=headers,
        timeout=600
        )
        
    #Update Browsing Results todo item
    if response.status_code == 200:
        content = response.json().get('result', [])
        service.call(
            "todo", "update_item", 
            entity_id=browsing_results_entity, 
            item=query,
            description=str(content)
            )
        return {"response": content}

    else:
        service.call(
            "todo", "update_item", 
            entity_id=browsing_results_entity, 
            item=query,
            description="Failed to get output. Check core logs for any information and check your server."
            )
        log.error("Failed to fetch search results")
        return {"error": response}