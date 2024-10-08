# Globant Data Engineer
For the Data Engineer test for Globant, divided in the following sections:

## 1.- API
Will use Flask for the local development and the data will be uploaded directly to BigQuery. To simplify the solution will asume that the Google default credentials are properly set up in the evironment.

The API accepts .csv files and uploads them directly to BigQuery, asumig the filename (without the extension) as table_id. 

It has the following body:

| Key | Type | Description | Values | Optional | 
|-----|------|-------------|--------|----------|
| file | File | File to upload | .csv files | NO |
| table_id | Text | Name of the destiantion table | any str | YES |
| column_names | Text | Column name, only replaces them when creating from scratch or when truncating | , separeted strs | YES |
| write_disposition | Text | Write disposition, on truncation if column_names is not defined, sets the column name as 0 based index values | WRITE_TRUNCATE, WRITE_APPEND | YES |


Example of POST call:

``` bash
curl --location 'http://127.0.0.1:5000' \
--form 'file=@"/C:/Users/andre/OneDrive/Desktop/globant/jobs.csv"' \
--form 'table_id="jobs"' \
--form 'column_names="id,jobs"' \
--form 'write_disposition="WRITE_TRUNCATE"'
```

## 2.- SQL
BigQuery will be used as Database for the test, in a proyect and dataset created for this. Given this decision, all the tables in the solutions will start with ```globant-apescara.data.*```.

All the solutions will be stored in the /sql path:
- question 1: [sql/jobs_by_department_by_q.sql](sql/jobs_by_department_by_q.sql)
- question 2: [sql/hired_by_department.sql](sql/hired_by_department.sql)