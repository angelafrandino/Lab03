import csv
from operator import attrgetter
from strumento import Strumento
from prestito import Prestito

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.responsabile = responsabile
        self.prestiti = {}          # Dizionario {codice_prestito: oggetto Prestito}
        self.strumenti = []         # Lista contenente gli oggetti Strumento
        self._prossimo_id_prestito = 1      # Contatore per generare P1, P2, P3...

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, mode = "r", encoding= 'utf-8') as file:
                reader = csv.reader(file)
                for riga in reader:
                    if not riga:
                        continue

                    codice = riga[0].strip()
                    tipo = riga[1].strip()
                    marca = riga[2].strip()
                    anno_acquisto = int(riga[3].strip())
                    valore = float(riga[4].strip())

                    nuovo_oggetto = Strumento(codice, tipo, marca, anno_acquisto, valore)
                    self.strumenti.append(nuovo_oggetto)

        except FileNotFoundError:
            print(f"Impossibile trovare il file specificato: '{file_path}'")


    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        max_id = 0

        for s in self.strumenti:        #cerco numero èiù alto tra strumenti esistenti
            if s.codice.startswith('S'):
                try:
                    num = int(s.codice[1:])  # Prende la parte numerica dopo la 'S'
                    if num > max_id:
                        max_id = num
                except ValueError:
                    pass

        nuovo_codice = f"S{max_id+1}"
        nuovo_strumento = Strumento(nuovo_codice, tipo, marca, anno_acquisto, valore)
        self.strumenti.append(nuovo_strumento)
        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti, key=attrgetter('marca'))

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""

        trovato = False
        for s in self.strumenti:        #controllo se strumento esiste nel deposito
            if s.codice == id_strumento:
                trovato = True
                break
        if not trovato:
            raise Exception("strumento non trovato")  # Blocca la funzione qui!

        for p in self.prestiti.values():        #controllo se strumento è già in prestito
            if p.id_strumento == id_strumento:
                raise Exception(f"lo strumento '{id_strumento}' è già in prestito.")

        codice_np = f"P{self._prossimo_id_prestito}"        #creo nuovo codice prestito
        self._prossimo_id_prestito += 1
        nuovo_p = Prestito(codice_np, data, id_strumento, cognome_allievo)
        self.prestiti[id_strumento] = nuovo_p
        return nuovo_p


    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito not in self.prestiti:
            raise Exception(f"Errore: Nessun prestito trovato con ID '{id_prestito}'.")

        del self.prestiti[id_prestito]
