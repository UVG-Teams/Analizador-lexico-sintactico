import matplotlib.pyplot as plt
import ply.yacc as yacc
import ply.lex as lex
import networkx as nx

class Analizer(object):

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

    precedence = (
        ( 'left', 'IMPLIES', 'SIMPLIES' ),
        ( 'left', 'AND', 'OR' ),
        ( 'left', 'RPAREN', 'LPAREN' ),
        ( 'right', 'NEGATION' )
    )

    @staticmethod
    def t_ALPHABET(t):
        r'[p,q,r,s,t,u,v,w,x,y,z]+'
        if option == 1:
            t.value = bool(t.value)
        return t

    @staticmethod
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    @staticmethod
    def t_error(t):
        print("Invalid Token:", t.value[0])
        t.lexer.skip(1)

    @staticmethod
    def p_and(p):
        'expr : expr AND expr'
        p[0] = p[1] and p[3]

    @staticmethod
    def p_expr(p):
        'expr : ALPHABET'
        p[0] = p[1]

    @staticmethod
    def p_or(p):
        'expr : expr OR expr'
        p[0] = p[1] or p[3]

    @staticmethod
    def p_negation(p):
        'expr : NEGATION expr'
        p[0] = not p[2]

    @staticmethod
    def p_implies(p):
        'expr : expr IMPLIES expr'
        p[0] = (not p[1]) and p[3]

    @staticmethod
    def p_simplies(p):
        'expr : expr SIMPLIES expr'
        p[0] = not(p[1] ^ p[3])

    @staticmethod
    def p_parens(p):
        'expr : LPAREN expr RPAREN'
        p[0] = p[2]

    @staticmethod
    def p_error(p):
        print("Error de sintaxis")

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.parser = yacc.yacc(module=self, **kwargs)

    def analize(self, data):
        self.lexer.input(data)

    def get_value(self, data):
        return self.parser.parse(data)

    def tokenss(self):
        tokens = []
        while True:
            token = self.lexer.token()
            if not token:
                break
            tokens.append(token)
        return tokens

def menu():
    print("""
        1. Calcular una expresión
        2. Generar grafo
        9. Salir
    """)

option = 1
analizer = Analizer()
while True:
    menu()
    option = int(input("Ingrese una opcion: "))
    if (option == 1):
        expresion = input("Ingrese una expresion a evaluar: ")
        print("Valor de verdad: ", int(analizer.get_value(expresion)))
    elif (option == 2):
        G = nx.DiGraph()
        expresion = input("Ingrese una expresion a graficar: ")
        analizer.analize(expresion)
        tokens = analizer.tokenss()
        relations = []
        for i in range(len(tokens)):
            token = tokens[i]
            if i-1 >= 0:
                previous_token = tokens[i-1]
            if i+1 < len(tokens):
                next_token = tokens[i+1]

            if token.type == "NEGATION":
                if next_token.type == "LPAREN":
                    relations.append((
                        "{con}:{label}".format(con = i, label = token.value),
                        "{con}:{label}".format(con = i+3, label = tokens[i+3].value)
                    ))
                else:
                    relations.append((
                        "{con}:{label}".format(con = i, label = token.value),
                        "{con}:{label}".format(con = i+1, label = next_token.value)
                    ))
            elif token.type == "SIMPLIES" or token.type == "IMPLIES" or token.type == "AND" or token.type == "OR":
                if next_token.type == "LPAREN":
                    relations.append((
                        "{con}:{label}".format(con = i, label = token.value),
                        "{con}:{label}".format(con = i+3, label = tokens[i+3].value)
                    ))
                else:
                    relations.append((
                        "{con}:{label}".format(con = i, label = token.value),
                        "{con}:{label}".format(con = i+1, label = next_token.value)
                    ))
                if previous_token.type == "RPAREN":
                    relations.append((
                        "{con}:{label}".format(con = i, label = token.value),
                        "{con}:{label}".format(con = i-3, label = tokens[i-3].value)
                    ))
                else:
                    relations.append((
                        "{con}:{label}".format(con = i, label = token.value),
                        "{con}:{label}".format(con = i-1, label = previous_token.value)
                    ))

        print(relations)
        G.add_edges_from(relations)
        plt.subplot(121)
        nx.draw(G, with_labels=True, font_size="8")
        plt.show()

    elif (option == 9):
        break
    else:
        print("Opción incorrecta")
