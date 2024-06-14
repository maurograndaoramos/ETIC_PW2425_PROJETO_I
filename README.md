# ETIC_PW2425_PROJETO_I
Repository for Project I

> [!IMPORTANT]
> MOST OF WHAT YOU SEE HERE IS WIP - LEMME COOK

# TO-DO
- [x] Get hyped about coding again cuz yeah this ain't been it
- [x] Create apps, structure File & Folder Model
- [ ] Fix the nasty upload bug (Consider moving hash logic to POST)
- [x] Bumped to 0.1.b1
- [x] Create templates and views for Drive
- [x] Start Web app to handle main page
- [x] Bumped to 0.2.0
- [ ] Finish User Authentication
- [ ] Handle POSTs and GETs for File/Folder up/download
- [ ] 
- [ ] 

# DIRECTORY STRUCTURE
```
├── EDrive
│   ├── drive
│   │   ├── __pycache__
│   │   ├── migrations
│   │   ├── static
│   │   │   └── css
│   │   │       └── styles.css
│   │   ├── templates
│   │   │   ├── drive.html
│   │   │   └── drive_generic.html
│   │   ├── uploads
│   │   │   └── hashed files in general
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── hub
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── web
│   │   ├── __pycache__
│   │   ├── migrations
│   │   ├── static
│   │   │   └── css
│   │   │       └── styles.css
│   │   ├── templates
│   │   │   ├── about.html
│   │   │   ├── home.html
│   │   │   ├── home_generic.html
│   │   │   └── premium.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── signals.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── db.sqlite3
│   └── manage.py
├── Dockerfile
├── Findings.txt
├── LICENSE
├── Makefile
├── README.md
├── compose.yml
├── poetry.lock
└── pyproject.toml
```

- ETIC_PW2425_PROJETO_I/ - Contains project critical files 
    - EDrive - Contains the entirety of the project
        - drive - Contains the file management page
        - hub - Contains the main django settings
        - web - Contains the landing page and other pages