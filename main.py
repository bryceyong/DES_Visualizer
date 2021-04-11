from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')

def main():
##

    i = 2
    j = 2
    k = i + j
    return render_template('index.html', i=i, j=j, k=k)

##
if __name__ == '__main__':
    app.run()