from selenium.webdriver import Firefox
import time as Time
import requests as Requests
from bs4 import BeautifulSoup
import re as Regex


class Downloader():
    def __init__(self, links):
        self.__Links = links


    def __Down(self, uri, output_file_name):
        try:
            print(f'Baixando {output_file_name} agora...')
            Response = Requests.get(uri)
            with open(output_file_name, 'wb') as File:
                File.write(Response.content)
            print(f'{output_file_name} baixado com sucesso!' + '\n')
        except MemoryError:
            print(f'{output_file_name} falhou!!!' + '\n')


    def Run(self):
        for Link in self.__Links:
            FileName = Link.split('/')[-1]
            self.__Down(Link, FileName)


class Scraper():
    def __init__(self):
        self.__Browser = Firefox()
        self.__Browser.implicitly_wait(35)


    def __Iterations(self, target):
        self.__Browser.get(target)
        Rows = self.__Browser.find_elements_by_xpath('//*[@id="xfiles"]/tbody/tr')
        return len(Rows)


    def __GetTargets(self, target):
        Iterations  = self.__Iterations(target)
        Counter     = 2
        Response    = []


        if (Iterations > 1):
            try:
                for Episode in range(2, Iterations + 1):
                    Time.sleep(3)
                    Element = self.__Browser.find_element_by_xpath('//*[@id="xfiles"]/tbody/tr[' + str(Episode) + ']/td[1]/a')
                    Url = Element.get_attribute('href')
                    Element.click()

                    Time.sleep(3)
                    Form = self.__Browser.find_element_by_tag_name('Form')
                    ID = Form.find_element_by_name('id').get_attribute('value')
                    Params = {"op": "download2", "id": ID, "rand": "", "referer": target,"method_free": "Free+Download", "method_premium": "", "adblock_detected": "0"}

                    Result = Requests.post(Url, Params)
                    Page = BeautifulSoup(Result.text, 'html.parser')

                    AllLinks = Page.findAll('a')

                    padrao = r'<a\s?href="(https://s.*)">'
                    for lk in AllLinks:
                        Match = Regex.search(padrao, str(lk))
                        if (Match):
                            OnlyLink = Regex.sub(r'">.*', '', Match.group(1))
                            Response.append(OnlyLink.strip())
                            self.__Save(OnlyLink.strip())

                    Counter += 1

                    if (Counter < Iterations + 1):
                        self.__Browser.get(target)
            except:
                self.__Browser.close()
                print('Falha inesperada! Tente novamente.')


        return Response


    def __Save(self, link):
        with open('Logs\LatestDownloaded.log.txt', 'a') as File:
            File.write(link + '\n')


    def Run(self):
        Targets = []

        with open('N_WaitingToDownload.txt', 'r') as File:
            for W in File:
                Targets += self.__GetTargets(W.strip())

        self.__Browser.close()

        if(Targets):
            Obj_Downloader = Downloader(Targets)
            Obj_Downloader.Run()