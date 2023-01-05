






import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where, Function

#consultas que acepta
stringa1 = 'SELECT * FROM people'         #//////////////////////////
#stringa2 = 'SELECT id, user_id, status FROM people order by status asc limit 3'  #//////////////////////////
stringa3 = 'SELECT user_id FROM people'  #//////////////////////////

def select(tokens):
  table = "" #aqui entran en toda la cadena 
  where_found = False
  select_found = False
  limit_found = False
  wildcard_found = False
  wildcard_count_found = False
  distinct_found = False
  count_found = False
  output_parenthesis_select_attributes = ""
  order_by_found = False
  order_by_rule = ""
  count_field = ""
  count_field_found = False

# itera a través de todos los tokens para ubicar el nombre de la tabla y encontrar la condición where,
# que se almacena en el vector analizado.
# (es) parsed -> ['status', '=', '"D"', 'OR', 'name', '<=', '"Carlo"', 'AND', 'name', '!=', '"Saretta"']
  for token in tokens:
    if token.value == "SELECT":
      select_found = True
    if token.value == "*":
      wildcard_found = True
      select_found = False




    if isinstance(token, Identifier) and not select_found and not order_by_found:
      table = token.value
    if isinstance(token,Identifier) and select_found :
      select_found = False
      output_parenthesis_select_attributes = convert_single_select_attribute(token) 
    if isinstance(token,IdentifierList) and select_found:
      select_found = False
      output_parenthesis_select_attributes = convert_multiple_select_attributes(token)



    if isinstance(token, Where):
      where_found = True
      output = convert_where_condition(token)
      # Si los operadores lógicos estuvieran presentes en la condición where
      # luego utilícelos para la construcción de la consulta final, de lo contrario
      # si se trataba de una condición simple, cree la consulta final con solo
      # el único selector presente.
      comma = ""

      if isinstance(output[0],LogicOperator):
        if distinct_found:
          output_parenthesis_distinct = '.distinct("' + distinct_value + '", ' + output[-1].created_string + ")"
          final_query = "db." + table + output_parenthesis_distinct
        if output_parenthesis_select_attributes != "" and not distinct_found:
          comma = ","
        if limit_found:
          limit_found = False
          final_query = "db."+ table +".find(" + output[-1].created_string + comma + " " + output_parenthesis_select_attributes + ")" + output_parenthesis_limit
        elif count_field_found:
          final_query = "db."+ table +".find(" + output[-1].created_string + comma + " " + output_parenthesis_select_attributes + "{" + count_field + ": {exists:true}}" + ")"
        else:
          final_query = "db."+ table +".find(" + output[-1].created_string + comma + " " + output_parenthesis_select_attributes + ")"

      elif output[1] == "like":
        original = output[2].replace('"', '')
        positions = [pos for pos, char in enumerate(original) if char == "%"]
        like_arg = original.replace("%", "/")
        if len(positions) == 1:
          if positions[0] == 0:
             like_arg = like_arg[:len(original)] + "$/" + like_arg[len(original):]
          elif positions[0] == len(original) - 1 :
            like_arg = like_arg[:0] + "/^" + like_arg[0:]
        final_query = "db." + table + ".find({" + output[0] + ": " + like_arg + "})"



  if not where_found:
    if distinct_found:
      final_query = "db."+ str(table) + output_parenthesis_distinct
    else:
      if wildcard_found:
        final_query = "db."+str(table)+".find({})"
      elif count_field_found:
        final_query = "db."+ table +".find({" + count_field + ": {exists:true}}" + ")" 
      elif output_parenthesis_select_attributes != "" :
        final_query = "db."+str(table)+".find({}," + output_parenthesis_select_attributes + ")"
      else:
        final_query = "db."+str(table)+".find({})"
  if order_by_found:
    final_query = final_query + ".sort({ " + order_by_column + ": " + order_by_rule + "})"
  if limit_found:
    final_query = final_query + output_parenthesis_limit
  if count_found:
    final_query = final_query + ".count()"

  return(final_query)
