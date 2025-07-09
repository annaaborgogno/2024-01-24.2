import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._methods = []
        self._years = []
        self._graph = nx.DiGraph()
        self._nodes = []
        self._edges = []
        self._idMap = {}
        self._soluzione = []
        self._costoMigliore = 0

    def getBestPath(self):
        self._soluzione = []
        self._lenMigliore = 0
        for nodo in self._graph.nodes:
            if self._graph.in_degree(nodo) == 0:
                parziale = [nodo]
                self._ricorsione(parziale)
        return self._soluzione, self._lenMigliore

    def _ricorsione(self, parziale):
        if self._graph.out_degree(parziale[-1]) == 0: #è una soluzione ammissibile
            if len(parziale) > self._lenMigliore:
                self._soluzione = copy.deepcopy(parziale)
                self._lenMigliore = len(parziale)

        for n in self._graph.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()

    def getMethods(self):
        self._methods = DAO.getMethods()
        return self._methods

    def getYears(self):
        self._years = DAO.getYears()
        return self._years

    def getNodes(self, method, year):
        self._nodes = DAO.getNodes(method, year)
        return self._nodes

    def addAllEdges(self, method, year, s):
        self._edges = DAO.getEdges(method, year, s)
        for e in self._edges:
            if e.product_number1 in self._idMap and e.product_number2 in self._idMap:
                u = self._idMap[e.product_number1]
                v = self._idMap[e.product_number2]
                self._graph.add_edge(u, v)
        return self._edges

    def buildGraph(self, year, method, s):
        self._graph.clear()
        self._nodes = []
        self._edges = []
        self._idMap = {}
        self.getNodes(method, year)
        self._graph.add_nodes_from(self._nodes)
        for n in self._nodes:
            self._idMap[n.product_number] = n
        self.addAllEdges(method, year, s)
        return self._graph

    def getGraphDetails(self):
        nNodes = self._graph.number_of_nodes()
        nEdges = self._graph.number_of_edges()
        return nNodes, nEdges

    def getProdottiRedd(self):
        candidati = []
        for n in self._graph.nodes:
            if self._graph.out_degree(n) == 0:
                in_deg = self._graph.in_degree(n)
                candidati.append((n, in_deg))

        candidati.sort(key=lambda x: x[1], reverse=True)
        top5 = candidati[:5]
        return top5