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
        'srlimit': limit  # Set the limit to the desired number of results
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    results = []
    if 'query' in data and 'search' in data['query']:
        for search_result in data['query']['search']:
            title = search_result['title']
            snippet = search_result['snippet']
            page_id = search_result['pageid']
            # Clean the snippet to remove HTML tags
            # print(snippet)
            # print() 
            cleaned_snippet = re.sub(r'<.*?>', '', snippet)
            results.append({
                'title': title,
                'snippet': cleaned_snippet,
                'url': f"https://en.wikipedia.org/?curid={page_id}"
            })
    
    return results

@app.route('/search_wikipedia', methods=['POST'])
def search_wikipedia_endpoint():
    # Get the JSON data from the request
    data = request.json
    print(data)

    if not data or 'query' not in data:
        return jsonify({'error': 'Missing "query" in request body'}), 400
    
    query = data['query']
    print(query)
    limit = data.get('limit', 10)  # Optional limit parameter, defaults to 10
    
    # Perform the search
    results = search_wikipedia(query, limit)
    
    # Return the results as a JSON response
    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
