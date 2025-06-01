
import re



def limpiar_comentario(texto):
    # Primer split: separa usuario y comentario sucio
    partes = texto.split("\n", 1)
    usuario = partes[0]
    comentario_sucio = partes[1] if len(partes) > 1 else ""

    # Buscar los dos últimos '\n' desde la derecha
    ultima_n = comentario_sucio.rfind("\n")
    penultima_n = comentario_sucio.rfind("\n", 0, ultima_n)

    if ultima_n != -1 and penultima_n != -1:  # Si hay dos saltos de línea
        return [usuario, comentario_sucio[:penultima_n], comentario_sucio[penultima_n+1:ultima_n], comentario_sucio[ultima_n+1:]]
    elif ultima_n != -1:  # Si solo hay un salto de línea
        return [usuario, "", comentario_sucio[:ultima_n], comentario_sucio[ultima_n+1:]]
    else:  # Si no hay saltos de línea adicionales
        return [usuario, "",comentario_sucio, comentario_sucio[:ultima_n]]

    
def completar_lista(lista):
    # Verificamos si el tercer elemento (índice 2) contiene un número seguido de un espacio y una letra (ej. "1 h")
    if len(lista) > 2 and ' ' in lista[2]:  
        # Si la lista tiene solo 3 elementos, significa que falta el segundo
        if len(lista) == 3:
            lista.insert(1, " ")  # Insertamos un espacio en la posición 1
    return lista



# def modelamiento (texto):

#     resultados = []

#     partes = texto.split('\n', 1)
#     nombre_usuario = partes[0].strip()
    
#     # Paso 3: Obtener el bloque de datos restantes
#     bloque_datos = partes[1]  # Asumimos que siempre habrá al menos una fecha

#     # Paso 5: Hacer un split del bloque de datos por el último salto de línea
#     lista_datos = bloque_datos.rsplit('\n', 1)
#     ultimo_datos = [lista_datos[-1]]

#     hora = None
# # Intentar reemplazar un espacio
#     for ultimo in ultimo_datos:
#         cambio = ultimo.replace(" ", "")

#         # Comprobar si hubo un cambio
#         if cambio != ultimo:
#             hora = cambio
#             reacciones = 0
#         else:
#             reacciones = cambio
    
#     if hora is None:
#         hora = "Pendiente"
 
#     resultados.append([nombre_usuario,bloque_datos,hora, reacciones]) 
        

#     return resultados


def modelamiento(texto):
    resultados = []

    partes = texto.split('\n', 1)
    nombre_usuario = partes[0].strip()

    # Validar que partes tenga al menos 2 elementos (nombre_usuario y bloque_datos)
    if len(partes) > 1:
        bloque_datos = partes[1]  # Asumimos que siempre habrá al menos una fecha o comentario

        # Paso 5: Hacer un split del bloque de datos por el último salto de línea
        lista_datos = bloque_datos.rsplit('\n', 1)
        ultimo_datos = [lista_datos[-1]]

        hora = None
        # Intentar reemplazar un espacio
        for ultimo in ultimo_datos:
            cambio = ultimo.replace(" ", "")

            # Comprobar si hubo un cambio
            if cambio != ultimo:
                hora = cambio
                reacciones = 0
            else:
                reacciones = cambio

        if hora is None:
            hora = "Pendiente"
    else:
        # Si no hay bloque de datos, asignar valores por defecto o vacíos
        bloque_datos = ""
        hora = "Pendiente"
        reacciones = 0

    resultados.append([nombre_usuario, bloque_datos, hora, reacciones])

    return resultados





def limpiar_comentarios_(data_cruda):
    datos_limpios = []

    for bloque in data_cruda:
        lineas = bloque.strip().split("\n")

        usuario = None
        comentario = []
        likes = 1  # valor por defecto si solo dice "Me gusta"

        for linea in lineas:
            linea = linea.strip()

            # Detectar nombre de usuario con "X sem"
            match_usuario = re.match(r'^([a-zA-Z0-9._]+)\s+\d+\s+sem$', linea)
            if match_usuario:
                usuario = match_usuario.group(1)
                continue

            # Detectar nombre de usuario sin fecha (casos raros como "eldiablodelcanto")
            if not usuario and re.match(r'^[a-zA-Z0-9._]+$', linea):
                usuario = linea
                continue

            # Detectar likes con número
            match_likes = re.match(r'^(\d+)\s+Me gusta$', linea)
            if match_likes:
                likes = int(match_likes.group(1))
                continue

            # Ignorar líneas innecesarias
            if "Responder" in linea or "Ver las" in linea:
                continue

            # Agregar comentario si no está vacío
            if linea and "Me gusta" not in linea:
                comentario.append(linea)

        if usuario and comentario:
            texto = " ".join(comentario).strip()
            datos_limpios.append([usuario, texto, likes])

    return datos_limpios