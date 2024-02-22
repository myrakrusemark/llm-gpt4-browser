from flask import Flask, request, jsonify
from browseweb import BrowseWeb
import threading

app = Flask(__name__)

def async_browse(search_results, title, search_query, user_input):
    try:
        browser = BrowseWeb()
        browser.main(search_results, title, search_query, user_input)
    except Exception as e:
        print(e)  # Logging the error; in real-world scenarios, consider logging this to a file or external logging service.

@app.route('/browseweb', methods=['POST'])
def search():
    data = request.json
    if not data or 'search_results' not in data:
        return jsonify({'error': 'Missing search_results'}), 400
    
    search_results = data['search_results']
    title = data['title']
    search_query = data['search_query']
    user_input = data['user_input']

    if not search_results:
        return jsonify({'error': 'Empty search_results'}), 400

    # Start the browse function in a separate thread
    threading.Thread(target=async_browse, args=(search_results, title, search_query, user_input)).start()

    # Immediately return a success message
    return jsonify({'message': 'Search initiated successfully'}), 202

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
