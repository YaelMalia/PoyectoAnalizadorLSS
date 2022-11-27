from re import I
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox
# Tokinzador variables______________________
specialL = [":", ",", "(", ")", "?", "*", "=", "$", "@",
            "~", "\"", "'", "“", "”", " ", "\n"]
operadoresA = ["*MAS", "*MENOS", "*MULT", "*DIV"]
operadoresRL = ["=ESMAYOR", "=ESMENOR", "=ESIGUAL", "=NOIGUAL", "=AND", "=OR"]
builtIn = ["equ", "CLASE", "HASTAAQUILAVAMOSADEJAR_", "ATRIBUTOS", "FINATRIBUTOS_",
           "DEFFUNCS", "FINDEFFUNCS_", "ESCRIBIDO", "RECIBIDO", "ITERAR", "FINITERAR_",
           "SI", "JALO", "FINJALO_", "NOJALO", "FINNOJALO_", "FINSI_", "PRINCIPAL", "FINPRINCIPAL_", "FUNC", "FINFUNC_", "ENT", "CAD", "BULL"]
tiposD = ["@ENT", "@CAD", "@BULL"]

tokens = []
tipo_token = []
lista_variables = []
lista_funciones = []

diccionarioVars = {
    # KEY (VAR) : {'TIPO', 'VALOR' .... }
}
# Parte lógica______________________


def cerrarF():
    root.destroy()


def AnalisisSintactico():

    # for ind in range (len(tokens)):
    #   if(tokens[ind] in builtIn):
    #      textoComentario = tokens[ind]
    #     textoComentario = str.config(fg="green")

    banderaErrorSintactico = False
    # ----------------------------PRUEBA DE COLORES----------------------------

    # Examinar estructura inicial-----
    # Primero deberá de tener la palabra reservada CLASE y nombre de la clase, seguido de un ":"
    indice = 0
    if(tokens[indice] == "CLASE" and tipo_token[indice] == "Built-In Word"):
        indice += 1
        if(tipo_token[indice] == "Nombre de método o clase"):
            indice += 1
            if(tokens[indice] == ":"):
                indice += 1
                # Tiene la estructura correcta para una clase, se continúa aquí --->
                #print("Estructura correcta")
                # Se bifurca en 3,  puede existir la declaración de atributos, funciones o directamente el principal
                if(tokens[indice] == "ATRIBUTOS" and tipo_token[indice] == "Built-In Word"):
                    indice += 1
                    if(tokens[indice] == ":"):
                        indice += 1
                        # Se esperaría encontrar declaración de variables
                        while(tokens[indice] != "FINATRIBUTOS_"):
                            if((tokens[indice] == "@ENT") or (tokens[indice] == "@CAD") or (tokens[indice] == "@BULL")):
                                indice += 1
                                if(tipo_token[indice] == "Var"):
                                    Vari = tokens[indice]
                                    # Si hay un carácter especial dentro del nombre de la variable, se envía un error de sintáxis
                                    for posi in range(len(Vari)):
                                        if((Vari[posi] in specialL)):
                                            banderaErrorSintactico = True
                                            # print(Vari[posi])
                                            break
                                        if(banderaErrorSintactico == True):
                                            #print("Error de sintáxis, la variable contiene palabras o carácteres no válidos")
                                            messagebox.showerror(
                                                "Error", f"Error de sintáxis, la variable contiene palabras o carácteres no válidos")
                                            break
                                        elif((tokens[indice] in operadoresA) or (tokens[indice] in operadoresRL) or (tokens[indice] in builtIn) or ((tokens[indice] in tiposD))):
                                            #print("Error de sintáxis, la variable contiene palabras o carácteres no válidos")
                                            messagebox.showerror(
                                                "Error", f"Error de sintáxis, la variable contiene palabras o carácteres no válidos")
                                            break
                                    else:
                                        # El nombre de la variable es correcto, se añade a la lista de variables
                                        lista_variables.append(tokens[indice])
                                        diccionarioVars[tokens[indice]] = {
                                            "tipoDato": "", "valor": "", "resoluble": "No"}
                                        # Almacenamos el tipo de dato
                                        lista_variables.append(
                                            tipo_token[indice-1])
                                        diccionarioVars[tokens[indice]
                                                        ]["tipoDato"] = tipo_token[indice-1]

                                        indice += 1
                                    if(tokens[indice] == "?"):
                                        indice += 1
                                        # La estructura para declarar una variable es correcta, se continúa leyendo

                                    else:
                                        #print("Error de sintáxis, se esperaba '?' en", tokens[indice-2], tokens[indice-1])
                                        messagebox.showerror(
                                            "Error", f"Error de sintáxis, se esperaba '?' en, {tokens[indice-2]}, {tokens[indice-1]}")
                                        break
                                else:
                                    #print("Error de sintáxis, se esperaba una variable")
                                    messagebox.showerror(
                                        "Error", f"Error de sintáxis, se esperaba una variable")
                                    break
                            else:
                                #print("Error de sintáxis, se esperaba el tipo de variable")
                                messagebox.showerror(
                                    "Error", f"Error de sintáxis, se esperaba el tipo de variable en {tokens[indice]} {tokens[indice+1]}")
                                break
                        indice += 1
                    else:
                        #print("Error de sintáxis, se esperaba ':' en", tokens[indice-1])
                        messagebox.showerror(
                            "Error", f"Error de sintáxis, se esperaba ':' en, {tokens[indice-1]}")
                # En caso de que se vaya directamente a la definición de funciones
                if(tokens[indice] == "DEFFUNCS" and tipo_token[indice] == "Built-In Word"):
                    indice += 1
                    if(tokens[indice] == ":"):
                        indice += 1
                        # Aquí se analiza que se tenga la estructura de una función declarada
                        while(tokens[indice] != "FINDEFFUNCS_"):
                            if(tokens[indice] == "~"):
                                indice += 1
                                if((tipo_token[indice] == "Built-In Word") and (tokens[indice] == "FUNC")):
                                    indice += 1
                                    if((tipo_token[indice] == "Built-In Word") and (tokens[indice] == "ENT" or tokens[indice] == "CAD" or tokens[indice] == "BULL")):
                                        indice += 1
                                        if(tipo_token[indice] == "Nombre de método o clase"):
                                            indice += 1
                                            if(tokens[indice] == "("):
                                                indice += 1
                                                # Leér tantos parámetros recibidos por la función (también se analiza la estructura de los argumentos)
                                                while(tokens[indice] != ")"):
                                                    if((tokens[indice] == "@ENT") or (tokens[indice] == "@CAD") or (tokens[indice] == "@BULL")):
                                                        indice += 1
                                                        if(tipo_token[indice] == "Var"):
                                                            indice += 1
                                                            if(tokens[indice] == ","):
                                                                indice += 1
                                                            elif(tokens[indice] == ")"):
                                                                break
                                                            else:
                                                                #print("Error sintáctico, se esperaba ','")
                                                                messagebox.showerror(
                                                                    "Error", f"Error sintáctico, se esperaba ','")
                                                                break
                                                        else:
                                                            #print("Error sintáctico, se esperaba una variable")
                                                            messagebox.showerror(
                                                                "Error", f"Error sintáctico, se esperaba una variable")
                                                            break
                                                    else:
                                                        #print("Error sintáctico, se esperaba el tipo de dato para el argumento recibido", tokens[indice])
                                                        messagebox.showerror(
                                                            "Error", f"Error sintáctico, se esperaba el tipo de dato para el argumento recibido, {tokens[indice]}")
                                                        break
                                                indice += 1
                                                if(tokens[indice] == "?"):
                                                    indice += 1
                                                else:
                                                    #print("Error sintáctico, se esperaba '?' en", tokens[indice-3], tokens[indice-2], tokens[indice-1])
                                                    messagebox.showerror(
                                                        "Error", f"Error sintáctico, se esperaba '?' en, {tokens[indice-3]}, {tokens[indice-2]}, {tokens[indice-1]}")
                                                    break
                                            else:
                                                #print("Error sintáctico, se esperaba '(' en", tokens[indice-4], tokens[indice-3], tokens[indice-2], tokens[indice-1])
                                                messagebox.showerror(
                                                    "Error", f"Error sintáctico, se esperaba '(' en, {tokens[indice-4]}, {tokens[indice-3]}, {tokens[indice-2]}, {tokens[indice-1]}")
                                                break
                                        else:
                                            #print("Error sintáctico, se esperaba nombre del método")
                                            messagebox.showerror(
                                                "Error", f"Error sintáctico, se esperaba nombre del método")
                                    else:
                                        #print("Error sintáctico, se esperaba el tipo de dato para la función")
                                        messagebox.showerror(
                                            "Error", f"Error sintáctico, se esperaba el tipo de dato para la función")
                                        break
                                else:
                                    #print("Error sintáctico, se esperaba palabra reservada FUNC")
                                    messagebox.showerror(
                                        "Error", f"Error sintáctico, se esperaba palabra reservada FUNC")
                                    break
                            else:
                                #print("Error sintáctico, se esperaba inicio de declaración de una función '~'")
                                messagebox.showerror(
                                    "Error", f"Error sintáctico, se esperaba inicio de declaración de una función '~'")
                                break
                        indice += 1
                # En caso de que se vaya a principal
                if(tokens[indice] == "PRINCIPAL" and tipo_token[indice] == "Built-In Word"):
                    indice += 1
                    if(tokens[indice] == ":"):
                        indice += 1
                        while(tokens[indice] != "FINPRINCIPAL_"):
                            # Todo código lógico aquí (Inicio del apartado principal) --->
                            # Aquí comienza analizar que esté correctamente el for "iterar"
                            if((tokens[indice] == "ITERAR") and (tipo_token[indice] == "Built-In Word") ):
                                indice += 1
                                if(tokens[indice] == "("):
                                    indice += 1                                                                                                                                                                                                                      # Intuye que la variable ha sido creada y es buscada en el diccionario
                                    if(tokens[indice] != "@ENT"):
                                        if(tokens[indice] in diccionarioVars and diccionarioVars[tokens[indice]]["tipoDato"] == "Var Entero"):
                                            print(tokens[indice] in diccionarioVars)
                                            print(diccionarioVars[tokens[indice]]["tipoDato"])
                                            indice += 1
                                            if(tokens[indice]==","):
                                                indice+=1
                                                if(tokens[indice] != "@ENT"):
                                                    if(tokens[indice] in diccionarioVars and diccionarioVars[tokens[indice]]["tipoDato"] == "Var Entero"):
                                                        print(tokens[indice] in diccionarioVars)
                                                        print(diccionarioVars[tokens[indice]]["tipoDato"])
                                                        indice+=1
                                                        if(tokens[indice]==")"):
                                                            indice+=1
                                                            if(tokens[indice]==":"):
                                                                indice+=1                            
                                                                while(tokens[indice]!="FINITERAR_"):
                                                                    messagebox.showinfo("Aviso","FINISH")
                                                                    break
                                                                indice+=1
                                                                messagebox.showinfo("SIU", "Se evaluó bien el iterar")
                                                            else:
                                                                messagebox.showerror("Error","Faltó :")
                                                                break
                                                        else:
                                                            messagebox.showerror("Error","Faltó ')'")
                                                            break
                                                    else:
                                                        messagebox.showerror("Error",f"Variable {tokens[indice]} no ha sido declarada previamente")
                                                        break
                                                else:
                                                    messagebox.showerror("Error","Debe usar una variable creada en la sección de atributos")
                                                    break
                                            else:
                                                messagebox.showerror("Error","Faltó una coma")
                                                break
                                        else:
                                            messagebox.showerror("Error",f"Variable {tokens[indice]} no ha sido declarada previamente")
                                            break
                                    else:
                                        messagebox.showerror("Error","Debe usar una variable creada en la sección de atributos")
                                        break
                                else:
                                    messagebox.showerror("Error","Falta parentesis de apertura")
                                    break
                                                                                                  

                        # ESCRIBIDO
                        # if(tokens[indice] == "ESCRIBIDO" and tipo_token[indice] == "Built-In Word"):
                        #     indice+=1
                        #     if(tokens[indice] == "("):
                        #         indice+=1
                        #         while(tokens[indice]!=")"):
                        #             if(tipo_token[indice] == "Cadena" or tipo_token[indice] == "Var"):
                        #                 indice+=1
                        #             if(tokens[indice] == "+"):
                        #                 indice+=1

                        # Analisis de las variables, existe, no existe y mismatch error
                            if(tipo_token[indice] == "Var"):
                                mivar = indice  # Recuperamos el indice para la variable
                            # Buscar en la lista de vars si existe
                                if(tokens[indice] in lista_variables):
                                    # Seguir analizando el código
                                    # obtenemos la posición del elemento del token para posterior obtener su tipo de dato
                                    posiVar = 0
                                    for pV in range(len(lista_variables)):
                                        if(lista_variables[pV] == tokens[indice]):
                                            posiVar = pV
                                            break
                                        else:
                                            continue
                                    tipoVar = str(lista_variables[posiVar+1])
                                    indice += 1
                                    if((tokens[indice] == "equ") and (tipo_token[indice] == "Asignación")):
                                        indice += 1
                                        # Comparativa para mismatch
                                        if(((tipoVar == "Var Entero") and (tipo_token[indice] == "Número")) or ((tipoVar == "Var Cadena") and (tipo_token[indice] == "Cadena")) or ((tipoVar == "Var Booleana") and (tipo_token[indice] == "Boolean"))):
                                            # Si coincide entonces avanza
                                            indice += 1
                                            if(tokens[indice] == "?"):
                                                diccionarioVars[tokens[mivar]]["valor"] = tokens[indice-1]
                                                diccionarioVars[tokens[mivar]]["resoluble"] = "Si"
                                                indice += 1
                                                # print(diccionarioVars)
                                            # Continua evaluando <---
                                                # print(diccionarioVars)
                                                # messagebox.showinfo("AVISO", "Se evaluó de manera simple")
                                            else:
                                                messagebox.showerror("Error", f"Se esperaba '?' en {tokens[indice-3]} {tokens[indice-2]} {tokens[indice-1]}")
                                                break
                                        # Aquí se podría agregar un elif() para hacer operaciones o al momento de recibir un dato con RECIBIDO
                                        elif(tipoVar == "Var Entero"):
                                            argumento1 = 0
                                            argumento2 = 0
                                            if((tokens[indice] == "*MAS") or (tokens[indice] == "*MENOS") or (tokens[indice] == "*MULT") or (tokens[indice] == "*DIV")):
                                                tipoOperador = indice
                                                indice += 1
                                                if(tokens[indice] == "("):
                                                    indice += 1
                                                    if(tipo_token[indice] == "Número"):
                                                        argumento1 = int(tokens[indice])
                                                        indice += 1
                                                    elif( tipo_token[indice] == "Var"):
                                                        if(tokens[indice] in diccionarioVars):
                                                            if(diccionarioVars[tokens[indice]]["tipoDato"] == "Var Entero"):
                                                                if(diccionarioVars[tokens[indice]]["valor"] != ""):
                                                                    argumento1 = int(diccionarioVars[tokens[indice]]["valor"])
                                                                    indice+=1
                                                                else:
                                                                    messagebox.showerror("Error", f"Error semántico, la variable {tokens[indice]} no se ha definido")
                                                                    break
                                                            else:
                                                                messagebox.showerror("Error", f"Error semántico, el tipo de variable para el primer argumento no es Var Entero {tokens[indice]}")
                                                                break
                                                        else:
                                                            messagebox.showerror("Error", f"Error semántico, variable utilizada {tokens[indice]} no existe")
                                                        if(tokens[indice] == ","):
                                                            indice += 1
                                                            if(tipo_token[indice] == "Número"):
                                                                argumento2 = int(tokens[indice])
                                                                indice += 1
                                                            elif( tipo_token[indice] == "Var"):
                                                                if(tokens[indice] in diccionarioVars):
                                                                    if(diccionarioVars[tokens[indice]]["tipoDato"] == "Var Entero"):
                                                                        if(diccionarioVars[tokens[indice]]["valor"] != ""):
                                                                            argumento2 = int(diccionarioVars[tokens[indice]]["valor"])
                                                                            indice+=1
                                                                        else:
                                                                            messagebox.showerror("Error", f"Error semántico, la variable {tokens[indice]} no se ha definido")
                                                                            break
                                                                    else:
                                                                        messagebox.showerror("Error", f"Error semántico, el tipo de variable para el segundo argumento no es Var Entero {tokens[indice]}")
                                                                        break
                                                                else:
                                                                    messagebox.showerror("Error", f"Error semántico, variable utilizada {tokens[indice]} no existe")
                                                                if(tokens[indice] == ")"):
                                                                    indice += 1
                                                                    if(tokens[indice] == "?"):
                                                                        indice += 1
                                                                        # messagebox.showinfo("Exito", "Se evaluó bien operador aritmético")
                                                                        # Se asigna el valor al diccionario de vars
                                                                        if(tokens[tipoOperador] == "*MAS"):
                                                                            diccionarioVars[tokens[mivar]]["valor"] = (argumento1 + argumento2)
                                                                            diccionarioVars[tokens[mivar]]["resoluble"] = "Si"
                                                                        if(tokens[tipoOperador] == "*MENOS"):
                                                                            diccionarioVars[tokens[mivar]]["valor"] = (argumento1 - argumento2)
                                                                            diccionarioVars[tokens[mivar]]["resoluble"] = "Si"
                                                                        if(tokens[tipoOperador] == "*MULT"):
                                                                            diccionarioVars[tokens[mivar]]["valor"] = (argumento1 * argumento2)
                                                                            diccionarioVars[tokens[mivar]]["resoluble"] = "Si"
                                                                        if(tokens[tipoOperador] == "*DIV"):
                                                                            if(argumento2 == 0):
                                                                                diccionarioVars[tokens[mivar]]["resoluble"] = "No"
                                                                                messagebox.showinfo("WHAT?!", "¿KESESO!")
                                                                            else:
                                                                                diccionarioVars[tokens[mivar]]["valor"] = (argumento1 / argumento2)
                                                                                diccionarioVars[tokens[mivar]]["resoluble"] = "Si"
                                                                    else:
                                                                        messagebox.showerror("Error", f"Error de sintáxis, se esperaba '?' en {tokens[indice-2]} {tokens[tokens-1]} {tokens[indice]}")
                                                                        break
                                                                else:
                                                                    messagebox.showerror("Error", f"Error de sintáxis, se esperaba cierre ')' en {tokens[indice-2]} {tokens[indice-1]} {tokens[indice]}")
                                                                    break
                                                            else:
                                                                messagebox.showerror("Error", f"Error semántico, se esperaba un dígito para segundo argumento de operador de tipo aritmético en {tokens[indice-2]} {tokens[indice-1]} {tokens[indice]} ")
                                                                break
                                                        else:
                                                            messagebox.showerror("Error", f"Error de sintáxis, se eperaba separador ',' en {tokens[indice-2]} {tokens[indice-1]} {tokens[indice]}")
                                                            break
                                                    else:
                                                        messagebox.showerror(
                                                            "Error", f"Error semántico, se esperaba un dígito para primer argumento de operador de tipo aritmético en {tokens[indice-2]} {tokens[indice-1]} {tokens[indice]} ")
                                                        break
                                            else:
                                                messagebox.showerror(
                                                    "Error", f"Error semántico, se esperaba operador aritmético para variable {tokens[indice-2]} entera")
                                                break
                                        # elif(otro token)
                                        elif(tipoVar == "Var Booleana"):
                                            # Relacionales
                                            if( (tokens[indice] == "=ESMAYOR") or (tokens[indice] == "=ESMENOR") ):
                                                posOp = indice
                                                arg1 = 0
                                                arg2 = 0
                                                indice+=1
                                                if(tokens[indice] == "("):
                                                    indice+=1
                                                    if(tipo_token[indice] == "Número"):
                                                        arg1 = int(tokens[indice])
                                                        indice+=1
                                                    elif( tipo_token[indice] == "Var"):
                                                        if(tokens[indice] in diccionarioVars):
                                                            if(diccionarioVars[tokens[indice]]["tipoDato"] == "Var Entero"):
                                                                if(diccionarioVars[tokens[indice]]["valor"] != ""):
                                                                    arg1 = int(diccionarioVars[tokens[indice]]["valor"])
                                                                    indice+=1
                                                                else:
                                                                    messagebox.showerror("Error", f"Error semántico, la variable {tokens[indice]} no se ha definido")
                                                                    break
                                                            else:
                                                                messagebox.showerror("Error", f"Error semántico, el tipo de variable para el primer argumento no es Var Entero {tokens[indice]}")
                                                                break
                                                        else:
                                                            messagebox.showerror("Error", f"Error semántico, variable utilizada {tokens[indice]} no existe")
                                                        if(tokens[indice] == ","):
                                                            indice+=1
                                                            if(tipo_token[indice] == "Número"):
                                                                arg2 = int(tokens[indice])
                                                                indice+=1
                                                            elif( tipo_token[indice] == "Var"):
                                                                if(tokens[indice] in diccionarioVars):
                                                                    if(diccionarioVars[tokens[indice]]["tipoDato"] == "Var Entero"):
                                                                        if(diccionarioVars[tokens[indice]]["valor"] != ""):
                                                                            arg2 = int(diccionarioVars[tokens[indice]]["valor"])
                                                                            indice+=1
                                                                        else:
                                                                            messagebox.showerror("Error", f"Error semántico, la variable {tokens[indice]} no se ha definido")
                                                                            break
                                                                    else:
                                                                        messagebox.showerror("Error", f"Error semántico, el tipo de variable para el primer argumento no es Var Entero {tokens[indice]}")
                                                                        break
                                                                else:
                                                                    messagebox.showerror("Error", f"Error semántico, variable utilizada {tokens[indice]} no existe")
                                                                if(tokens[indice] == ")"):
                                                                    indice+=1
                                                                    if(tokens[indice] == "?"):
                                                                        indice+=1
                                                                        # messagebox.showinfo("SIU", "Evalué operador relacional")
                                                                        if(tokens[posOp] == "=ESMAYOR"):
                                                                            LogicRes = (arg1>arg2)
                                                                            diccionarioVars[tokens[mivar]]["valor"] = LogicRes
                                                                            diccionarioVars[tokens[mivar]]["resoluble"] = "Si"
                                                                        if(tokens[posOp] == "=ESMENOR"):
                                                                            LogicRes = (arg1<arg2)
                                                                            diccionarioVars[tokens[mivar]]["valor"] = LogicRes
                                                                            diccionarioVars[tokens[mivar]]["resoluble"] = "Si"
                                                                    else:
                                                                        messagebox.showerror("Error", f"Error de sintáxis, se esperaba '?' en {tokens[indice-2]} {tokens[indice-1]} {tokens[indice]}")
                                                                else:
                                                                    messagebox.showerror("Error", f"Error de sintáxis, se esperaba ')' en {tokens[indice-2]} {tokens[indice-1]} {tokens[indice]}")
                                                                    break
                                                            else:
                                                                messagebox.showerror("Error", f"Error semántico, se esperaba segundo argumento de tipo numérico en {tokens[indice-2]} {tokens[tokens-1]} {tokens[indice]}")
                                                                break
                                                        else:
                                                            messagebox.showerror("Error", f"Error de sintáxis, se esperaba separador ',' en {tokens[indice-2]} {tokens[indice-1]} {tokens[indice]}")
                                                            break
                                                    else:
                                                        messagebox.showerror("Error", f"Error semántico, se esperaba primer argumento de tipo numérico en {tokens[indice-2]} {tokens[indice-1]} {tokens[indice]}")
                                                        break
                                                else:
                                                    messagebox.showerror("Error", f"Error de sintáxis, se esperaba '(' en {tokens[indice-2]} {tokens[indice-1]} {tokens[indice]}")
                                                    break
                                            #Comparación para ESIGUAL y NOIGUAL
                                            elif( (tokens[indice] == "=ESIGUAL") or (tokens[indice] == "=NOIGUAL") ):
                                                operacionTipo = indice
                                                global comparar1; global comparar2
                                                indice+=1
                                                if(tokens[indice] == "("):
                                                    indice+=1
                                                    if(tipo_token[indice] == "Cadena"):
                                                        comparar1 = tokens[indice]
                                                        indice+=1
                                                    elif(tipo_token[indice] == "Var"):
                                                        if(tokens[indice] in diccionarioVars):
                                                            if(diccionarioVars[tokens[indice]]["valor"] !=""):
                                                                auxTipo = diccionarioVars[tokens[indice]]["tipoDato"]
                                                                if(auxTipo == "Var Entero"):
                                                                    comparar1 = int(diccionarioVars[tokens[indice]]["valor"])
                                                                if(auxTipo == "Var Cadena"):
                                                                    comparar1 = diccionarioVars[tokens[indice]]["valor"]
                                                                if(auxTipo == "Var Booleana"):
                                                                    comparar1 = bool(diccionarioVars[tokens[indice]]["valor"])
                                                                indice+=1
                                                            else:
                                                                messagebox.showerror("Error", f"Error semántico, la variable utilizada {tokens[indice]} no tiene asignado ningún valor")
                                                                break
                                                        else:
                                                            messagebox.showerror("Error", f"Error semántico, variable utilizada {tokens[indice]} no declarada previamente")
                                                            break
                                                    elif(tipo_token[indice] == "Número"):
                                                        comparar1 = int(diccionarioVars[tokens[indice]]["valor"])
                                                        indice+=1
                                                    elif(tipo_token[indice] == "Boolean"):
                                                        comparar1 = bool(tokens[indice])
                                                        indice+=1
                                                    else:
                                                        messagebox.showerror("Error", f"Error de sintáxis, valor para el primer argumento no es valido en {tokens[indice-2]} {tokens[indice-1]} {tokens[indice]}")
                                                        break
                                                    # Podría fallar después de esto
                                                    if( (tokens[indice] == ",") and (tokens[indice-1]) != "("):
                                                        indice+=1
                                                        if(tipo_token[indice] == "Cadena"):
                                                            comparar2 = tokens[indice]
                                                            indice+=1
                                                        elif(tipo_token[indice] == "Var"):
                                                            if(tokens[indice] in diccionarioVars):
                                                                if(diccionarioVars[tokens[indice]]["valor"] !=""):
                                                                    auxTipo = diccionarioVars[tokens[indice]]["tipoDato"]
                                                                    if(auxTipo == "Var Entero"):
                                                                        comparar2 = int(diccionarioVars[tokens[indice]]["valor"])
                                                                    if(auxTipo == "Var Cadena"):
                                                                        comparar2 = diccionarioVars[tokens[indice]]["valor"]
                                                                    if(auxTipo == "Var Booleana"):
                                                                        comparar2 = bool(diccionarioVars[tokens[indice]]["valor"])
                                                                    indice+=1
                                                                else:
                                                                    messagebox.showerror("Error", f"Error semántico, la variable utilizada {tokens[indice]} no tiene asignado ningún valor")
                                                                    break
                                                            else:
                                                                messagebox.showerror("Error", f"Error semántico, variable utilizada {tokens[indice]} no declarada previamente")
                                                                break
                                                        elif(tipo_token[indice] == "Número"):
                                                            comparar2 = int(diccionarioVars[tokens[indice]]["valor"])
                                                            indice+=1
                                                        elif(tipo_token[indice] == "Boolean"):
                                                            comparar2 = bool(tokens[indice])
                                                            indice+=1
                                                        else:
                                                            messagebox.showerror("Error", f"Error de sintáxis, valor para el segundo argumento no es valido en {tokens[indice-2]} {tokens[indice-1]} {tokens[indice]}")
                                                            break
                                                        if( (tokens[indice] == ")") and (tokens[indice-1]!=",") ):
                                                            indice+=1
                                                            if(tokens[indice] == "?"):
                                                                indice+=1
                                                                if(tokens[operacionTipo] == "=ESIGUAL"):
                                                                    resLogico = (comparar1 == comparar2)
                                                                    diccionarioVars[tokens[mivar]]["valor"] = resLogico
                                                                    diccionarioVars[tokens[mivar]]["resoluble"] = "Si"
                                                                if(tokens[operacionTipo] == "=NOIGUAL"):
                                                                    resLogico = (comparar1 != comparar2)
                                                                    diccionarioVars[tokens[mivar]]["valor"] = resLogico
                                                                    diccionarioVars[tokens[mivar]]["resoluble"] = "Si"
                                                                # messagebox.showinfo("SIU", f"Evalué {tokens[operacionTipo]}")
                                                            else:
                                                                messagebox.showerror("Error", f"Error de sintáxis, se esperaba '?' en {tokens[indice-1]} {tokens[indice]}")
                                                        else:
                                                            messagebox.showerror("Error", f"Error de sintáxis, se esperaba ')' en {tokens[indice-1]} {tokens[indice]}")
                                                            break
                                                    else:
                                                        messagebox.showerror("Error", f"Error de sintáxis, se esperaba separador de argumentos ',' en {tokens[indice-2]} {tokens[indice-1]} {tokens[indice]}")
                                                        break
                                                else:
                                                    messagebox.showerror("Error", f"Error de sintáxis, se esperaba '(' en {tokens[indice-1]} {tokens[indice]}")
                                                    break
                                        else:
                                            messagebox.showerror(
                                                "Error", f"Error semántico, mismatch error, variable '{tokens[indice-2]}' es de tipo {tipoVar} y se le asignó {tipo_token[indice]}")
                                            break
                                    else:
                                        messagebox.showerror(
                                            "Error", f"Se esperaba palabra reservada 'equ' para asignación de valor a variable '{tokens[indice-1]}'")
                                        break
                                else:
                                    messagebox.showerror(
                                        "Error", f"Error semántico, variable '{tokens[indice]}' no declarada previamente")
                                    break
                            #BIFURCACIÓN PARA EL CASO DEL SI JALO NO JALO
                            if((tokens[indice] == "SI") and (tipo_token[indice] == "Built-In Word")):
                                indice += 1
                                if(tokens[indice]=="("):
                                    indice+=1
                                    #"=ESMAYOR", "=ESMENOR", "=ESIGUAL", "=NOIGUAL", "=AND", "=OR"
                                    if(tokens[indice] == "=ESMAYOR" or tokens[indice] == "=ESMENOR" or tokens[indice] == "=ESIGUAL" or tokens[indice] == "=NOIGUAL"):
                                        indice+=1
                                        if(tokens[indice]=="("):
                                            indice+=1
                                            if(tokens[indice] != "@ENT" or tokens[indice] != "@CAD" or tokens[indice] != "@BULL"):
                                                #ESTE EVALÚA EN CASO DE QUE SE QUIERAN COMPARAR ENTEROS
                                                if(tokens[indice] in diccionarioVars and diccionarioVars[tokens[indice]]["tipoDato"] == "Var Entero"):
                                                    indice+=1
                                                    if(tokens[indice]==","):
                                                        indice+=1
                                                        if(tokens[indice] != "@ENT" or tokens[indice] != "@CAD" or tokens[indice] != "@BULL"):
                                                            if(tokens[indice] in diccionarioVars and diccionarioVars[tokens[indice]]["tipoDato"] == "Var Entero"):
                                                                indice+=1
                                                                if(tokens[indice]==")"):
                                                                    indice+=1
                                                                    #AQUI PUEDE IR OTRA OPERACIÓN PARA EL IF E
                                                                    if(tokens[indice]==")"):
                                                                        indice+=1
                                                                        
                                                                        if(tokens[indice]==":"):
                                                                            indice+=1
                                                                            #AQUI VA LA COMPROBACIÓN CUANDO SALTE A "JALO:"                                                                                                                                                        #-------------AQUI VA LA COMPROBACIÓN CUANDO SALTE A "JALO:"-------------#
                                                                            if(tokens[indice]=="JALO"):
                                                                                indice+=1
                                                                                if(tokens[indice]==":"):
                                                                                    indice+=1
                                                                                    while(tokens[indice]!="FINJALO_"):
                                                                                        break
                                                                                    indice+=1
                                                                                    if(tokens[indice]=="NOJALO"):
                                                                                        indice+=1
                                                                                        if(tokens[indice]==":"):
                                                                                            indice+=1
                                                                                            while(tokens[indice]!="FINNOJALO_"):
                                                                                                break
                                                                                            indice+=1
                                                                                            if(tokens[indice]=="FINSI_"):
                                                                                                indice+=1
                                                                                            else:
                                                                                                messagebox.showerror("Error","Se esperaba el cierre del SI():")
                                                                                                break
                                                                                        else:
                                                                                            messagebox.showerror("Error","Se esperaba ':' después del NOJALO")
                                                                                            break
                                                                                    else:
                                                                                        messagebox.showerror("Error","Se esperaba parte final del SI(): 'NOJALO:'")
                                                                                        break 
                                                                                else:
                                                                                    messagebox.showerror("Error","Se esperaba ':'")
                                                                                    break
                                                                            else:
                                                                                messagebox.showerror("Error","Se esperaba el cuerpo del SI():")
                                                                                break
                                                                    else:
                                                                        messagebox.showerror("Error","Se esperaba ')'")
                                                                        break
                                                                else:
                                                                    messagebox.showerror("Error","Se esperaba ')'")
                                                                    break
                                                            else:
                                                                messagebox.showerror("Error",f"Variable {tokens[indice]} no defininida en el cuerpo de atributos")
                                                                break
                                                        else:
                                                            messagebox.showerror("Error","Debe usar una variable que esté en los atributos") 
                                                            break  
                                                    else:
                                                        messagebox.showerror("Error","Se esperaba una ','")
                                                        break 
                                                    #ESTE EVALÚA EN CASO DE QUE SE QUIERAN COMPARAR CADENAS
                                                elif(tokens[indice] in diccionarioVars and diccionarioVars[tokens[indice]]["tipoDato"] == "Var Cadena"):
                                                    indice+=1
                                                    if(tokens[indice]==","):
                                                        indice+=1
                                                        if(tokens[indice] != "@ENT" or tokens[indice] != "@CAD" or tokens[indice] != "@BULL"):
                                                            if(tokens[indice] in diccionarioVars and diccionarioVars[tokens[indice]]["tipoDato"] == "Var Cadena"):
                                                                indice+=1
                                                                if(tokens[indice]==")"):
                                                                    indice+=1
                                                                    if(tokens[indice]==")"):
                                                                        indice+=1
                                                                        if(tokens[indice]==":"):
                                                                            indice+=1
                                                                            #AQUI VA LA COMPROBACIÓN CUANDO SALTE A "JALO:"                                                                                                                                                        #-------------AQUI VA LA COMPROBACIÓN CUANDO SALTE A "JALO:"-------------#
                                                                            if(tokens[indice]=="JALO"):
                                                                                indice+=1
                                                                                if(tokens[indice]==":"):
                                                                                    indice+=1
                                                                                    while(tokens[indice]!="FINJALO_"):
                                                                                        break
                                                                                    indice+=1
                                                                                    if(tokens[indice]=="NOJALO"):
                                                                                        indice+=1
                                                                                        if(tokens[indice]==":"):
                                                                                            indice+=1
                                                                                            while(tokens[indice]!="FINNOJALO_"):
                                                                                                break
                                                                                            indice+=1
                                                                                            if(tokens[indice]=="FINSI_"):
                                                                                                indice+=1
                                                                                            else:
                                                                                                messagebox.showerror("Error","Se esperaba el cierre del SI():")
                                                                                                break
                                                                                        else:
                                                                                            messagebox.showerror("Error","Se esperaba ':' después del NOJALO")
                                                                                            break
                                                                                    else:
                                                                                        messagebox.showerror("Error","Se esperaba parte final del SI(): 'NOJALO:'")
                                                                                        break 
                                                                                else:
                                                                                    messagebox.showerror("Error","Se esperaba ':'")
                                                                                    break
                                                                            else:
                                                                                messagebox.showerror("Error","Se esperaba el cuerpo del SI():")
                                                                                break
                                                                    else:
                                                                        messagebox.showerror("Error","Se esperaba ')'")
                                                                        break
                                                                else:
                                                                    messagebox.showerror("Error","Se esperaba ')'")
                                                                    break
                                                            else:
                                                                messagebox.showerror("Error",f"Variable {tokens[indice]} no defininida en el cuerpo de atributos")
                                                                break
                                                        else:
                                                            messagebox.showerror("Error","Debe usar una variable que esté en los atributos") 
                                                            break  
                                                    else:
                                                        messagebox.showerror("Error","Se esperaba una ','")
                                                        break 
                                                #ESTE EVALÚA EN CASO DE QUE SE QUIERAN COMPARAR BOOLEANOS
                                                elif(tokens[indice] in diccionarioVars and diccionarioVars[tokens[indice]]["tipoDato"] == "Var Booleana"):
                                                    indice+=1
                                                    if(tokens[indice]==","):
                                                        indice+=1
                                                        if(tokens[indice] != "@ENT" or tokens[indice] != "@CAD" or tokens[indice] != "@BULL"):
                                                            if(tokens[indice] in diccionarioVars and diccionarioVars[tokens[indice]]["tipoDato"] == "Var Booleana"):
                                                                indice+=1
                                                                if(tokens[indice]==")"):
                                                                    indice+=1
                                                                    if(tokens[indice]==")"):
                                                                        indice+=1
                                                                        if(tokens[indice]==":"):
                                                                            indice+=1
                                                                            #AQUI VA LA COMPROBACIÓN CUANDO SALTE A "JALO:"                                                                                                                                                        #-------------AQUI VA LA COMPROBACIÓN CUANDO SALTE A "JALO:"-------------#
                                                                            if(tokens[indice]=="JALO"):
                                                                                indice+=1
                                                                                if(tokens[indice]==":"):
                                                                                    indice+=1
                                                                                    while(tokens[indice]!="FINJALO_"):
                                                                                        break
                                                                                    indice+=1
                                                                                    if(tokens[indice]=="NOJALO"):
                                                                                        indice+=1
                                                                                        if(tokens[indice]==":"):
                                                                                            indice+=1
                                                                                            while(tokens[indice]!="FINNOJALO_"):
                                                                                                break
                                                                                            indice+=1
                                                                                            if(tokens[indice]=="FINSI_"):
                                                                                                indice+=1
                                                                                            else:
                                                                                                messagebox.showerror("Error","Se esperaba el cierre del SI():")
                                                                                                break
                                                                                        else:
                                                                                            messagebox.showerror("Error","Se esperaba ':' después del NOJALO")
                                                                                            break
                                                                                    else:
                                                                                        messagebox.showerror("Error","Se esperaba parte final del SI(): 'NOJALO:'")
                                                                                        break 
                                                                                else:
                                                                                    messagebox.showerror("Error","Se esperaba ':'")
                                                                                    break
                                                                            else:
                                                                                messagebox.showerror("Error","Se esperaba el cuerpo del SI():")
                                                                                break
                                                                    else:
                                                                        messagebox.showerror("Error","Se esperaba ')'")
                                                                        break
                                                                else:
                                                                    messagebox.showerror("Error","Se esperaba ')'")
                                                                    break
                                                            else:
                                                                messagebox.showerror("Error",f"Variable {tokens[indice]} no defininida en el cuerpo de atributos")
                                                                break
                                                        else:
                                                            messagebox.showerror("Error","Debe usar una variable que esté en los atributos") 
                                                            break  
                                                    else:
                                                        messagebox.showerror("Error","Se esperaba una ','")
                                                        break 
                                                    #HASTA AQUI#
                                            else:
                                                messagebox.showerror("Error","Debe usar una variable que se encuentré en el cuerpo de atributos")
                                                break
                                        else:
                                            messagebox.showerror("Error","Se esperaba un paréntesis de aperutra '('")
                                            break
                                    else:
                                        messagebox.showerror("Error","Se esperaba un operador relacional")            
                                else:
                                    messagebox.showerror("Error","Se esperaba un paréntesis de aperutra '('")
                                    break         
                            #JOSTO AQUÍ IRÍA OTRA BIFURACIÓN   
                            # break 
                        indice+=1
                        if(tokens[indice] == "HASTAAQUILAVAMOSADEJAR_"):
                            messagebox.showinfo("EXITO", "PROGRAMA COMPILADO CORRECTAMENTE")
                        else:
                            messagebox.showerror("Error", f"Se esperaba cierre de clase 'HASTAAQUILAVAMOSADEJAR_'")                                      
                    else:
                        messagebox.showerror(
                            "Error", f"Error de sintáxis, se esperaba ':' en, {tokens[indice-1]}, {tokens[indice]}")
                else:
                    #print("Error de sintáxis, se esperaba declaración de atributos, funciones o principal")
                    messagebox.showerror(
                        "Error", f"Error de sintáxis, se esperaba declaración de atributos, funciones o principal")
            else:
                #print("Error de sintáxis, se esperaba ':' en", tokens[indice-2], tokens[indice-1])
                messagebox.showerror(
                    "Error", f"Error de sintáxis, se esperaba ':' en, {tokens[indice-2]}, {tokens[indice-1]}")
        else:
            #print("Error de sintáxis, palabra reservada no puede ser nombre de una clase en", tokens[indice-1], tokens[indice], tokens[indice+1])
            messagebox.showerror(
                "Error", f"Error de sintáxis, se esperaba palabra reservada 'CLASE' en {tokens[indice]}")
    else:
        #print("Error de sintáxis, se esperaba palabra reservada 'CLASE' en", tokens[indice])
        messagebox.showerror(
            "Error", f"Error de sintáxis, palabra reservada no puede ser nombre de una clase en {tokens[indice-1]}, {tokens[indice]}, {tokens[indice+1]}")
    print(diccionarioVars)
    return 0


#-----------------------------------------------------------------------------------------#
#--------------------------------------TOKENIZADOR----------------------------------------#
#-----------------------------------------------------------------------------------------#
def getTextInput(cadena, tokens, tipo_token):
    diccionarioVars.clear()
    lista_variables.clear()
    lista_funciones.clear()
    bandera = True

    while(len(cadena) > 0 and bandera == True):
        token = ""
        # primer caracter es númerico
        if((cadena[0].isdigit())):
            i = 0
            for c in cadena:
                if (not c.isdigit()):
                    break
                i += 1
            token = cadena[0:i]
            cadena = cadena[i::]
            if("." in cadena):
                messagebox.showerror(
                    "Error", f"Error léxico, números decimales no disponibles")
                bandera = False
                break
            else:
                tipo_token.append("Número")
        # primer caracter es especial
        elif(cadena[0] in specialL):
            # espacios
            if(cadena[0] == " " or cadena[0] == "\n"):
                i = 0
                for c in cadena:
                    if (c != " " and c != "\n"):
                        break
                    i += 1
                cadena = cadena[i::]
            # cadenas con comillas dobles
            elif(cadena[0] == "\"" or cadena[0] == "“"):
                i = 1
                for c in cadena[1::]:
                    if (c == "\"" or c == "”"):
                        break
                    i += 1
                token = cadena[1:i]
                tipo_token.append("Cadena")
                cadena = cadena[(i+1)::]
            # cacdenas con comillas simples
            elif(cadena[0] == "'"):
                i = 1
                for c in cadena[1::]:
                    if (c == "'"):
                        break
                    i += 1
                token = cadena[1:i]
                tipo_token.append("Cadena")
                cadena = cadena[(i+1)::]
            # variables
            elif(cadena[0] == "$"):
                i = 1
                for c in cadena[1::]:
                    if (c == "$"):
                        break
                    i += 1
                token = cadena[1:(i)]
                tipo_token.append("Var")
                cadena = cadena[(i+1)::]
            # Caso de operadores
            elif(cadena[0] == "*" or cadena[0] == "=" or cadena[0] == "@"):
                i = 1
                for c in cadena[1::]:
                    if (c in specialL):
                        break
                    i += 1
                token = cadena[0:i]
                # Para detectar tipo de operador aritmético
                if(token[0] == "*"):
                    if(token == "*MAS"):
                        tipo_token.append("Operador suma")
                    elif(token == "*MENOS"):
                        tipo_token.append("Operador resta")
                    elif(token == "*MULT"):
                        tipo_token.append("Operador multiplicación")
                    elif(token == "*DIV"):
                        tipo_token.append("Operador división")
                # Para detectar tipo de relacional
                elif(token[0] == "="):
                    if(token == "=ESMAYOR"):
                        tipo_token.append("Relacional mayor que")
                    elif(token == "=ESMENOR"):
                        tipo_token.append("Relacional menor que")
                    elif(token == "=ESIGUAL"):
                        tipo_token.append("Relacional comparador")
                    elif(token == "=NOIGUAL"):
                        tipo_token.append("Relacional diferente de")
                    elif(token == "=AND"):
                        tipo_token.append("Relacional AND")
                    elif(token == "=OR"):
                        tipo_token.append("Relacional OR")
                # Para detectar tipo de dato
                elif(token[0] == "@"):
                    if(token == "@ENT"):
                        tipo_token.append("Var Entero")
                    elif(token == "@CAD"):
                        tipo_token.append("Var Cadena")
                    elif(token == "@BULL"):
                        tipo_token.append("Var Booleana")
            # Detectando tipo de operador
                if(cadena[0] == "*"):
                    if(not token in operadoresA):
                        messagebox.showerror(
                            "Error", f"Error léxico {token}")  # error léxico
                        bandera = False
                elif(cadena[0] == "="):
                    if(not token in operadoresRL):
                        messagebox.showerror(
                            "Error", f"Error léxico {token}")  # error léxico
                        bandera = False
                elif(cadena[0] == "@"):
                    if(not token in tiposD):
                        messagebox.showerror(
                            "Error", f"Error léxico {token}")  # error léxico
                        bandera = False
                cadena = cadena[i::]
            # caracter especial
            else:
                token = cadena[0]
                cadena = cadena[1::]
                tipo_token.append("Caracter especial")
         # Asignación
        elif(cadena[0] == "e" and cadena[1] == "q" and cadena[2] == "u"):
            token = cadena[0:3]
            cadena = cadena[3::]
            tipo_token.append("Asignación")
        # primer caracter es normal
        else:
            i = 0
            for c in cadena:
                if (c in specialL):
                    break
                i += 1
            token = cadena[0:i]
            cadena = cadena[i::]
            if(token in builtIn):
                tipo_token.append("Built-In Word")
            elif((token == "True") or (token == "False")):
                bool(token)
                tipo_token.append("Boolean")
            else:
                if( (token[0] == "-") and (token[1:]).isdigit() ):
                    tipo_token.append("Número")
                else:
                    tipo_token.append("Nombre de método o clase")

        if(token != ""):
            tokens.append(token)
    AnalisisSintactico()


def crearTablaTokens(tokens, tipo_token):
    newWindow = Toplevel(root)
    newWindow.title("Tabla de tokens")
    newWindow.config(background="#334856")
    newWindow.geometry(f"{700}x{300}+{200}+{30}")
    # Creación de tabla________
    columns = ('Num', 'Token', 'ID')
    tree = ttk.Treeview(newWindow, columns=columns, show='headings')
    tree.heading('Num', text='Num')
    tree.heading('Token', text='Token')
    tree.heading('ID', text='ID_String')

    tree.grid(row=3, column=0)
    scrollbar = ttk.Scrollbar(
        newWindow, orient=tkinter.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=3, column=1, sticky='ns')

    for items in range(len(tokens)):
        tree.insert('', tkinter.END, values=(
            items, tokens[items], tipo_token[items]))

    tokens.clear()
    tipo_token.clear()


#-----------------------------------------------------------------------------------------#
#-----------------------------------Creación de la raíz-----------------------------------#
#-----------------------------------------------------------------------------------------#
root = Tk()
root.config(background="#26292b")
root.overrideredirect(0)
root.geometry(f"{750}x{650}+{200}+{30}")
root.title("Analizador LSS")
# Creación de Frame______________________
Frame1 = Frame(root, background="#26292b")
Frame1.pack()
# Creación de label "Titulo"______________________
LabelTitle = Label(Frame1, text="ANALIZADOR LÉXICO", font=(
    "Verdana", 16), background="#26292b", fg="#FFFFFF")
LabelTitle.grid(row=0, column=0)
# Creación de label "Titulo"______________________
LabelTitle = Label(Frame1, text="", background="#26292b")
LabelTitle.grid(row=2, column=0)
# Caja de texto______________________
textoComentario = Text(Frame1, width=75, height=20,
                       background="#2e3239", fg="white")
textoComentario.grid(row=1, column=0)
scrollVert = Scrollbar(Frame1, command=textoComentario.yview)
scrollVert.grid(row=1, column=1, sticky="nsew")
textoComentario.config(yscrollcommand=scrollVert.set)
# Botones play______________________
#add=PhotoImage(file="C:\\Users\\yaelc\\Desktop\\Semestre 7\\Lenguajes Automatas 2\\compilador\\Tokenizer\\Proyectofinal\\play.png")
botonañadir = Button(Frame1, text="P", command=lambda: getTextInput(textoComentario.get("1.0", "end"), tokens, tipo_token))
botonañadir.place(relx=0.9, rely=0.028, anchor=CENTER)
# Botones cerrar______________________
#cerrar=PhotoImage(file="C:\\Users\\yaelc\\Desktop\\Semestre 7\\Lenguajes Automatas 2\\compilador\\Tokenizer\\Proyectofinal\\cerrar.png")
btncerrar = Button(Frame1, text="X", command=cerrarF)
btncerrar.place(relx=0.978, rely=0.028, anchor=CENTER)


#-----------------Barra menú--------------------#
barraMenu = Menu(root)
root.config(menu=barraMenu, width=300, height=300)
MenuLSS = Menu(barraMenu, tearoff=0)
MenuLSS.add_command(label="Tabla de tokens",
                    command=lambda: crearTablaTokens(tokens, tipo_token))
MenuLSS.add_command(label="Tabla de variables")
barraMenu.add_cascade(label="Tablas", menu=MenuLSS)

root.mainloop()
