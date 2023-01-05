
import tkinter as tk
from tkinter import*
import sqlparse#libreria de sql cup y lex
import Traductor_Insert as ins
import Traductor_Select as slc
#import Traductor_Delete as dl



def Boton_Analizar(len_sql,analizador_s , name):
    consulta_mql = " "
    consulta_sin = " "
    consulta = name.get()
    formato = sqlparse.format(consulta, keyword_case="upper")
    analizado = sqlparse.parse(formato)  # analiza la primera cadena
    token_list = analizado[0]  # extraer la primera consulta (si hay más de una en la cadena)
    tokens = token_list.tokens  # extrae todas las palabras de la consulta y las clasifica según su tipo
    tipo_consulta = tokens[0].value
    if tipo_consulta == "SELECT":
            consulta_mql = slc.select(tokens)
            consulta_sin = "CONSULTA DE TIPO SELECT"

    elif tipo_consulta == "INSERT":
        #print("consulta de tipo INSERT")
        consulta_mql = ins.insert(tokens)
        consulta_sin = "CONSULTA DE TIPO INSERT"
    else:
        #consulta_mql = "CONSULTA DE SQL ERRADA ERROR EN LA LINEA 1 XD XD XD XD"
        consulta_sin = "CONSULTA DE SQL ERRADA se esperava un SELECT,FROM,INSERT"
    #print("LA CONSULTA REALIZADA ES: ", consulta_mql)
    print("LA CONSULTA REALIZADA ES: ",consulta_sin)
    len_sql.delete('1.0', tk.END) #ELIMINAR EL TEXT BOX
    len_sql.insert(tk.END, consulta_mql)

    analizador_s.delete('1.0', tk.END) #ELIMINAR EL TEXT BOX
    analizador_s.insert(tk.END, consulta_sin)
    
def Vista_tkinker():
    #declaramos ventana
    windows = tk.Tk()
    windows.title("MySQL pasar a MongoDB ")
    windows.minsize(700, 500)
    #analiza texto encabezado
    label = tk.Label(windows, text="Traductor de SQL a MQL",font=("Arial", 12), bg="#7C96A8", fg="white", width=80, height=2)
    label.place(x=0, y=10)
    #anbaliza el texto de salida qml
    len_sql = tk.Text(windows, width= 35, height = 20)
    len_sql.place(x=380, y=90)
    len_sql.insert(tk.END,"")
    #salidassss errores
    analizador_s = tk.Text(windows, width= 85, height = 5)
    analizador_s.place(x=8, y=420)
    analizador_s.insert(tk.END,"")
    #analiza texto de etrada sql
    name = tk.StringVar()
    nameEntered = tk.Entry(windows,width = 47, textvariable=name)
    nameEntered.place(x=8, y=90)
    #pantalla fiunta

    #nameEntered.grid(column=0, row=1)
    #analiza botn
    button = tk.Button(windows, text="TRADUCIR", command=lambda: Boton_Analizar(len_sql,analizador_s,name))
    button.place(x=310, y=250)
    
    #mostrar pantalllaso errores
    text_errores = Text(windows, width= 35, height = 18)
    text_errores.place(x=8, y=110)
    windows.mainloop()

def main():
    Vista_tkinker()



if __name__ == "__main__":
    main()
