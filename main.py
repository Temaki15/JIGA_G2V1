import serial.tools.list_ports
import serial
import threading
import binascii
import flet as ft
from time import sleep
from views.configuracoes import configuracoes
from views.teste_automatico import teste_automatico
from views.acionamentos import acionamentos

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 1024
    page.window_height = 600
    page.title = "Jiga AGVS G2"
    page.fonts = {"Orbitron": "fonts/Orbitron_Medium.ttf",}
    page.theme = ft.Theme(font_family="Orbitron")
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 0    
    page.window_resizable = False
    # page.window_full_screen = True
    page.window_maximizable = False
    # page.window_frameless = True
    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.OPEN_UPWARDS
    page.theme = theme
    page.update()

    def mockup_button(e):
        dlg = ft.AlertDialog(title = ft.Text("Nada programado ainda"))
        page.dialog = dlg
        dlg.open = True
        page.update()

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [           
                    ft.Container(
                        bgcolor = ft.colors.WHITE,
                        padding = 0,
                        margin=ft.margin.all(-10),
                        image_src="/images/abstract_bg.jpg",
                        image_fit = ft.ImageFit.COVER,
                        width = 1024,
                        height = 600,
                        expand=True,
                        alignment = ft.alignment.center,
                        content = ft.Stack(
                                    [
                                        ft.Container(
                                            # bgcolor = ft.colors.RED,
                                            width=1000,
                                            height=300,
                                            content = ft.Image(src=f"/images/Logo_AGVS.png", width=512, height=200, fit=ft.ImageFit.CONTAIN),    
                                            alignment = ft.alignment.center,
                                        ),

                                        ft.Text(
                                            "Jiga de Testes G2",
                                            font_family = "Orbitron",
                                            color = ft.colors.WHITE,
                                            width = 700,
                                            size = 45,
                                            bottom = 90,
                                            text_align = ft.TextAlign.CENTER,
                                        ),

                                        ft.Row(
                                            [
                                                ft.ElevatedButton("Teste Automático", on_click=lambda _: page.go("/teste"), bgcolor="#333333"),
                                                ft.ElevatedButton("Acionamento e Leitura RT", on_click=lambda _: page.go("/acionamentos"), bgcolor="#333333"),
                                                ft.ElevatedButton("Configurações", on_click=lambda _: page.go("/configuracoes"), bgcolor="#333333"),
                                                # ft.ElevatedButton("Configurações", on_click=ft.AlertDialog(title = "HJFKJHKJHKJHK"), bgcolor="#333333")
                                            ],
                                            bottom = 10,
                                            width = 700,
                                            alignment= ft.MainAxisAlignment.CENTER
                                        ),
                                    ],
                                    width = 700,
                                    height = 400,
                                ),               
                    ),
                ],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                vertical_alignment = ft.MainAxisAlignment.CENTER,
            )
        )
        page.update()

###################################### Pagina de teste automático ###################################################
        if page.route == "/teste":
            page.views.append(
                teste_automatico(page)
            )
        page.update()


################################## Pagina de acionamento e leituras manuais#########################################
        if page.route == "/acionamentos":
            page.views.append(
                acionamentos(page)
            )
        page.update()


######################################## Pagina de configurações ##################################################
        if page.route == "/configuracoes":
            print(len(page.views))
            page.views.append(
                configuracoes(page)
            )
        page.update()

    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, assets_dir="assets")