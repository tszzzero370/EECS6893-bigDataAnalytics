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
        return render_template("general/age_distribution.html")
    elif request.url.split('=')[1] == 'gender':
        return render_template('general/gender.html')
    elif request.url.split('=')[1] == 'education':
        return render_template('general/education.html')
    else:
        return hello_world


@app.route('/property')
def property():
    if request.url.split('=')[1] == 'property':
        return render_template("property/property.html")
    elif request.url.split('=')[1] == 'housing_type':
        return render_template('property/house_type.html')
    else:
        return hello_world


@app.route('/family')
def family():
    if request.url.split('=')[1] == 'marriage':
        return render_template("family/marriage.html")
    elif request.url.split('=')[1] == 'children':
        return render_template('family/children.html')
    elif request.url.split('=')[1] == 'size':
        return render_template('family/size.html')
    else:
        return hello_world


@app.route('/contact')
def contact():
    pass

@app.route('/occupation')
def occupation():
    if request.url.split('=')[1] == 'type':
        return render_template("occupation/type.html")
    elif request.url.split('=')[1] == 'status':
        return render_template('occupation/status.html')
    else:
        return hello_world

@app.route('/income')
def income():
    if request.url.split('=')[1] == 'annual':
        return render_template("income/annual.html")
    elif request.url.split('=')[1] == 'category':
        return render_template('income/income_category.html')
    else:
        return hello_world

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/predict')
def input():
    return render_template('input.html')


@app.route('/get_input')
def get_input():
    birthday = request.args.get("birthday")  # 2022-12-05
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
    employ_date = request.args.get("employ_date")  # 2022-12-05
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
