import serial.tools.list_ports
import serial
import threading
import binascii
import flet as ft
from time import sleep
# def pop_error(txt_alert):
#     ft.AlertDialog(txt_alert)


#Para a comunicação Serial
write_data = [0]*16 #+4 de metadados
receive_data = [0]*9000
receive_data_aux = [0]*19
receive_pos = 0

pkg_end = b'\x0d'       #Indica fim do pacote
pkg_size = 19           #Tamanho do pacote
pkg_init_1 = b'\xFF'    #Indica início do pacote, byte 1
pkg_init_2 = b'\xFE'    #Indica início do pacote, byte 2
valTeste = False        #Indica se está em teste, com mais prints
init1 = 0               #Recebe o byte 1 do início do pacote
init2 = 0               #Recebe o byte 2 do início do pacote

ser = 0                 #Para realizar a conexão com a serial
vetBytes = [0]*15       #Informações recebidas pela serial, vindas da CAN
Send_vetBytes = [0]*15  #Para enviar na Serial e, depois, pela CAN: O primeiro byte é ID_1, o segundo é ID_2 e o terceiro é tamanho. Os restantes são data
con_except = 0          #Contador para erro de comunicação
reconectar = False      #Para indicar que deve tentar reconexão
countTotal = 0          #Contador para quantidade de mensagens, apenas para debug

###########################################################################################################################
# try:
#     ser = serial.Serial('COM11', 9600, parity = serial.PARITY_NONE, stopbits = 1, write_timeout=1000)
# except Exception as ex:

    # print("Erro abrindo comunicacao serial can: ")
    # print(ex)
###########################################################################################################################

def Altera_ID():
    input = IdInput.get("1.0", "end-1c")
    debug.config(text = input)
    
def write_serial():
    global ser, Send_vetBytes, reconectar

    #return
    try:
        pk = [0]*19

        pk[0] = 255&0xFF
        pk[1] = 254&0xFF
    
    
        #Bytes
        for i in range(15):
            pk[2 + i] = Send_vetBytes[i]&0xFF
    

        ck = 0
        for n in range(17):
            ck += pk[n]

        pk[17] = ck&0xFF
        pk[18] = 13&0xFF
    
        #print(pk)

        time.sleep(0.005)
        ser.write(pk)
    except Exception as ex:
        print(ex)    

def motor_50_1():
    global temp_now, con_temp, tempEspera, caseSend, encoder_case, encoder_temp, tempEspera_encoder, encoder_alterna 
  
    Send_vetBytes[0] = 0        #ID
    Send_vetBytes[1] = 41       #ID
    Send_vetBytes[2] = 8        #Quantidade de dados

    Send_vetBytes[3] = 0x30     #Identificador '0'
    Send_vetBytes[4] = 1        #Flag_manual e sentido 1-automatico sentido 1 / 3-automatico sentido 0
    Send_vetBytes[5] = 50       #Velocidade
    Send_vetBytes[6] = 0        #Dados
    Send_vetBytes[7] = 0        #Dados
    Send_vetBytes[8] = 0        #Dados
    Send_vetBytes[9] = 0        #Dados
    Send_vetBytes[10] = 0       #Dados

    tempEspera = 0.025          #25ms
    write_serial()              #SEND MSG CAN

def thread_read():
    global ser, countTotal, receive_data, receive_pos, valTeste, init1, init2, receive_data_aux, vetBytes, debug
    
    while(True):
        if(ser.inWaiting() <= 0):
            time.sleep(0.01)
        while (ser.inWaiting() > 0):
            for data in ser.read():
                data = data&0xff
                
                receive_data[receive_pos] = data
                receive_pos = receive_pos + 1           
                if(data == 13 and receive_pos >= pkg_size):
                    i = receive_pos-pkg_size
                    
                    countTotal += 1
                    
                    #if valTeste == True:
                        #print("ERR - ")
                        #print(countTotal)
                                    

                   # else:
                   #     print("OK")
                        
                   
           
                    valTeste = True
                  
                    init1 = receive_data[receive_pos - pkg_size]
                    init2 = receive_data[receive_pos - pkg_size +1]
          
                    if(receive_pos >= 19 and receive_data[receive_pos - pkg_size] == 255 and receive_data[receive_pos - pkg_size +1] == 254):
                        #print('Parte 2')
                        ck = 0
                        ck2 = 0
                        for number in range(receive_pos - pkg_size, receive_pos - 2):
                            ck2 += receive_data[number]

                        ck2 = ck2&0xff
                        
                        #print("a:"+str(ck2))
                        #print("b:"+str(receive_data[receive_pos -2]))
                        if(ck2 == receive_data[receive_pos -2]&0xff):
                            #Validou tudo
                            
                            #Bytes
                            vetBytes[0] = receive_data[(receive_pos - 19 + 2)]
                            vetBytes[1] = receive_data[(receive_pos - 19 + 3)]
                            vetBytes[2] = receive_data[(receive_pos - 19 + 4)]
                            vetBytes[3] = receive_data[(receive_pos - 19 + 5)]
                            vetBytes[4] = receive_data[(receive_pos - 19 + 6)]
                            vetBytes[5] = receive_data[(receive_pos - 19 + 7)]
                            vetBytes[6] = receive_data[(receive_pos - 19 + 8)]
                            vetBytes[7] = receive_data[(receive_pos - 19 + 9)]
                            vetBytes[8] = receive_data[(receive_pos - 19 + 10)]
                            vetBytes[9] = receive_data[(receive_pos - 19 + 11)]
                            vetBytes[10] = receive_data[(receive_pos - 19 + 12)]
                            vetBytes[11] = receive_data[(receive_pos - 19 + 13)]
                            vetBytes[12] = receive_data[(receive_pos - 19 + 14)]
                            vetBytes[13] = receive_data[(receive_pos - 19 + 15)]
                            vetBytes[14] = receive_data[(receive_pos - 19 + 16)]
                            
#                             print(vetBytes[6])
                            debug.config(text = vetBytes[1])
                            val_corrente.config(text = vetBytes[4])
                            val_tensao.config(text = vetBytes[5])
                            val_potencia.config(text = vetBytes[6])    
                            
                            receive_pos = 0                            
                            
                            valTeste = False
                            printer2 = "DATA: "
                            
                            if(ser.inWaiting() <= 0):
                                time.sleep(0.005)
                            #print("CHEGOU B\n")
                        else:
                            print("Falha CK")
#                             pub_debug_can.publish("FALHA CK")
                           
                    else:
                        printer = "DATA: "
                        if(receive_pos >= 19):
                            for number in range(receive_pos - pkg_size, receive_pos):
                                printer += " " + str(receive_data[number])
#                             pub_debug_can.publish(printer)
#                         pub_debug_can.publish("FALHA 1, Tamanho: " + str((receive_pos - pkg_size)) + " receive_pos: " + str(receive_pos) + " init 1:" + str(receive_data[receive_pos - 15]) ) 
                        
                        
                        
                
                if(receive_pos >= 9000):
#                     pub_debug_can.publish("RST")
                    receive_pos = 0

row_style: dict = {
    "top": 0,
    "bottom": 0,
    "left": 0,
    "right": 0,
    "alignment": "spaceAround",
    "vertical_alignment": "center",
    "expand": True
}

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 1024
    page.window_height = 600
    page.bgcolor = ft.colors.RED
    page.title = "Jiga AGVS G2"
    page.fonts = {"Orbitron": "fonts/Orbitron_Medium.ttf",}
    page.theme = ft.Theme(font_family="Orbitron")
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0
    page.window_resizable = False
    # page.window_full_screen = True
    # page.window_maximizable = False
    # page.window_frameless = True
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
                                                ft.ElevatedButton("configurações", on_click=lambda _: page.go("/configurações"), bgcolor="#333333"),
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
                # appbar= ft.AppBar(
                #     leading=ft.Icon(ft.icons.PALETTE),
                #     bgcolor=ft.colors.AMBER_400,
                # ),
                horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                vertical_alignment= ft.MainAxisAlignment.CENTER,
               
            )
        )
        page.update()

        if page.route == "/teste":
            page.views.append(
                ft.View(
                    "/teste",
                    [
                        ft.AppBar(
                            title=ft.Text("Teste Automático"),
                            bgcolor="#252525",
                            leading = ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_color="#ddac13",
                                icon_size=20,
                                tooltip="Voltar",
                                on_click=lambda _: page.go("/"),
                            ),
                        ),

                        # ft.Container(
                        #     bgcolor = ft.colors.WHITE,
                        #     padding = 0,
                        #     margin=ft.margin.all(-10),
                        #     image_src="/images/abstract_bg.jpg",
                        #     image_fit = ft.ImageFit.COVER,
                        #     width = 1024,
                        #     height = 600,
                        #     expand=True,
                        #     alignment = ft.alignment.center,
                        #     content =()                             
                        # ),
                    ],
                )
            )
        page.update()


        if page.route == "/acionamentos":
            page.views.append(
                ft.View(
                    "/acionamentos",
                    [
                        ft.AppBar(
                            title=ft.Text("Acionamentos e Leituras RT"),
                            bgcolor="#252525",
                            leading = ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                icon_color="#ddac13",
                                icon_size=20,
                                tooltip="Voltar",
                                on_click=lambda _: page.go("/"),
                            ),
                        ),

                        # ft.Container(
                        #     bgcolor = ft.colors.WHITE,
                        #     padding = 0,
                        #     margin=ft.margin.all(-10),
                        #     image_src="/images/abstract_bg.jpg",
                        #     image_fit = ft.ImageFit.COVER,
                        #     width = 1024,
                        #     height = 600,
                        #     expand=True,
                        #     alignment = ft.alignment.center,
                        #     content =()                             
                        # ),
                    ],
                )
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