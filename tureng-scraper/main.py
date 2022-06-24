from bs4 import BeautifulSoup as bs
import requests
import sys

class word:
    meaning = ""
    type = ""
    category = ""
    isOK = True

    def __init__(self, element) -> None:
        try:
            self.meaning = element.find(class_="tr ts").text
            self.category = element.find_all(class_="hidden-xs")[1].text
            i = element.find("i").text
            if "i." in i:
                self.type = "isim"
            elif "f." in i:
                self.type = "fiil"
            else:
                self.type = "sıfat"
            
        except:
            self.isOK = False

def appendToList(tr_elements):
    list = []
    newList = []
    for i in tr_elements:
        wordItem = word(i)
        if wordItem.isOK:
            list.append(word(i))
    ln = len(list)
    if ln < 10:
        i = 0
        while i < ln:
            newList.append(list[i])
            i += 1
    else:
        i = 0
        while(i < 10):
            newList.append(list[i])
            i += 1
    json_string = "{'word': ["
    for i in newList:
        json_string += str(i.__dict__)#json.dumps(i.__dict__, ensure_ascii=False)
        if i != newList[-1]:
            json_string += ","
    json_string += "]}"
    return json_string

try:
    input = str(sys.argv[1])
    req = requests.get("https://tureng.com/tr/turkce-ingilizce/" + input)
    soup = bs(req.text, features="html.parser")
    fileName = "./words/" + input + ".json"
    soupBool = True

    for i in soup.find_all("h1"):
        if "Aradığınız terimin karşılığı bulunamadı" in i.text or "Sanırız yanlış oldu, doğrusu şunlar olabilir mi?" in i.text:
            soupBool = False

    if soupBool:
        sys.stdout = open(fileName,"w")
        tr_elements = soup.find_all("tr")
        json_string = appendToList(tr_elements).replace("'", '"')
        print(json_string)

except:
    pass