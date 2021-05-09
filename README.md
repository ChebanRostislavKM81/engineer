### LAUNCH INSTRUCTION
Launch command ```docker-compose up``` in terminal


If you have not got any postgres server, open ```localhost:8081```, connect to PgAdmin (PGADMIN_DEFAULT_EMAIL=admin@kpi.ua PGADIN_DEFAULT_PASSWORD=admin) and create new one


Also, you can change email and password in ```docker-compose.yaml``` file


After you make sure that you have postgres server, change the ```.env``` file with your database name, username and password. 


Also you have to print your path to Downloads(folder, where your web-site downloads stored) into ```download_path``` variable


Now you need to open another terminal and input these commands:


If you run it on Windows:


```py -m venv new_env```


```new_env\Scripts\activate.bat```


```pip install -r requiremtns.txt```


```py main.py```



If you run it on Linux/Mac:


```python3 -m venv new_env```


```new_env\Scripts\activate.bat```


```pip install -r requiremtns.txt```


```python3 main.py```

