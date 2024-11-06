from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "It just works"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)