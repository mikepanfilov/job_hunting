import os
import requests
from dotenv import load_dotenv
from terminaltables import DoubleTable

PROGRAMMING_LANGUAGES = [
    'TypeScript',
    'Swift',
    'Scala',
    'Objective-C',
    'Go', 
    'C', 
    'C#', 
    'C++', 
    'PHP', 
    'Ruby',
    'Python', 
    'Java', 
    'JavaScript',
    '1С'
]

def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return  (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    else:
        return salary_to * 0.8

def predict_rub_salary_hh(vacancy):
    prediction = predict_salary(vacancy['from'], vacancy['to'])
    if vacancy['currency'] != 'RUR' or prediction == '0':
        return None
    else:
        return prediction

def predict_rub_salary_sj(vacancy):
    prediction = predict_salary(vacancy['payment_from'], vacancy['payment_to'])
    if vacancy['currency'] != 'rub' or prediction == '0':
        return None
    else:
        return prediction

def get_hh_mean_salary(language):
    predicted_salaries = []
    page = 0
    pages_number = 1
    while page < pages_number:

        payload= {
        'text':f'программист {language}',
        'area':'1',
        'period':'30',
        'only_with_salary': True,
        'page':page
        }
        url = 'https://api.hh.ru/vacancies/'

        response = requests.get(url, params=payload)
        response.raise_for_status()
        results = response.json()

        for post in results['items']:
            if predict_rub_salary_hh(post['salary']):
                predicted_salaries.append(predict_rub_salary_hh(post['salary']))
        
        pages_number = results['pages']
        page += 1

    return {
        'vacancies_found':results['found'],
        'vacancies_processed': len(predicted_salaries),
        'average_salary': int(sum(predicted_salaries) / len(predicted_salaries)),
        }

def head_hunter_salaries():
    salaries_by_language={}
    for language in PROGRAMMING_LANGUAGES:
        salaries_by_language[language] = get_hh_mean_salary(language)

    return ('HeadHunter Moscow', salaries_by_language)

def get_sj_mean_salaries(superjob_key,language):
    headers = {
        'X-Api-App-Id':superjob_key
    }
    predicted_salaries = []
    page = 0
    more = True
    while more:
        payload = {
            'catalogues':48,
            'town':4,
            'page':page,
            'keywords':language,
        }

        url = 'https://api.superjob.ru/3.0/vacancies/'
        response = requests.get(url, headers=headers, params=payload)
        results = response.json()

        for vacancy in results['objects']:
            if predict_rub_salary_sj(vacancy):
                predicted_salaries.append(predict_rub_salary_sj(vacancy))

        page += 1
        more = results['more']

        if len(predicted_salaries) != 0:
            return {
                'vacancies_found':results['total'],
                'vacancies_processed': len(predicted_salaries),
                'average_salary': int(sum(predicted_salaries) / len(predicted_salaries)),
            }
        else:
            return {
                'vacancies_found':results['total'],
                'vacancies_processed': len(predicted_salaries),
                'average_salary': 0,
            }

def supejob_salaries(superjob_key):
    salaries_by_language={}
    for language in PROGRAMMING_LANGUAGES:
        salaries_by_language[language] = get_sj_mean_salaries(superjob_key, language)
    return ('SuperJob Moscow', salaries_by_language)

def tablify(title, dictionary):
    table_data = [['Язык программирования', 
    'Вакансий найдено', 
    'Вакансий обработано',
    'Средняя зарплата']]
    for language,subdict in dictionary.items():
        if language and subdict['average_salary'] != 0:
            formed_row = [
                language, 
                subdict['vacancies_found'], 
                subdict['vacancies_processed'], 
                subdict['average_salary']
            ]
            table_data.append(formed_row)
    table_instance = DoubleTable(table_data, title)
    print(table_instance.table)

def main():
    load_dotenv()
    superjob_key = os.getenv('SUPJOB_KEY')

    title, stats = head_hunter_salaries()
    tablify(title, stats)
    title, stats = supejob_salaries(superjob_key)
    tablify(title, stats)

if __name__ == "__main__":
    main()