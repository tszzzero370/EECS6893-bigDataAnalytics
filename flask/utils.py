import numpy as np
import tensorflow as tf


def onehot(y, K):
    """
        One-hot encoding function.
        Inputs
        - y: (uint8) a numpy array of shape (N, 1) containing labels; y[i] = k means
            that X[i] has label k, where 0 <= k < K.
        - K: total number of classes
        Returns a numpy array
        - y_onehot: (float) the encoded labels of shape (N, K)
        """
    N = y.shape[0]  # get input size
    y_onehot = np.zeros((N, K))  # initialize onehot array
    for i in range(N):
        y_onehot[i, y[i].astype(int)] = 1  # put a "1" in its place (y[i]) as label

    return y_onehot


def sigmoid(x):
    y = 1 / (1 + np.exp(-x))
    return y


def activation(y):
    """
        modded sigmoid function
        Input
        - y: (float) output of the classifier, shape 1X2
            [1, 0] => no overdue
            [0, 1] => potential overdue
        Return
        - pred: (int) prediction, scalar
            0 => potential credit card
            1 => no credit card
        - poss: (float) possibility of getting a credit card
        """
    if y[0, 0] >= y[0, 1]:
        pred = 0  # give prediction
        poss = sigmoid(y[0, 0] * 2)
    else:
        pred = 1  # give prediction
        poss = 1 - sigmoid(y[0, 1] * 2)
    return pred, poss


def get_prob(input_encoded):
    # reload model
    model_status = tf.keras.models.load_model('model_status')
    # "model_status" is a folder, and it should be the same place as the app.py
    model_status.summary()  # Check architecture, can be omitted when deployed

    # reload the second model
    model_months = tf.keras.models.load_model('model_months')
    # "model_months" is a folder, and it should be the same place as the app.py
    model_months.summary()  # Check architecture, can be omitted when deployed

    P_status = activation(model_status.predict(input_encoded.reshape(1, 52)))[1]
    P_months = activation(model_months.predict(input_encoded.reshape(1, 52)))[1]
    P = P_status * 3/5 + P_months * 1/10  # weighted average
    return P


def get_encoded(gender, car, realty, children, income, age, employ_age, mobile, work_phone, fixed_line, email, family,
                income_type, housing, education, marital, occupation):
    input_encoded = np.zeros(52)
    # 12 features [0:12]
    input_encoded[0] = gender
    input_encoded[1] = car
    input_encoded[2] = realty
    input_encoded[3] = children
    input_encoded[4] = income
    input_encoded[5] = age
    input_encoded[6] = employ_age
    input_encoded[7] = mobile
    input_encoded[8] = work_phone
    input_encoded[9] = fixed_line
    input_encoded[10] = email
    input_encoded[11] = family
    # income type [12:16]
    input_encoded[12 + income_type] = 1
    # housing type [17:22]
    input_encoded[17 + housing] = 1
    # education type [23:27]
    input_encoded[23 + education] = 1
    # family status [28:32]
    input_encoded[28 + marital] = 1
    # occupation type [33:51]
    input_encoded[33 + occupation] = 1

    return input_encoded

def normalization(children, income, age, employ_age, family):
    # normalization
    # ['CNT_CHILDREN']
    min_children = 0
    max_children = 19
    children = (children - min_children) / (max_children - min_children)

    # ['AMT_INCOME_TOTAL']
    min_income = 0
    max_income = 157500
    income = (income - min_income) / (max_income - min_income)

    # ['DAYS_BIRTH']
    min_age = -25152
    max_age = -7489
    age = (age - min_age) / (max_age - min_age)

    # ['DAYS_EMPLOYED']
    min_work = -15713
    max_work = 0
    employ_age = (employ_age - min_work) / (max_work - min_work)

    # ['CNT_FAM_MEMBERS']
    min_family = 1
    max_family = 20
    family = (family - min_family) / (max_family - min_family)

    return children, income, age, employ_age, family
