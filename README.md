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
Operate in mysql database console.

export table overdue_details as a csv file.

## Generate html files
run
```shell
pip install -r requirements.txt
```
run analysis.py
```shell
python analysis.py
```
