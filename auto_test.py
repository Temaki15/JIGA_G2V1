import flet as ft

def auto_test(page: ft.Page):

    return ft.View(
        "/auto_test",

        controls = [
            ft.Text("This is the auto test page"),
            ft.ElevatedButton("HOME", on_click = lambda _: page.go("/"))
        ]
    )