from flask import Flask, request, jsonify
from flask_cors import CORS
from src.main import answer_query

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    response = answer_query(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
