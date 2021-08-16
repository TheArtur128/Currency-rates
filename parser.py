from bs4 import BeautifulSoup
import requests
import json
import datetime

class Currency:
    #Пространство ссылок на все валюты
    everyone = []
    #Время в которое мы парсили валюты
    time = []
    #Принимает всю напарсиную информацию в таблице
    def __init__(self, code, units, name, vaule, change):
        self.__code = code
        self.__name = name
        self.__cost_to_Ruble = float(vaule) / float(units)
        #Отсикаем дробь до 1.0000 если требуеться
        if len(str(self.__cost_to_Ruble).split(".")[1]) > 4:
            self.__cost_to_Ruble = float(f'{str(self.__cost_to_Ruble).split(".")[0]}.{str(self.__cost_to_Ruble).split(".")[1][:4]}')
        self.__change = float(change.replace(",", "."))

    def __str__(self):
        return f"{self.__name} ({self.__code}): {self.__cost_to_Ruble} ({self.__change})"

#Парсит информацию валют и заносит её в экземпляры класса Currency
def update_Ruble_vaule():
    print("Parsing, parsing, parsing...")
    URL = "https://www.banki.ru/products/currency/cb"
    Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
    #Получаем контент html страницы
    page = requests.get(URL, headers=Headers)
    content = BeautifulSoup(page.content, "lxml")
    #Парсим таблицу всех валют
    currency_table = content.find("table", class_="standard-table standard-table--row-highlight").find("tbody").find_all("tr")
    #Под каждую валюту создаём экземпляр и суём туда информацию с этой валюты с таблы на сайте
    Currency.everyone = []
    for item in currency_table:
        all_info = item.find_all("td")
        Currency.everyone.append(Currency(all_info[0].text.strip(), all_info[1].text.strip(), all_info[2].text.strip(), all_info[3].text.strip(), all_info[4].text.strip()))
    #Устанавливаем время
    Currency.time = str(datetime.datetime.now().date())
    print("mission accomplished!\n")

#Записываем данные в json файл
def conversion_all_to_json():
    #Если мы не имеем обьекты то конвертация завершаеться
    if Currency.everyone == []:
        print("No data 0.0\nFor get data enter 1\n")
        return False
    #Данные которые мы отправим в космос или в json файл.
    #По умолчанию хранит время парсинга
    data = [{"Right time": Currency.time}]
    #Добовляем в капсулу данные каждой валюты
    for item in Currency.everyone:
        data.append(item.__dict__)
    #Отпровляем нашу капсулу в космос
    with open("Currency.json", "w") as file:
        json.dump(data, file, indent=4)
    print("mission accomplished!\n")

#Выводит информацию всех напарсиных валют
def get_all_currency():
    if Currency.everyone == []:
        print("No data 0.0\nFor get data enter 1\n")
        return False
    for item in Currency.everyone:
        print("#", item)
    print("")

#Интерфейс
while True:
    way = input("1. - Parsing data of Currency\n2. - Get data of every currencyt\n3. - Conversion all currency to json\n#Or enter something else to exit\n\> ").strip()
    print("")
    #Парсим
    if way == "1":
        update_Ruble_vaule()
    #Выводим данные в консоль
    elif way == "2":
        get_all_currency()
    #Отпровляем данные в космос
    elif way == "3":
        conversion_all_to_json()
    #Уходим в закат
    else:
        break
