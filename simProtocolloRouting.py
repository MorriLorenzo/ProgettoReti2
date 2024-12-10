# Simulazione del protocollo di Routing

class Nodo:
    def __init__(self, nome):
        # Inizializza un nodo con il proprio nome e una tabella di routing
        # La tabella di routing parte con un unico elemento: se stesso con costo 0
        self.nome = nome
        self.tabella_di_routing = {nome: (0, nome)}  # {destinazione: (costo, prossimo_hop)}

    def aggiorna_tabella_di_routing(self, vicino, tabella_vicino):
        # Aggiorna la tabella di routing in base ai dati ricevuti dal nodo vicino
        aggiornato = False
        for destinazione, (costo_destinazione, prossimo_hop) in tabella_vicino.items():
            # Calcola il nuovo costo passando attraverso il nodo vicino
            nuovo_costo = vicino.tabella_di_routing[self.nome][0] + costo_destinazione
            # Aggiorna solo se la destinazione non è presente o il nuovo costo è inferiore
            if destinazione not in self.tabella_di_routing or nuovo_costo < self.tabella_di_routing[destinazione][0]:
                self.tabella_di_routing[destinazione] = (nuovo_costo, vicino.nome)
                aggiornato = True
        return aggiornato

    def stampa_tabella_di_routing(self):
        # Stampa in modo leggibile la tabella di routing del nodo
        print(f"Tabella di routing per {self.nome}:")
        print("Destinazione\tCosto\tProssimo Hop")
        for destinazione, (costo, prossimo_hop) in sorted(self.tabella_di_routing.items()):
            print(f"{destinazione}\t\t{costo}\t{prossimo_hop}")
        print()

class Rete:
    def __init__(self):
        # Inizializza una rete vuota
        self.nodi = {}

    def aggiungi_nodo(self, nome_nodo):
        # Aggiunge un nuovo nodo alla rete
        self.nodi[nome_nodo] = Nodo(nome_nodo)

    def collega_nodi(self, nome_nodo1, nome_nodo2, costo):
        # Collega due nodi con un costo specificato
        if nome_nodo1 not in self.nodi or nome_nodo2 not in self.nodi:
            raise ValueError("Entrambi i nodi devono esistere nella rete.")

        nodo1, nodo2 = self.nodi[nome_nodo1], self.nodi[nome_nodo2]
        # Aggiorna le tabelle di routing per riflettere la connessione diretta
        nodo1.tabella_di_routing[nome_nodo2] = (costo, nome_nodo2)
        nodo2.tabella_di_routing[nome_nodo1] = (costo, nome_nodo1)

    def simula_aggiornamenti_routing(self):
        # Simula iterativamente gli aggiornamenti delle tabelle di routing fino a stabilità
        aggiornato = True
        while aggiornato:
            aggiornato = False
            for nodo in self.nodi.values():
                for nome_vicino, (costo, _) in list(nodo.tabella_di_routing.items()):  # Itera su una copia
                    if nome_vicino != nodo.nome:  # Evita di aggiornare verso se stesso
                        vicino = self.nodi[nome_vicino]
                        # Propaga le informazioni di routing dai vicini
                        if nodo.aggiorna_tabella_di_routing(vicino, vicino.tabella_di_routing):
                            aggiornato = True

    def stampa_tutte_tabelle_di_routing(self):
        # Stampa le tabelle di routing di tutti i nodi della rete
        for nodo in self.nodi.values():
            nodo.stampa_tabella_di_routing()

# Esempio di utilizzo:
if __name__ == "__main__":
    rete = Rete()

    # Aggiungi nodi alla rete
    for nome_nodo in ["A", "B", "C", "D"]:
        rete.aggiungi_nodo(nome_nodo)

    # Collega i nodi con i relativi costi
    rete.collega_nodi("A", "B", 1)
    rete.collega_nodi("A", "C", 4)
    rete.collega_nodi("B", "C", 2)
    rete.collega_nodi("C", "D", 1)

    # Simula gli aggiornamenti delle tabelle di routing
    rete.simula_aggiornamenti_routing()

    # Stampa le tabelle di routing finali
    rete.stampa_tutte_tabelle_di_routing()
