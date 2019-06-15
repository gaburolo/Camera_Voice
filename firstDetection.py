import threading
from tkinter import *
from PIL import Image, ImageTk
from imageai.Detection import ObjectDetection
import os,socket,base64
from compilador import *
from ast import literal_eval

execution_path = os.getcwd()
canvasX = 500
canvasY = 680
HOST = '172.18.48.249'

def carga_imagen(img):
    original = Image.open(img)
    resized = original.resize((canvasX,canvasY),Image.ANTIALIAS)
    imagen = ImageTk.PhotoImage(resized)
    return imagen

def main():

    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel("faster")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #s.bind((socket.gethostname(), 8000))
        s.bind((HOST, 8000))
    except socket.error as err:
        print("Error de bind")
        sys.exit()

    s.listen(5)

    img = carga_imagen("listo.png")
    canvas.create_image(0, 0, image=img, anchor=NW)

    text.config(state="normal")
    text.delete(1.0, END)
    text.insert(INSERT,"Esperando una conexion")
    text.config(state="disabled")

    while True:
        print("esperando una conexion")
        clientsocket, address = s.accept()
        print(f"Conexion desde {address} establecida ")
        f = open("recibido.png", "wb")

        img = carga_imagen("cargando1.png")
        canvas.create_image(0, 0, image=img, anchor=NW)

        full_msg = ''

        #msg = clientsocket.recv(1024)
        #print(msg)
        #temp = msg[22:]
        #full_msg += temp.decode("utf-8")
        while True:
            msg = clientsocket.recv(1024)
            #print(msg)
            if len(msg) < 1024:
                try:
                    #temp = msg[7:]
                    #full_msg += temp.decode("utf-8")
                    full_msg += msg.decode("utf-8")
                except:
                    print("No se pudo decodificar el mensaje")
                break
            try:
                full_msg += msg.decode("utf-8")
            except:
                print("No se pudo decodificar el mensaje")
        #msg = clientsocket.recv(100000)
        print(full_msg)
        try:
            js = literal_eval(str(full_msg))
        except:
            print("No se pudo convertir el mensaje a formato json")

        text.config(state="normal")
        text.delete(1.0, END)
        text.insert(INSERT, "Datos sensor ultrasonico: "+str(js["distancia"])+"cm de distancia\n\nDatos camara: Fotografia con un peso de "+str(len(js["imagen"]))+" bytes\n\n")
        text.config(state="disabled")

        try:
            imagen = base64.b64decode(js["imagen"])
            f.write(imagen)
            detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path, "recibido.png"),
                                                     output_image_path=os.path.join(execution_path,
                                                                                    "imagenew.png"),
                                                     minimum_percentage_probability=40)

            img = carga_imagen("imagenew.png")
            canvas.create_image(0, 0, image=img, anchor=NW)
            objetos_detectados = compilar1(detections)
            """if len(detections) != 0:
                for eachObject in detections:
                    objetos_detectados += ""+str(verificarGen(traducir(eachObject["name"])))+ ";" + str(eachObject["percentage_probability"] )+" "
            else:
                objetos_detectados += "una pared u objeto desconocido "
            """
            text.config(state="normal")
            text.insert(INSERT,"Objeto(s) identificado(s): "+objetos_detectados+"\n\n")

            msg_to_send = compilar2(detections,js)

            #msg_to_send = direccion(str(js["direccion"]))+"hay "+objetos_detectados+"a "+str(js["distancia"])+"cm de distancia de usted"
            print("Natural: "+msg_to_send)
            print("\nMorse: "+str(encode(msg_to_send)))

            text.insert(INSERT, "Mensaje en lenguaje natural: "+msg_to_send+"\n\nMensaje en codigo morse: "+encode(msg_to_send)+"\n\n")
            text.config(state="disabled")

            clientsocket.send(bytes(msg_to_send, "utf-8"))
            clientsocket.close()
        except:
            print("Error grave")
            clientsocket.close()
            img = carga_imagen("listo.png")
            canvas.create_image(0, 0, image=img, anchor=NW)
            text.config(state="normal")
            text.delete(1.0, END)
            text.insert(INSERT, "Esperando una conexion")
            text.config(state="disabled")



#Creacion de la ventana
ventana = Tk()
ventana.title("LookAhead")
ventana.geometry("1295x683+10+10")
ventana.config(bg="black")
ventana.resizable(False,False)

#Creacion del canvas
canvas = Canvas(ventana,width=canvasX,height=canvasY)
canvas.pack()
canvas.place(x=0, y=0)
canvas.config(bg="black")
imgFondo = carga_imagen("cargando1.png")
canvas.create_image(0, 0, image=imgFondo, anchor=NW)

#Creacion del cuadro de texto
text = Text(ventana,width=97,height=43)
text.place(x=canvasX,y=0)
text.insert(INSERT,"Espere un momento por favor...")
text.config(state="disabled")

scroller = Scrollbar(ventana, orient="vertical", command=text.yview)
#scroller.place(x=1106, y=0)

text.config(state=DISABLED, yscrollcommand=scroller.set)
scroller.pack(side="right", fill="y")

#Creacion de los hilos
soc = threading.Thread(target=main,args=())
soc.start()
ventana.mainloop()



"""
execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel("faster")

for x in range(0,2):
    print("entre")

    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "animales"+str(x)+".jpg"), output_image_path=os.path.join(execution_path , "imagenew"+str(x)+".jpg"),minimum_percentage_probability=40)
    if len(detections) != 0:
        for eachObject in detections:
            print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
    else:
        print("pared")"""
