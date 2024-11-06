from flask import Flask, jsonify

app = Flask(__name__)

# Define the root endpoint
@app.route('/')
def home():
    return "It just works"

# Define the version endpoint
@app.route('/version')
def version():
    # The version is hard-coded here but should match the Docker image version
    app_version = "1.0.0"
    return app_version

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)