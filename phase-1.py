import string
from collections import defaultdict


white_space = [' ' , '  ','\r','\n','\t','\f','\v']
keyword  = ['if', 'else', 'void', 'int', 'break', 'while', 'return']
see = ["(",")","{","}","[","]","+","-",",",":",";","<"]
digits = ["0","1","2","3","4","5","6","7","8","9"]
symbol  = ["(",")","{","}","[","]","+","-","*","=","/",",",":",";","<"]
lower_case_alphabet =  list("abcdefghijklmnopqrstuvwxyz")
upper_case_alphabet  = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
all_alphabets = lower_case_alphabet + upper_case_alphabet
excluded_symbols = [char for char in symbol if char not in ['/', '*']]
excluded_symbols_1= [char for char in symbol if char not in ['=']]
excluded_symbols_2= [char for char in symbol if char not in ['*']]
excluded_symbols_3= [char for char in symbol if char not in ['/']]
all_chars = set(string.printable)
ees= [char for char in all_chars if char !='*']


type_dict = { 'Digit' : digits , '^Digit': symbol + white_space + ['\x00'] ,  'SEE' :see , 'Alpha' : all_alphabets , 
         'alpha' : lower_case_alphabet , '^alpha' : upper_case_alphabet + digits + symbol + white_space + ['\x00'] ,
         'AlphaDigit' : all_alphabets + digits , '^AlphaDigit' : symbol + white_space + ['\x00'] , '^Alpha' : digits + symbol + white_space + ['\x00'],
           '^/*':  all_alphabets + digits + excluded_symbols + white_space + ['\x00'] , 
           '^/' : excluded_symbols_3 + all_alphabets + digits +white_space + ['\x00'] , 
           '^*/':  all_alphabets + digits + excluded_symbols + white_space + ['\x00'],
           '^=' : all_alphabets + digits + excluded_symbols_1 + white_space + ['\x00'] ,
           'Whitespace' : white_space , '^Whitespace' :  all_alphabets + symbol + digits + ['\x00'] ,
            '^*' :  all_alphabets + digits + excluded_symbols_2 + white_space + ['\x00'] ,
            'ees' : ees }


class DFA:
    def __init__(self):

        self.start_state = None
        self.accept_states = set()
        self.marked_accept_states = set()
        self.states_type = {}
        self.current_state = 0
        self.states = set()
        self.alphabet = set()
        self.transitions = {} 


    def add_state(self, state, is_start=False, is_accept=False , is_marked_accept = False):
        self.states.add(state)
        if is_start:
            self.start_state = state
            self.current_state = state
        if is_accept:
            self.accept_states.add(state)
        if is_marked_accept:
            self.marked_accept_states.add(state)


    def check_transition(self ,char) :
        types = []
        for type, val in type_dict.items() :
            if char in val :
                types.append(type)

        return types



    def process_input(self, char):
        possible_transitions = self.check_transition(char)
        current_transiton = None
                 
        for t in self.transitions[self.current_state] :
            if t in possible_transitions :
                current_transiton = t

        
        if char in self.transitions[self.current_state]:
            current_transiton  = char
        
        
        if not current_transiton :
           return False 
        

        self.current_state = self.transitions[self.current_state][current_transiton]

        return True


    def make_transition(self, src_state, input_symbol, dest_state):
        if src_state not in self.transitions:
            self.transitions[src_state] = {}
        self.transitions[src_state][input_symbol] = dest_state
        self.alphabet.add(input_symbol)


    def is_accept_state(self):
        if ( self.current_state in self.marked_accept_states) :
            return True, self.states_type[self.current_state]
        elif ( self.current_state in self.accept_states) :
            return False , self.states_type[self.current_state]
        else :
            return None, None






    def add_mini_dfa(self, token_type , mini_dfa_transitions, start_offset):
        """
        Adds a mini DFA to the current DFA.
        :param mini_dfa_transitions: A dictionary representing the transitions of the mini DFA.
        :param start_offset: The starting offset for the state IDs in the mini DFA.
        """
        for src, transitions in mini_dfa_transitions.items():
            last_offset = 0 
            if ( src == 0 ) :
                src_state = 0
            else :
                src_state = start_offset + src
                self.add_state(src_state)
                self.states_type[src_state] = token_type
            
            for input_symbol, dest in transitions.items():
                if isinstance(dest, tuple):
                    dest_state, is_accept, is_marked_accept = dest
                    self.add_state(start_offset + dest_state, is_accept=is_accept, is_marked_accept=is_marked_accept)
                    self.states_type[start_offset + dest_state] = token_type
                else:
                    dest_state = dest

                self.make_transition(src_state, input_symbol, start_offset + dest_state)
                last_offset = start_offset + dest_state
                
        return last_offset


# NUM states and transitions:
# number of nodes = 3 
# 0 - Digit -> 1
# 1 - Digit -> 1
# 1 - ^Digit -> 2*a

# ID states and transitions:
# number of nodes = 3 
# 0 - Alpha -> 1
# 1 - AlphaDigit -> 1
# 1 - ^AlphaDigit -> 2*a

# KEYWORD states and transitions:
# number of nodes = 3 
# 0 - Alpha -> 1
# 1 - alpha -> 1
# 1 - ^Alpha -> 2*a

# SYMBOL states and transitions:
# number of nodes = 3 
# 0 - = -> 1
# 1 - = -> 2a
# 1 - ^= -> 3*a
# 0 - SEE -> 4a
# 0 - / -> 5
# 5 - ^/* -> 6a

# WHITESPACE states and transitions:
#number of nodes = 3
# 0 - Whitespace -> 1
# 1 - Whitespace -> 1
# 1 - ^Whitespace -> 2*a

#COMMENT states and transitions:
#number of nodes = 3
# 0 - / -> 1
# 1 - * -> 2
# 2 - * -> 3
# 2 - ^* -> 2
# 3 - ^*/ -> 2
# 3 - * -> 3
# 3 - / -> 4a


def add_token_states(dfa):

        num_dfa = {
            0: {'Digit': 1},
            1: {'Digit': 1, '^Digit': (2, False, True)}
        }

        id_dfa = {
            0: {'Alpha': 1},
            1: {'AlphaDigit': 1, '^AlphaDigit': (2, False, True)}
        }

        keyword_dfa = {
            0: {'Alpha': 1},
            1: {'AlphaDigit': 1, '^AlphaDigit': (2, False, True)}
        }

        symbol_dfa = {
            0: {'=': 1, 'SEE': (4, True, False), '*' : 5 },
            1: {'=': (2, True, False), '^=': (3, False, True)},
            5: {'^/' : (6 , False, True) }}



        whitespace_dfa = {
            0: {'Whitespace': 1},
            1: {'Whitespace': 1, '^Whitespace': (2, False, True)}
        }

        comment_dfa = {
            0: {'/': 1},
            1: {'*': 2},
            2: {'*': 3, 'ees': 2},
            3: {'^*/': 2, '*': 3, '/': (4, True, False) }

        }
        dfa.states_type[0] = 'None'
        offset = len(dfa.states)
        
        dfa.add_state(0)
        
        offset = dfa.add_mini_dfa("NUM", num_dfa, 0)

        offset = dfa.add_mini_dfa("ID",id_dfa, offset)

        offset = dfa.add_mini_dfa("KEYWORD",keyword_dfa, offset)

        offset = dfa.add_mini_dfa("SYMBOL",symbol_dfa, offset)
        
        offset+=4

        offset = dfa.add_mini_dfa("WHITESPACE",whitespace_dfa, offset)

        offset = dfa.add_mini_dfa("COMMENT",comment_dfa, offset)

        dfa.add_state(offset +1, is_accept=False, is_marked_accept=True)
        dfa.make_transition(19, '^/*', offset +1)        
        dfa.states_type[offset +1] = "SYMBOL"

key_table = []
id_table = []
tokens_table= defaultdict(list)
lexical_errors_table = defaultdict(list)
point1 = 0
point2 = 0 
line_number = 1
line_comment_starts = 0


def get_next_token(input_string ,current_ch  , dfa , temp) :
            global point1, point2, line_number, line_comment_starts
            token_tpye_str = ''

            if (dfa.current_state == 19  and input_string[point2+1]!= '*') :
                token_tpye_str= f"(SYMBOL, /)"
                dfa.current_state = 0
                point2+=1
                point1=point2
                return token_tpye_str


            if ( temp == 0 and dfa.current_state== 19) :
                line_comment_starts= line_number
            is_marked, token_type = dfa.is_accept_state()


            if( dfa.states_type[dfa.current_state] == 'COMMENT' and ( dfa.current_state not in (dfa.accept_states or dfa.marked_accept_states))):
                if(input_string[point2+1] == '\x00'):
                    first_of_comment = ''
                    if(len(input_string[point1:point2+1]) >= 7) :
                        first_of_comment = input_string[point1:point1+7]
                    else : first_of_comment = input_string[point1:point2+1]

                    lexical_errors_table[line_comment_starts].append(f"({first_of_comment}..., Unclosed comment)")
                    return 'error'
            
            

            if (token_type in ['ID','KEYWORD']):
                if(input_string[point1:point2] in keyword) :
                    token_type = 'KEYWORD'
                else : token_type = 'ID'
            

            if not token_type  :
                point2+=1
            
            elif (is_marked) :

                dfa.current_state = 0
                if ( current_ch == '\n'):
                    line_number-=1
                
                if token_type =='ID' :
                      id_table.append(input_string[point1:point2])

                if token_type not in  ['WHITESPACE', 'COMMENT']:
                    token_tpye_str = f"({token_type}, {input_string[point1:point2]})"
                point1 = point2
                return token_tpye_str

            else :

                if token_type =='ID' :
                      id_table.append(input_string[point1:point2+1])

                if token_type not in  ['WHITESPACE', 'COMMENT']:
                    token_tpye_str = f"({token_type}, {input_string[point1:point2+1]})"

                dfa.current_state = 0
                point2+=1 
                point1=point2
                return  token_tpye_str
            
            return 'white_space_comment'



def Scanner ( input_string , dfa ) :

    global point1, point2, line_number, line_comment_starts
    input_string = input_string +'\x00'

    while point1 != len(input_string) -1 :
        start_ch =input_string[point1]
        current_ch = input_string[point2]
        if(current_ch == '\n'):
            line_number+=1

        temp = dfa.current_state  
        result = dfa.process_input(current_ch)
        if result :

            next_token = get_next_token(input_string ,current_ch  , dfa , temp)
            if ( next_token != 'error' and next_token!= 'white_space_comment' and next_token.startswith("(") ) :
                tokens_table[line_number].append(next_token)
                continue

            if(next_token == 'error') :
                break
            if(next_token == 'white_space_comment'):
                continue

        else :

            if (dfa.states_type[dfa.current_state]== 'SYMBOL'  and current_ch == "/" and point2 >=1 and  input_string[point2-1] =='*') :
                    lexical_errors_table[line_number].append(f"(*/, Unmatched comment)")
                    dfa.current_state = 0
                    point2+=1
                    point1=point2
                    continue   
            
            if(dfa.current_state == 0 or dfa.states_type[dfa.current_state] in ['ID','KEYWORD' , 'SYMBOL']):
                lexical_errors_table[line_number].append(f"({input_string[point1:point2+1]}, Invalid input)")
                dfa.current_state = 0
                point2+=1
                point1=point2
                continue

            if( dfa.states_type[dfa.current_state] == 'WHITESPACE'):
                lexical_errors_table[line_number].append(f"({input_string[point2]}, Invalid input)")
                dfa.current_state = 0
                point2+=1
                point1=point2
                continue

            if(dfa.states_type[dfa.current_state] == 'NUM') :
                lexical_errors_table[line_number].append(f"({input_string[point1:point2+1]}, Invalid number)")
                dfa.current_state = 0
                point2+=1
                point1=point2
                continue

            if( dfa.states_type[dfa.current_state] == 'COMMENT' and point2>=1 and input_string[point2-2] == '*'):
                    lexical_errors_table[line_number].append(f"(*/, Unmatched comment)")
                    dfa.current_state = 0
                    point1=point2
                    continue   
            
            if (dfa.states_type[dfa.current_state] == 'COMMENT') :
                lexical_errors_table[line_number].append(f"(/, Invalid input)")
                dfa.current_state = 0
                point2+=1
                point1=point2
                continue

    return


def display_dfa(dfa):
    print("DFA States and Transitions:")
    for state in dfa.states:
        print(f"State {state}:")
        if ( state !=  0 ) :
            print("type: ", dfa.states_type[state])
        if state in dfa.transitions:
            for input_symbol, dest_state in dfa.transitions[state].items():
                print(f"  On '{input_symbol}' -> State {dest_state}")
        if state in dfa.accept_states:
            print("  [Accept State]")
        if state in dfa.marked_accept_states:
            print("  [Marked Accept State]")

    print("\n")



def write_symbol_table():
    unique_symbols = set ([ 'if', 'else', 'void', 'int', 'while', 'break', 'return' ] + id_table)
    with open('symbol_table.txt', 'w') as file:
        for index, symbol in enumerate(unique_symbols, start=1):
            file.write(f"{index}.\t{symbol}\n")


def write_tokens():
    with open('tokens.txt', 'w') as file:
        for line_number in sorted(tokens_table):
            tokens = ' '.join(tokens_table[line_number])
            file.write(f"{line_number}.\t{tokens}\n")

def write_lexical_errors():
    with open('lexical_errors.txt', 'w') as file:
        for line_number, errors in lexical_errors_table.items():
            errors_str = ' '.join(errors)
            file.write(f"{line_number}.\t{errors_str}\n")
        if len ( lexical_errors_table) ==0  :
            file.write("There is no lexical error.")


with open('input.txt', 'r') as file:
    content = file.read()

dfa = DFA()
add_token_states(dfa)
Scanner(content, dfa)
write_symbol_table()
write_tokens()
write_lexical_errors()

