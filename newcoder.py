from flask import Flask, request

app = Flask(__name__)

@app.route('/out', methods=['POST'])
def receive_data():
    # Retrieve data from the request
    message = request.form['message']
    print(message)
    # You can process the message here as needed
    return "Message received", 200



if __name__ == '__main__':
    app.run(port=5000, debug=True)
