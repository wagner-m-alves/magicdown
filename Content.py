from os import listdir
from os.path import isfile, join
import re as Regex


class Serie:
    def Load(self):
        Response = []

        try:
            with open('DATA\SERIES.txt', 'r') as File:
                for Line in File:
                    Serie = Line.strip()
                    Response.append(Serie)
        except FileNotFoundError:
            print('Erro! Dados não localizados.')
        except IsADirectoryError:
            print('Erro! Foi informado um diretorio ao invés de um arquivo.')
        except PermissionError:
            print('Erro! Permissão negada.')
        except Exception:
            print('Erro! Não foi possível carregar os dados.')
        finally:
            return Response


    def New(self, name):
        try:
            with open('DATA\SERIES.txt', 'a') as File:
                File.write(str(name).upper() + '\n')
            print('Nova serie cadastrada com sucesso!')
        except IsADirectoryError:
            print('Erro! Foi informado um diretorio ao invés de um arquivo.')
        except PermissionError:
            print('Erro! Permissão negada.')
        except Exception:
            print('Erro! Não foi possível salvar novos dados.')


class Session:
    def Load(self, serie_name):
        Response = []

        try:
            Path = f'DATA\SESSIONS'
            Response = [f for f in listdir(Path) if isfile(join(Path, f)) and Regex.search(serie_name, f)]
        except Exception:
            print('Erro! Não foi possível carregar os dados.')
        finally:
            return Response


    def __ExistEpisodeLink(self, serie_name, session_number, magnetic_link):
        Response = False

        try:
            with open(f'DATA\SESSIONS\\{serie_name}.S{session_number}.txt', 'r') as File:
                for Line in File:
                    if Line.strip() == magnetic_link:
                        Response = True
                        break

            return Response
        except Exception:
            print('Erro! Não foi possível verificar se o link existe!')


    def AddNewEpisodeLink(self, serie_name, session_number, magnetic_link):
        try:
            Counter = 0

            for Link in list(magnetic_link):
                if not self.__ExistEpisodeLink(serie_name, session_number, Link):
                    Counter += 1

                    with open(f'DATA\SESSIONS\\{serie_name}.S{session_number}.txt', 'a') as File:
                        File.write(Link + '\n')

                    with open('T_WaitingToDownload.txt', 'a') as File:
                        File.write(Link + '\n')

            print(f'Episodio(s) da {session_number}ª temporada de {serie_name} adicionado(s): {Counter}')

        except IsADirectoryError:
            print('Erro! Foi informado um diretorio ao invés de um arquivo.')
        except PermissionError:
            print('Erro! Permissão negada.')
        except Exception:
            print('Erro! Não foi possível salvar novos dados.')