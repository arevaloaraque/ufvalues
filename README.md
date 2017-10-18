Application to view history of UF values from a selected year. The values are extracted from the page http://www.bcentral.cl through Web Scraping. The downloaded data is stored in a project database if it does not exist, it also allows you to view the value in UFs of a specified amount and date.

# Requirements
- **Python 2.x**
- **Virtualenv**
- **Git control versions**
- **Pip**
- **Bower**

# Installation
Clone the repository in your pc
```sh
$ git clone https://github.com/arevaloaraque/ufvalues.git
```

Go to the repository folder
```sh
$ cd ufvalues
```

Create virtual environment
```sh
$ virtualenv env --no-site-packages
```

Install dependencies
```sh
$ pip install -r requirements.txt
$ cd static
$ bower install
$ cd ..
```

Create database
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

Run tests
```sh
$ python manage.py test
```

Start application
```sh
$ python manage.py runserver
```

Open browser at http://localhost:8000
