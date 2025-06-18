from flask import Flask, render_template, request, redirect


app = Flask(__name__) 

#home page
@app.route("/", methods = ["POST", "GET"])  
def index():
    if request.method == "POST":
        city = request.form["city"]
        print(f"\nYou chose: {city}")
    return render_template("index.html")

if __name__ in "__main__":
    app.run(debug=True, port = 5001)