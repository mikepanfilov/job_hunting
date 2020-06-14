# Programming vacancies compare

This is a comparing tool of different language job positions at Headhunter and Suberjob job aggregation services.
The script geting latest vacancies from services via API, collecting salary forks and returns a result tables to stdout.

## How to install

Python version 3 is required.

It's better is you'll use virtual environment tool (such as virtualenv) and install libs from requirements.txt:

```bash
$ pip install -r requirements.txt
```

After that just start the main.py and see the results:

```bash
$ python3 main.py
```

## Environment Variables

1. SuperJob's API resource requires a secret key which you can get after registration at <https://api.superjob.ru/>.
2. Make a .env file and put gotten key into a variable `SUPJOB_KEY=v3.r...` after that script will get access to resource.

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
