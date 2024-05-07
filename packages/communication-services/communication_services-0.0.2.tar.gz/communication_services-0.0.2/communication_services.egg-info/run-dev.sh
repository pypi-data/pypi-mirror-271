function initial()
{
    source .venv/bin/activate
    source .env
}

function commitdb()
{
    ./manage.py makemigrations
}

function migratedb()
{
    ./manage.py migrate
}

function runserver()
{
    ./manage.py runserver 8002
}

function shell()
{
    ./manage.py shell
}


function setup()
{
    virtualenv .venv -p /usr/bin/python3
    initial
}

function shell()
{
    ./manage.py shell
}

function start()
{
    initial; runserver
}

function export_packages()
{
    pip freeze > requirement.txt
}

function import_packages(){
    pip install -r requirement.txt
    
}

function start_rabbitMQ (){
    # core is my project name
    celery -A core  worker -l info
}

function create_user(){
    python ./manage.py createsuperuser
}

function upload_project_to_pypi(){
    python setup.py sdist
    pip install twine
    twine upload dist/*

}