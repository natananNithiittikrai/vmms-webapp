[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=DrNattapoom_vmms-webapp&metric=coverage)](https://sonarcloud.io/summary/new_code?id=DrNattapoom_vmms-webapp)

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=DrNattapoom_vmms-webapp&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=DrNattapoom_vmms-webapp)

# Vending Machine Management System

MUIC ICCS372 Software Engineering

# Repository Files

```
├── database
│   ├── database_service.py
│   ├── utils.py
│   └── vending_machine.db
├── models
│   ├── base.py
│   ├── product.py
│   ├── stock.py
│   └── vending_machine.py
├── templates
│   ├── add.html
│   ├── base.html
│   ├── index.html
│   └── update.html
├── tests
│   ├── test_api_add_product_stock.py
│   ├── test_api_add_vending_machine.py
│   ├── test_api_delete_product_stock.py
│   ├── test_api_delete_vending_machine.py
│   ├── test_api_update_product_stock.py
│   └── test_api_update_vending_machine.py
├── .gitignore
├── app.py
└── checklist.md
```

# Project Setup

```
Python 3.9.13

Package Requirements
   -  flask
   -  sqlite3
   -  sqlalchemy
```

# Run

Please run app.py to start a webapp running on http://127.0.0.1:5000

```
python app.py
```

<b> Note: </b> The current working directory <b> must be </b> where the files are located.
