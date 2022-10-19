from hashlib import new
from re import I
from tkinter import *
from tkinter import ttk
import tkinter
from tkinter import messagebox 
#Tokinzador variables______________________
specialL = [":",",","(",")","?","*","=","$","@","~","\"","'","“","”"," ","\n"]
operadoresA = ["*MAS","*MENOS","*MULT","*DIV"]
operadoresRL = ["=ESMAYOR","=ESMENOR","=ESIGUAL","=NOIGUAL","=AND","=OR"]
builtIn = ["CLASE", "HASTAAQUILAVAMOSADEJAR_", "ATRIBUTOS", "FINATRIBUTOS_",
            "DEFFUNCS", "FINDEFFUNCS_", "ESCRIBIDO", "RECIBIDO", "ITERAR", "FINITERAR_",
            "SI", "JALO", "FINJALO_", "NOJALO", "FINNOJALO_", "FINSI_", "PRINCIPAL", "FINPRINCIPAL_", "FUNC", "FINFUNC_", "ENT", "CAD", "BULL"]
tiposD = ["@ENT","@CAD","@BULL"]

tokens = []
tipo_token = []
lista_variables = []
lista_funciones = []
#Parte lógica______________________
def cerrarF():
    root.destroy()

def AnalisisSintactico(text):

    #for ind in range (len(tokens)):
     #   if(tokens[ind] in builtIn):
      #      textoComentario = tokens[ind]
       #     textoComentario = str.config(fg="green")
            
    banderaErrorSintactico = False
    #----------------------------PRUEBA DE COLORES----------------------------

    #Examinar estructura inicial-----
    #Primero deberá de tener la palabra reservada CLASE y nombre de la clase, seguido de un ":"
    indice = 0
    if(tokens[indice] == "CLASE" and tipo_token[indice] == "Built-In Word"):
        indice+=1
        if(tipo_token[indice] == "Nombre de método o clase"):
            indice+=1
            if(tokens[indice] == ":"):
                indice+=1
                #Tiene la estructura correcta para una clase, se continúa aquí --->
                #print("Estructura correcta")
                #Se bifurca en 3,  puede existir la declaración de atributos, funciones o directamente el principal
                if(tokens[indice] == "ATRIBUTOS" and tipo_token[indice] == "Built-In Word"):
                    indice+=1
                    if(tokens[indice] == ":"):
                        indice+=1
                        #Se esperaría encontrar declaración de variables
                        while(tokens[indice]!="FINATRIBUTOS_"):
                            if((tokens[indice] == "@ENT") or (tokens[indice] == "@CAD") or (tokens[indice] == "@BULL")):
                                indice+=1
                                if(tipo_token[indice] == "Var"):
                                    Vari = tokens[indice]
                                    #Si hay un carácter especial dentro del nombre de la variable, se envía un error de sintáxis
                                    for posi in range(len(Vari)):
                                        if((Vari[posi] in specialL)):
                                            banderaErrorSintactico = True
                                            print(Vari[posi])
                                            break
                                        if(banderaErrorSintactico == True):
                                            #print("Error de sintáxis, la variable contiene palabras o carácteres no válidos")
                                            messagebox.showerror("Error",f"Error de sintáxis, la variable contiene palabras o carácteres no válidos")
                                            break
                                        elif((tokens[indice] in operadoresA) or (tokens[indice] in operadoresRL) or (tokens[indice] in builtIn) or ((tokens[indice] in tiposD))):
                                            #print("Error de sintáxis, la variable contiene palabras o carácteres no válidos")
                                            messagebox.showerror("Error",f"Error de sintáxis, la variable contiene palabras o carácteres no válidos")
                                            break
                                    else:
                                        #El nombre de la variable es correcto, se añade a la lista de variables
                                        lista_variables.append(tokens[indice])
                                        indice+=1
                                    if(tokens[indice] == "?"):
                                        indice+=1
                                        #La estructura para declarar una variable es correcta, se continúa leyendo
                                        
                                    else:
                                        #print("Error de sintáxis, se esperaba '?' en", tokens[indice-2], tokens[indice-1])
                                        messagebox.showerror("Error",f"Error de sintáxis, se esperaba '?' en, {tokens[indice-2]}, {tokens[indice-1]}")
                                        break
                                else:
                                    #print("Error de sintáxis, se esperaba una variable")
                                    messagebox.showerror("Error",f"Error de sintáxis, se esperaba una variable")
                                    break
                            else:
                                #print("Error de sintáxis, se esperaba el tipo de variable")
                                messagebox.showerror("Error",f"Error de sintáxis, se esperaba el tipo de variable")
                                break
                        indice+=1
                    else:
                        #print("Error de sintáxis, se esperaba ':' en", tokens[indice-1])
                        messagebox.showerror("Error",f"Error de sintáxis, se esperaba ':' en, {tokens[indice-1]}")
                #En caso de que se vaya directamente a la definición de funciones
                if(tokens[indice] == "DEFFUNCS" and tipo_token[indice] == "Built-In Word"):
                    indice+=1
                    if(tokens[indice] == ":"):
                        indice+=1
                        #Aquí se analiza que se tenga la estructura de una función declarada
                        while(tokens[indice]!="FINDEFFUNCS_"):
                            if(tokens[indice] == "~"):
                                indice+=1
                                if((tipo_token[indice] == "Built-In Word") and (tokens[indice] == "FUNC")):
                                    indice+=1
                                    if((tipo_token[indice] == "Built-In Word") and (tokens[indice] == "ENT" or tokens[indice] == "CAD" or tokens[indice] == "BULL")):
                                        indice+=1
                                        if(tipo_token[indice] == "Nombre de método o clase"):
                                            indice+=1
                                            if(tokens[indice] == "("):
                                                indice+=1
                                                #Leér tantos parámetros recibidos por la función (también se analiza la estructura de los argumentos)
                                                while(tokens[indice]!=")"):
                                                    if((tokens[indice] == "@ENT") or (tokens[indice] == "@CAD") or (tokens[indice] == "@BULL")):
                                                        indice+=1
                                                        if(tipo_token[indice] == "Var"):
                                                            indice+=1
                                                            if(tokens[indice] == ","):
                                                                indice+=1
                                                            elif(tokens[indice] == ")"):
                                                                break
                                                            else:
                                                                #print("Error sintáctico, se esperaba ','")
                                                                messagebox.showerror("Error",f"Error sintáctico, se esperaba ','")
                                                                break
                                                        else:
                                                            #print("Error sintáctico, se esperaba una variable")
                                                            messagebox.showerror("Error",f"Error sintáctico, se esperaba una variable")
                                                            break
                                                    else:
                                                        #print("Error sintáctico, se esperaba el tipo de dato para el argumento recibido", tokens[indice])
                                                        messagebox.showerror("Error",f"Error sintáctico, se esperaba el tipo de dato para el argumento recibido, {tokens[indice]}")
                                                        break
                                                indice+=1
                                                if(tokens[indice] == "?"):
                                                    indice+=1
                                                else:
                                                    #print("Error sintáctico, se esperaba '?' en", tokens[indice-3], tokens[indice-2], tokens[indice-1])
                                                    messagebox.showerror("Error",f"Error sintáctico, se esperaba '?' en, {tokens[indice-3]}, {tokens[indice-2]}, {tokens[indice-1]}")
                                                    break
                                            else:
                                                #print("Error sintáctico, se esperaba '(' en", tokens[indice-4], tokens[indice-3], tokens[indice-2], tokens[indice-1])
                                                messagebox.showerror("Error",f"Error sintáctico, se esperaba '(' en, {tokens[indice-4]}, {tokens[indice-3]}, {tokens[indice-2]}, {tokens[indice-1]}")
                                                break
                                        else:
                                            #print("Error sintáctico, se esperaba nombre del método")
                                            messagebox.showerror("Error",f"Error sintáctico, se esperaba nombre del método")
                                    else:
                                        #print("Error sintáctico, se esperaba el tipo de dato para la función")
                                        messagebox.showerror("Error",f"Error sintáctico, se esperaba el tipo de dato para la función")
                                        break
                                else:
                                    #print("Error sintáctico, se esperaba palabra reservada FUNC")
                                    messagebox.showerror("Error",f"Error sintáctico, se esperaba palabra reservada FUNC")
                                    break
                            else:
                                #print("Error sintáctico, se esperaba inicio de declaración de una función '~'")
                                messagebox.showerror("Error",f"Error sintáctico, se esperaba inicio de declaración de una función '~'")
                                break
                        indice+=1   
                #EN CASO DE QUE SE VAYA A PRINCIPAL#
                #------------------------------------------------#
                #--------------SECCIÓN PRINCIPAL-----------------#
                #------------------------------------------------#
                if(tokens[indice] == "PRINCIPAL" and tipo_token[indice] == "Built-In Word"):
                    indice+=1
                    if(tokens[indice] == ":"):
                        indice+=1
                        #Todo código lógico aquí (Inicio del apartado principal) --->
                        #ESCRIBIDO
                        if(tokens[indice] == "ESCRIBIDO" and tipo_token[indice] == "Built-In Word"):
                            indice+=1
                            if(tokens[indice] == "("):
                                indice+=1
                                while(tokens[indice]!=")"):
                                    if(tipo_token[indice] == "Cadena" or tipo_token[indice] == "Var"):
                                        indice+=1
                                    if(tokens[indice] == "+"):
                                        indice+=1

                    else:
                        messagebox.showerror("Error",f"Error de sintáxis, se esperaba ':' en, {tokens[indice-1]}, {tokens[indice]}")
                else:
                    #print("Error de sintáxis, se esperaba declaración de atributos, funciones o principal")
                    messagebox.showerror("Error",f"Error de sintáxis, se esperaba declaración de atributos, funciones o principal")
            else:
                #print("Error de sintáxis, se esperaba ':' en", tokens[indice-2], tokens[indice-1])
                 messagebox.showerror("Error",f"Error de sintáxis, se esperaba ':' en, {tokens[indice-2]}, {tokens[indice-1]}")
        else:
            #print("Error de sintáxis, palabra reservada no puede ser nombre de una clase en", tokens[indice-1], tokens[indice], tokens[indice+1])
            messagebox.showerror("Error",f"Error de sintáxis, se esperaba palabra reservada 'CLASE' en {tokens[indice]}")
    else:
        #print("Error de sintáxis, se esperaba palabra reservada 'CLASE' en", tokens[indice])
        messagebox.showerror("Error",f"Error de sintáxis, palabra reservada no puede ser nombre de una clase en {tokens[indice-1]}, {tokens[indice]}, {tokens[indice+1]}")
    print(lista_variables)
    return 0

def getTextInput(cadena, tokens):
    newWindow = Toplevel(root)
    newWindow.title("Tabla de tokens")
    newWindow.config(background="#334856")
    newWindow.geometry(f"{700}x{300}+{200}+{30}")
    #Creación de tabla______________________
    columns = ('Num', 'Token', 'ID')
    tree = ttk.Treeview(newWindow, columns=columns, show='headings')
    tree.heading('Num', text='Num')
    tree.heading('Token', text='Token')
    tree.heading('ID', text='ID_String')

    tree.grid(row=3, column=0)
    scrollbar = ttk.Scrollbar(newWindow, orient=tkinter.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=3, column=1, sticky='ns')
    bandera = True
    while(len(cadena) > 0 and bandera == True):
        token = ""       
        #primer caracter es númerico
        if(cadena[0].isdigit()):
            i = 0
            for c in cadena:
                if (not c.isdigit()):
                    break
                i += 1
            token = cadena[0:i]
            cadena = cadena[i::]
            tipo_token.append("Número")
        #primer caracter es especial
        elif(cadena[0] in specialL):
            #espacios
            if(cadena[0] == " " or cadena[0] == "\n"):
                i = 0
                for c in cadena:
                    if (c != " " and c != "\n"):
                        break
                    i += 1
                cadena = cadena[i::]
            #cadenas con comillas dobles
            elif(cadena[0] == "\"" or cadena[0] == "“"):
                i = 1
                for c in cadena[1::]:
                    if (c == "\"" or c == "”"):
                        break
                    i += 1
                token = cadena[1:i]
                tipo_token.append("Cadena")
                cadena = cadena[(i+1)::]
            #cacdenas con comillas simples
            elif(cadena[0] == "'"):
                i = 1
                for c in cadena[1::]:
                    if (c == "'"):
                        break
                    i += 1
                token = cadena[1:i]
                tipo_token.append("Cadena")
                cadena = cadena[(i+1)::]
            #variables
            elif(cadena[0] == "$"):
                i = 1
                for c in cadena[1::]:
                    if (c == "$"):
                        break
                    i += 1
                token = cadena[1:(i)]
                tipo_token.append("Var")
                cadena = cadena[(i+1)::]
            #Caso de operadores
            elif(cadena[0] == "*" or cadena[0] == "=" or cadena[0] == "@"):
                i = 1
                for c in cadena[1::]:
                    if (c in specialL):
                        break
                    i += 1
                token = cadena[0:i]
                #Para detectar tipo de operador aritmético
                if(token[0] == "*"):
                    if(token == "*MAS"):
                        tipo_token.append("Operador suma")
                    elif(token == "*MENOS"):
                        tipo_token.append("Operador resta")
                    elif(token == "*MULT"):
                        tipo_token.append("Operador multiplicación")
                    elif(token == "*DIV"):
                        tipo_token.append("Operador división")
                #Para detectar tipo de relacional
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
                #Para detectar tipo de dato
                elif(token[0] == "@"):
                    if(token == "@ENT"):
                        tipo_token.append("Var Entero")
                    elif(token == "@CAD"):
                        tipo_token.append("Var Cadena")
                    elif(token == "@BULL"):
                        tipo_token.append("Var Booleana")
            #Detectando tipo de operador
                if(cadena[0] == "*"):
                    if(not token in operadoresA):
                        print("Error léxico: " + token)#error léxico
                        bandera = False
                elif(cadena[0] == "="):
                    if(not token in operadoresRL):
                        print("Error léxico: " + token)#error léxico
                        bandera = False
                elif(cadena[0] == "@"):
                    if(not token in tiposD):
                        print("Error léxico: " + token)#error léxico
                        bandera = False
                cadena = cadena[i::]
            #caracter especial
            else:
                token = cadena[0]
                cadena = cadena[1::]
                tipo_token.append("Caracter especial")
         #Asignación
        elif(cadena[0] == "e" and cadena[1] == "q" and cadena[2] == "u"):
            token = cadena[0:3]
            cadena = cadena[3::]
            tipo_token.append("Asignación")
        #primer caracter es normal
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
            else:
                tipo_token.append("Nombre de método o clase")

        if(token != ""):
            tokens.append(token)
   
    #AnalisisSintactico()
#---------------------------------------------------------------------------------------------------------
    for items in range(len(tokens)):
        tree.insert('', tkinter.END, values=(items,tokens[items], tipo_token[items]))

#Creación de la raíz______________________
root=Tk()
root.config(background="#26292b")
root.title("TEAM CODE")
root.overrideredirect(0)
root.geometry(f"{750}x{650}+{200}+{30}")
#Creación de Frame______________________
Frame1=Frame(root, background="#26292b")
Frame1.pack()
#Creación de label "Titulo"______________________
LabelTitle=Label(Frame1, text="ANALIZADOR LÉXICO",font=("Verdana",16),background="#26292b",fg="#FFFFFF")
LabelTitle.grid(row=0, column=0)
#Creación de label "Titulo"______________________
LabelTitle=Label(Frame1, text="",background="#26292b")
LabelTitle.grid(row=2, column=0)
#Caja de texto______________________
textoComentario=Text(Frame1, width=75, height=20,background="#2e3239", fg="white")
textoComentario.grid(row=1, column=0)
scrollVert=Scrollbar(Frame1, command=textoComentario.yview)
scrollVert.grid(row=1,column=1, sticky="nsew")
textoComentario.config(yscrollcommand=scrollVert.set)
#Botones play______________________
add=PhotoImage(file="D:\\Archivos de programa\\Uni 7°\\Lenguajes y Autómatas 2\\T3\\PoyectoAnalizadorLSS-main\\play.png")
botonañadir=Button(Frame1, image=add, width=24, height=24, command=lambda:AnalisisSintactico(textoComentario.get("1.0","end")))
botonañadir.place(relx=0.9, rely=0.028, anchor=CENTER)
#Botones cerrar______________________
cerrar=PhotoImage(file="D:\\Archivos de programa\\Uni 7°\\Lenguajes y Autómatas 2\\T3\\PoyectoAnalizadorLSS-main\\cerrar.png")
btncerrar=Button(Frame1, image=add, width=24, height=24,command=cerrarF)
btncerrar.place(relx=0.978, rely=0.028, anchor=CENTER)

#-----------------Barra menú--------------------#
barraMenu=Menu(root)
root.config(menu=barraMenu, width=300, height=300)
MenuLSS=Menu(barraMenu, tearoff=0)
MenuLSS.add_command(label="Tabla de tokens", command=lambda:getTextInput(textoComentario.get("1.0","end"),tokens))
MenuLSS.add_command(label="Tabla de variables")
barraMenu.add_cascade(label="Tablas", menu=MenuLSS)

root.mainloop()