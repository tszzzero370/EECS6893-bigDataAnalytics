from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/age')
def age():
    return render_template("age_distribution.html")

@app.route('/gender')
def gender():
    return render_template('gender.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/families')
def families():
    return render_template("families_OverDue.html")

@app.route('/income')
def income():
    return render_template('meanIncome_OverDue.html')

@app.route('/past_due')
def past_due():
    return render_template('pastDue_OverDue.html')

@app.route('/real_estate')
def real_eastate():
    return render_template('realestateLoans_OverDue.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
