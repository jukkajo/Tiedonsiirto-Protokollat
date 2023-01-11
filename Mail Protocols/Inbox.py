from threading import Lock
#sailöö spostit "palvelimelle", tai sanotaan, imitoi tätä, ei talleta pysyvästi mitään tietokantaan tms.

class Inbox:
    Lock = Lock()    
    #t-rakenne
    spostit = list()
    def __init__(self):
        pass
    
    #palauttaa postit rivinvaihdolla eroteltuna
    def palauta_sposti(self):
        lista = ""
        
        for i in range(len(self.spostit)):
            #
            lista += self.spostit[i].__str__() + "\n"
        
        return lista

    #sailö uusi    
    def sailo_sposti(self, sposti):
        self.Lock.acquire()
        self.spostit.append(sposti)
        self.Lock.release()

    def laske_postit(self):
        return len(self.spostit)

    def palauta_pop3_postit(self):
        #spostit rivinvaihdoilla eroteltuna
        rvlista= ""
        monesv = 1
        for i in range(len(self.spostit)):
            rvlista += str(monesv) + " " + str(self.spostit[i].__str__().encode("utf-8")) + "\n"
            monesv += 1

        #ylim rv lopussa
        if len(self.spostit) != 0:
            return rvlista[:-1]
        
        return rvlista
