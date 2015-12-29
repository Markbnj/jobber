from flask import Flask
from redis import StrictRedis

app = Flask(__name__)

@app.route('/jobs/', methods=['GET', 'POST'])
def jobs(job=None):
    return "Get job descriptions here."

if __name__ == "__main__":
    rd = StrictRedis(host='localhost', port=6379)
    app.run()