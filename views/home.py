import flet as ft
from flet_route import Params, Basket

nav_icon_style: dict = {
    "offset": ft.transform.Offset(0, 0),
    "opacity": 1,
    "animate_offset": ft.Animation(500, "decelerate"),
    "animate_opacity": ft.Animation(300, "decelerate"),
    # "disable": True,    
}

class NavIcon(ft.Icon):
    def __init__(self, icon_name: str):
        super(NavIcon, self).__init__(name = icon_name,  **nav_icon_style)


nav_item_style: dict = {
    "width": 40,
    "height": 40,
    "shape": ft.BoxShape("circle"),   
}

class NavItem(ft.Container):
    def __init__(self, icon_name: str, text: ft.Text):
        super(NavItem, self).__init__(**nav_item_style, on_hover=self.selected)

        self.text: Text = text

        self.y0: Any = ft.transform.Offset(0, 0)
        self.y1: Any = ft.transform.Offset(0, -1)

        self.t0: Any = ft.transform.Offset(0, 1)
        self.t1: Any = ft.transform.Offset(0, 0)

        self.icon = NavIcon(icon_name)
        self.content = self.icon

    def selected(self, e):
        self.icon.offset = self.y1 if e.data == "true" else self.y0
        self.icon.opacity = 0 if e.data == "true" else 1

        self.text.offset = self.t1 if e.data == "true" else self.t0
        self.text.opacity = 1 if e.data == "true" else 0

        self.update()
        self.text.update()
        pass


nav_text_style: dict = {
    "width": 105,
    "size": 11.5,
    "text_align": "center",
    "offset": ft.transform.Offset(0, 1),
    "opacity": 0,
    "animate_offset": ft.Animation(350, "decelerate"),
    "animate_opacity": ft.Animation(500, "decelerate"),
}

class NavText(ft.Text):
    def __init__(self, value: str):
        super(NavText, self).__init__(value = value, **nav_text_style)


row_style: dict = {
    "top": 0,
    "bottom": 0,
    "left": 0,
    "right": 0,
    "alignment": "spaceAround",
    "vertical_alignment": "center",
    "expand": True
}


def Home(page: ft.Page, params: Params, basket: Basket):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor = "#1e1e1e"
    page.title = "Jiga AGVS G2"
    page.fonts = {"Orbitron": "font/Orbitron_Medium.ttf",}
    page.theme = ft.Theme(font_family="Orbitron")
    page.update()

    icons: list = ["home", "person", "notifications", "settings", "copy"]
    text: list = [NavText(title.upper()) for title in icons]

    stack: ft.Stack =  ft.Stack(
            expand = True,
            controls = [
                ft.Row(
                    **row_style, controls = text
                ),
                ft.Row(
                    **row_style,
                    spacing = 0,
                    controls= [NavItem(name, text[i]) for i, name in enumerate(icons)],
                    
                )
            ]
        )

    page.add(
            ft.Container(
                ft.Stack(
                    [
                        ft.Image(
                            src = "images/Logo_AGVS.png",
                            width = 400,            
                            fit=ft.ImageFit.CONTAIN,
                            right = 50,
                        ),

                        # ft.Text(
                        #     "JIGA DE TESTES G2",
                        #     font_family="Orbitron",
                        #     size = 50,
                        #     color = ft.colors.WHITE,
                        # ),

                        ft.Container(
                            width = 520,
                            height = 55,
                            shape = ft.BoxShape("rectangle"),
                            border_radius = 10,
                            bgcolor = "#3e3e42",
                            bottom = 80,
                            content = stack,
                        )
                    ],
                ),
                width=520,
                height=400,
            ),
        )
    
    

    return ft.View(
        "/",
        {
            ft.Text("piroca de batata")

        }
        
    )