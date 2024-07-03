import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo=nx.Graph()
        self._lista_nodi=[]
        self.idMap={}
        self.best_path=[]
        self._max_peso=0

    def getAnni(self):
        return DAO.getAllYears()

    def getSquadreAnno(self, anno):
        self._lista_nodi=DAO.getTeams(anno)
        for nodo in self._lista_nodi:
            self.idMap[nodo.ID]=nodo
        return self._lista_nodi

    def buildGraph(self, anno):
        self.grafo.clear()
        self.grafo.add_nodes_from(self._lista_nodi)
        salariTeam=DAO.getPeso2(anno, self.idMap)
        for s1 in self.grafo.nodes:
            for s2 in self.grafo.nodes:
                if s1!=s2:
                    self.grafo.add_edge(s1, s2, weight=salariTeam[s1]+salariTeam[s2])

    def getAdiacenti(self, s0):
        adiacenti={}
        if s0 not in self.grafo.nodes:
            return
        for nbr in self.grafo.neighbors(s0):
            adiacenti[nbr]=self.grafo[s0][nbr]["weight"]
        print(adiacenti)
        sorted_adiacenti={k:v for k,v in sorted(adiacenti.items(), key=lambda item:item[1], reverse=True)}
        return sorted_adiacenti

    def getPercorso(self, squadraP):
        self.best_path = []
        self._ricorsione2([squadraP], -1)
        return self.best_path, self._max_peso

    def _ricorsione(self, parziale, ultimo_peso):
        #controllo se parziale sia meglio di best
        peso=self.calcolaPeso(parziale)
        if peso>self._max_peso:
            self._max_peso=peso
            self.best_path = copy.deepcopy(parziale)
        #continuo ad aggiungere nodi (tra tutti i vicini aggiungi il primo che soddisfa i vincoli)
        for nbr in self.grafo.neighbors(parziale[-1]):
            p=self.grafo[parziale[-1]][nbr]["weight"]
            if nbr not in parziale and (p<ultimo_peso or ultimo_peso==-1):
                parziale.append(nbr)
                self._ricorsione(parziale, p)
                parziale.pop()
    def _ricorsione2(self, parziale, ultimo_peso):
        #controllo se parziale sia meglio di best
        peso=self.calcolaPeso(parziale)
        if peso>self._max_peso:
            self._max_peso=peso
            self.best_path = copy.deepcopy(parziale)
        #continuo ad aggiungere nodi
        #sorto in ordine decrescente perche voglio MASSIMIZZARE il peso
        listaVicini=[]
        for nbr in self.grafo.neighbors(parziale[-1]):
            p= self.grafo[parziale[-1]][nbr]["weight"]
            listaVicini.append((nbr, p))
        # prendo IL PRIMO NODO CON PESO MAGGIORE CHE SODDISFA I VINCOLI
        listaVicini.sort(key=lambda x: x[1], reverse=True)
        for v in listaVicini:
            if v[0] not in parziale and (v[1]<ultimo_peso or ultimo_peso==-1):
                parziale.append(v[0])
                self._ricorsione2(parziale, v[1])
                parziale.pop()
                return
    def calcolaPeso(self, parziale):
        peso=0
        for i in range (0, len(parziale)-1):
            n1=parziale[i]
            n2=parziale[i+1]
            peso+=self.grafo[n1][n2]["weight"]
        return peso






    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)
