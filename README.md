# flask_project_template
folder template for my flask project


## Getting Start
* <b>Remarks:</b> some modification need to be done before it can be run on docker 

### 1. Installing Dependencies

#### Python 3.8
Install the latest version of python for your platform follow this link: [python docs](https://packaging.python.org/guides/installing-using-pip-and-vitual-environments/)
* Remmark this project has been tested to work with python3.7

#### Virtual Enviornment
I recommend working within a virtual environment . This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs
```
python3.8 -m venv [path_to_desired_place]/venv/dmLibrary
source ./dmLibrary/bin/activate
```

#### PIP Dependencies
Once you have your virtual environment setup and running, install dependencies if you current directory is where this Readme is, you should be ready to run the [requirement file](requirements.txt)
```
pip install -r requirements.txt
```


##### Key Dependencies
<b>Flask</b> is a lightweight backend microservices framework. Flask is required to handle requests and responses.


#### Install the package
along with this Readme you should see the [setup.py](setup.py) file in the same location

```
pip3 install -e .
```

### 2. Setup postgres database for the service to connect to
if you already have postgres database running and ready to be connect you can just config the service to connect to it

but if not we already provide [the script](docker-psql.sh) to run postgres database inside docker.

please config it before running

```
source docker-psql.sh
```

### 3. Create/Updata database table
As the name state, you only need to run this when you need to create database table or update it (if this is the first time you connect the service to the database the you sure does to run this)

<b>Remarks</b>: you need to run this in the directory where migration folder is located(same location as this readme)

```
./dmLibrary/bin/run-manage db upgrade
```

### 4. Config the service
before running, please make sure that the configuration will work at your side. you can config the service into ways.
- [defaults.py](./dmLibrary/defaults.py)
- enviroment varaible

if same config happen to be in both places. then the service will use the value in enviroment varaible

to understand how this service configuration works you can see this [config file](./dmLibrary/config.py)

#### Configurable Parameter
here's  the list of configuration and there uses;

- <b>SQLALCHEMY_DATABASE_URI</b>: URL string for the service to connect to
- <b>PORT</b>: port for the flask api will be running on for accepting rest api request
- <b>LOG_FILE_PATH</b>: location where the service will log to



### Running the service
if you using the virtual enviroment everything should be ready in bin folder

```
./dmLibrary/bin/run-api
```

### Deployment process
1. clone this git
```
git clone [git_uri]
cd [git_dmLibrary]
```
    1.1 for production you can just use master
    1.2 for test environment please use develop branch
    ```
    git checkout develop
    
    ```
2. change directory into dmLibrary
```
cd dmLibrary
```

3. run postgres in docker (only it's not currently run)
```
source docker-psql.sh
```
4. create virtualenv
    4.1 if no virtual env install it
    ```
    pip3 install virtualenv
    ```
    4.2 make virtualenv
    ```
    virtualenv "$HOME"/dmLibrary
    ```
    4.3 activate virtualenv
    ```
    source "$HOME"/dmLibrary/bin/activate
    ```
    4.4 install requirement
    ```
    pip3 install -r requirements.txt
    ```
    4.5 install package
    pip3 install -e  .
5. run flask-migration to make sure the database has correct database model version
```
run-manage db upgrade
```

6. cp our supvisor run scritp into proper place
```
sudo cp dmLibrary.ini /etc/supervisord.d/
```
7. run the service with supervisor
```
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start
```




