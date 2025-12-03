
import random

def inicializar_matriz(cantidad_filas: int, cantidad_columnas: int, valor:int) -> list: #Inicializo la matriz
    """
    DESCRIPCION:
        Crea una matriz de tamaño cantidad_filas X cantidad_columnas rellenada con el valor dado.
    
    PARAMETROS:
        cantidad_filas (int): número de filas.
        cantidad_columnas (int): número de columnas.
        valor (int): valor con el cual se rellena cada celda.
    
    RETORNA:
        matriz (list): matriz creada.
    """
    matriz = []
    for i in range(cantidad_filas):
        fila = []
        for _ in range(cantidad_columnas):
            fila.append(valor)
        matriz.append(fila) #Añade la fila completa a la matriz.
    return matriz

def chequear_fila(matriz:list, fila:int, numero:int):
    """
    DESCRIPCION:
        Revisa si un número ya existe en la fila indicada.
    
    PARAMETROS:
        matriz (list 9X9): tablero actual.
        fila (int): índice de fila a verificar.
        numero (int): número a buscar.
    
    RETORNA:
        True si el número aparece en la fila.
        False si no aparece.
    """
    retorno = False
    for i in range(9):
        if matriz[fila][i] == numero:
            retorno = True 
    return retorno 

def chequear_columna(matriz:list, columna:int, numero:int):
    """
    DESCRIPCION:
        Verifica si un número está presente en la columna indicada.
    
    PARAMETROS:
        matriz: tablero Sudoku.
        columna: columna a revisar.
        numero: número a buscar.
    
    RETORNA:
        True si el número aparece.
        False si no aparece.
    """   
    retorno = False
    for i in range(9):
        if matriz[i][columna] == numero:
            retorno = True
    return retorno

def chequear_region(matriz:list, fila:int, columna:int, numero:int):
    """
    DESCRIPCION:
        Verifica si un número ya existe en la región 3×3 correspondiente a (fila, columna).
    
    PARAMETROS:
        matriz
        fila
        columna
        numero
    
    RETORNA:
        True si el número ya está en la región.
        False si no está.
    """
    retorno = False
    fila_vertice = (int) (fila/3) * 3  
    columna_vertice = (int) (columna/3) * 3  

    for i in range(3):
        for j in range(3):
            if matriz[i + fila_vertice][j + columna_vertice] == numero:  
                retorno = True

    return retorno 

def validar_numero(matriz, fila, columna, numero): #validamos el numero
    """
    DESCRIPCION:
        Determina si un número puede colocarse en una celda sin violar reglas de Sudoku.
    
    PARAMETROS:
        matriz
        fila
        columna
        numero
    
    RETORNA:
        True si colocar el número es válido.
        False si generaría conflicto.
    """    
    if numero == 0:
        return True  
    valor_anterior = matriz[fila][columna]
    matriz[fila][columna] = 0
    fila_ok = not chequear_fila(matriz, fila, numero)
    columna_ok = not chequear_columna(matriz, columna, numero)
    region_ok = not chequear_region(matriz, fila, columna, numero)

    matriz[fila][columna] = valor_anterior
    return fila_ok and columna_ok and region_ok #retorna el numero si es que pasa todos los chequeos

def region_completa(matriz, fila, columna):
    """
    DESCRIPCION:
        Indica si la región 3x3 que contiene (fila, columna) está llena (sin ceros).
    
    RETORNA:
        True si no hay ceros en esa región.
        False si todavía falta completar algo.
    """
    fila_vertice = (fila//3)*3
    columna_vertice = (columna//3)*3
    for i in range(3):
        for j in range(3):
            if matriz[fila_vertice + i][columna_vertice + j] == 0:
                return False
    return True

def tablero_completo(matriz):
    """
    DESCRIPCION:
        Revisa si todas las celdas están completas (no hay ceros).

    RETORNA:
        True si el tablero está completo.
        False si hay alguna celda vacía.
    """
    for fila in matriz:
        if 0 in fila:
            return False
    return True

def generar_tablero_facil_por_region(numeros_por_region): #genera los numeros por region 
    """
    DESCRIPCION:
        Crea un tablero inicial completando cada región con cierta cantidad de números aleatorios válidos.

    PARAMETROS:
        numeros_por_region (int): cantidad de pistas en cada región.

    RETORNA:
        Una matriz 9x9 parcialmente completada.
    """
    matriz = inicializar_matriz(9, 9, 0)

    for region_fila in range(3):
        for region_col in range(3):
            intentos = 0
            puestos = 0
            while puestos < numeros_por_region:
                if intentos > 100:  # Si no se logra, resetear la región y reintentar
                    for i in range(3):
                        for j in range(3):
                            matriz[region_fila*3 + i][region_col*3 + j] = 0
                    puestos = 0
                    intentos = 0
                numero = random.randint(1,9)
                fila = random.randint(0,2) + region_fila*3
                col = random.randint(0,2) + region_col*3
                if matriz[fila][col] == 0 and validar_numero(matriz, fila, col, numero):
                    matriz[fila][col] = numero
                    puestos += 1
                else:
                    intentos += 1
    return matriz

def region_correcta(matriz, region_f, region_c):
    """
    DESCRIPCION:
        Valida si una región 3x3 está correcta:
            Sin ceros
            Sin números repetidos

    PARAMETROS:
        region_f: índice de la región en vertical (0 a 2)
        region_c: índice de la región en horizontal

    RETORNA:
        True si la región está completa y sin repetir.
        False si falta completar o está mal.
    """
    numeros = []
    for f in range(region_f*3, region_f*3+3):
        for c in range(region_c*3, region_c*3+3):
            num = matriz[f][c]
            if num == 0:
                return False   # incompleta
            numeros.append(num)
    return len(numeros) == 9 and len(set(numeros)) == 9  # sin repetidos

def actualizar_puntaje(puntaje, matriz, fila, columna, numero, celda_incorrecta):
    """
    DESCRIPCION:
        Actualiza el puntaje cuando el usuario ingresa un número.

    PARAMETROS:
        puntaje actual
        matriz
        fila, columna donde se ingresó
        numero ingresado
        celda_incorrecta: si ya estaba marcada como error

    RETORNA:
        puntaje ajustado.
    """
    if validar_numero(matriz, fila, columna, numero):
        puntaje += 1
        if tablero_completo(matriz):
            puntaje += 81
    else:
        if not celda_incorrecta:
            pass
    return puntaje

def actualizar_puntaje_regiones(matriz, regiones_completadas, puntaje):
    """
    DESCRIPCION:
        Suma puntuación por regiones 3x3 completadas correctamente.

    PARAMETROS:
        matriz: tablero actual
        regiones_completadas: matriz 3x3 de booleanos
        puntaje

    RETORNA:
        puntaje actualizado.
    """
    for rf in range(3):
        for rc in range(3):
            if not regiones_completadas[rf][rc]:  
                if region_correcta(matriz, rf, rc):
                    puntaje += 9
                    regiones_completadas[rf][rc] = True
    return puntaje