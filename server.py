from flask import Flask, request, jsonify
from browseweb import BrowseWeb

app = Flask(__name__)

"""
Example 
curl --location "http://127.0.0.1:5000/browseweb" --header "Content-Type: application/json" --data "{\"search_results\":[{\"title\":\"OpenAI\",\"url\":\"https://openai.com\",\"snippet\":\"OpenAI is an AI research and deployment company.\", \"query\": \"copyright\"},{\"title\":\"Wikipedia\",\"url\":\"https://wikipedia.org\",\"snippet\":\"Wikipedia is a free online encyclopedia, created and edited by volunteers around the world.\", \"query\": \"copyright\"},{\"title\":\"GitHub\",\"url\":\"https://github.com\",\"snippet\":\"GitHub is a development platform inspired by the way you work.\", \"query\": \"copyright\"}]}"
"""

@app.route('/browseweb', methods=['POST'])
def search():
    data = request.json
    print(data)
    search_results = data.get('search_results')
    query = search_results[0]['query']

    print(search_results)
    if not search_results:
        return jsonify({'error': 'Missing search_results'}), 400

    try:
        browser = BrowseWeb()
        output = browser.main(search_results, query)
        return jsonify({'result': output})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)