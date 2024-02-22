import requests

search_query = "search"
user_input = "test results"


url = "http://homeassistant:8123/api/services/todo/update_item"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjYTFkMGIwMTVjY2Y0YzQ5OTdiMTc3NGExMWY1MTZlZCIsImlhdCI6MTcwODM1MzIzMSwiZXhwIjoyMDIzNzEzMjMxfQ.Olw8vML8DClsTSKKcgYxwAYrUee9MKUnXTDAjCxh14U",
    "content-type": "application/json",
}
data = {
    "entity_id": "todo.browsing_results",
    "item": "test",
    "description": "desc"
}

response = requests.post(url, headers=headers, json=data)
print(response.text)