from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/ideas/<subGroupId>', methods=['GET'])
def get_data():
    # Here you can add the functionality you want.
    # For example, let's return a simple JSON response.
    data = {"key": "value"}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)