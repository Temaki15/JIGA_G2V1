import serial.tools.list_ports
import serial
import threading
import binascii
import flet as ft
from time import sleep

flag_em_teste = True
flag_conectado = False

#Comunicação Serial
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



class SampleRod(ft.BarChartRod):
    def __init__(self, y: float, hovered: bool = False):
        super().__init__()
        self.hovered = hovered
        self.y = y

    def _before_build_command(self):
        self.to_y = self.y + 1 if self.hovered else self.y
        self.color = ft.colors.YELLOW if self.hovered else ft.colors.WHITE
        self.border_side = (
            ft.BorderSide(width=1, color="#91700D")
            if self.hovered
            else ft.BorderSide(width=0, color = "#ddac13")
        )
        super()._before_build_command()

    def _build(self):
        self.tooltip = str(self.y)
        self.width = 22
        self.color = "#ddac13"
        self.bg_to_y = 20
        self.bg_color = "#ddac13"

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

        sleep(0.005)
        ser.write(pk)
    except Exception as ex:
        print(ex)   

def thread_read():
    global ser, countTotal, receive_data, receive_pos, valTeste, init1, init2, receive_data_aux, vetBytes, debug
    
    while(True):
        if(ser.inWaiting() <= 0):
            sleep(0.01)
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

  
def teste_automatico(page):

    def on_chart_event(e: ft.BarChartEvent):
        for group_index, group in enumerate(chart.bar_groups):
            for rod_index, rod in enumerate(group.bar_rods):
                rod.hovered = e.group_index == group_index and e.rod_index == rod_index
        chart.update()

    chart = ft.BarChart(
        bar_groups=[
            ft.BarChartGroup(
                x = 0,
                group_vertically = True,
                bar_rods=[SampleRod(20)],
            ),
            ft.BarChartGroup(
                x=1,
                bar_rods=[SampleRod(6.5)],
            ),
            ft.BarChartGroup(
                x=2,
                bar_rods=[SampleRod(5)],
            ),
            ft.BarChartGroup(
                x=3,
                bar_rods=[SampleRod(7.5)],
            ),
            ft.BarChartGroup(
                x=4,
                bar_rods=[SampleRod(9)],
            ),
        ],

        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=0, label=ft.Text("Digi_IN")),
                ft.ChartAxisLabel(value=3, label=ft.Text("Anal_IN")),
                ft.ChartAxisLabel(value=4, label=ft.Text("Digi_OUT")),
                ft.ChartAxisLabel(value=1, label=ft.Text("Relés")),
                ft.ChartAxisLabel(value=2, label=ft.Text("Xbee")),
            ],
        ),
        on_chart_event=on_chart_event,
        interactive=True,
    )
    
    def COM_connect(e):
        try:
            ser = serial.Serial('COM11', 9600, parity = serial.PARITY_NONE, stopbits = 1, write_timeout=1000)
            page.show_snack_bar(ft.SnackBar(ft.Text("Conectado a porta COM11", color = ft.colors.WHITE), open=True, bgcolor = "#333333"))
            flag_conectado = True
        except Exception as ex:
            page.show_snack_bar(ft.SnackBar(ft.Text("Erro ao conectar", color = ft.colors.WHITE), open=True, bgcolor = "#333333"))
            flag_conectado = False
            
    return ft.View(
                    "/teste",
                    [
                        ft.AppBar(
                            title=ft.Text("Teste Automático"),
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
                                            width = page.window_width,
                                            # bgcolor = ft.colors.RED,
                                            controls = [
                                                ft.Container(
                                                    alignment = ft.alignment.center,
                                                    width = 512,
                                                    height = 480,
                                                    bgcolor = "#ddac13",
                                                    border_radius=ft.border_radius.all(5),
                                                    content=ft.Column(
                                                        controls = [
                                                            # ft.Text(COM_connect(), color = ft.colors.BLACK,)
                                                        ]
                                                    ),
                                                ),

                                                ft.Container(
                                                    chart,
                                                    bgcolor = ft.colors.TRANSPARENT,
                                                    padding=10,
                                                    border_radius=5,
                                                    expand=True
                                                )
                                            ]
                                        ),

                                        ft.ProgressBar(
                                            width = 1024,
                                            color = "#ddac13",
                                            bgcolor = ft.colors.TRANSPARENT,
                                            visible = flag_em_teste,
                                            tooltip = "Teste em execução" 
                                        ),
                                    ]
                                )
                        ),
                    ],
                    
                    ft.FloatingActionButton(
                        content=ft.Row(
                            [ft.Icon(ft.icons.ADD, color = ft.colors.BLACK), ft.Text("Conectar", color = ft.colors.BLACK)], alignment="center", spacing=5
                        ),
                        bgcolor = "#ddac13",
                        shape=ft.RoundedRectangleBorder(radius=5),
                        on_click = COM_connect,
                        width=120,
                        mini=True,
                        # disabled = True,
                    ),
                )