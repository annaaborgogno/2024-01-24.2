import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selectedMethod = None

    def handle_creaGrafo(self, e):
        year = self._view._ddYear.value
        if year is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un anno", color="red"))
            self._view.update_page()
            return

        if self._selectedMethod is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un metodo", color="red"))
            self._view.update_page()
            return

        method = self._selectedMethod.Order_method_type

        sInput = self._view._ricavoDiff.value
        if sInput == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un numero per la percentuale di ricavo", color="red"))
            self._view.update_page()
            return

        try:
            sVal = float(sInput)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore numerico", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(year, method, sVal)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato", color="green"))
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}, numero di archi {nEdges}"))
        self._view.update_page()

    def handle_calcolaProdotti(self, e):
        res = self._model.getProdottiRedd()
        for n, d in res:
            self._view.txt_result.controls.append(ft.Text(f" Prodotto: {n.product_number}, con {d} archi entranti e ricavo {n.ricavoTot}"))
        self._view.update_page()

    def handle_search(self, e):
        soluzione, lenMigliore = self._model.getBestPath()
        self._view.txt_result.controls.append(ft.Text(f"Il cammino migliore è stato trovato, con lunghezza {lenMigliore}", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"I nodi che lo compongono sono:"))
        for n in soluzione:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def fillDDMethods(self):
        methods = self._model.getMethods()
        for m in methods:
            self._view._ddMethod.options.append(ft.dropdown.Option(data=m, text=m.Order_method_type, on_click=self._getSelectedMethod))

    def _getSelectedMethod(self, e):
        if e.control.data is None:
            self._selectedMethod = None
        else:
            self._selectedMethod = e.control.data
            print(f"Method called: {self._selectedMethod}")
        return self._selectedMethod

    def fillDDYear(self):
        years = self._model.getYears()
        for y in years:
            self._view._ddYear.options.append(ft.dropdown.Option(y))
