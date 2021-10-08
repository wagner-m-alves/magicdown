import selenium.webdriver as Webdriver
import re as Regex
import time as Time
from Content import Serie


class Browser:
    def __init__(self):
        self.__Current      = None
        self.__Selected     = None
        self.__Options      = {'C': 'Google Chrome', 'F': 'Mozilla Firefox'}


    def OpenBrowser(self, what):
        self.__Selected = what

        try:
            if(what == 'C'):
                print(f'Abrindo {self.__Options[self.__Selected]}...')
                self.__Current = Webdriver.Chrome()
                self.__Current.implicitly_wait(20)
                self.__Current.minimize_window()
                print(f'{self.__Options[self.__Selected]} aberto com sucesso!')
            elif(what == 'F'):
                print(f'Abrindo {self.__Options[self.__Selected]}...')
                self.__Current = Webdriver.Firefox()
                self.__Current.implicitly_wait(20)
                self.__Current.minimize_window()
                print(f'{self.__Options[self.__Selected]} aberto com sucesso!')
            else:
                print('Opção invalida! Tente novamente.')
        except Exception:
            print('Falha! Infelizmente não foi possível abrir o navegador.')


    def AccessPage(self, url):
        try:
            print(f'Acessando página: {url}...')
            self.__Current.get(url)
        except Exception:
            self.CloseBrowser()
            print('Falha! Infelizmente não foi possível acessar a página.')


    def FindElement(self, many, by, param):
        Element = None

        try:
            if(many == True):
                if(by == 'class_name'):
                    Element = self.__Current.find_elements_by_class_name(param)
                elif(by == 'css_selector'):
                    Element = self.__Current.find_elements_by_css_selector(param)
                elif(by == 'id'):
                    Element = self.__Current.find_elements_by_id(param)
                elif(by == 'name'):
                    Element = self.__Current.find_elements_by_name(param)
                elif(by == 'tag_name'):
                    Element = self.__Current.find_elements_by_tag_name(param)
                elif(by == 'xpath'):
                    Element = self.__Current.find_elements_by_xpath(param)
            elif(many == False):
                if (by == 'class_name'):
                    Element = self.__Current.find_element_by_class_name(param)
                elif (by == 'css_selector'):
                    Element = self.__Current.find_element_by_css_selector(param)
                elif (by == 'id'):
                    Element = self.__Current.find_element_by_id(param)
                elif (by == 'name'):
                    Element = self.__Current.find_element_by_name(param)
                elif (by == 'tag_name'):
                    Element = self.__Current.find_element_by_tag_name(param)
                elif (by == 'xpath'):
                    Element = self.__Current.find_element_by_xpath(param)
            else:
                print('Falha! Um ou mais parametros invalidos.')

            return Element
        except Exception:
            self.CloseBrowser()
            print('Falha! Não foi possível encontrar o elemento.')


    def CloseBrowser(self):
        self.__Current.close()
        print(f'{self.__Options[self.__Selected]} fechado com sucesso!')


class ComandoTorrentsOrg(Browser):
    def __init__(self):
        Browser.__init__(self)
        Browser.OpenBrowser(self, 'F')
        self.Name       = 'ComandoTorrentsOrg'
        self.Address    = 'https://comandotorrents.org'


    def __Filter(self, sample):
        try:
            Response = False

            # Verificar se é Dual Audio
            Match = Regex.search(r'DUAL', sample)
            if(Match):
                Response = True

            return Response
        except Exception:
            print('Erro! Não foi possível filtrar.')


    def __Treat(self, magnetic_link):
        return str(magnetic_link).split('&')[0]


    def __Search(self, content):
        Content = str(content).lower()

        # Acessar página principal do site
        Browser.AccessPage(self, self.Address)

        # Pesquisar conteúdo
        try:
            print(f'Pesquisanado por: {Content}...')
            Form = Browser.FindElement(self, False, 'tag_name', 'form')
            Form.find_element_by_tag_name('input').send_keys(Content)
            Form.submit()

            # Encontrar link do conteúdo
            Time.sleep(20)
            Article = Browser.FindElement(self, False, 'tag_name', 'article')
            Link = Article.find_element_by_tag_name('header').find_element_by_tag_name('a').get_attribute('href')
            print('Pesquisa concluída com sucesso!')

            # Retornar link do conteúdo
            return Link
        except Exception:
            Browser.CloseBrowser(self)
            print('Erro! Não foi possível pesquisar.')


    def GetMagneticLinks(self, Serie, Session):
        Content = f'{Serie} {Session}ª temporada dual audio'
        Url = self.__Search(Content)
        Response = []

        # Acessar página do conteúdo
        Browser.AccessPage(self, Url)

        # Extrair links
        try:
            print('Extraíndo links da página...')
            Div = Browser.FindElement(self, False, 'class_name', 'entry-content')
            Links = Div.find_elements_by_tag_name('a')

            for L in Links:
                Link = L.get_attribute('href')

                if (self.__Filter(Link)):
                    Response.append(self.__Treat(Link))

            if Response:
                print(f'Links extraídos: {len(Response)}')
            else:
                print(f'Links extraídos: {0}')

            return Response
        except Exception:
            Browser.CloseBrowser(self)
            print('Erro! Não foi possível obter magneticlinks.')