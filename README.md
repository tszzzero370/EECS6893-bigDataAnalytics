# credit-card-analysis
This is a course project of EECS E6893 Big Data Analytics at Columbia University.

## Generate overdue_details.csv
Create a schema in mysql and load csv files in "./input" to mysql databases.
Operate in mysql database console.
```sql
update credit_record set STATUS=REPLACE (STATUS,'0','1');
update credit_record set STATUS=REPLACE (STATUS,'2','1');
update credit_record set STATUS=REPLACE (STATUS,'3','1');
update credit_record set STATUS=REPLACE (STATUS,'4','1');
update credit_record set STATUS=REPLACE (STATUS,'5','1');
update credit_record set STATUS=REPLACE (STATUS,'X','0');
update credit_record set STATUS=REPLACE (STATUS,'C','0');

create table overdue as
select a.id, overdue_freq, overdue_times from
(select id, avg(STATUS) as overdue_freq from credit_record group by id) as a
left join
(select id, sum(STATUS) as overdue_times from credit_record group by id) as b
on a.id = b.id;

create table overdue_details as
select * from
(select id as aid, overdue_freq, overdue_times from overdue) as a
left join
(select * from application_record) as b
on a.aid = b.id;
```
export table overdue_details as a csv file.

## Generate html files
run
```shell
pip install -r requiremnts.txt
```
run analysis.py
```shell
python analysis.py
```
