# Bazaar of Wonders
Bazaar of Wonders is a Django-based web application that aggregates card details and pricing statistics for trading card games, namely, Magic: The Gathering.

## Table of Contents

- [Features](#features)
- [Visuals](#visuals)
- [Installation](#installation)
- [Documentation](#documentation)
- [Tests](#tests)
- [Team](#team)

## Features
 - Card listings
 - Card information
 - Search and filter
 - User portal
 - Promotions

## Visuals
![Homepage Example](https://user-images.githubusercontent.com/41175151/86148117-d7c8c380-babf-11ea-9f4c-a574fba00d6c.png)

## Installation

### Clone
```shell
$ git clone https://github.com/Bazaar-Trader/Bazaar_Of_Wonders.git
```
 ### Create virtual environment
```shell
$ virtualenv env --no-site-packages
$ source env/bin/activate
```
### Install dependencies
```shell
$ pip3 install -r requirements.txt
```
### Run project managament commands 
```shell
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```
View on browser: http://localhost:8000 
 
 ## Documentation
 
Trello: https://trello.com/b/Z6YaeKNS/cis4934-project-group-bazaar
 ## Tests
 ### Steps to implement custom unit testing
1. Locate correct testing file where '*' is models, views, or templates.
```shell
 directory: bazaar_of_wonders/main/tests/test_*.py
```
2. Run test command. The test file can be specified by concatenating the file name.
```shell
 python3 mangage.py test
```

 ## Team
 
| <a href="http://github.com/ahillebra" target="_blank">**Project Manager**</a> | <a href="http://github.com/kdewey13" target="_blank">**SCRUM Master**</a> | <a href="http://github.com/kerekovskik" target="_blank">**Dev Team**</a> | <a href="http://github.com/dorianmeade" target="_blank">**Dev Team**</a> | <a href="http://github.com/matthewrabe" target="_blank">**Dev Team**</a> |
| :---: |:---:| :---:| :---:| :---:|
| [![Ashleigh Hillebrand](https://avatars0.githubusercontent.com/u/41175151?s=460&u=e59b91d99418dbeca3f3db49c3cb534fd6308dcb&v=4&s=200)](http://github.com/ahillebra) | [![Kelsey Dewey](https://avatars0.githubusercontent.com/u/40505163?s=400&u=e48b8b620316f566a560a3f5ad7ba56492233c0c&v=4s&=200)](http://github.com/kdewey13) | [![Konstantin Kerekovskik](https://avatars3.githubusercontent.com/u/23172746?s=400&v=4&s=200)](http://github.com/kerekovskik) | [![Dorian Meade](https://avatars2.githubusercontent.com/u/32111245?s=460&u=ddbe2f1c66d7c31f85f7f3f308b794f199d361ad&v=4s&=150)](http://github.com/dorianmeade) | [![Matthew Rabe](https://avatars0.githubusercontent.com/u/44124858?s=400&v=4&s=200)](http://github.com/matthewrabe) 
| <a href="http://github.com/ahillebra" target="_blank">`github.com/ahillebra`</a> | <a href="http://github.com/kdewey13" target="_blank">`github.com/kdewey13`</a> | <a href="http://github.com/kerekovskik" target="_blank">`github.com/kerekovskik`</a> | <a href="http://github.com/dorianmeade" target="_blank">`github.com/dorianmeade`</a> | <a href="http://github.com/matthewrabe" target="_blank">`github.com/matthewrabe`</a> |
