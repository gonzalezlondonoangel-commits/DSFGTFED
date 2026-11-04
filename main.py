
# ============================================================
# CLASSNOTE
# Calculadora matematica creada por Angel
# Python 3 + Streamlit
# Calculadora con procedimientos matematicos detallados
# ============================================================

import ast
import math
import operator
import re
import streamlit as st

# ============================================================
# 1. CONFIGURACION
# ============================================================

st.set_page_config(
    page_title="CLASSNOTE - Calculadora matematica",
    page_icon="🧮",
    layout="centered"
)

AZUL = "#087BFF"
AZUL_OSCURO = "#06152E"
AMARILLO = "#FFD928"
NEGRO = "#05070B"
BLANCO = "#FFFFFF"
GRIS = "#AFC7E8"

# ============================================================
# 2. DISENO VISUAL
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #06152E;
    color: white;
}

h1, h2, h3 {
    color: #FFD928 !important;
}

p, label, span {
    color: white;
}

div[data-baseweb="input"] input {
    background-color: #05070B;
    color: #FFD928;
    border: 1px solid #087BFF;
    border-radius: 9px;
}

.stButton button {
    background-color: #FFD928;
    color: #06152E;
    font-weight: bold;
    border-radius: 10px;
    border: none;
    min-height: 43px;
}

.stButton button:hover {
    background-color: #087BFF;
    color: white;
}

.resultado {
    background-color: #05070B;
    border: 2px solid #087BFF;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
}

.resultado h1 {
    color: #FFD928 !important;
    font-size: 36px;
}

.procedimiento {
    background-color: #102747;
    border-left: 5px solid #FFD928;
    border-radius: 9px;
    padding: 15px;
    margin: 10px 0;
}

.pie {
    color: #AFC7E8;
    text-align: center;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. FORMATO DE NUMEROS
# ============================================================

def formato(numero):

    if isinstance(numero, bool):
        return "Verdadero" if numero else "Falso"

    if isinstance(numero, int):
        return str(numero)

    if isinstance(numero, float):

        if not math.isfinite(numero):
            return str(numero)

        if numero.is_integer():
            return str(int(numero))

        return f"{numero:.10g}"

    return str(numero)


# ============================================================
# 4. FUNCIONES MATEMATICAS
# ============================================================

def promedio(*numeros):

    if not numeros:
        raise ValueError(
            "Debes ingresar numeros para calcular el promedio."
        )

    return sum(numeros) / len(numeros)


def porcentaje(numero, tasa):

    return numero * tasa / 100


def raiz(numero):

    if numero < 0:
        raise ValueError(
            "No existe una raiz cuadrada real de un numero negativo."
        )

    return math.sqrt(numero)


def raiz_n(numero, indice):

    if indice == 0:
        raise ValueError("El indice de la raiz no puede ser cero.")

    if not float(indice).is_integer():
        raise ValueError("El indice debe ser un numero entero.")

    indice = int(indice)

    if numero < 0:

        if indice % 2 == 0:
            raise ValueError(
                "No existe una raiz par real de un numero negativo."
            )

        return -((-numero) ** (1 / indice))

    return numero ** (1 / indice)


FUNCIONES = {
    "promedio": promedio,
    "porcentaje": porcentaje,
    "raiz": raiz,
    "sqrt": raiz,
    "raiz_n": raiz_n,
    "abs": abs
}


# ============================================================
# 5. OPERADORES MATEMATICOS
# ============================================================

OPERADORES = {

    ast.Add: (operator.add, "+", "Suma"),

    ast.Sub: (operator.sub, "-", "Resta"),

    ast.Mult: (operator.mul, "×", "Multiplicacion"),

    ast.Div: (operator.truediv, "÷", "Division"),

    ast.FloorDiv: (
        operator.floordiv,
        "//",
        "Division entera"
    ),

    ast.Mod: (
        operator.mod,
        "%",
        "Modulo"
    ),

    ast.Pow: (
        operator.pow,
        "^",
        "Potenciacion"
    )
}

UNARIOS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg
}


# ============================================================
# 6. PREPARAR EXPRESIONES
# ============================================================

def preparar(texto):

    texto = texto.strip()

    if not texto:
        raise ValueError("Escribe una operacion matematica.")

    texto = texto.replace("×", "*")
    texto = texto.replace("÷", "/")
    texto = texto.replace("−", "-")
    texto = texto.replace("^", "**")
    texto = texto.replace("√(", "raiz(")

    # Convertir porcentajes directos.
    # Ejemplo: 15% = 15/100

    texto = re.sub(
        r"(?<![\w.)])(\d+(?:\.\d+)?)\s*%",
        r"(\1/100)",
        texto
    )

    # Multiplicacion implicita.
    # Ejemplo: 5(7) = 5*7

    texto = re.sub(
        r"(?<=[0-9.)])\s*(?=\()",
        "*",
        texto
    )

    texto = re.sub(
        r"(?<=\))\s*(?=[0-9])",
        "*",
        texto
    )

    # Multiplicacion antes de funciones.
    # Ejemplo: 2raiz(9)

    for nombre in FUNCIONES:

        texto = re.sub(
            r"(?<=[0-9.)])\s*(?=" + nombre + r"\s*\()",
            "*",
            texto
        )

    return texto


# ============================================================
# 7. VALIDAR EXPRESIONES
# ============================================================

def validar(arbol):

    permitidos = (

        ast.Expression,
        ast.Constant,
        ast.Num,
        ast.BinOp,
        ast.UnaryOp,
        ast.Call,
        ast.Name,
        ast.Load,

        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,

        ast.UAdd,
        ast.USub,
        ast.Not,

        ast.Compare,
        ast.Eq,
        ast.NotEq,
        ast.Lt,
        ast.LtE,
        ast.Gt,
        ast.GtE,

        ast.BoolOp,
        ast.And,
        ast.Or
    )

    nodos = list(ast.walk(arbol))

    if len(nodos) > 150:
        raise ValueError("La operacion es demasiado extensa.")

    for nodo in nodos:

        if not isinstance(nodo, permitidos):
            raise ValueError(
                "La expresion contiene elementos no permitidos."
            )


# ============================================================
# 8. MOTOR MATEMATICO PASO A PASO
# ============================================================

def evaluar(nodo, pasos):

    # Expresion principal.

    if isinstance(nodo, ast.Expression):

        return evaluar(nodo.body, pasos)

    # Numeros.

    if isinstance(nodo, ast.Constant):

        if type(nodo.value) in (int, float, bool):
            return nodo.value

        raise ValueError("Solo se permiten numeros.")

    if isinstance(nodo, ast.Num):
        return nodo.n

    # --------------------------------------------------------
    # OPERACIONES ARITMETICAS
    # --------------------------------------------------------

    if isinstance(nodo, ast.BinOp):

        a = evaluar(nodo.left, pasos)

        b = evaluar(nodo.right, pasos)

        tipo = type(nodo.op)

        if tipo not in OPERADORES:
            raise ValueError("Operador no permitido.")

        if tipo == ast.Pow and abs(b) > 100:
            raise ValueError("El exponente es demasiado grande.")

        funcion, simbolo, nombre = OPERADORES[tipo]

        if tipo in (
            ast.Div,
            ast.FloorDiv,
            ast.Mod
        ) and b == 0:

            raise ZeroDivisionError(
                "No se puede dividir entre cero."
            )

        resultado = funcion(a, b)

        if isinstance(resultado, complex):
            raise ValueError("El resultado no es un numero real.")

        if isinstance(resultado, float) and not math.isfinite(resultado):
            raise ValueError("El resultado esta fuera de rango.")

        # Construir procedimiento detallado.

        if tipo == ast.Add:

            explicacion = (
                f"Sumamos {formato(a)} y {formato(b)}."
            )

        elif tipo == ast.Sub:

            explicacion = (
                f"Restamos {formato(b)} a {formato(a)}."
            )

        elif tipo == ast.Mult:

            explicacion = (
                f"Multiplicamos {formato(a)} por {formato(b)}."
            )

        elif tipo == ast.Div:

            explicacion = (
                f"Dividimos {formato(a)} entre {formato(b)}."
            )

        elif tipo == ast.Pow:

            explicacion = (
                f"Elevamos {formato(a)} al exponente {formato(b)}."
            )

        elif tipo == ast.Mod:

            explicacion = (
                f"Calculamos el residuo de dividir "
                f"{formato(a)} entre {formato(b)}."
            )

        else:

            explicacion = (
                f"Realizamos una {nombre.lower()}."
            )

        pasos.append({
            "titulo": nombre,
            "explicacion": explicacion,
            "formula": (
                f"{formato(a)} {simbolo} {formato(b)}"
                f" = {formato(resultado)}"
            )
        })

        return resultado

    # --------------------------------------------------------
    # NUMEROS POSITIVOS Y NEGATIVOS
    # --------------------------------------------------------

    if isinstance(nodo, ast.UnaryOp):

        valor = evaluar(nodo.operand, pasos)

        if isinstance(nodo.op, ast.Not):

            resultado = not bool(valor)

            pasos.append({
                "titulo": "Negacion logica",
                "explicacion": "Invertimos el valor de verdad.",
                "formula": (
                    f"NOT {formato(valor)} = {formato(resultado)}"
                )
            })

            return resultado

        tipo = type(nodo.op)

        if tipo not in UNARIOS:
            raise ValueError("Operacion unaria no permitida.")

        resultado = UNARIOS[tipo](valor)

        if tipo == ast.USub:

            pasos.append({
                "titulo": "Signo negativo",
                "explicacion": (
                    "Aplicamos el signo negativo al numero."
                ),
                "formula": (
                    f"-({formato(valor)}) = {formato(resultado)}"
                )
            })

        return resultado

    # --------------------------------------------------------
    # FUNCIONES MATEMATICAS
    # --------------------------------------------------------

    if isinstance(nodo, ast.Call):

        if not isinstance(nodo.func, ast.Name):
            raise ValueError("Funcion no permitida.")

        nombre = nodo.func.id

        if nombre not in FUNCIONES or nodo.keywords:
            raise ValueError("Funcion no permitida.")

        argumentos = [
            evaluar(x, pasos) for x in nodo.args
        ]

        resultado = FUNCIONES[nombre](*argumentos)

        if isinstance(resultado, complex):
            raise ValueError("Resultado no real.")

        if isinstance(resultado, float) and not math.isfinite(resultado):
            raise ValueError("Resultado fuera de rango.")

        # PROMEDIO

        if nombre == "promedio":

            cantidad = len(argumentos)
            suma = sum(argumentos)

            pasos.append({
                "titulo": "Calculo del promedio",
                "explicacion": (
                    "Sumamos todos los valores y dividimos "
                    "entre la cantidad de numeros."
                ),
                "formula": (
                    f"({' + '.join(formato(x) for x in argumentos)}) "
                    f"= {formato(suma)}"
                )
            })

            pasos.append({
                "titulo": "Division del promedio",
                "explicacion": (
                    f"Dividimos la suma entre {cantidad} valores."
                ),
                "formula": (
                    f"{formato(suma)} / {cantidad} "
                    f"= {formato(resultado)}"
                )
            })

        # PORCENTAJE

        elif nombre == "porcentaje":

            numero, tasa = argumentos

            pasos.append({
                "titulo": "Formula del porcentaje",
                "explicacion": (
                    "Multiplicamos la cantidad por el porcentaje "
                    "y dividimos entre 100."
                ),
                "formula": (
                    f"({formato(numero)} × {formato(tasa)}) / 100"
                )
            })

            pasos.append({
                "titulo": "Resultado del porcentaje",
                "explicacion": "Realizamos las operaciones indicadas.",
                "formula": (
                    f"{formato(numero * tasa)} / 100 "
                    f"= {formato(resultado)}"
                )
            })

        # RAIZ CUADRADA

        elif nombre in ("raiz", "sqrt"):

            numero = argumentos[0]

            pasos.append({
                "titulo": "Radicacion",
                "explicacion": (
                    f"Buscamos el numero que multiplicado por si mismo "
                    f"produce {formato(numero)}."
                ),
                "formula": (
                    f"√{formato(numero)} = {formato(resultado)}"
                )
            })

        # RAIZ DE CUALQUIER INDICE

        elif nombre == "raiz_n":

            numero, indice = argumentos

            pasos.append({
                "titulo": "Raiz de indice n",
                "explicacion": (
                    f"Buscamos un numero que elevado a "
                    f"{formato(indice)} produzca {formato(numero)}."
                ),
                "formula": (
                    f"raiz_n({formato(numero)}, {formato(indice)}) "
                    f"= {formato(resultado)}"
                )
            })

        # VALOR ABSOLUTO

        elif nombre == "abs":

            numero = argumentos[0]

            pasos.append({
                "titulo": "Valor absoluto",
                "explicacion": (
                    "Calculamos la distancia del numero al cero, "
                    "sin considerar su signo."
                ),
                "formula": (
                    f"|{formato(numero)}| = {formato(resultado)}"
                )
            })

        return resultado

    # --------------------------------------------------------
    # COMPARACIONES
    # --------------------------------------------------------

    if isinstance(nodo, ast.Compare):

        a = evaluar(nodo.left, pasos)

        for op, comp in zip(
            nodo.ops,
            nodo.comparators
        ):

            b = evaluar(comp, pasos)

            if isinstance(op, ast.Eq):
                ok, simbolo = a == b, "=="

            elif isinstance(op, ast.NotEq):
                ok, simbolo = a != b, "!="

            elif isinstance(op, ast.Lt):
                ok, simbolo = a < b, "<"

            elif isinstance(op, ast.LtE):
                ok, simbolo = a <= b, "<="

            elif isinstance(op, ast.Gt):
                ok, simbolo = a > b, ">"

            elif isinstance(op, ast.GtE):
                ok, simbolo = a >= b, ">="

            else:
                raise ValueError("Comparacion no permitida.")

            pasos.append({
                "titulo": "Comparacion matematica",
                "explicacion": (
                    f"Comparamos {formato(a)} con {formato(b)}."
                ),
                "formula": (
                    f"{formato(a)} {simbolo} {formato(b)} "
                    f"= {formato(ok)}"
                )
            })

            if not ok:
                return False

            a = b

        return True

    # --------------------------------------------------------
    # OPERACIONES LOGICAS AND
    # --------------------------------------------------------

    if isinstance(nodo, ast.BoolOp) and isinstance(nodo.op, ast.And):

        for elemento in nodo.values:

            valor = evaluar(elemento, pasos)

            if not valor:

                pasos.append({
                    "titulo": "Logica AND",
                    "explicacion": (
                        "AND necesita que todas las condiciones "
                        "sean verdaderas. Una condicion es falsa."
                    ),
                    "formula": "AND = Falso"
                })

                return False

        pasos.append({
            "titulo": "Logica AND",
            "explicacion": (
                "Todas las condiciones son verdaderas."
            ),
            "formula": "AND = Verdadero"
        })

        return True

    # --------------------------------------------------------
    # OPERACIONES LOGICAS OR
    # --------------------------------------------------------

    if isinstance(nodo, ast.BoolOp) and isinstance(nodo.op, ast.Or):

        for elemento in nodo.values:

            valor = evaluar(elemento, pasos)

            if valor:

                pasos.append({
                    "titulo": "Logica OR",
                    "explicacion": (
                        "OR es verdadero porque al menos una "
                        "condicion es verdadera."
                    ),
                    "formula": "OR = Verdadero"
                })

                return True

        pasos.append({
            "titulo": "Logica OR",
            "explicacion": (
                "Todas las condiciones son falsas."
            ),
            "formula": "OR = Falso"
        })

        return False

    raise ValueError("Operacion matematica no compatible.")


# ============================================================
# 9. CALCULAR Y GENERAR PROCEDIMIENTOS
# ============================================================

def calcular_con_procedimiento(texto):

    expresion = preparar(texto)

    arbol = ast.parse(
        expresion,
        mode="eval"
    )

    validar(arbol)

    pasos = []

    resultado = evaluar(
        arbol,
        pasos
    )

    return resultado, pasos


# ============================================================
# 10. ESTADO DE LA APLICACION
# ============================================================

if "operacion" not in st.session_state:
    st.session_state.operacion = ""

if "resultado_calculo" not in st.session_state:
    st.session_state.resultado_calculo = None

if "historial" not in st.session_state:
    st.session_state.historial = []


def insertar(valor):

    st.session_state.operacion += valor

    st.session_state.resultado_calculo = None


def borrar():

    st.session_state.operacion = (
        st.session_state.operacion[:-1]
    )

    st.session_state.resultado_calculo = None


def limpiar():

    st.session_state.operacion = ""

    st.session_state.resultado_calculo = None


def ejecutar_calculo():

    texto = st.session_state.operacion.strip()

    if not texto:

        st.session_state.resultado_calculo = {
            "error": "Primero debes escribir una operacion."
        }

        return

    try:

        resultado, pasos = calcular_con_procedimiento(texto)

        datos = {
            "operacion": texto,
            "resultado": formato(resultado),
            "pasos": pasos
        }

        st.session_state.resultado_calculo = datos

        st.session_state.historial.insert(
            0,
            datos.copy()
        )

        st.session_state.historial = (
            st.session_state.historial[:20]
        )

    except Exception as error:

        st.session_state.resultado_calculo = {
            "error": str(error)
        }


# ============================================================
# 11. ENCABEZADO
# ============================================================

st.markdown(
    """
    <div style="text-align:center; padding:15px 0;">

        <h1 style="font-size:45px;">
            <span style="color:#087BFF;">A</span>
            <span style="color:#FFD928;">+</span>
            CLASSNOTE
        </h1>

        <h4 style="color:#AFC7E8;">
            Calculadora matemática paso a paso
        </h4>

        <p>
            Resuelve tus problemas y comprende cada procedimiento.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# 12. ENTRADA
# ============================================================

st.subheader("✏️ ESCRIBE TU OPERACION")

st.text_input(
    "Operacion matematica",
    key="operacion",
    placeholder="Ejemplo: (8)(8^2)/6"
)

st.caption(
    "Puedes escribir directamente o utilizar el teclado inferior."
)


# ============================================================
# 13. TECLADO MATEMATICO
# ============================================================

st.subheader("⌨️ TECLADO MATEMATICO")

botones = [

    [
        ("AC", "AC"),
        ("BORRAR", "BORRAR"),
        ("(", "("),
        (")", ")")
    ],

    [
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("÷", "÷")
    ],

    [
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("×", "×")
    ],

    [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("−", "−")
    ],

    [
        ("0", "0"),
        (".", "."),
        ("%", "%"),
        ("+", "+")
    ],

    [
        ("POTENCIA", "^"),
        ("RAIZ", "raiz("),
        ("AND", " and "),
        ("OR", " or ")
    ],

    [
        ("NOT", " not "),
        ("<", "<"),
        (">", ">"),
        ("=", "CALCULAR")
    ]
]

for fila_numero, fila in enumerate(botones):

    columnas = st.columns(4)

    for columna_numero, (titulo, valor) in enumerate(fila):

        with columnas[columna_numero]:

            if valor == "AC":

                st.button(
                    titulo,
                    key=f"ac_{fila_numero}",
                    on_click=limpiar,
                    use_container_width=True
                )

            elif valor == "BORRAR":

                st.button(
                    titulo,
                    key=f"borrar_{fila_numero}",
                    on_click=borrar,
                    use_container_width=True
                )

            elif valor == "CALCULAR":

                st.button(
                    titulo,
                    key=f"igual_{fila_numero}",
                    on_click=ejecutar_calculo,
                    use_container_width=True
                )

            else:

                st.button(
                    titulo,
                    key=f"tecla_{fila_numero}_{columna_numero}",
                    on_click=insertar,
                    args=(valor,),
                    use_container_width=True
                )


# ============================================================
# 14. BOTON PRINCIPAL
# ============================================================

st.divider()

st.button(
    "🟡 CALCULAR OPERACION",
    key="calcular_principal",
    on_click=ejecutar_calculo,
    use_container_width=True
)


# ============================================================
# 15. MOSTRAR RESULTADO Y PROCEDIMIENTO
# ============================================================

datos = st.session_state.resultado_calculo

if datos:

    if "error" in datos:

        st.error(datos["error"])

    else:

        st.divider()

        st.markdown(
            """
            <h2 style="color:#FFD928;">
                📊 RESULTADO
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="resultado">

                <p style="color:#AFC7E8;">
                    RESULTADO FINAL
                </p>

                <h1>{datos["resultado"]}</h1>

            </div>
            """,
            unsafe_allow_html=True
        )

        # PROCEDIMIENTO

        st.divider()

        st.markdown(
            """
            <h2 style="color:#FFD928;">
                📚 PROCEDIMIENTO MATEMATICO
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.write("**Operacion original:**")

        st.code(datos["operacion"])

        if datos["pasos"]:

            for numero, paso in enumerate(
                datos["pasos"],
                start=1
            ):

                st.markdown(
                    f"""
                    <div class="procedimiento">

                        <h4 style="color:#FFD928;">
                            PASO {numero}: {paso["titulo"]}
                        </h4>

                        <p>
                            {paso["explicacion"]}
                        </p>

                        <h4 style="color:#FFFFFF;">
                            {paso["formula"]}
                        </h4>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "Esta operacion no necesita pasos intermedios."
            )

        st.success(
            f"RESULTADO FINAL: {datos['resultado']}"
        )


# ============================================================
# 16. HISTORIAL
# ============================================================

st.divider()

st.subheader("🕘 HISTORIAL DE OPERACIONES")

if st.session_state.historial:

    for numero, registro in enumerate(
        st.session_state.historial,
        start=1
    ):

        with st.expander(
            f"Operacion {numero}: {registro['operacion']}"
        ):

            st.write(
                "**Operacion:**",
                registro["operacion"]
            )

            st.write(
                "**Resultado:**",
                registro["resultado"]
            )

            for i, paso in enumerate(
                registro["pasos"],
                start=1
            ):

                st.write(
                    f"Paso {i}: {paso['titulo']}"
                )

                st.write(paso["explicacion"])
                st.code(paso["formula"])

else:

    st.info(
        "Aun no tienes operaciones en el historial."
    )


# ============================================================
# 17. GUIA DE UTILIZACION
# ============================================================

st.divider()

st.subheader("📖 GUIA DE UTILIZACION")

st.markdown("""
| Operacion | Como escribirla |
|---|---|
| Suma | `8+5` |
| Resta | `10-4` |
| Multiplicacion | `5*6` |
| Multiplicacion implicita | `5(7)` |
| Division | `20/4` |
| Potenciacion | `2^3` |
| Raiz cuadrada | `raiz(81)` |
| Raiz de indice | `raiz_n(27,3)` |
| Porcentaje | `porcentaje(200,15)` |
| Porcentaje directo | `200*15%` |
| Promedio | `promedio(4,6,8)` |
| Valor absoluto | `abs(-25)` |
| Comparacion | `8>5` |
| Logica AND | `5>3 and 8>4` |
| Logica OR | `5<3 or 8>4` |
| Logica NOT | `not 5>3` |
""")

st.info(
    "Recuerda: utiliza ^ para las potencias y raiz() "
    "para las raices cuadradas."
)


# ============================================================
# 18. PIE DE PAGINA
# ============================================================

st.markdown(
    """
    <div class="pie">

        <h3 style="color:#FFD928;">
            CLASSNOTE
        </h3>

        Calculadora matemática creada por Angel.

        <br>

        Desarrollada con Python y Streamlit.

        <br>

        © 2026 CLASSNOTE

    </div>
    """,
    unsafe_allow_html=True
)
