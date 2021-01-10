# AdRecognition

## Link to the presentation

[Clic here](Project_Presentation.pdf)

## Start Project

Before running : get your credentials from Google Cloud Platform as JSON file. Name it `ggcredentials.json` at the root of the project.


Create your Mysql DB with :
```sql
 CREATE DATABASE urls_categories;
 USE urls_categories;
 CREATE TABLE urls_table;
 CREATE TABLE urls_table (id INT, url VARCHAR(1000), brand VARCHAR(250), category VARCHAR(250), time DATETIME DEFAULT CURRENT_TIMESTAMP, displayed TYNINT);
 ALTER TABLE urls_table MODIFY id INT PRIMARY KEY AUTO_INCREMENT;
```

Run : 
```python
python3 -m pip install -r ./requirements.txt
python3 adRecognition.py https://www.url.com/video.mp4
```

