# Student Grade Data Visualization with CRUD Operations (Flask App)
Flask Application that uses a CSV to store student grade distributions across different courses. 
* CRUD Operations have been implemented to add/remove/edit entries from the CSV file
* Data is read in using Pandas
* Data is visualized using plotly and rendered within jinja templated HTML file

Developed for RV University and presented to concerned faculty on 11 Jan 2024.

# Requirements
	Python = 3.x
    Flask = 2.2.5
    plotly==5.18.0

Highly recommend that you use [Visual Studio Code](https://www.jetbrains.com/idea) as your IDE with this project.

# Steps to setup
### 1. Clone repository
Clone repository to your local machine using "git clone

https://github.com/hhk998402/Flask-App-Example.git

### 2. Configure Flask Variables
Copy `.env.example` into a new file in the root folder called `.env`

You can change the `FLASK_RUN_PORT` value to whatever port you wish.
 
The `FLASK_ENV` value indicates whether the server should support hot-reloading. In production mode, you will have to manually restart the server to reflect any changes made since last run. We will be using development mode in this project.

### 3. Download the required dependencies
Create a `requirements.txt` file in your project root (if it doesn't already exist) and paste the following content into it
```
antiorm==1.2.1
attrs==23.2.0
click==8.1.7
db==0.1.1
flasgger==0.9.7.1
Flask==2.2.5
importlib-metadata==6.7.0
importlib-resources==5.12.0
itsdangerous==2.1.2
Jinja2==3.1.2
jsonschema==4.17.3
MarkupSafe==2.1.3
mistune==3.0.2
numpy==1.21.6
packaging==23.2
pandas==1.3.5
pkgutil-resolve-name==1.3.10
plotly==5.18.0
pyrsistent==0.19.3
python-dateutil==2.8.2
python-dotenv==0.21.1
pytz==2023.3.post1
PyYAML==6.0.1
six==1.16.0
tenacity==8.2.3
typing-extensions==4.7.1
Werkzeug==2.2.3
zipp==3.15.0
```
Install venv package
```
pip install virtualenv
```
Activate the virtual environment
```
python3 -m venv venv
source venv/bin/activate


(Windows)
python3 -m venv venv
.\venv\bin\activate.bat
```
Install the packages using pip
```
pip install
```

### 4. Run application
After successful installation of dependencies, you can run the application with this command
```
flask run
```

Use http://localhost:3000/view_records

Alter the port number based on the server configuration done in `.env` file

### 5. Swagger documentation
Open swagger document using http://localhost:3000/apidocs

Alter the port number based on the server configuration done in `.env` file

### 7. Explore APIs
	
	Create an entry: POST /api/data 
	Get an entry by record ID: GET /api/data/{record_id}
	Get all records: GET /api/data
	Update record by record ID: PUT /api/data/{record_id}
	Delete record by record ID: DELETE /api/data/{record_id}
