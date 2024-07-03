import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choise_anno = None
        self._choise_squadra = None

    def handleCreaGrafo(self, e):
        self._model.buildGraph(self._choise_anno)
        self._view._txt_result.controls.append(ft.Text(f"Grafo creato con {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi"))
        self._view.update_page()

    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()
        adiacenti=self._model.getAdiacenti(self._choise_squadra)
        self._view._txt_result.controls.append(ft.Text(f"Adiacenti per la squadra {str(self._choise_squadra)}"))
        for nodo in adiacenti.keys():
            self._view._txt_result.controls.append(ft.Text(f"{str(nodo)} {adiacenti[nodo]} "))
        self._view.update_page()


    def handlePercorso(self, e):
        self._view._txt_result.controls.clear()
        percorso, best_peso=self._model.getPercorso(self._choise_squadra)
        print(percorso)
        self._view._txt_result.controls.append(ft.Text(f"Percorso trovato con peso massimo {best_peso}"))
        for squadra in percorso:
            self._view._txt_result.controls.append(ft.Text(f"{squadra} "))
        self._view.update_page()


    def fillddAnno(self):
        anni=self._model.getAnni()
        for anno in anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(data=int(anno), text=anno, on_click=self.readDDAnno))

    def readDDAnno(self, e):
        print("read dd anno called")
        if e.control.data==None:
            self._choise_anno=None
            return
        self._choise_anno=e.control.data

    def handle_squadre(self, e):
        print("handle squadre called")
        squadre_anno=self._model.getSquadreAnno(self._choise_anno)
        self._view._txtOutSquadre.controls.clear()
        self._view._txtOutSquadre.controls.append(
            ft.Text(f"Squadre presenti nell'anno{self._choise_anno}= {len(squadre_anno)}"))
        for squadra in squadre_anno:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{squadra}"))
            self._view._ddSquadra.options.append(ft.dropdown.Option(data=squadra, text=str(squadra), on_click=self.readDDSquadra))
        self._view.update_page()

    def readDDSquadra(self, e):
        if e.control.data is None:
            self._choise_squadra=None
            return
        self._choise_squadra=e.control.data

