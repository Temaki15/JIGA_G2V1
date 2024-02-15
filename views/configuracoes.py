import flet as ft

def configuracoes(page):

    return ft.View(
        "/configuracoes",
        [
            ft.AppBar(
                title=ft.Text("Configurações"),
                bgcolor = "#252525",
                actions = [
                    ft.PopupMenuButton(
                        items = [
                            ft.PopupMenuItem(text="Item 1"),
                            ft.PopupMenuItem(),  # divider
                            ft.PopupMenuItem(
                                text="Checked item", checked=False
                            ),
                        ]
                    ),
                ],

                leading = ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color="#ddac13",
                    icon_size=20,
                    tooltip="Voltar",
                    on_click=lambda _: page.go("/"),
                ),
            ),

            ft.Container(
                padding = 0,
                margin = ft.margin.all(-10),
                image_src ="/images/abstract_bg.jpg",
                image_fit = ft.ImageFit.COVER,
                width = 1024,
                height = 544,
                expand = True,
                alignment = ft.alignment.center,
                content = 
                    ft.Column(
                        controls = [
                                ft.Row(
                                    alignment = ft.MainAxisAlignment.SPACE_AROUND,
                                    # Vertical_alignment = ft.CrossAxisAlignment.CENTER,
                                    # width = page.window_width,
                                    width = 100,
                                    # bgcolor = ft.colors.RED,
                                    controls = [
                                        ft.Container(
                                            content=ft.Text("Piroca"),
                                            alignment = ft.alignment.center,
                                            width = 1024,
                                            height = 480,
                                            bgcolor = "#ddac13",
                                            border_radius=ft.border_radius.all(5),
                                        ),          
                                    ]
                                ),

                                ft.ProgressBar(
                                    width = 1024,
                                    color = "amber",
                                    bgcolor = "#1e1e1e",
                                    visible = True,
                                    tooltip = "Teste em execução" 
                                ),
                            ]
                    )
            ),
        ],
    )
