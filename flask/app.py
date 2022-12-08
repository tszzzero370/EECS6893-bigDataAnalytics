from datetime import datetime

from flask import Flask, render_template, request

app = Flask(__name__)


# Path and View
# @app.route('Path')
# def function():
#     View

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/general')
def general():
    if request.url.split('=')[1] == 'age':
        return render_template("age_distribution.html")
    elif request.url.split('=')[1] == 'gender':
        return render_template('gender.html')
    elif request.url.split('=')[1] == 'education':
        return render_template('education.html')
    else:
        return hello_world


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


@app.route('/predict')
def input():
    return render_template('input.html')


@app.route('/get_input')
def get_input():
    birthday = request.args.get("birthday") #2022-12-05
    age = datetime.today() - datetime.strptime(birthday, '%Y-%m-%d')
    gender = int(request.args.get("gender"))
    education = int(request.args.get("education"))
    car = int(request.args.get("car"))
    realty = int(request.args.get("realty"))
    housing = int(request.args.get("housing"))
    family = int(request.args.get("family"))
    marital = int(request.args.get("marital"))
    children = int(request.args.get("children"))
    income_type = int(request.args.get("income_type"))
    occupation = int(request.args.get("occupation"))
    income = int(request.args.get("income"))
    employ_date = request.args.get("employ_date") #2022-12-05
    employ_age = datetime.today() - datetime.strptime(employ_date, '%Y-%m-%d')
    mobile = int(request.args.get("mobile"))
    work_phone = int(request.args.get("work_phone"))
    fixed_line = int(request.args.get("fixed_line"))
    email = int(request.args.get("email"))

    result = {"prediction": True, "possibility": 0.8}
    return result

# def model_1():
#     return p
#
# def model_2():
#     return p

if __name__ == '__main__':
    app.run(host='0.0.0.0')
