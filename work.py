
defined_names = []
procedures = []
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
            line = line.strip()
            print(line)
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
    elif "name" == tokens[0]:
        return name_fun()
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
    elif tokens[0] in procedures:
        #falta
        pass
    elif "if" == tokens[0]:
        estado = funct_if(tokens,estado)
    elif "while" == tokens[0]:
        estado = funct_while(tokens,estado)
    elif "repeat" == tokens[0]:
        estado = funct_repeat(tokens,estado)
    else:
        estado = validate_command(tokens,estado)
    return estado

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
        procedures.append(procedure_name)
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
                defined_names.append(i)   
                lst_val_created.append(i)    
        else:
            estado = False     
    else:
        estado = False
    return estado
def validate_command(tokens,estado):
    for token in tokens:
        if token in defined_names:
            continue
        elif token.startswith('(') and token.endswith(')'):
            function_name = token[1:-1]
            if function_name not in defined_names:
                estado = False
        else:
            estado = False  
    return estado
def two_pos_function(tokens,estado,fn):
    #aun no esta acabada la funcion
    val = ""

    for i in tokens:
        if i == fn:
            continue
        elif fn in i:
            i = i.split("(")
            val += i[1]
        else:
            val += i

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

    for i in tokens:
        if i == "if":

            cual = "if"
            co =  cond_detection(tokens,estado)
        elif i == "else":
            cual = "else"
        
        for j in i:
            if j == "{":

                cond_block = True
                block = block_inside(tokens,estado,cual)

                if not(block):
                    return False
            elif j == "}":
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
def funct_while(tokens,estado):
    #TODO hacerla toda
    return estado
def funct_repeat(tokens,estado):
    #TODO hacerla toda
    return estado
def cond_detection(tokens,estado):

    #completar function
    i = 0
    el = tokens[i]

    while el != "{":
        if "can" in el:            
            return can_detection(tokens)
        else:
            estado = False
        i +=1
        el = tokens[i]
    return estado
def can_detection(lst):
    can_detect = False
    for i in range(1,len(lst)):
        if lst[i] == "{" or i == "}":
            break
        if lst[i] == "can":
            can_detect = True
            #toca revisar si esta bien que can este seprado de los parentesis
            continue
        elif "can" in lst[i]:
            can_detect = True

            new_lst = lst[i].split("(")
            lst = new_lst[1:len(new_lst)+1]
            #toca ver como selecciono lo que quiero   
            return verify_simple_command(lst) 
        else:
            return False

    if can_detect == False:
        return False
    else: 
        return True
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
    if c== "if":
        compare = 1
    elif c == "else":
        compare = 2
    for i in tokens:
        for j in i:
            if j == "{":
                bracket_o+=1
            elif j == "}":
                bracket_o = 0
                break
            elif bracket_o == compare:
                block_inside+= j
        if j == "}":
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

    
                
            
print(upload_txt("a.txt"))