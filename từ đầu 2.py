import speech_recognition as sr
from youtube_search import YoutubeSearch
from gtts import gTTS
from selenium.webdriver.common.by import By
import os
import time
import playsound
import wikipedia
import datetime
from datetime import date
from datetime import datetime
import time
import webbrowser
import re
from selenium import webdriver
import requests
from time import strftime


wikipedia.set_lang("vi")



def speak(text):
    print("Bot: {}".format(text))
    tts = gTTS(text=text,lang='vi')
    filename='voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def get_audio():
    print("\nBot: Đang nghe")
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Tôi: ", end="")
        audio = r.listen(source, phrase_time_limit=8)
        try:
            text = r.recognize_google(audio, language="vi")
            print(text)
            return text.lower()
        except:
            print("...")
            return 0
        
        
def stop():
    speak("Hẹn gặp lại!")
    time.sleep(2)

def get_text():
    for i in range(3):
        text = get_audio()
        if text:
            return text.lower()
        elif i < 2:
            continue
    time.sleep(2)
    return 0
# Ở đây là bước chào hỏi. Alex sẽ phân vùng thời gian để trò chuyện với bạn cho hợp lý nha ^^
def hello():
    day_time = int(time.strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng . Chúc bạn một ngày tốt lành.")
    elif 12 <= day_time < 18:
        speak("Chào buổi chiều . Bạn đã dự định gì cho chiều nay chưa.")
    else:
        speak("Chào buổi tối . Bạn đã ăn tối chưa nhỉ.")
    time.sleep(5)

def stop():
    speak("Hẹn gặp lại bạn sau!")
    time.sleep(2)

def get_time(text):
    now = datetime.now()
    if "giờ" in text:
        speak('Bây giờ là %d giờ %d phút %d giây' % (now.hour, now.minute, now.second))
    elif "ngày" in text:
        speak("Hôm nay là ngày %d tháng %d năm %d" %
              (now.day, now.month, now.year))
    else:
        speak("Bot chưa hiểu ý của bạn. Bạn nói lại được không?")
    time.sleep(4)

def open_application(text):
    if "google" in text:
        speak("Mở Google Chrome")
        time.sleep(2)
        os.startfile('C:\Program Files\Google\Chrome\Application\chrome.exe') # Trong ngoặc là đường dẫn đến ứng dụng trong máy mình, các bạn tự tìm trong máy mình sao cho đúng nha
    elif "cày" in text:
        speak("mở cày")
        time.sleep(2)
        os.startfile("test4.py")
    else:
        speak("Ứng dụng chưa được cài đặt. Bạn hãy thử lại!")
        time.sleep(3)

def play_song():
    speak('Xin mời bạn chọn tên bài hát')
    time.sleep(2)
    mysong = get_text()
    while True:
        result = YoutubeSearch(mysong, max_results=10).to_dict()
        if result:
            break
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.get(url)
    time.sleep(1)
    browser.find_element(By.XPATH, '//*[@id="movie_player"]').click()
    speak("Bài hát bạn yêu cầu đã được mở.")
    time.sleep(3)

def xem_phim():
    speak('Xin mời bạn chọn phim')
    time.sleep(2)
    mysong = get_text()
    url = 'https://www.youtube.com/results?search_query=' + mysong
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.get(url)
    speak("Mở youtube và tìm " + mysong)
    time.sleep(3)

# Muốn đi chơi mà sợ trời mưa thì hãy xem dự báo thời tiết nha, nhớ gọi Alex đó
def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    time.sleep(3)
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
                                                                           hourset = sunset.hour, minset = sunset.minute, 
                                                                           temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
        speak(content)
        time.sleep(28)
    else:
        speak("Không tìm thấy địa chỉ của bạn")
        time.sleep(2)
# Bật mí là con Bot này rất rất là "nhiều chuyện". Nên hổng biết cái gì cứ hỏi nó nha ^^
def tell_me_about():
    try:
        speak("Bạn muốn nghe về gì ạ")
        time.sleep(2)
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0].split(".")[0])
        time.sleep(10)
        for content in contents[1:]:
            speak("Bạn muốn nghe thêm không")
            time.sleep(2)
            ans = get_text()
            if "có" not in ans:
                break    
            speak(content)
            time.sleep(10)

        speak('Cảm ơn bạn đã lắng nghe!!!')
        time.sleep(3)
    except:
        speak("Bot không định nghĩa được thuật ngữ của bạn. Xin mời bạn nói lại")
        time.sleep(5)

def google(text):
    speak('bạn muốn tìm gì')
    time.sleep(2)
    search = get_text()
    url = 'https://www.google.com/search?q=' + search
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    browser.get(url)
    speak("Mở google và tìm " + search)
    time.sleep(3)

def open_website(text):
    reg_ex = re.search('mở (.+)', text)
    if reg_ex:
        domain = reg_ex.group(1)
        url = 'https://www.' + domain
        options = webdriver.ChromeOptions()
        options.add_experimental_option('detach', True)
        browser = webdriver.Chrome(options=options)
        browser.maximize_window()
        browser.get(url)
        speak("Trang web bạn yêu cầu đã được mở.")
        time.sleep(3)
        return True
    else:
        return False

def AI():
    speak("xin chào bạn!")
    print("\nBot: Xin chào bạn!")
    while True:
        text = get_text()
        if text == "bắt đầu":
                speak("bạn hãy nói lệnh")
                text = get_text()
                if "chào robot" in text or "hello" in text:
                    hello()
                elif "bye" in text or "tạm biệt" in text:
                    stop()
                    break
                elif "ứng dụng" in text:
                    speak("Tên ứng dụng bạn muốn mở là ")
                    time.sleep(3)
                    text1 = get_text()
                    open_application(text1)
                elif "chơi nhạc" in text:
                    play_song()
                elif "phim" in text:
                    xem_phim()
                elif "giờ" in text or "ngày" in text:
                    get_time(text)
                elif "định nghĩa" in text:
                    tell_me_about()
                elif "thời tiết" in text:
                    current_weather()
                elif 'tìm kiếm' in text:
                    google()
                elif "mở " in text:
                    open_website(text)
                else:
                    speak("bạn cần tôi giúp gì?")

AI()