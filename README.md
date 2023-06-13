# 💼 Employment web 
A web page that displays the hierarchy of employees in a tree-like format.

## 🖥️ Technologies 
![Python](https://img.shields.io/badge/-Python-blue?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-blue?style=for-the-badge&logo=postgresql&logoColor=white)
![Django](https://img.shields.io/badge/-Django-green?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-blue?style=for-the-badge&logo=docker&logoColor=white)
![HTML](https://img.shields.io/badge/-HTML-orange?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/-CSS-blue?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/-JavaScript-yellow?style=for-the-badge&logo=javascript&logoColor=white)
![Bootstrap](https://img.shields.io/badge/-Bootstrap-purple?style=for-the-badge&logo=bootstrap&logoColor=white)

## 📝 Requirements

- Python 3.7+
- Django 4.2.1+
- PostgreSQL

## 🛠 Before installation
1. Clone the project repository

```bash
git clone https://github.com/Anatolii-Poznyak/employ_test_task.git
cd employ_test_task
```
2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Create .env file based on .env.sample file and set variables.

```bash
cp .env.sample .env
```

- If you want to use docker - set POSTGRES_HOST=db 

## 🐳 Run with DOCKER
- DOCKER should be installed

```shell
  docker-compose up
```
- server will run on 127.0.0.1:8000
- Create first employee-admin from terminal to be able to login (enter the container) and load test data from .json file
```shell
docker ps
docker exec -it <your container name> /bin/bash
python manage.py createsuperuser
python manage.py loaddata employee_json
```

## 🖼 Demo pictures
<details>
  <summary>Home</summary>

  ![tree](static/demo/tree.png)
</details>
<details>
  <summary>Login</summary>

  ![login](static/demo/login.png)
</details>
<details>
  <summary>Employees</summary>

  ![employees](static/demo/filter.png)
</details>
<details>
  <summary>Create</summary>

  ![create](static/demo/create.png)
</details>
<details>
  <summary>Update</summary>

  ![update](static/demo/update.png)
</details>
<details>
  <summary>Delete</summary>

  ![delete](static/demo/delete.png)
</details>
<details>
  <summary>Transfer</summary>

  ![transfer](static/demo/transfer.png)
</details>
<details>
  <summary>Logout</summary>

  ![logout](static/demo/logout.png)
</details>
<details>
  <summary>50.000</summary>

  ![Fixture](static/demo/fixtura.png)
</details>

## 📚 Additional info
- For testing: run tests -> `python manage.py test`
- If you want to create your specific amount of test- data -> run script for create JSon with data -> `python DB_Seeder.py 300 2` (first param - count of employees, second - level of inheritance). It will rewrite employee_data.json (by default 1000 records in file)
- To load data from created fixture to your db -> `python manage.py loaddata employee_data`
