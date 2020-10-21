import ply.lex as lex
import ply.yacc as yacc
import networkx as nx
import matplotlib.pyplot as plt

opcion = 1

tokens = (
    'ALPHABET',
    'LPAREN',
    'RPAREN',
    'PREDICATE',
    'AND',
    'OR',
    'SIMPLIES',
    'IMPLIES',
    'NEGATION'
)

t_ignore = ' \t'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_AND = r'\^'
t_OR = r'\°'
t_IMPLIES = r'\=>'
t_SIMPLIES = r'\<=>'
t_NEGATION = r'\~'

def t_ALPHABET( t ) :
    r'[p,q,r,s,t,u,v,w,x,y,z]+'
    if opcion == 1:
        t.value = bool( t.value )
    
    return t

def t_newline( t ):
  r'\n+'
  t.lexer.lineno += len( t.value )

def t_error( t ):
  print("Invalid Token:",t.value[0])
  t.lexer.skip( 1 )

lexer = lex.lex()

precedence = (
    ( 'left', 'IMPLIES', 'SIMPLIES' ),
    ( 'left', 'AND', 'OR' ),
    ( 'left', 'RPAREN', 'LPAREN' ),
    ( 'right', 'NEGATION' )
)

def p_and( p ) :
    'expr : expr AND expr'
    p[0] = p[1] and p[3]

def p_expr( p ) :
    'expr : ALPHABET'
    p[0] = p[1] 

def p_or( p ) :
    'expr : expr OR expr'
    p[0] = p[1] or p[3]

def p_negation( p ) :
    'expr : NEGATION expr'
    p[0] = not p[2]

def p_implies( p ) :
    'expr : expr IMPLIES expr'

    p[0] = (not p[1]) and p[3]

def p_simplies( p ) :
    'expr : expr SIMPLIES expr'
    p[0] = not(p[1]^p[3])    #((not p[1]) and p[3]) or ((not p[3]) and p[1]) 

def p_parens( p ) :
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error( p ):
    print("Syntax error in input!")


continuar = True
while continuar:
    print("""
        1. Calcular una expresión
        2. Generar grafo
    """)

    opcion = int(input("Ingrese una opcion: "))
    if (opcion == 1):
        parser = yacc.yacc()
        res = parser.parse("(p<=>p)")
        print(int(res))

    elif (opcion == 2):
        G = nx.DiGraph()
        lexer.input("p<=>~p")
        tokens = []
        while True:
            token = lexer.token()
            if not token:
                break

            # print(token)
            tokens.append(token)

        relations = []
        for i in range(len(tokens)):
            token = tokens[i]
            if i-1 >= 0:
                previous_token = tokens[i-1]
            if i+1 < len(tokens):
                next_token = tokens[i+1]
            
            # if token.type == "RPAREN" and i+1 < len(tokens):
            #     relations.append(("{con}:{label}".format(con = i+1, label = next_token.value), "{con}:{label}".format(con = i-2, label = tokens[i-2].value)))
            if token.type == "NEGATION":
                if next_token.type == "LPAREN":
                    relations.append(("{con}:{label}".format(con = i, label = token.value), "{con}:{label}".format(con = i+3, label = tokens[i+3].value)))
                else:
                    relations.append(("{con}:{label}".format(con = i, label = token.value), "{con}:{label}".format(con = i+1, label = next_token.value)))
                    # lexer.input("~(p^q)=>(p°q)")
            elif token.type == "SIMPLIES" or token.type == "IMPLIES" or token.type == "AND" or token.type == "OR":
                if next_token.type == "LPAREN":
                    relations.append(("{con}:{label}".format(con = i, label = token.value), "{con}:{label}".format(con = i+3, label = tokens[i+3].value)))
                else:
                    relations.append(("{con}:{label}".format(con = i, label = token.value), "{con}:{label}".format(con = i+1, label = next_token.value)))
                if previous_token.type == "RPAREN":
                    relations.append(("{con}:{label}".format(con = i, label = token.value), "{con}:{label}".format(con = i-3, label = tokens[i-3].value)))
                else:
                    relations.append(("{con}:{label}".format(con = i, label = token.value), "{con}:{label}".format(con = i-1, label = previous_token.value)))

            # if token.type != "RPAREN" and token.type != "LPAREN":
            #     G.add_node("{con}:{label}".format(con = i, label = token.value), value = token.value, label = token.value)

        print(relations)
        G.add_edges_from(relations)
        plt.subplot(121)
        nx.draw(G, with_labels=True, font_size="8")
        plt.show()

    else:
        print("Opción incorrecta")