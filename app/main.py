# Thank you https://towardsdatascience.com/creating-restful-apis-using-flask-and-python-655bad51b24
import time

from flask import Flask, request, jsonify
from plover import PloverDB

app = Flask(__name__)
print("Starting to load data..")
start = time.time()
plover = PloverDB(is_test=True)
print(f"Finished loading data. Took {round((time.time() - start) / 60, 1)} minutes.")


@app.route('/query/', methods=['POST'])
def run_query():
    query = request.json
    answer = plover.answer_query(query)
    return jsonify(answer)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2244)
