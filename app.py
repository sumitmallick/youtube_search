import flask
from flask import request, jsonify
from youtube_search import YoutubeSearch
from datetime import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
all_data = []


@app.route('/', methods=['GET'])
def home():
    return '''<h1>YouTube Search API</h1>
<p>A prototype API for searching for youtube feeds.</p>'''


@app.route('/api/v1/youtube/search/all', methods=['GET'])
def api_all():
    return jsonify(all_data)


@app.route('/api/v1/youtube/search/', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'search' in request.args:
        search = str(request.args['search'])
    else:
        return "Error: No search field provided. Please specify an id."

    # Create an empty list for our results
    final_results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    results = YoutubeSearch('music', max_results=10).to_dict()
    if results:
        temp = list(results)
        valid_list = []
        for temp in temp:
            print(temp['duration'])
            if temp['duration']!=0:
                valid_list.append(temp)
        sortedArray = sorted(
            valid_list,
            key=lambda x: datetime.strptime(str(x['duration']), '%M:%S'), reverse=True
        )
        final_results.extend(sortedArray)
    all_data.extend(final_results)
    # for book in final_results:
    #     if book['id'] == id:
    #         results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify({"result": final_results, "comment": "This result doesn't includes live videos as it's duration time is 0 till it's live"})

app.run()