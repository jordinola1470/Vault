import re

class Utils():

    @staticmethod

    def limpiar_markdown(texto):
        # Elimina encabezados, asteriscos, guiones, etc.
        texto = re.sub(r'\*\*(.*?)\*\*', r'\1', texto)  # negrita
        texto = re.sub(r'\*(.*?)\*', r'\1', texto)      # cursiva
        texto = re.sub(r'#+\s?', '', texto)             # encabezados tipo ###
        texto = re.sub(r'`{1,3}(.*?)`{1,3}', r'\1', texto)  # código
        return texto

# response_texto_plano = limpiar_markdown(response.output_text)

# return {
#     "openai": response_texto_plano
# }