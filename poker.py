
# import modules ######################################################################################
import random

# declaracion de variables ############################################################################
PALOS = '♠ ♡ ♢ ♣'.split(' ')
RANGO = '2 3 4 5 6 7 8 9 10 J Q K A'.split(' ')
VALORES = {"*":0,"♠":0,"♡":0,"♣":0, "♢":0, "2":1, "3":2, "4":3, "5":4, "6":5, "7":6, "8":7, "9":8, "10":9, "J":10, "Q":11, "K":12, "A":13}
LISTA_JUGADAS = {'Carta más alta': 1, 'Pareja': 2, 'Doble pareja': 3, 'Trio': 4, 'Escalera': 5, 'Color': 6, 'Full': 7, 'Poker': 8, 'Escalera Color': 9, 'Escalera real': 10 }

MAZO = [(r, p) for r in RANGO for p in PALOS]
JUGADORES = {}
JUGADA = {}


# Funciones #############################################################################################

# pide jugadores de 3 formas diferentes
# 1ª > ingresando los nombre de jugadores (máximo 7)
# 2ª > ingresando un número del 1 al 7, generará los jugadores
# 3ª > ingresando un ENTER al principio generará una partida con 7 jugadores
def pide_jugadores(JUGADORES):
    max =7
    jugador = input('''
Ingrese el nombre del primer jugador, o bien...
\nSi ingresa un número entre 1 y 7 los generará automáticamente. 
\n(ENTER para generar una partida de 7 jugadores) : ''')
    if jugador.isnumeric() and int(jugador) <= max:
        for x in range(int(jugador)):
            word = 'Jugador '+str(x+1)
            JUGADORES[word] = []
    elif jugador == '':
        JUGADORES['Alice'] = []
        JUGADORES['Bob'] = []
        JUGADORES['Charlie'] = []
        JUGADORES['Dave'] = []
        JUGADORES['Eve'] = []
        JUGADORES['Frank'] = []
        JUGADORES['Mallory'] = []
    else:
        JUGADORES[jugador] = []
        while jugador !="" and max > 1:
            jugador = input('Ingrese el nombre de un jugador; máximo 7 (ENTER para terminar) : ')
            if jugador == "": break
            JUGADORES[jugador] = []
            max -= 1

# baraja mazo
def baraja_mazo(MAZO):
    random.shuffle(MAZO)

# reparte cartas
def reparte_cartas(mazo, jugadores):
    for reparto in range(0,5):
        for jugador in jugadores:
            jugadores[jugador].extend(mazo[:1])
            mazo = mazo[1:]

# imprime jugadas
def imprime_mano(jugadores):
    print('''
    ||||||  Cartas de los Jugadores   ||||||
    ========================================''')
    for jugador in jugadores:
        print("{: >10}   ".format(jugador), end='')
        for parte in jugadores[jugador]:
            print("{:>2} {:<2}".format(*parte), end=' ')
        print()

# ordena cartas
def lista_orden(jugador, lista_jugadores):
    valores = []
    for carta in range(0,5):
        valores.append(lista_jugadores[jugador][carta][0])
    lista_ordenada = sorted(valores, key = lambda x: VALORES[x])
    return lista_ordenada

# revisa valor de repetición
def valor_rep(jugador, lista_jugadores):
    valor = []
    for carta in range(0,5):
        valor.append(lista_jugadores[jugador][carta][0])
    valor = sorted(valor, key = lambda x: VALORES[x])
    valor_repetido = {i:valor.count(i) for i in valor}
    return valor_repetido, valor

# Funciones de jugadas ############################################################################

# revisa carta mas alta en la mano del jugador
def revisa_carta_alta(jugador, lista_jugadores):
    JUGADA[jugador] = ('Carta más alta',lista_orden(jugador, lista_jugadores)[-1], "-".join(x for x in lista_orden(jugador, lista_jugadores)[:-1]))

# revisa pareja en la mano del jugador
def revisa_pareja(jugador, lista_jugadores):
    valor = []
    valor_repetido = {}
    valor_repetido , valor= valor_rep(jugador, lista_jugadores)
    if valor_repetido[max(valor_repetido, key=valor_repetido.get)] == 2 and list(valor_repetido.values()).count(2) == 1:
        resto = [x for x in valor if x != max(valor_repetido, key=valor_repetido.get)]
        JUGADA[jugador] = ('Pareja',max(valor_repetido, key=valor_repetido.get), "-".join(x for x in resto))
        return True
    else:
        return False

# revisa doble pareja en la mano del jugador
def revisa_doble_pareja(jugador, lista_jugadores):
    valor_repetido , valor= valor_rep(jugador, lista_jugadores)
    pareja = "-".join([x for x in list(valor_repetido) if valor_repetido[x]==2])
    if valor_repetido[max(valor_repetido, key=valor_repetido.get)] == 2 and list(valor_repetido.values()).count(2) == 2:
        resto = [x for x in valor if valor_repetido[x] !=2]
        JUGADA[jugador] = ('Doble pareja',pareja,"-".join(x for x in resto))
        return True
    else:
        return False

# revisa trio en la mano del jugador
def revisa_trio(jugador, lista_jugadores):
    valor = []
    valor_repetido = {}
    valor_repetido , valor= valor_rep(jugador, lista_jugadores)
    if valor_repetido[max(valor_repetido, key=valor_repetido.get)] == 3:
        resto = [x for x in valor if x != max(valor_repetido, key=valor_repetido.get)]
        JUGADA[jugador] = ('Trio',max(valor_repetido, key=valor_repetido.get), "-".join(x for x in resto))
        return True
    elif valor_repetido[max(valor_repetido, key=valor_repetido.get)] != 3 and valor_repetido[max(valor_repetido, key=valor_repetido.get)] == 2 and list(valor_repetido.values()).count(2) != 2:
        resto = [x for x in valor if x != max(valor_repetido, key=valor_repetido.get)]
        JUGADA[jugador] = ('Pareja',max(valor_repetido, key=valor_repetido.get), "-".join(x for x in resto))
        return False


# revisa escalera en la mano del jugador
def revisa_escalera(jugador, lista_jugadores):
    tot = []
    for x in lista_orden(jugador, lista_jugadores):
        tot.append(VALORES[x])
    if tot[1] - tot[0] == 1 and tot[2] - tot[1] == 1 and tot[3] - tot[2] == 1 and tot[4] - tot[3] == 1:
        JUGADA[jugador] = ('Escalera',lista_orden(jugador, lista_jugadores)[4], '*')
        return True
    elif set(lista_orden(jugador, lista_jugadores)) == set(['A', '2', '3', '4', '5']):
        JUGADA[jugador] = ('Escalera',lista_orden(jugador, lista_jugadores)[3], '*')
        return True
    else:
        return False

# revisa color en la mano del jugador
def revisa_color(jugador, lista_jugadores):
    palos = []
    for carta in range(0,5):
        palos.append(lista_jugadores[jugador][carta][1])
    if len(set(palos)) == 1:
        JUGADA[jugador] = ('Color',palos[0],"-".join(x for x in lista_orden(jugador, lista_jugadores)))
        return True
    else:
        return False

# revisa full_house en la mano del jugador
def revisa_full_house(jugador, lista_jugadores):
    valor = []
    valor_repetido = {}
    valor_repetido , valor= valor_rep(jugador, lista_jugadores)
    if list(valor_repetido.values()).count(3) == 1 and list(valor_repetido.values()).count(2) == 1:
        trio = [x for x in list(valor_repetido) if valor_repetido[x] == 3]
        pareja = [x for x in list(valor_repetido) if valor_repetido[x] == 2]
        JUGADA[jugador] = ('Full',trio[0], pareja[0])
        return True
    else:
        return False

# revisa poker en la mano del jugador
def revisa_poker(jugador, lista_jugadores):
    valor = []
    valor_repetido = {}
    valor_repetido , valor= valor_rep(jugador, lista_jugadores)
    if valor_repetido[max(valor_repetido, key=valor_repetido.get)] == 4:
        resto = [x for x in valor if x != max(valor_repetido, key=valor_repetido.get)]
        JUGADA[jugador] = ('Poker',max(valor_repetido, key=valor_repetido.get),"-".join(x for x in resto))
        return True
    else:
        return False

# revisa escalera de color en la mano del jugador
def revisa_escalera_color(jugador, lista_jugadores):
    if revisa_color(jugador, lista_jugadores) and revisa_escalera(jugador, lista_jugadores):
        JUGADA[jugador] = ('Escalera Color',JUGADA[jugador][1],'*')
        return True
    else:
        return False

# revisa escalera real o flor imperial en la mano del jugador
def revisa_escalera_real(jugador, lista_jugadores):
    palos = []
    for carta in range(0,5):
        palos.append(lista_jugadores[jugador][carta][1])
    if  JUGADA[jugador][1] == 'A' and revisa_escalera_color(jugador, lista_jugadores) :
        JUGADA[jugador] = ('Escalera real',JUGADA[jugador][1],palos[0])
        return True
    else:
        return False

#######################################################################################################


def revisar_jugada(lista_jugadores):
    for jugador in lista_jugadores:
        revisa_carta_alta(jugador, lista_jugadores)
        revisa_pareja(jugador, lista_jugadores)
        revisa_doble_pareja(jugador, lista_jugadores)
        revisa_trio(jugador, lista_jugadores)
        revisa_escalera(jugador, lista_jugadores)
        revisa_color(jugador, lista_jugadores)
        revisa_full_house(jugador, lista_jugadores)
        revisa_poker(jugador, lista_jugadores)
        revisa_escalera_color(jugador, lista_jugadores)
        revisa_escalera_real(jugador, lista_jugadores)

# revisar jugadas ganadoras
def revisar_ganador(JUGADA):
    # Asigna puntuaciones
    print('''
    ========================================
     Jugador       Mano       Figura  Resto
    ========================================''')
    for jugador, cartas in JUGADA.items():
        print( "{:>10}".format(jugador) , end='')
        print("     {:<15}  {:<5}{:<7}".format(*cartas))
        JUGADA[jugador] = JUGADA[jugador] + (LISTA_JUGADAS[JUGADA[jugador][0]],)
    print()
    # Revisa jugadas más altas
    puntos = [JUGADA[x][3] for x in JUGADA]
    max_puntos = max(puntos)
    print("La jugada más alta ha sido >>> ",[x for x, y in LISTA_JUGADAS.items() if y == max_puntos])
    # Revisa empates
    count_winners = puntos.count(max(puntos))
    # Si unicamente hay un ganador
    if count_winners == 1:
        print('Hay 1 solo jugador con >>> ',[x for x, y in LISTA_JUGADAS.items() if y == max_puntos])
        for jugador in JUGADA.keys():
            if JUGADA[jugador][3] == max_puntos:
                print('El ganador es >>> **', jugador, "** que ha sacado *", JUGADA[jugador][0], '* de', JUGADA[jugador][1], ' + ', JUGADA[jugador][2], 'de resto.')
    #Si hay mas de 1 ganador
    else:
        print('Hay ',count_winners,' jugadores con >>> ',[x for x, y in LISTA_JUGADAS.items() if y == max_puntos])
        # Crear lista de ganadores para el desempate
        ganadores = {}
        for jugador in JUGADA.keys():
            if JUGADA[jugador][3] == max_puntos:
                ganadores[jugador] = JUGADA[jugador]
        # Comparar cartas
        leader = ''
        empate = []
        for jugador in ganadores.keys():
            if leader == '':
                leader = jugador
            else:
                for x in range(len(JUGADA[jugador][1].split('-')), 0, -1):
                    if VALORES[JUGADA[jugador][1].split('-')[x-1]] > VALORES[JUGADA[leader][1].split('-')[x-1]]:
                        leader = jugador
                        break
                    elif VALORES[JUGADA[jugador][1].split('-')[x-1]] < VALORES[JUGADA[leader][1].split('-')[x-1]]:
                        break
                    elif x == 1 and VALORES[JUGADA[jugador][1].split('-')[x-1]] == VALORES[JUGADA[leader][1].split('-')[x-1]]:
                        for x in range(len(JUGADA[jugador][2].split('-')), 0, -1):
                            if VALORES[JUGADA[jugador][2].split('-')[x-1]] > VALORES[JUGADA[leader][2].split('-')[x-1]]:
                                leader = jugador
                                break
                            elif VALORES[JUGADA[jugador][2].split('-')[x-1]] < VALORES[JUGADA[leader][2].split('-')[x-1]]:
                                break
                            elif x == 1 and VALORES[JUGADA[jugador][1].split('-')[x-1]] == VALORES[JUGADA[leader][1].split('-')[x-1]]:
                                print('Empate exacto entre: ',jugador,' y ', leader)
                                if jugador not in empate:
                                    empate.append(jugador)
                                if leader not in empate:
                                    empate.append(leader)
        print()
        print('||||| RESULTADO |||||')
        print('=====================')
        if len(empate) != 0:
            print('El dinero de la mesa se repartirá entre los siguientes jugadores, por tener una jugada idéntica:')
            for jug in empate:
                print('>>>>>     ',jug)
        else:
            print('El ganador del desempate ha sido >>> **', leader, "** que ha sacado *", JUGADA[leader][0], '* de', JUGADA[leader][1], ' + ', JUGADA[leader][2], 'de resto.')


# MAIN > programa principal ##############################################################################

# pide nombre de jugadores
pide_jugadores(JUGADORES)
# baraja el mazo
baraja_mazo(MAZO)
# reparte cartas a jugadores
reparte_cartas(MAZO, JUGADORES)
# imprime mano
imprime_mano(JUGADORES)
# revisa las manos de los jugadores
revisar_jugada(JUGADORES)
# revisar jugador ganador
revisar_ganador(JUGADA)
