@service(supports_response = "optional")
def clear_todo_list(entity_id=None):
    # Get the to-do item service response
    todo_list = todo.get_items(entity_id=entity_id, return_response=True)

    # Put items in an iterable list
    summaries = [item["summary"] for item in todo_list["todo.search_results"]["items"]]

    # Remove each item
    removed_items = 0
    for summary in summaries:
        service.call(
            "todo", "remove_item", 
            entity_id=entity_id, 
            item=summary
            )
        removed_items += 1

    return {"removed_items": removed_items}