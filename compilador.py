import os
import sys

MorseMap = [
    ['A', ".-"],
    ['B', "-..."],
    ['C', "-.-."],
    ['D', "-.."],
    ['E', "."],
    ['F', "..-."],
    ['G', "--."],
    ['H', "...."],
    ['I', ".."],
    ['J', ".---"],
    ['K', ".-.-"],
    ['L', ".-.."],
    ['M', "--"],
    ['N', "-."],
    ['O', "---"],
    ['P', ".--."],
    ['Q', "--.-"],
    ['R', ".-."],
    ['S', "..."],
    ['T', "-"],
    ['U', "..-"],
    ['V', "...-"],
    ['W', ".--"],
    ['X', "-..-"],
    ['Y', "-.--"],
    ['Z', "--.."],
    ['a', ".-"],
    ['b', "-..."],
    ['c', "-.-."],
    ['d', "-.."],
    ['e', "."],
    ['f', "..-."],
    ['g', "--."],
    ['h', "...."],
    ['i', ".."],
    ['j', ".---"],
    ['k', ".-.-"],
    ['l', ".-.."],
    ['m', "--"],
    ['n', "-."],
    ['o', "---"],
    ['p', ".--."],
    ['q', "--.-"],
    ['r', ".-."],
    ['s', "..."],
    ['t', "-"],
    ['u', "..-"],
    ['v', "...-"],
    ['w', ".--"],
    ['x', "-..-"],
    ['y', "-.--"],
    ['z', "--.."],
    [' ', " "],

    ['1', ".----"],
    ['2', "..---"],
    ['3', "...--"],
    ['4', "....-"],
    ['5', "....."],
    ['6', "-...."],
    ['7', "--..."],
    ['8', "---.."],
    ['9', "----."],
    ['0', "-----"],

    ['.', "·–·–·–"],
    [',', "--..--"],
    ['?', "..--.."],
    ['!', "-.-.--"],
    [':', "---..."],
    [';', "-.-.-."],
    ['(', "-.--."],
    [')', "-.--.-"],
    ['"', ".-..-."],
    ['@', ".--.-."],
    ['&', ".-..."],
]

objetosIngEsp = [
    ["chair", "silla"],
    ["dining table","mesa"],
    ["table","mesa"],
    ["person","persona"],
    ["handbag","bulto"],
    ["suitcase","maleta"],
    ["cell phone","celular"],
    ["bird","pajaro"],
    ["tv","tv"],
    ["dog","perro"],
    ["cow","vaca"],
    ["sheep","oveja"],
    ["horse","caballo"],
    ["cat","gato"],
    ["giraffe","jirafa"],
    ["teddy bear","oso de peluche"],
    ["bear","oso"],
    ["truck","camion"],
    ["car","carro"],
    ["elephant","elefante"],
    ["motorcycle ","motocicleta"],
    ["bus","autobus"],
    ["bicycle","bicicleta"]
]

femenino = ["silla","mesa","persona","maleta","tv","vaca","oveja","jirafa","motocicleta","bicicleta","zebra"]



def encode(string):
    print("Convirtiendo a codigo morse")
    stringMorse = ""
    for i in string:
        for j in MorseMap:
            if i == j[0]:
                #print(i)
                stringMorse += j[1]
                #print(j[1])
                break
    return stringMorse

def traducir(word):
    palabra = word
    for i in objetosIngEsp:
        if word == i[0]:
                # print(i)
                palabra = i[1]
                # print(j[1])
                break
    return palabra

def verificarGen(palabra):
    string = ""
    cont = len(femenino)
    for i in femenino:
        if palabra == i:
            string = "una "+palabra
            break
        cont-=1
    if cont == 0:
        string = "un "+palabra
    return string

def verificarGen2(palabra):
    string = ""
    cont = len(femenino)
    for i in femenino:
        if palabra == i:
            string = "una"
            break
        cont-=1
    if cont == 0:
        string = "un"
    return string

def direccion(dir):
    if dir=="adelante":
        return "Al frente "
    elif dir=="atras":
        return "Detras suyo "
    elif dir=="izquierda":
        return "A su izquierda "
    elif dir=="derecha":
        return "A su derecha "


def compilar1(detections):
    objetos_detectados = ""
    if len(detections) != 0:
        for eachObject in detections:
            objetos_detectados += "" + str(verificarGen(traducir(eachObject["name"]))) + ";" + str(
                eachObject["percentage_probability"]) + " "
    else:
        objetos_detectados += "una pared u objeto desconocido "
    return objetos_detectados

def contar(lista,obj):
    cant = 0
    for i in lista:
        if i == obj:
            cant += 1
    if cant == 1:
        return verificarGen2(traducir(obj))
    else:
        return str(cant)

def contar2(lista,obj):
    cant = 0
    for i in lista:
        if i == obj:
            cant += 1
    return cant

def eliminar(lista,obj):
    posicion = 0
    listaAux = []
    for eachObject in lista:
        listaAux.append(eachObject)
    while posicion < len(listaAux):
        if listaAux[posicion] == obj:
            listaAux.pop(posicion)
        else:
            posicion = posicion + 1
    return listaAux

def compilar2(detections,js):
    objetos_detectados = ""
    cont = len(detections)
    lista =[]
    if len(detections) != 0:
        if len(detections) > 1:
            for eachObject in detections:
                lista.append(eachObject["name"])
            while len(lista) > 0:
                if len(lista) == 1:
                    objetos_detectados += "y " + str(verificarGen(traducir(lista[0]))) + " "
                    lista = eliminar(lista, lista[0])
                else:
                    listaAux = eliminar(lista,lista[0])
                    if len(listaAux) == 0:
                        if contar(lista,lista[0]) == cont:
                            objetos_detectados += contar(lista, lista[0]) +" "+ str(traducir(lista[0])) + "s "
                            lista = eliminar(lista, lista[0])
                        else:
                            objetos_detectados += "y " + contar(lista, lista[0]) +" "+ str(traducir(lista[0])) + "s "
                            lista = eliminar(lista, lista[0])
                    else:
                        if contar2(lista, lista[0]) > 1:
                            objetos_detectados += contar(lista, lista[0]) +" "+ str(traducir(lista[0])) + "s "
                            lista = eliminar(lista, lista[0])
                        else:
                            objetos_detectados += contar(lista, lista[0]) + " " + str(traducir(lista[0])) + " "
                            lista = eliminar(lista, lista[0])

            #cont -= 1
        else:
            for eachObject in detections:
                objetos_detectados += str(verificarGen(traducir(eachObject["name"]))) + " "
    else:
        objetos_detectados += "una pared"


    """if len(detections) != 0:
        if len(detections) > 1:
            for eachObject in detections:
                if cont == 1:
                    objetos_detectados += "y " + str(verificarGen(traducir(eachObject["name"]))) + " "
                else:
                    objetos_detectados += str(verificarGen(traducir(eachObject["name"]))) + " "
                cont-=1
        else:
            for eachObject in detections:
                objetos_detectados += str(verificarGen(traducir(eachObject["name"]))) + " "
    else:
        objetos_detectados += "una pared"
"""

    msg_to_send = direccion(str(js["direccion"])) + "a " + str(
        js["distancia"]) + "cm hay " + objetos_detectados

    return msg_to_send