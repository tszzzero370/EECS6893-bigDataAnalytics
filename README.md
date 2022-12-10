# credit-card-analysis
This is a course project of EECS E6893 Big Data Analytics at Columbia University.
```txt
├── README.md
├── analysis_demo.ipynb
├── flask
│   ├── app.py
│   ├── screenshot
│   │   └── education.png
│   ├── static
│   │   └── bootstrap
│   │       └── bootstrap.5.2.2.min.css
│   └── templates
├── input
│   ├── README.md
│   ├── application_record.csv
│   ├── credit_record.csv
│   ├── details_final.csv
│   └── overdue_details.csv
├── requirements.txt
└── visualization
    ├── by_general
    │   ├── age&gender
    │   │   ├── age_distrbtn.html
    │   │   ├── female_pie.html
    │   │   └── male_pie.html
    │   └── education
    │       ├── education_distrbtn.html
    │       ├── pie_edu_overdue.html
    │       └── pie_edu_paidOff.html
    └── by_propertyOwning
        └── property
```

## Generate overdue_details.csv
Create a schema in mysql and load csv files in "./input" to mysql databases.

run **preprocess.sql** to do pre processing. 

export table overdue_details as a csv file.


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
cd credit-card-analysis/flask
pip install -r requirements.txt 
```
## 5. Run Project
```shell
python app.py
```
