import requests
from bs4 import BeautifulSoup

def ft_requests(url,header=None,proxies=None):
    request = requests.get(url=url,headers=header,proxies=proxies)
    if not request.ok:
        print(f"requests bad , error code {request.status_code}")
        return 1 
    soup = BeautifulSoup(request.text,"lxml")
    return soup

def link_wallpaper(url , resolution = None):
    soup = ft_requests(url)

    max = ""
    for i in soup.find_all("a",{"class": "resolutions__link"}):
        #? Ajout une possibiliter de choisir un resolution si possible  

        max = i["href"] 
    return "https://wallpaperscraft.com"+max

def link_download(url, file="./imgs.jpg"):
    soup = ft_requests(url)
    x = soup.find("a",{"class":"gui-button"})["href"]

    response = requests.get(x,stream=True)

    with open(file, 'wb') as f:
        f.write(response.content)


# * FONCTION APPEL 
def ft_wallpaper(file = "./"):
    page = 1
    url = f"https://wallpaperscraft.com/catalog/anime/page{page}"
    soup = ft_requests(url)

    #! moddification nul pour des teste plus fun
    #* for link in soup.find_all("a",{"class" : "wallpapers__link"})
    
    y = soup.find_all("a",{"class" : "wallpapers__link"})
    y.pop(0)

    for link in y:
        x = link_wallpaper("https://wallpaperscraft.com/"+link["href"])
        link_download(x,file)
        
        return 1 
    
ft_wallpaper("./img.jpg")