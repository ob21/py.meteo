import requests
import json

session = requests.Session()
session.trust_env = False

api_key = "56be7192b69f7116538006ce67cd4e3c"
base_url = "http://api.openweathermap.org/data/2.5/weather?q="
params_base = "&lang=fr&units=metric"

cities = ["Ruoms", "Rennes", "Royan", "Biarritz", "Annecy", "Dinard", 
"Saint-Lary-Soulan", "Sanary", "Pornic", "Mont-Dore"]

def getCities():
    # build the url
    url = "http://obriand.fr/meteo/get_cities.php"
    # make the http request to openweathermap
    print("request " + url)
    # proxy = {"http": "http://p-goodway.rd.francetelecom.fr:3128"}
    # r = session.get(url, proxies=proxy)
    r = session.get(url)
    print("response = " + r.text)
    global cities
    cities = r.text.split(",")
    cities.remove("")
    print(cities)

def getMeteoFor(c):
    # build the url
    url = base_url + c + params_base + "&APPID=" + api_key

    # make the http request to openweathermap
    print("request " + url)
    # proxy = {"http": "http://p-goodway.rd.francetelecom.fr:3128"}
    # r = session.get(url, proxies=proxy)
    r = session.get(url)
    print("response = " + r.text.encode('utf-8'))

    # parse the json and get the data
    data = json.loads(r.text);
    print()
    city = data['name'].encode('utf-8')
    code = data['weather'][0]['id']
    main = data['weather'][0]['main'].encode('utf-8')
    description = data['weather'][0]['description'].encode('utf-8')
    icon = data['weather'][0]['icon']
    temp = data['main']['temp']
    pressure = data['main']['pressure']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    print("Meteo de " + c + " : ")
    print(code)
    print(icon)
    print(main)
    print(description)
    print("temp = " + str(temp))
    print("pressure = " + str(pressure))
    print("temp_min = " + str(temp_min))
    print("temp_max = " + str(temp_max))
    print("humidity = " + str(humidity))
    print("wind_speed = " + str(wind_speed))

    # create a entry on the obriand bdd
    print()
    data = {'city': city, 'code': code, 'icon': icon, 'main': main, 'description': description, 'temp': temp, 'pressure': pressure, 'humidity': humidity, 'temp_min': temp_min, 'temp_max': temp_max, 'wind_speed': wind_speed}
    dataUrl = "http://obriand.fr/meteo/add.php"
    print("request post data = " + dataUrl + " with " + str(data).encode('utf-8'))
    # r = session.post(dataUrl, data=data, proxies=proxy)
    r = session.post(dataUrl, data=data)
    print("response data = " + r.text.encode('utf-8'))
    print()

getCities()
for c in cities:
    #print(c)
    getMeteoFor(c)


