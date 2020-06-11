import re
import urllib
import ctypes
import random
import os
from tkinter import *
from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from PIL import ImageTk
from PIL import Image

#파일 경로를 설정한
path = "C:/Temp/BG" 

#해당 경로가 없으면 디렉토리 생성
if not os.path.exists("C:/Temp"):
    print("C:/Temp", "폴더를 생성합니다...")
    os.mkdir("C:/Temp")
    
#파싱
def BG_Parsing():
    print("바탕화면 카테고리를 랜덤으로 불러옵니다...")
    cnt = 0
    links = []
    #unsplash 사이트에서 카테고리별 링크를 리스트에 넣는다
    urls = [ "https://unsplash.com/t/wallpapers" , "https://unsplash.com/t/textures-patterns" , "https://unsplash.com/t/nature", "https://unsplash.com/t/current-events", "https://unsplash.com/t/current-events"
        , "https://unsplash.com/t/business-work", "https://unsplash.com/t/film", "https://unsplash.com/t/animals", "https://unsplash.com/t/travel", "https://unsplash.com/t/fashion", "https://unsplash.com/t/food-drink",
        "https://unsplash.com/t/spirituality", "https://unsplash.com/t/experimental", "https://unsplash.com/t/people", "https://unsplash.com/t/health", "https://unsplash.com/t/arts-culture"]
    #카테고리중 랜덤으로 하나를 지정한다
    url = urls[random.randint(0, len(urls)-1)]
    #지정된 카테고리 사이트를 파싱한다
    html = urlopen(url)
    obj = BeautifulSoup(html, "html.parser")
    
    #a으로 시작하는 코드에서 /photos라고 되있는 부분을 전부 필터링한다
    for link in obj.find_all("a", href = re.compile('^(/photos)')):
        #필터링 중 다른 정보도 섞여있기 때문에 파싱된 소스에서 이미지는 앞에 href가 붙는데 다시 필터링한다
        if 'href' in link.attrs:
            #파싱한 정보를 이미지 다운로드 링크 형식에 맞춰 다시 복구한다. 그리고 links 변수에 append 한다
            links.append("https://unsplash.com" + link.attrs['href'] + "/download?force=true")
            #6장을 다운받으면 중지
            if cnt == 5:
                break
            cnt += 1
    #links 리턴한다
    return links

#이미지 다운로드
def IMG_Down():
    cnt = 1
    #파싱함수에서 받은 리턴값을 links에 넣는다
    links = BG_Parsing()
    
    print("바탕화면 다운로드 시작합니다...")
    #links별로 파일을 다운로드한다
    for link in links:
        #파일 경로를 지정한다
        paths = path + str(cnt) + ".png"
        urlretrieve(link, paths)
        print("(",cnt, "/ 6 )",os.path.getsize(paths)/1024,'KB 다운로드 완료')
        cnt += 1

#파싱과 이미지 다운로드를 실행한다
IMG_Down()

#이미지 형식을 fnameList에 추가한다
fnameList = []
for n in range (1, 7) :
    fnameList.append(str(n) + ".png")

#몇번째 그림인지 판별하는 인덱스
num = 0

#다음 클릭시
def clickNext():
    #전역변수 num으로 증감한다. 만약 6장이 초과되었으면 다시 0번째로 돌아간다
    global num
    num += 1
    if num > 5:
        num = 0
    
    #이미지 사이즈가 커서 불러온 후 16:9 비율에 맞춰 리사이징 시킨다
    file = Image.open(path + fnameList[num])
    resize = file.resize((800, 450))
    photo = ImageTk.PhotoImage(resize)
    pLabel.configure(image = photo)
    pLabel.image = photo
    #적용 버튼을 클릭하면 setwallpaper 함수가 불러와진 후 해당그림을 바탕화면으로 지정한다
    btnApply = Button(window, text = "바탕화면 적용", command = (lambda: setWallpaper(path + fnameList[num])))

#이전 클릭시
def clickPrev():
    #전역변수 num으로 증감한다. 만약 0장 미만이면 다시 6번째로 돌아간다
    global num
    num -= 1
    if num < 0:
        num = 5
        
    #이미지 사이즈가 커서 불러온 후 16:9 비율에 맞춰 리사이징 시킨다
    file = Image.open(path + fnameList[num])
    resize = file.resize((800, 450))
    photo = ImageTk.PhotoImage(resize)
    pLabel.configure(image = photo)
    pLabel.image = photo
    #적용 버튼을 클릭하면 setwallpaper 함수가 불러와진 후 해당그림을 바탕화면으로 지정한다
    btnApply = Button(window, text = "바탕화면 적용", command = (lambda: setWallpaper(path + fnameList[num])))

#바탕화면 설정. dll 로드 후 해당 경로 이미지를 적용시킨다
def setWallpaper(path):
    return ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
   
#tk 크기와 제목 지정한다
window = Tk()
window.geometry("834x526")
window.title("Today Splash")

#버튼 역할을 지정한다
btnPrev = Button(window, text = "<< 이전", command = clickPrev)
btnNext = Button(window, text = "다음 >>", command = clickNext)
btnApply = Button(window, text = "바탕화면 적용", command = (lambda: setWallpaper(path + fnameList[num])))

#처음 로딩시 원본 이미지를 창 크기에 맞춰 리사이징 시킨다
file = Image.open(path + fnameList[num])
resize = file.resize((800, 450))
photo = ImageTk.PhotoImage(resize)
pLabel = Label(window, image = photo)

#버튼 위치를 지정한다
btnPrev.place(x = 300, y = 10)
btnNext.place(x = 473, y = 10)
btnApply.place(x = 370, y = 10)
pLabel.place(x = 15, y = 50)

#실행
window.mainloop()