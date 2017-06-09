from bs4 import BeautifulSoup
import webbrowser
import urllib
import requests
import re
from tqdm import tqdm
import zipfile

class Subtitle:
    def download(self,moviepath,moviename):
        try:
                
            base_url='http://www.subscene.com'
            url='http://www.subscene.com/subtitles/'+moviename+'/english'
            soup=BeautifulSoup(requests.get(url).content,'lxml')
            tag=soup.find('a',href=re.compile("/english/*"))
            soup=BeautifulSoup(requests.get(base_url+tag['href']).content,'lxml')
            tag1=soup.find('a',href=re.compile("/subtitle/download*"))
            url = base_url+tag1['href']
            response = requests.get(url, stream=True)
            subtitle_zip_file=moviepath+"\\"+moviename+".zip"
            with open(subtitle_zip_file, "wb") as handle:
                for data in tqdm(response.iter_content()):
                    handle.write(data)
        except:
            print("Error downloading file")
        try:
            zip_ref=zipfile.ZipFile(subtitle_zip_file,'r')
            zip_ref.extractall(moviepath)
            zip_ref.close()
        except:
            print("error extracting")
s=Subtitle()
s.download("G:\movies\Logan'","Logan")

