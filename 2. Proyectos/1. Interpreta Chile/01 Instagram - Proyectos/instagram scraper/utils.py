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


def extraer_comentarios_desde_lista(lista_textos):
    resultados = []
    for texto in lista_textos:
        lineas = texto.split('\n')
        nombre_actual = None
        comentario_actual = []

        ignorar = {'Me gusta', 'Responder'}
        
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
            if any(palabra in linea for palabra in ignorar):
                continue
            if linea.endswith('sem') or linea.endswith('semResponder'):
                continue
            
            if ' ' not in linea and not any(char.isdigit() for char in linea) and not any(c in linea for c in ['😂','🤮','🎪','🆘']):
                if nombre_actual is not None:
                    resultados.append([nombre_actual, ' '.join(comentario_actual).strip()])
                nombre_actual = linea
                comentario_actual = []
            else:
                comentario_actual.append(linea)
        
        if nombre_actual is not None:
            resultados.append([nombre_actual, ' '.join(comentario_actual).strip()])
    return resultados


# resultado = extraer_comentarios_desde_lista(texto_scrap)
# for r in resultado:
#     print(r)