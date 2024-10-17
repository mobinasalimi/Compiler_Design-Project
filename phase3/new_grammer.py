ss = []
data_block_base = 762
data_block_memory = []
symbol_table = {}
Program_block = []
break_check_stack = []
scope_stack = [ ]
global_sb = {}
is_while = True
loop_stack = []
current_sb = []
temp_base = 1500
temp_current_index = -4
data_size = 4
top_sp = 750
STACK_PLACE =  6000
fsp = 3000
we_have_aregs = False
print_stack = []
args_stack = []
help_stack =[]
runtime_stack = []
temp_id_stacks = {}
start_of_new_statement = 0



def get_temp_index():
        global temp_current_index
        temp_current_index = 4 + temp_current_index
        return temp_current_index + temp_base




class AR( ) :
    def __init__(self, return_value, arguments , return_address) -> None:
        self.return_value = return_value
        self.arguments = arguments
        self.return_addres = return_address
        

class RuntimeStack() :
    def __init__(self) -> None:
        self.stack =[]
        self.base_pointer = 5000




class Data :
    def __init__(self, lexeme, type , memory_address , size=4 , array_size = 1 , args = None) -> None:
        self.lexeme = lexeme
        self.type = type
        self.memory_address = memory_address
        self.size = size
        self.array_size = array_size
        self.value = 0
        self.args = []


    def set_args(self, args) :
        self.args = args
    



def get_data_memory_current_index ( ) :
    return (len(data_block_memory) - 1 ) * 4 + data_block_base

def current_scope() :
    if ( len(scope_stack) == 0) :
         return 0
    return scope_stack[-1]




def get_index_from_data_block (address) :
     if ('@' in address) :
          address = ( int(address[1:])  - data_block_base) // 4 
          return address
     elif ('#' not  in address) :
          address =  ( int(address[1:])  - data_block_base) // 4 
          return address
    

def get_data_block_memory(address , line_number = 1) :
     print(address)
     if ('@' in str(address) ) :
          t = address
          address = ( int(address[1:])  - data_block_base) // 4 
          print("ahhhhhh", address , len( data_block_memory)  )

          if ( address >= len( data_block_memory) ) :
               print( line_number)

            #    if  (f'{t}_{len(runtime_stack)}'  in temp_id_stacks and temp_id_stacks[f'{t}_{len(runtime_stack)}'] !=None ) :
            #      return temp_id_stacks[f'{t}_{len(runtime_stack)}'].type
            #    else :
               return "temp_int"
          
          if ( address < 0) :
            return 'nuh'

          address =  data_block_memory[address].memory_address
          address = ( address - data_block_base ) // 4

          print("$$ ",  data_block_memory[address].lexeme)

          return data_block_memory[address].type
     elif ('#' not  in str(address)) :
          t = address
          address =  ( int(address)  - data_block_base) // 4 

          if ( address >= len( data_block_memory) ) :
            #    if  (f'{t}_{len(runtime_stack)}'  in temp_id_stacks  and temp_id_stacks[f'{t}_{len(runtime_stack)}'] !=None ) :
            #      return temp_id_stacks[f'{t}_{len(runtime_stack)}'].type
            #    else :
                    return "temp_int"
          
          if ( address <  0 ) :
            return 'nuh'

          return data_block_memory[address].type
          
          
              
     


          
     
    
def search_data_in_sb(sb,name) :
    datas = []
    # print(name)
    for data in sb[::-1] :
        datas.append(data.lexeme)
        if data.lexeme == name :
            return data
        
    # print(datas)
    return None


def check_data_is_global(name) :
    if name in global_sb :
        return global_sb[name]
    else : return None





#### added by mobina


semantic_errors = []
def error_handle(action, datas , line_number) :
    if action == 'DEC_VARIABLE'   or action == 'DEC_POINT' or action == 'DEC_ARR' :
        name,type = datas[0], datas[1]
        if (type == 'void') :
            semantic_errors.append(f"#{line_number} : Semantic Error! Illegal type of void for '{name}'.")
        else : return True
    if action == 'DEC_FUNC' :
        if (datas in symbol_table.keys() and datas!= 'main'):
            # semantic_errors.append(f"#{line_number} : ")
            return False
        else : return True
    if action == 'BREAK' :
        print("break_check_stack",break_check_stack)
        if(not break_check_stack) :
            print("Semantic Error! No 'while' found for 'break'.")
            semantic_errors.append(f"#{line_number} : Semantic Error! No 'while' found for 'break'.")
            return False
        else : return True
    if action == 'PID' :
        name = datas
        print(scope_stack)
        print('name for error: ' , name)
        if name in global_sb.keys() :
             return True
             
        if len(scope_stack) == 0 :
            data_in_gloabl = check_data_is_global(name)
            if data_in_gloabl is None :
                semantic_errors.append(f"#{line_number} : Semantic Error! '{name}' is not defined.")
                a = ss.pop()
                ADD_OR_SUB = ss.pop()
                b = ss.pop()
                return False
            else : return True
        else :
            current_sb = symbol_table[current_scope()]
            data_in_current_symbol_table = search_data_in_sb(current_sb , name)
            if data_in_current_symbol_table is None :
                semantic_errors.append(f"#{line_number} : Semantic Error! '{name}' is not defined.")
                return False
            else : return True

    if action == 'ADD_SUB':
        a , b = datas[0] , datas[1]
        if ( a == -1 or b == -1 ) :
            return False
        a_is_int , b_is_int = False , False
        print('hiiiiii',a ,b , len(data_block_memory) )

        if '#' in str(a) :
            a_is_int = True
        elif ('int' in get_data_block_memory(a , line_number) and  'arr' not in get_data_block_memory(a , line_number) ) :
            a_is_int = True
        else :
            a_is_int = False

        if '#' in str(b) :
            b_is_int = True
        elif ('int' in get_data_block_memory(b , line_number) and  'arr' not in get_data_block_memory(b , line_number) ) :
            b_is_int = True
        else :
            b_is_int = False
            
        if a_is_int and b_is_int :
            return True
        else : 
            if a_is_int == True:
                a_type = 'int'
            else:
                a_type = 'array'

            if b_is_int == True:
                b_type = 'int'
            else:
                b_type = 'array'

            semantic_errors.append(f"#{line_number} : Semantic Error! Type mismatch in operands, Got {a_type} instead of {b_type}.")
            return False
        

    if action == 'MULT':
        a , b = datas[0] , datas[1]
        a_is_int , b_is_int = False , False
        a , b = datas[0] , datas[1]
        if ( a == -1 or b == -1 ) :
            return False

        if '#' in str(a) :
             a_is_int = True
        elif ('int' in get_data_block_memory(a , line_number) and  'arr' not in get_data_block_memory(a , line_number) ) :
             a_is_int = True
        else :
             a_is_int = False

        if '#' in str(b) :
             b_is_int = True
        elif ('int' in get_data_block_memory(b , line_number) and  'arr' not in get_data_block_memory(b , line_number) ) :
             b_is_int = True
        else :
             b_is_int = False
        
        if a_is_int and b_is_int :
             return True
        else : 
            if a_is_int == True:
                a_type = 'int'
            else:
                a_type = 'array'

            if b_is_int == True:
                b_type = 'int'
            else:
                b_type = 'array'

            semantic_errors.append(f"#{line_number} : Semantic Error! Type mismatch in operands, Got {a_type} instead of {b_type}.")
            return False
        
    if action == 'COMPARE' :
        a , b = datas[0] , datas[1]
        a_is_int , b_is_int = False , False
        print("classical",get_data_block_memory(a) , a , get_data_block_memory(b) , b)

        a , b = datas[0] , datas[1]


        if ( a == -1 or b == -1 ) :
            return False

        if '#' in str(a) :
             a_is_int = True
        elif ('int' in get_data_block_memory(a ,line_number) and  'arr' not in get_data_block_memory(a , line_number) ) :
             a_is_int = True
        else :
             a_is_int = False

        if '#' in str(b) :
             b_is_int = True
        elif ('int' in get_data_block_memory(b , line_number) and  'arr' not in get_data_block_memory(b , line_number) ) :
             b_is_int = True
        else :
             b_is_int = False
        
        if a_is_int and b_is_int :
             return True
        else : 
            if a_is_int == True:
                a_type = 'int'
            else:
                a_type = 'array'

            if b_is_int == True:
                b_type = 'int'
            else:
                b_type = 'array'
            semantic_errors.append(f"#{line_number} : Semantic Error! Type mismatch in operands, Got {a_type} instead of {b_type}.")
            return False
        
    if action == 'ASSIGN' :
        
        a , b = datas[0] , datas[1]
        a_is_int , b_is_int = False , False
        print("classy",a , b)
        a , b = datas[0] , datas[1]


        print("arrrrr", a , b , line_number)


        if ( a == -1 or b == -1 ) :
            return False
        

        if '#' in str(a) :
             a_is_int = True
        elif ('int' in get_data_block_memory(a , line_number) and  'arr' not in get_data_block_memory(a  , line_number) ) :
             a_is_int = True
        else :
             a_is_int = False

        if '#' in str(b) :
             b_is_int = True
        elif ('int' in get_data_block_memory(b , line_number) and  'arr' not in get_data_block_memory(b , line_number) ) :
             b_is_int = True
        else :
             b_is_int = False
        
        if a_is_int and b_is_int :
             return True
        else : 
            if a_is_int == True:
                a_type = 'int'
            else:
                a_type = 'array'

            if b_is_int == True:
                b_type = 'int'
            else:
                b_type = 'array'




            semantic_errors.append(f"#{line_number} : Semantic Error! Type mismatch in operands, Got {a_type} instead of {b_type}.")

            return False         





def get_ofs(data1, data2 ) :
    # print("mommy ", data1.lexeme , data2.lexeme  )
    return data1.memory_address - data2.memory_address  + 8
    



def  PID(token, line_number):
        # print('pid',token , ss)
        if ( 'main' in symbol_table ) :
             print("dib")
        adr = 0 
        name = token
        offset = 0
        address = 0
        is_global_or_main = False
        if name != 'output':
            # print('kharrrrrr ', name, global_sb.keys())
            if error_handle('PID', name , line_number) :
                if (len(scope_stack) > 0 ) :
                    cs = current_scope()
                    current_symbol_table = symbol_table[cs]
                    data = search_data_in_sb(current_symbol_table , name )
                    if ( data != None):
                        # print(data , name)
                        data1 = current_symbol_table[1]
                        offset = get_ofs(data , data1)
                        
                        if ( data1.lexeme == 'main' ) :
                            is_global_or_main = True
  
                if current_scope() == 'main' :
                    for d in symbol_table[current_scope()] :
                        if d.lexeme == name :
                            is_global_or_main = True
                
                if (name in global_sb) :
                    is_global_or_main = True
                
                if is_global_or_main :
                    # print(name)
                    if name in global_sb and  search_data_in_sb(symbol_table['main'] , name) == None:
                         ss.append(global_sb[name].memory_address)
                        #  print("**" , ss)
                    else :
                        address = search_data_in_sb(symbol_table['main'] , name).memory_address 
                        ss.append(address)
                        # print('$$' , ss , is_global_or_main , name )

                if not is_global_or_main  :
                    address = get_temp_index()
                    print("gooz", ('ADD', top_sp, f'#{offset}', address) , token)
                    Program_block.append(('ADD', top_sp, f'#{offset}', address))
                    ss.append(f'@{address}')
                    help_stack.append(token)
                    temp_id_stacks[f'@{address}_{len(runtime_stack)}'] = data


                    
                
                # print("nastaran ", token, ss  )
                # print([ (d.memory_address , d.type , d.lexeme) for d in symbol_table[current_scope()]])
            else : 
                    ss.append(-1)
        
        else:
            ss.append('OUTPUT')
            print_stack.append('print')
            
                
                    





def SAVE(token , line_number):
    if ( len(Program_block) ==0) :
        #taghir
        Program_block.append(('ASSIGN', f'#{STACK_PLACE}' ,fsp ,  None))
        Program_block.append(('ASSIGN',  f'#{top_sp + 4}' , top_sp ,   None))
        Program_block.append(('ASSIGN', '#50000', str(data_block_base - 4) , None))
        Program_block.append(('ASSIGN', '#50000', str(STACK_PLACE - 4) , None))
        #taghir
        Program_block.append('EMPTY')
        symbol_table['main'] = []
    if(token=='+'):
        token = 'ADD'
    if(token == '-'):
        token = 'SUB'
    if token == '<':
            token = 'LT'
    elif token == '==':
            token = 'EQ'

    ss.append(token)




def DEC_VARIABLE(line_number) :
    name = ss.pop()
    type = ss.pop()
    if error_handle('DEC_VARIABLE' ,[name, type] , line_number) :
        data_memory_index = get_data_memory_current_index() + data_size 
        data = Data(lexeme = name ,type = type , memory_address = data_memory_index)
        # added to memory
        data_block_memory.append(data)
        # added to symbol table 
        if ( current_scope() == 0 ) :
             global_sb[name] = data
            #  symbol_table['0'].append(data)
        else : 
            symbol_table[current_scope()].append(data)


        
            
def DEC_ARRAY(line_number) :
    # print("befor dec array", ss)
    # print(Program_block)
    # for d in Program_block :
    #     print(d)
    global data_memory_index
    print("size is fucking cool ", ss)
        
    size = ss.pop()
    array_name = ss.pop()
    data_memory_index = get_data_memory_current_index() 
    # data = Data(lexeme=array_name , type='arr', memory_address=data_memory_index , array_size=size)
    # data_block_memory.append(data)
    if not error_handle('DEC_ARR' ,[array_name, type] , line_number) :
         return
         
         

    for i in range(int(size) ) :
        # data_memory_index +=data_size
             
        data = Data(lexeme=array_name, type='arr_int_val',memory_address= get_data_memory_current_index() + 4 ,  array_size = size )
        if ( i == 0) :
              if ( current_scope() != 0 ) :
                symbol_table[current_scope()].append(data)
              else :
                   global_sb[data.lexeme] = data
                   
             
        data_block_memory.append(data)
    
    # for i in range(len(data_block_memory)) :
    #      print("kill me ", data_block_memory[i].lexeme , data_block_memory[i].memory_address , data_block_memory[i].type )



  

def DEC_FUNCTION(line_number) :

    func_name = ss.pop()
    return_type = ss.pop()
    scope_stack.append(func_name)
    if (func_name == 'main') :
        # Program_block[0](('ASSIGN', '#10000', str(data_block_base - 4) , None))
        # Program_block[1](('ASSIGN', '#10000', str(STACK_PLACE - 4) , None))
        # Program_block[2](('ASSIGN', f'#{STACK_PLACE}' ,fsp ,  None))
        # Program_block[3](('ASSIGN',  f'#{top_sp + 4}' , top_sp ,   None))


        current_pb_index = len(Program_block)
        Program_block[4]  =  ('JP' , str(current_pb_index) ,None , None ) 

    data = Data(lexeme=func_name , type = 'func_'+ return_type, memory_address= len(Program_block) )
    # ?

    
    
    if error_handle( 'DEC_FUNC', func_name , line_number):
        global_sb[func_name] = data
        symbol_table[func_name] = []
        symbol_table[func_name].append(data)
        ss.append(func_name)







def SAVE_ARGS(line_number) :
    # print( "khaste shodam ", ss)
    func_name = ss.pop()
    # print()
    if ( current_scope()!= func_name ) :
         scope_stack.pop()
         scope_stack.append(func_name)
         
    args = symbol_table[func_name][1:]
    symbol_table[func_name][0].set_args(args)


def END_FUNCTION(line_number):
        scope_stack.pop()
        # self.current_symbol_table = self.global_symbol_table
        RETURN_VOID(line_number)




def DEC_ARRAY_POINTER( line_number) :
    array_name = ss.pop()
    type = ss.pop()

    if not error_handle('DEC_POINT' ,[array_name, type] , line_number) :
         return
         
    if error_handle('DEC_VARIABLE' ,[array_name, type] , line_number) :
        data_memory_index = get_data_memory_current_index() + data_size
        data = Data(lexeme=array_name, type='arr',memory_address=data_memory_index)
        data_block_memory.append(data)
        # data = search_data_in_sb( symbol_table[current_scope()] ,array_name )
        symbol_table[current_scope()].append(data)

    



def BREAK(line_number) :
    # check = error_handle('BREAK', is_while)
    # if check :
    q = 0
    if error_handle('BREAK', q , line_number):
        print("added break")
        loop_stack.append(len(Program_block))
        Program_block.append('EMPTY')
        


def SAVE_IF (line_number) :
    # print("ss", ss)
    ss.append(len(Program_block))

    Program_block.append('EMPTY')


def JPF_SAVE_IF(line_number) :
    print(ss)
    while len(ss)> 0 and (type(ss[-1]) == str or ss[-1] >= data_block_base ):
            ss.pop()
    # print(ss)
    index = ss.pop()
    expression  = ss.pop()
    to_jump = len(Program_block) + 1
    # print('marg',index)
    if Program_block[index] == 'EMPTY' :
        Program_block[index] =  ('JPF' ,  str(expression) ,  to_jump , None )
        ss.append( len(Program_block))
        # print("padarsag", len(Program_block) )
        Program_block.append('EMPTY')

    else : print('ERROR')

def JP_IF(line_number ) :
    while type(ss[-1]) == str or ss[-1] >= data_block_base:
            ss.pop()

    print(ss)
    index = ss.pop()
    print(index)
    jump_to = len(Program_block)
    if Program_block[index]== 'EMPTY' :
        Program_block[index] = ( 'JP', str(jump_to) , None , None)

    
def LABEL(line_number) :

    ss.append(len(Program_block))
    break_check_stack.append("label")

def SAVE_WHILE(line_number):
    ss.append(len(Program_block))
    Program_block.append('EMPTY')
    


def WHILE(line_number) :
    # print(ss)

    while type( len(ss)>=0 and  ss[-1]) == str or ss[-1] >= data_block_base:
            ss.pop()
    
    # print(ss)
    cond_index = ss.pop()
    expression  = ss.pop()
    to_jump = len(Program_block) + 1
    
    print("bad while " , "cond_index", cond_index , "expression" , expression , "to_jump" ,to_jump, len(Program_block) )
    # for I , d in enumerate(Program_block) :
    #         print(I , d)
    # print(Program_block)
    if Program_block[cond_index] == 'EMPTY' :

        print( "cry ",ss , ('JPF' ,  str(expression) , to_jump , None ) , "index :",  cond_index )
        Program_block[cond_index] =  ('JPF' ,  str(expression) , to_jump , None )

    else :
         print('error')
         return
    

    # while type(ss[-1]) == str or ss[-1] >= data_block_base:
    #         ss.pop()
    break_check_stack.pop()
    unconditional_jump  = ss.pop()
    # print("just check ", ( 'JP', unconditional_jump ,None , None) , len(Program_block) )
    Program_block.append(( 'JP', unconditional_jump ,None , None))

    to_jump_when_break = len(Program_block)

    # print("shit happens", loop_stack)

    if(len(loop_stack)>0 ) :
         print("added the break")
         break_index = loop_stack.pop()
         if (Program_block[break_index] != 'EMPTY') :
              print('error')
         else :
              print(('JP', to_jump_when_break , None , None))
              Program_block[break_index] = ( ('JP', to_jump_when_break , None , None))
              




def RETURN_VALUE(line_number):
        # print("len :", len(Program_block))
        # print("GA ", ss)
        return_value = ss.pop()
        temp = get_temp_index()
        Program_block.append(('ASSIGN', f'@{top_sp}', temp, None))
        Program_block.append(('ASSIGN', return_value, f'@{temp}', None))

        temp = get_temp_index()

        Program_block.append(('ADD', top_sp, f'#{data_size}', temp))

        Program_block.append(('SUB', fsp, f'#{data_size}', fsp))
        Program_block.append(('ASSIGN', f'@{fsp}', top_sp, None))

        Program_block.append(('ASSIGN', f'@{temp}', temp, None))
        Program_block.append(('JP', f'@{temp}', None, None))
      


def RETURN_VOID(line_number):
        temp = get_temp_index()

        Program_block.append(('ADD', top_sp, f'#{data_size}', temp))

        Program_block.append(('SUB', fsp, f'#{data_size}', fsp))
        Program_block.append(('ASSIGN', f'@{fsp}', top_sp, None))

        Program_block.append(('ASSIGN', f'@{temp}', temp, None))
        Program_block.append(('JP', f'@{temp}', None, None))



def ASSIGN(line_number) :
    a = ss.pop()
    if ( error_handle('ASSIGN' , [ ss[-1], a], line_number)) :
        Program_block.append( ('ASSIGN', str(a), str(ss[-1]) , None ))
    # print("daddy 4 = ", str(ss[-1]))
    


def att_array(b ,size):
    t1 = get_temp_index()
    base_t = get_temp_index()
    # print("heeeey" , ('ASSIGN', b , base_t , None ) )
    Program_block.append(('ASSIGN', b , base_t , None ))
    Program_block.append(('ADD', base_t , size, t1 ))
    ss.append(f'@{t1}')
    temp_id_stacks[f'@{t1}_{len(runtime_stack)}'] = Data(lexeme='?', type='int' , memory_address='1000')

    


def const_array(b ,size):
    t1 = get_temp_index()
    Program_block.append(('ADD', f'#{b}' , size, t1 ))
    ss.append(f'@{t1}')
    temp_id_stacks[f'@{t1}_{len(runtime_stack)}'] = Data(lexeme='?', type='int' , memory_address='1000')


def cal_array_size(ofs):
    temp_size  = get_temp_index()
    Program_block.append(('MULT', '#4', ofs, temp_size))
    return temp_size






def ARR_ADDR(line_number) :
    # print(ss)
    ofs = ss.pop()
    b = ss.pop()
    # print("mobina", b)
    temp_size =  cal_array_size(ofs)
    if ('@' not in str(b) ) :
        const_array(b , temp_size )
    else :
         att_array(b , temp_size)





def ADD_SUB( line_number) :
    # t = a + b
    with open('output.txt', 'w') as file:
        for index, instruction in enumerate(Program_block):
            # Format the instruction with appropriate placeholders for None values
            formatted_instruction = ', '.join(str(item) if item is not None else '' for item in instruction)
            # Write the formatted instruction to the file
            file.write(f'{index}\t({formatted_instruction})\n')
    print("hi ",ss)
    a = ss.pop()
    ADD_OR_SUB  = ss.pop()
    b = ss.pop()
    print("samaneeee",a , b)
    t = get_temp_index()



        
    if error_handle('ADD_SUB',[a,b], line_number):
        Program_block.append( (ADD_OR_SUB , b , a , t ))
    else :
         print("heyyyyyyyyyy")
    print('saggg', ss)
    ss.append(t)
    temp_id_stacks[f'{t}_{len(runtime_stack)}'] = Data(lexeme='?', type='int' , memory_address='1000')
    print("bitch", ss)
 


def MULT (line_number ) :
    # print(ss)
    a = ss.pop()
    b = ss.pop()
    t =  get_temp_index()
    if error_handle('MULT' , [a , b] ,line_number) :
        Program_block.append( ('MULT' , a , b , t ))
    ss.append(t)
    temp_id_stacks[f'{t}_{len(runtime_stack)}'] = Data(lexeme='?', type='int' , memory_address='1000')





def SAVE_RELOP_RESULT(line_number):
        # print("ss :", ss)
        a = ss.pop()
        compare  = ss.pop()
        b = ss.pop()
        t = get_temp_index()

        if error_handle('COMPARE' , [a , b] , line_number):
            Program_block.append( (compare , b , a , t ))
        ss.append(t)
        temp_id_stacks[f'{t}_{len(runtime_stack)}'] = Data(lexeme='?', type='int' , memory_address='1000')





def SAVE_CONST(token,line_number):
        ss.append('#' + token)



def NEG(line_number) :
    expression_address = ss.pop()
    t = get_temp_index()
    Program_block.append(('SUB','#0',expression_address, t))
    ss.append(t)
    temp_id_stacks[f'{t}_{len(runtime_stack)}'] = Data(lexeme='?', type='int' , memory_address='1000')




def ARGS(line_number):
        
        # if (datas in symbol_table.keys() and datas!= 'main'):
        #     semantic_errors.append(f"#{line_number} : ")
        if ( ( not print_stack ) and  (ss[-1] != 'OUTPUT') ):
             ss.append("args_func")
             args_stack.append('args_func')
        



def CHECK_OUTPUT(line_number):
        # print("lovely ", [(d.lexeme , d.memory_address ) for d in symbol_table[current_scope()]])
        print("hey hey hey ", ss)
        if (len(ss) >= 2) :
            if (( print_stack ) and (ss[len(ss)-2] == 'OUTPUT')) :
                    # print('to print ! ',ss)
                    to_print_add = ss.pop()
                    Program_block.append(('PRINT',to_print_add , None , None) )
                    # print('added')
                    
                    ss.pop()
                    print_stack.pop()
                    print('mew', ss)
                    

            

def check_is_print(args):
    #  print('args', args)

     if (  len(ss)>0 and ( len(print_stack) > 0  or ss[-1] == 'OUTPUT')) :
          if not args:
               print('error')
               return False
          else :
               return True
          
     return False
          


def search_for_func(address) :
     for name in global_sb :
          if ( global_sb[name].memory_address == address ):
               return  global_sb[name]
     return None


     

def get_offset_func(current_sb) :
     print( "current_sb :", current_sb[0].lexeme )
    #  for i ,  d in enumerate(Program_block) :
    #     print(i , d)

     
    #  with open('output.txt', 'w') as file:
    #         for index, instruction in enumerate(Program_block):
    #             # Format the instruction with appropriate placeholders for None values
    #             formatted_instruction = ', '.join(str(item) if item is not None else '' for item in instruction)
    #             # Write the formatted instruction to the file
    #             file.write(f'{index}\t({formatted_instruction})\n')
     x = current_sb[-1].memory_address - current_sb[1].memory_address + 12
     return x




def GET_FF(size) :
            ff = -1
            index = 0
            for name  in global_sb:
                if 'func' in global_sb[name].type :
                    ff = index - 1
                    break
                index += 1

            # ff = max(ff, 0)
            type  = global_sb[list(global_sb.keys())[ff]].type
            memory_address = global_sb[list(global_sb.keys())[ff]].memory_address
            arr_size = global_sb[list(global_sb.keys())[ff]].array_size
            firs_address = global_sb[list(global_sb.keys())[0]].memory_address

            if 'arr' in type or arr_size >1  :
                 memory_address = 4 * arr_size + memory_address
            return size + memory_address -  firs_address
            
     



def att_arg(argument , t) :
        temp = get_temp_index()
        Program_block.append(('ASSIGN', argument, temp, None))
        Program_block.append(('ASSIGN',temp, f'@{t}', None)) 



def pass_args(arguments, called_function, start , line_number) :
     func_args = called_function.args
     print("func_args" , func_args[0].lexeme)
     print(current_scope())
     if len(arguments) != len(func_args) :
            semantic_errors.append(f"#{line_number} : Semantic Error! Mismatch in numbers of arguments of '{called_function.lexeme}'.")
            return
     
     print("cill arguments",  arguments , line_number)
     for i, arg in enumerate(arguments) :
         ##### added by mobina for semantic errors
            formal_arg_type = func_args[i].type

            a , b = arg , formal_arg_type
            
            a_is_int , b_is_int = False , False

            if '#' in str(a) :
                    a_is_int = True
            elif ('int' in get_data_block_memory(a) and  'arr' not in get_data_block_memory(a) ) :
                    a_is_int = True
            else :
                    a_is_int = False

            if ('int' in b and 'arr' not in b):
                 b_is_int = True

            if a_is_int == True:
                a_type = 'int'
            else:
                a_type = 'array'

            if b_is_int == True:
                    b_type = 'int'
            else:
                    b_type = 'array'

           

            if a_type != b_type and len(func_args) == len(arguments):
                semantic_errors.append(f"#{line_number} : Semantic Error! Mismatch in type of argument {i+1} of '{called_function.lexeme}'. Expected '{formal_arg_type}' but got '{a_type}' instead.")

            arg = func_args[i]
            name = arg.lexeme
            # if ( runtime_stack)
            t = get_temp_index() 
            offset = 0
            data = None

            if (len(scope_stack) > 0 ) :
                        # cs = current_scope()
                        # current_symbol_table = symbol_table[cs]
                        # data = search_data_in_sb(current_symbol_table , name )
                        # if ( data != None):
                        #     # print(data , name)
                        #     data1 = current_symbol_table[1]
                        #     offset = get_ofs(data , data1)
                            
                        #     if ( data1.lexeme == 'main' ) :
                        #         is_global_or_main = True

                        current_s = current_scope()
                        current_symbol_table = symbol_table[called_function.lexeme]
                        # print( [d.lexeme for d in current_symbol_table])
                        data = search_data_in_sb(current_symbol_table , name )
                        
                        if ( data != None):
                            print('find the data ', data.lexeme, ' or ', name , 'in ' , called_function.lexeme )
                            data1 = current_symbol_table[1]
                            offset = get_ofs(data , data1)
                        else :
                            print("error in pass args" ,name , called_function.lexeme )
                            x = []
                            for d in current_symbol_table :
                                x.append(d.lexeme)
                            #  print(x)

            if ( data == None) :
                print('error')
                return
            # print( "daddy ", ('ADD', start , '#' + str(offset) , t ) )
            Program_block.append( ('ADD', start , '#' + str(offset) , t ) )
            if 'arr' not in data.type:
                Program_block.append( ('ASSIGN',arguments[i], f'@{t}', None))
                
            else :
                if ( '@'  in str(arguments[i]) ) :
                    att_arg(arguments[i])
                else :
                    Program_block.append ( ( 'ASSIGN',f'#{arguments[i]}', f'@{t}', None))

   
        


def jump_and_return( size , start_of_function_call_instructions , called_function ) :
        #taghir 

        print(('daddy 2', top_sp, f'#{size}', top_sp))
        temp3 = get_temp_index()
        Program_block.append(('ASSIGN', top_sp , temp3))
        Program_block.append(('ADD', temp3 ,f'#{size}' , temp3 ))

        temp = get_temp_index()
        Program_block.append(('ADD', temp3 ,'#4', temp ))

        Program_block.append(('ASSIGN', temp3, top_sp , ))
        #taghir

        Program_block.append(('ASSIGN', f'#{len(Program_block)+ 3}', f'@{temp}', None))

        return_value_temp = get_temp_index()
        Program_block.append(('ASSIGN', f'#{return_value_temp}', f'@{top_sp}', None))

        # print("not sure", ('JP', called_function.memory_address, None, None) )

        Program_block.append(('JP', called_function.memory_address, None, None))

        # print("call_stack befor ", [d[0].lexeme for d in runtime_stack] , "current", current_scope() )
        # print(scope_stack)
        # print([d[0].lexeme for d in runtime_stack])
        scope_stack.pop()
        symbol_table[current_scope()] = runtime_stack.pop()

        # print("call_stack after ", [d[0].lexeme for d in runtime_stack] , "current", current_scope() )

        # print("fairy tale",  start_of_new_statement, start_of_function_call_instructions - 1 )

        # for i in range( start_of_new_statement, start_of_function_call_instructions - 1):

        #     if ( 'PRINT' in  Program_block[i] ) :
        #         print("yes !",  Program_block[i] )
        #     Program_block.append(Program_block[i])

        return return_value_temp



def CALL_FUNC( func , size, arguments , line_number):
        func_name = func.lexeme
        current_sb =  symbol_table[current_scope()]
        func_sb = symbol_table[func_name]
        Program_block.append(('ASSIGN', top_sp, f'@{fsp}', None))
        Program_block.append(('ADD', '#4', str(fsp), str(fsp)))
        start_of_function_call_instructions = len(Program_block)
        runtime_stack.append(current_sb)
        scope_stack.append(func_name)
        start_index_of_ar = get_temp_index()



        # print('daddy 3 ', ('ADD', top_sp, '#' + str(size) , start_index_of_ar ) )
        # for d in Program_block :
        #     print(d)

        Program_block.append( ('ADD', top_sp, '#' + str(size) , start_index_of_ar ) )
        #arguments, called_function, start
        
        pass_args(arguments, func, start_index_of_ar , line_number )

        # size , start_of_function_call_instructions , called_function

        return_value = jump_and_return(  size , start_of_function_call_instructions , func)

        ss.append(return_value )
        print("kharrr", )
        # temp_id_stacks[f'{return_value}_{len(runtime_stack)}'] = Data(lexeme='?',type='return')
        # print("return value kiri", return_value)


def S():
    global start_of_new_statement
    start_of_new_statement = len(Program_block)



def CHECK_ARGS(line_number):
        
        if 'args_func' not in ss:
            print("groot", ss)
            return
        arguments = []


        while  len(args_stack) > 0 and ss[-1] !='args_func':
            arg = ss.pop()
            arguments.append(arg)

        ss.pop()

        if (check_is_print (arguments)) :
             print("hush")
             ss.append(arguments[-1])
             return
        else :
            size = 8
            arguments  = arguments[::-1]
            func_mem_add = ss.pop()
            func = search_for_func(func_mem_add)

            if current_scope() in symbol_table and len(symbol_table[current_scope()]) > 1 :

                    print("current_scope() : ", current_scope())
                    current_sb = symbol_table[current_scope()]
                    print("current_sb[1].memory_address" , current_sb[-1].memory_address )
                    size = get_offset_func(current_sb)
            
            if  current_scope() == 'main':
                 size = GET_FF(size)


        if ( func == None):
             print('error in check_args')
             return 
        
        CALL_FUNC(func , size, arguments , line_number)
        print("a ss in check args", ss)

        

def CHECK_ARGS_S() :
      CHECK_ARGS()
      S()
     





    

left = 'left'
right = 'right'
null = None

grammar_rules =  [
  { left: 'Program', right: ['DeclarationList'] },
  { left: 'DeclarationList', right: ['Declaration', 'DeclarationList'] },
  { left: 'DeclarationList', right: ['epsilon'] },
  { left: 'Declaration', right: ['DeclarationInitial', 'DeclarationPrime'] },
  { left: 'DeclarationInitial', right: ['@SAVE','TypeSpecifier', '@SAVE', 'ID'] },
  { left: 'DeclarationPrime', right: ['FunDeclarationPrime'] },
  { left: 'DeclarationPrime', right: ['VarDeclarationPrime'] },
  { left: 'VarDeclarationPrime', right: [';' , '@DEC_VARIABLE'] },
  { left: 'VarDeclarationPrime', right: ['[', '@SAVE','NUM', ']',';' ,'@DEC_ARRAY' ] },
  { left: 'FunDeclarationPrime', right: ['@DEC_FUNCTION','(', 'Params', ')','@SAVE_ARGS', 'CompoundStmt' , '@END_FUNCTION'] },
  { left: 'TypeSpecifier', right: ['int'] },
  { left: 'TypeSpecifier', right: ['void'] },
  { left: 'Params', right: ['@SAVE','int','@SAVE', 'ID', 'ParamPrime', 'ParamList'] },
  { left: 'Params', right: ['void'] },
  { left: 'ParamList', right: [',', 'Param', 'ParamList'] },
  { left: 'ParamList', right: ['epsilon'] },
  { left: 'Param', right: ['DeclarationInitial', 'ParamPrime'] },
  { left: 'ParamPrime', right: ['[', ']', '@DEC_ARRAY_POINTER'] },
  { left: 'ParamPrime', right: ['epsilon' , '@DEC_VARIABLE'] },
  { left: 'CompoundStmt', right: ['{','DeclarationList', 'StatementList', '}' ] },
  { left: 'StatementList', right: ['Statement', 'StatementList'] },
  { left: 'StatementList', right: ['epsilon'] },
  { left: 'Statement', right: ['ExpressionStmt' ] },
  { left: 'Statement', right: ['CompoundStmt'] },
  { left: 'Statement', right: ['SelectionStmt'] },
  { left: 'Statement', right: ['IterationStmt'] },
  { left: 'Statement', right: ['ReturnStmt'] },
  { left: 'ExpressionStmt', right: ['Expression',  ';' ] },
  { left: 'ExpressionStmt', right: ['break' , '@BREAK', ';'] },
  { left: 'ExpressionStmt', right: [';'] },
  { left: 'SelectionStmt', right: ['if', '(', 'Expression', ')' , '@SAVE_IF' , 'Statement', 'else','@JPF_SAVE_IF', 'Statement' ,'@JP_IF'] },
  { left: 'IterationStmt', right: ['while','@LABEL', '(', 'Expression', ')','@SAVE_WHILE', 'Statement', '@WHILE' ] },
  { left: 'ReturnStmt', right: ['return', 'ReturnStmtPrime' ] },
  { left: 'ReturnStmtPrime', right: [ '@RETURN_VOID', ';'] },
  { left: 'ReturnStmtPrime', right: ['Expression', '@RETURN_VALUE', ';' ] },
  { left: 'Expression', right: ['SimpleExpressionZegond'] },
  { left: 'Expression', right: ['@PID' ,'ID', 'B' , '@CHECK_OUTPUT'] },
  { left: 'B', right: ['=', 'Expression' , '@ASSIGN'] },
  { left: 'B', right: ['[', 'Expression', ']', '@ARR_ADDR' ,'H'] },
  { left: 'B', right: ['SimpleExpressionPrime'] },
  { left: 'H', right: ['=', 'Expression', '@ASSIGN'] },
  { left: 'H', right: ['G', 'D', 'C'] },
  { left: 'SimpleExpressionZegond', right: ['AdditiveExpressionZegond', 'C'] },
  { left: 'SimpleExpressionPrime', right: ['AdditiveExpressionPrime', 'C'] },
  { left: 'C', right: ['Relop', 'AdditiveExpression', '@SAVE_RELOP_RESULT'] },
  { left: 'C', right: ['epsilon'] },
  { left: 'Relop', right: [ '@SAVE', '<'] },
  { left: 'Relop', right: ['@SAVE' , '=='] },
  { left: 'AdditiveExpression', right: ['Term', 'D'] },
  { left: 'AdditiveExpressionPrime', right: ['TermPrime', 'D'] },
  { left: 'AdditiveExpressionZegond', right: ['TermZegond', 'D'] },
  { left: 'D', right: ['@SAVE' , 'Addop', 'Term','@ADD_SUB' ,'D'] },
  { left: 'D', right: ['epsilon'] },
  { left: 'Addop', right: ['+'] },
  { left: 'Addop', right: ['-'] },
  { left: 'Term', right: ['SignedFactor', 'G'] },
  { left: 'TermPrime', right: ['SignedFactorPrime', 'G'] },
  { left: 'TermZegond', right: ['SignedFactorZegond', 'G'] },
  { left: 'G', right: ['*', 'SignedFactor','@MULT', 'G'] },
  { left: 'G', right: ['epsilon'] },
  { left: 'Factor', right: ['(', 'Expression', ')'] },
  { left: 'Factor', right: ['@PID','ID', 'VarCallPrime'] },
  { left: 'Factor', right: ['@SAVE_CONST','NUM'] },
  { left: 'VarCallPrime', right: ['(', '@ARGS' , 'Args', ')','@CHECK_ARGS' ] },
  { left: 'VarCallPrime', right: ['VarPrime'] },
  { left: 'VarPrime', right: ['[', 'Expression', ']', '@ARR_ADDR'] },
  { left: 'VarPrime', right: ['epsilon'] },
  { left: 'FactorZegond', right: ['(', 'Expression', ')'] },
  { left: 'FactorZegond', right: ['@SAVE_CONST','NUM'] },
  { left: 'Args', right: ['ArgList'] },
  { left: 'Args', right: ['epsilon'] },
  { left: 'ArgList', right: ['Expression', 'ArgListPrime'] },
  { left: 'ArgListPrime', right: [',', 'Expression', 'ArgListPrime'] },
  { left: 'ArgListPrime', right: ['epsilon'] },
  { left: 'SignedFactor', right: ['+', 'Factor'] },
  { left: 'SignedFactor', right: ['-', 'Factor','@NEG'] },
  { left: 'SignedFactor', right: ['Factor'] },
  { left: 'SignedFactorPrime', right: ['FactorPrime'] },
  { left: 'FactorPrime', right: ['(', '@ARGS' ,'Args', ')', '@CHECK_ARGS'] },
  { left: 'FactorPrime', right: ['epsilon'] },
  { left: 'SignedFactorZegond', right: ['+', 'Factor'] },
  { left: 'SignedFactorZegond', right: ['-', 'Factor', '@NEG'] },
  { left: 'SignedFactorZegond', right: ['FactorZegond'] }
]
