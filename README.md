# credit-card-analysis
This is a course project of EECS E6893 Big Data Analytics at Columbia University.
```txt
├── README.md
├── dataset
│   ├── README.md
│   ├── application_record.csv
│   ├── credit_record.csv
│   ├── details_final.csv
│   ├── overdue_details.csv
│   └── preprocess.sql
├── flask
│   ├── app.py
│   ├── model_months/
│   ├── model_status/
│   ├── static
│   │   ├── bootstrap/
│   │   └── js
│   │       └── input.js
│   ├── templates
│   │   ├── about.html
│   │   ├── base.html
│   │   ├── contact
│   │   │   └── contact.html
│   │   ├── demo.html
│   │   ├── family
│   │   │   ├── children.html
│   │   │   ├── marriage.html
│   │   │   └── size.html
│   │   ├── general
│   │   │   ├── age_distribution.html
│   │   │   ├── education.html
│   │   │   └── gender.html
│   │   ├── income
│   │   │   ├── annual.html
│   │   │   └── income_category.html
│   │   ├── index.html
│   │   ├── input.html
│   │   ├── occupation
│   │   │   ├── days.html
│   │   │   ├── status.html
│   │   │   └── type.html
│   │   └── property
│   │       ├── house_type.html
│   │       └── property.html
│   ├── utils.py
│   └── visualization.py
├── machine learning
│   ├── CreditCard_MLPforMonths.ipynb
│   ├── CreditCard_MLPforStatus.ipynb
│   ├── Evaluate_MLPforBoth.ipynb
│   ├── README.md
│   ├── Utils.ipynb
│   ├── correlation.png
│   ├── hist_months.png
│   ├── model_months/
│   ├── model_status/
│   ├── training.png
│   └── training_months.png
├── requirements.txt
└── visualization
    ├── visualization.py
    ├── datasource
    │   └── details_final.csv
    └── html files...
```

# Process CSV files
Create a schema in mysql and load csv files in "./input" to mysql databases.

run **preprocess.sql** to do pre processing. 

export table overdue_details as a csv file.

...

# Deploy on Cloud Server
## 1. pre-requisite
```shell
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install git
sudo apt-get install wget
```
## 2. Install Python Environment
```shell
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
bash Anaconda3-2022.10-Linux-x86_64.sh
source ./anaconda3/bin/activate 
conda init
conda create -n flask python=3.7
conda activate flask
```
## 3. Install Project
```shell
git clone https://github.com/youthtoday/credit-card-analysis.git
```
## 4. Install Requirements
```
cd credit-card-analysis
pip install -r requirements.txt 
```
## 5. Run Project
```shell
cd flask
python app.py
```
