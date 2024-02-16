from flask import Flask, request, jsonify
from llm_gpt4_browser import BrowseWeb

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    search_term = data.get('search_term')
    if not search_term:
        return jsonify({'error': 'Missing search_term'}), 400

    try:
        browser = BrowseWeb()
        output = browser.main(search_term)
        return jsonify({'result': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
