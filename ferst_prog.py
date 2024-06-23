import requests
from bs4 import BeautifulSoup
import csv

link = 'https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B0%D0%BC%D0%B5%D0%BD%D1%81%D0%BA%D0%BE%D0%B5-303007130'
respons = requests.get(link).text

soup = BeautifulSoup(respons, 'lxml')
block = soup.find('div', id='blockDays')
check = block.find('div', id='bd1')


def show(check):
    result1 = check.find_all('p')
    date_time = []    
    for i in result1:
        date_time.append(i.text)

    result2 = check.find('div')['title']    
    meteor=(f'{result2}')

    result4 = check.find_all('span')
    temp=(f'min {result4[0].text} max {result4[1].text}')

    return date_time, meteor, temp


all_date = []
for i in range(1, 8):  
    check = block.find('div', id='bd'+str(i))  
    all_date.append(show(check))
# print(all_date)

def weather_forecast(date_info):
    
    
    weather_description = date_info[1]
    temperature_range = date_info[2].split()    


    # Форматування дати
    day_of_week = date_info[0][0]
    day_of_month = date_info[0][1]
    month = date_info[0][2]
    
    # Форматований рядок для виведення
    formatted_output = f"{day_of_month} {month:<6} {day_of_week:<15}{weather_description:<40} | {temperature_range[0]:<5} {temperature_range[1]:<4} | {temperature_range[2]:<5} {temperature_range[3]:<4}|\n"
    list_wether = [
        day_of_month, month, day_of_week, weather_description,
        temperature_range[1], temperature_range[3] 
                   ]
    return formatted_output, list_wether

# Виклик функції для виведення даних


with open('wether.txt', 'w', encoding='utf-8') as file:
    for line in all_date:
        file.write(weather_forecast(line)[0])    
file.close()

with open('weather_csv.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Дата','Месяц','День недели', 'Погода', 'Температура'])
    for line in all_date:
        writer.writerow(weather_forecast(line)[1])
csvfile.close()