
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where, Function, Parenthesis, Values
import string

# Consultas que podemos rtealizar
#cadena1 = "INSERT INTO items (name,price) VALUES('Kellogs',2);"
def insert(tokens):
  tabla = ""
  #where_found = False
  columnas = []
  val_temporal = []
  valor = []

# 

#recorre todos los tokens para localizar el nombre de la tabla y encontrar los nombres de las columnas y los nombres de los valores,
# que se almacenan en las columnas y listas de valores respectivamente.
  for token in tokens:
    if isinstance(token, Function):
      tabla = token[0].value
      columnas = Encontrar_columna_nom(token)
    if isinstance(token,Values):
      val_temporal = Encontrar_columna_val(token)

# Aplicar formato a los elementos de los valores para eliminar la puntuación y los elementos vacíos
  valor = Valores_formato(val_temporal)

# calcula el nombre de la columna asociada para cada valor y crea la consulta mongodb correspondiente
  salida_parentesis = convertir_en_mongo(columnas, valor)
  
# Si se agrega más de una tupla, el resultado se incluye entre corchetes
  if (len(columnas) != len(valor)):
    salida_parentesis = "[" + salida_parentesis + "]"
  salida = "db." + tabla + ".insert( " + salida_parentesis + " )"
  return salida


def Encontrar_columna_nom(token):
  columnas = []
  for par in token:
    if isinstance(par,Parenthesis):
      for idlist in par:
        if isinstance(idlist,IdentifierList):
          for id in idlist:
            if isinstance(id,Identifier):
              columnas.append(id.value)
  return columnas

def Encontrar_columna_val(token):
  val_temporal = []
  for par in token:
    if isinstance(par,Parenthesis):
      for idlist in par:
        if isinstance(idlist,IdentifierList):
          for id in idlist:
            val_temporal.append(id.value)
  return val_temporal

def Valores_formato(val_temporal):
  valor = []
  new_s_p = string.punctuation.translate(str.maketrans('','','-'))
  for s in val_temporal:
      s = s.translate(str.maketrans('','',new_s_p))
      valor.append(s)
  valor = list(filter(None, valor))
  return valor

def convertir_en_mongo(columnas, valor):
  salida_parentesis = ""
  for i, value in enumerate(valor, start = 0):
    first_elem = ""
    last_elem = ""
    id_col = i%len(columnas)
    if id_col == 0:
      first_elem = "{"
    elif id_col == len(columnas)-1:
      last_elem = "}"
    salida_parentesis = salida_parentesis + first_elem +columnas[id_col]  + ": '" + value + "'" + last_elem
    if value != valor[-1]:
      salida_parentesis = salida_parentesis + ", "
  return salida_parentesis