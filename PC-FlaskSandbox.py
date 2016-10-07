from flask import Flask, render_template

app = Flask("Ninja Money Game")


@app.route('/')
def hello_world():
    x = "Casino"
    return render_template("index.html", show=x)

if __name__ == '__main__':
    app.run()
