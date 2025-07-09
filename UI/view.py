import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._ddyear = None
        self._ddcolor = None
        self.btn_graph = None
        self.txt_result = None
        self.txt_container = None

        self._ddnode = None
        self.btn_search = None
        self.txtOut2 = None

    def load_interface(self):
        # title
        self._title = ft.Text("TdP 2025 - Prova tema d'esame", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW with some controls
        # text field for the name
        self._ddYear = ft.Dropdown(label="Anno")
        self._controller.fillDDYear()
        # button for the "creat graph" reply
        self.btn_graph = ft.ElevatedButton(text="Creazione grafo", on_click=self._controller.handle_creaGrafo)
        row1 = ft.Row([self._ddYear, self.btn_graph],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        self._ddMethod = ft.Dropdown(label="Metodo")
        self._controller.fillDDMethods()
        self.btn_graph = ft.ElevatedButton(text="Calcola prodotti", on_click=self._controller.handle_calcolaProdotti)

        row2 = ft.Row([self._ddMethod, self.btn_graph],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self._ricavoDiff = ft.TextField(label="Differenza ricavi")
        self.btn_search = ft.ElevatedButton(text="Cerca Percorso", on_click=self._controller.handle_search)
        row3 = ft.Row([self._ricavoDiff, self.btn_search],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=10, auto_scroll=False)
        self._page.controls.append(self.txt_result)

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()