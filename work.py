
defined_names = []
procedures = {}
lista_corchetes = []
lista_direcciones = ["north", "south", "west", "east","front", "right", "left","back"]
lst_turn = ["left","right","around"]
lst_turnto = ["north", "south", "west", "east"]
proc_in_process = False
lst_val_created = []
def upload_txt(txt_direction):
    estado = True
    with open(txt_direction) as txt:
        for line in txt:

            p_a =line.count("(")
            p_c = line.count(")")
            if p_a != p_c:
                return False
            line = line.strip()
            if not line:
                continue
            if ";" in line:
                line = line[0:len(line)-1]
            tokens = line.split()

            estado = process_tokens(tokens,estado,proc_in_process)
            if estado == False:
                break

    if sum(lista_corchetes) != 0:
        estado = False
    return estado
def process_tokens(tokens,estado,proc):
    try:
        if tokens[0] == "defVar":
            estado = define_variable(tokens,estado)
        elif tokens[0] == "defProc":
            if "(" in tokens or ")" in tokens:
                return False
            estado = define_procedure(tokens,estado)
        elif tokens[0] == "{":
            lista_corchetes.append(1)
        elif tokens[0] == "}":
            lista_corchetes.append(-1)
            if proc:
                proc = False
                for j in lst_val_created:
                    defined_names.remove(j)
                    lst_val_created = []
        elif "walk" in tokens[0]:

            estado = two_pos_function(tokens,estado,"walk")
        elif "leap" in tokens[0]:
            estado = two_pos_function(tokens,estado,"leap")
        elif "drop"in tokens[0]:

            estado = one_pos_func(tokens,estado,"drop",defined_names)
        elif "jump" in tokens[0]:
            estado = jump_function(tokens,estado)
        elif "get" in tokens[0]:
            estado = one_pos_func(tokens,estado,"get",defined_names)
        elif "grab" in tokens[0]:
            estado = one_pos_func(tokens,estado,"grab",defined_names)
        elif "letGo" in tokens[0]:
            estado = one_pos_func(tokens,estado,"letGo",defined_names)
        elif "turn" in tokens[0]:
            estado = one_pos_func(tokens,estado,"turn",lst_turn)
        elif "turnto" in tokens[0]:
            estado = one_pos_func(tokens,estado,"turnto",lst_turnto)
        elif tokens[0] == "nop()" or tokens[0] == "nop ()":
            estado = True
        elif "if" in tokens[0]:

            estado = funct_if(tokens,estado)

        elif tokens[0].split("(")[0] in procedures:
            #falta
            return found_proc(tokens,estado)
            pass
        elif "if" == tokens[0]:
            estado = funct_if(tokens,estado)
        elif "while" == tokens[0]:

            estado = funct_while(tokens,estado)
        elif "nop()" == tokens[0]:
            return True
        elif tokens[0] == "repeat":
            estado = funct_repeat(tokens,estado)
        else:
            if name_fun(tokens,estado,proc_in_process):
                return True
            estado = validate_command(tokens,estado)
        return estado
    except:
        if tokens == "":
            return True
        return False

def define_variable(tokens, estado):
    if len(tokens) >= 3:
        variable_name = tokens[1]
        defined_names.append(variable_name)
    else:
        estado = False
    return estado

def define_procedure(tokens,estado):
    if len(tokens) >= 3:
        procedure_name = tokens[1]
        procedures[procedure_name] = 0
        proc_in_process = True
        val = ""
        for i in range(2,len(tokens)):
            el = tokens[i]
            if len(el) < 1:
                if el != "(" and el != ")":
                    val += el
            else:
                for x in el:
                    if x != "(" and x != ")" and x != " ":
                        val +=x
        if "{" not in val and "}" not in val:
            estado = True
            lst_val = val.split(",")
            for i in lst_val:
                procedures[procedure_name] +=1
                defined_names.append(i)   
                lst_val_created.append(i)    
        else:
            estado = False     
    else:
        estado = False

    return estado
def validate_command(tokens,estado):
    val = ""
    for token in tokens:
        if token in defined_names:
            continue
        elif token.startswith('(') and token.endswith(')'):
            function_name = token[1:-1]
            
            if function_name not in defined_names:
                estado = False
            elif function_name in procedures.keys():
                estado = True
            else:
                estado = False
            for j in token:
                if j != "(" and j != ")":
                    val +=j
        else:
            for j in token:
                if j != "(" and j != ")":
                    val +=j
            estado = False 
    if estado:
        lst = val.split(",")

        if len(lst) != procedures[function_name]:
            return estado
    return estado
def two_pos_function(tokens,estado,fn):
    #aun no esta acabada la funcion
    val = ""

    c = 0
    for i in tokens:
        if i == fn:
            pass
        elif fn in i:

                i = i.split("(")

                try:
                
                    val += i[1]
                except:
                    pass
        else:

            val += i

        c+=1

    correct_str =""
    for i in val:
        if i != "(" and i != ")":

            correct_str+=i

    lst_walk_fn = correct_str.split(",")

    es_numero = None
    try:
        int(lst_walk_fn[0])

        es_numero = True
    except:
        es_numero = False
    try:

        if lst_walk_fn[0] in defined_names:
            estado = True
        elif es_numero:
            estado = True
        else:
            
            return False
        if lst_walk_fn[1] in lista_direcciones:

            return True
        else: 

            return False
    except:

        return estado
def one_pos_func(tokens,estado,fn,type):

    if tokens[0] != fn:
        tokens[0].split("(")
    val = ""
    word = "()"
    for i in tokens:
        if fn == i:
            return False
        if fn in i:
            i =i.replace(fn,"")

            for j in i:
                if j not in word:
                    val+=j
                elif j == "," or j == ";":
                    return False
                else:
                    continue
        elif i not in word:
            for j in i:
                if j not in word:
                    val +=j                        
        elif i in word:
            continue
        else:
            estado = False
    number = 0
    try:
        int(val)
        number = True
    except:
        number = False
    if "turn" in fn:
        number = False
    if val in type:
                return True
    elif number:
        return True
    else: 
                estado = False
    return estado     
def funct_if(tokens,estado):
    #TODO hacerla toda
    co = True
    cond_block = False
    cual = None
    ahg = 0
    for i in tokens:
        ahg +=1
        if i == "if":
            cual = "if"
            if tokens[1] == "not:":
                co = cond_detection(tokens[2])
            else:
                am = ""
                hay = False
                for k in range(1,len(tokens)):
                    for m in tokens[k]:
                        if m == "{":
                            hay = True
                            break
                        else:
                          am += m  
                    if hay:
                        break
                co =  cond_detection(am)
        elif i == "else":
            cual = "else"
        
        for j in i:
            if j == "{":
                cond_block = True
                block = block_inside(tokens,estado,cual)
                estado = block
                if not(block):

                    return False
                lista_corchetes.append(1)
            elif j == "}":
                lista_corchetes.append(-1)
                if cond_block:
                    cond_block = False
                else:
    
                    return False 
            if co:
                estado = True
            else:

                return False
    if cond_block:

        return False
    return estado
def cond_detection(cond):

    #completar function
    i = 0
    est_not = False

    if "can" in cond: 
         
        return can_detection(cond)
    elif "facing" in cond:
        return facing_detection(cond)
    else:
        return False
def can_detection(pcan):
    can_detect = False
    if pcan == "can":
            return False
    elif "can" in pcan:
            new_lst = pcan.split("(")
            lst = new_lst[1:len(new_lst)+1]
            #toca ver como selecciono lo que quiero  

            return verify_simple_command(lst) 
    else:
        return False
def verify_simple_command(command):
    estado = None
    if "walk" in command:

        estado = two_pos_function(command,True,"walk")
    elif "leap" in command:
        estado = two_pos_function(command,True,"leap")
    elif "drop"in command:
        estado = one_pos_func(command,True,"drop",defined_names)
    elif "get" in command:
        estado = one_pos_func(command,True,"get",defined_names)
    elif "grab" in command:
        estado = one_pos_func(command,"grab",defined_names)
    elif "letGo" in command:
        estado = one_pos_func(command,"letGo",defined_names)
    elif "turn" in command:
        estado = one_pos_func(command,"turn",lst_turn)
    elif "turnto" in command:
        estado = one_pos_func(command,"turnto",lst_turnto)
    elif "jump" in command:
        estado = jump_function(command,estado)
    elif command == "nop()":
        estado = True
    else:
        return False
    return estado
def jump_function(tokens,estado):
    val = ""
    no = "jump()"
    for i in tokens:
        for j in i:
            if j not in no:
                val += j
    if "," not in val:
        return False
    lst_word = val.split(",")
    if len(lst_word) > 2 or len(lst_word)<2:
        return False
    for k in lst_word:
        try:
            int(k)
        except:
            if k in defined_names:
                estado = True
            else:
                return False
    return True
def block_inside(tokens,estado,c):
    bracket_o = 0
    block_inside = ""
    compare = 0
    term = False

    if c== "if":
        compare = 1

    elif c == "else":

        compare = 2

    for i in tokens:
        for j in i:
            if j == "{":

                bracket_o+=1

                lista_corchetes.append(1)
            elif j == "}" and bracket_o == compare:

                lista_corchetes.append(-1)
                bracket_o = 0
                term = True
                break
            elif j == "}":
                lista_corchetes.append(-1)
            elif bracket_o == compare:

                block_inside+= j
        if term:
            break

    lst = block_inside.strip().split()
    if ";" in lst:

        return False
    if bracket_o >0:

        return False

    return process_tokens(lst,estado,proc_in_process)
    
def name_fun(tokens,estado,poc_i_p):
    if len(tokens) != 3:
        return False 
    val = tokens[0]

    try:
        int(tokens[2])
        defined_names.append(val)
        return True
    except:
        if tokens[2] in defined_names:
            return True
        return False
def facing_detection(fac):
    start = ""
    end = ""
    count = 0
    if "not" in fac:
        return False
    for i in fac:
        if i == "(":
            start = count
        elif i == ")":
            end = count
        count +=1
    try:
        inside = fac[start+1:end]

        if inside in lista_direcciones:
            return True
        else:
            return False
    except:
        return False
        
def funct_while(tokens, estado):

    if len(tokens) < 3:
        return False

    cond = ""
    block_inside = []
    a = False
    for i in range(1,len(tokens)):
        for j in tokens[i]:
            if j != "{":
                cond += j
            else:
                a = True
                break
        if a:
            break

    val = ""

    if not(cond_detection(cond)):
        return False
    cor = False

    for i in range(2,len(tokens)):
            for j in tokens[i]:

                if j == "{":
                    lista_corchetes.append(1)
                    cor = True
                elif j == "}":
                    lista_corchetes.append(-1)
                elif cor:
                    val +=j
    lst = val.strip().split()

    if ";" in lst:
        return False

    return process_tokens(lst,estado,proc_in_process)
def funct_repeat(tokens, estado):
    if tokens[0] != "repeat":

        return False
    try:
        n = int(tokens[1]) 
    except ValueError:
        return False
    if tokens[2] != "times":

        return False
    block_inside = ""
    for i in range(3,len(tokens)):
        for j in tokens[i]:
            if j != "{" and j != "}":
                block_inside += j
            elif j == "{":
                lista_corchetes.append(1)
            elif j == "}":
                lista_corchetes.append(-1)

    return verify_simple_command(block_inside)

def found_proc(tokens,estado):

    name = tokens[0].split("(")
    val = "" 
    hs = False

    for l in procedures.keys():

        if l in name[0]:
            hs = True
    if hs:
  

        el_par = False
        for i in tokens:

            if name[0] in i:

                i = i.replace(name[0],"")

            for j in i:
                if j == "(":
                    el_par = True
                elif j == ")":
                    pass
                elif el_par:
                    val +=j
    else:
        return False

    lst = val.split(",")

    if len(lst) != procedures[name[0]]:
        return False
    else:
        return True 
            
print(upload_txt("a.txt"))