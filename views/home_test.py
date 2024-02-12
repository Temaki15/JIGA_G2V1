import flet as ft
from flet_route import Params, Basket

def Home1(page: ft.Page, params: Params, basket: Basket):
    print(Params)

    return ft.View(
        "/",

        controls = [
            ft.Text("This is HOME"),
            ft.ElevatedButton("page 1", on_click = lambda _: page.go("/page1/10")),
            ft.ElevatedButton("page 2", on_click = lambda _: page.go("/page2/TMK"))
        ]
    )