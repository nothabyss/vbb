from flask import *
import datalayer.enc as enc
app=Flask("block")
app.config.from_object(app.config)

# @app.route("/")
# def hello():
#     return "hello world"

@app.route('/')
def index():
    data = enc.rsakeys()
    response = make_response(jsonify(data), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
app.run()
