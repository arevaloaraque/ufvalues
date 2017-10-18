Application to view the history of UF values of a selected year. The values are extracted from the page http://www.bcentral.cl by means of web scraping. The downloaded data is stored in the project database if this data it does not exist, it also allows you to view the UF value for a specified amount and date.

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
