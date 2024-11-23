from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def search_wikipedia(query, limit=10):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': query,
        'format': 'json',
        'utf8': 1,
        'srlimit': limit  
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    results = []
    if 'query' in data and 'search' in data['query']:
        for search_result in data['query']['search']:
            title = search_result['title']
            snippet = search_result['snippet']
            page_id = search_result['pageid']
          
            cleaned_snippet = re.sub(r'<.*?>', '', snippet)
            results.append({
                'title': title,
                'snippet': cleaned_snippet,
                'url': f"https://en.wikipedia.org/?curid={page_id}"
            })
    
    return results

@app.route('/search_wikipedia', methods=['GET'])
def search_wikipedia_endpoint():
  
    query = request.args.get('query')
    limit = request.args.get('limit', default=10, type=int)  
    
    if not query:
        return jsonify({'error': 'Missing "query" parameter'}), 400
    
    results = search_wikipedia(query, limit)
    
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
