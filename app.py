from flask import Flask, render_template


app = Flask(__name__) 

#home page
@app.route("/")  
def index():
    return render_template("index.html")

if __name__ in "__main__":
    app.run(debug=True, port = 5001)