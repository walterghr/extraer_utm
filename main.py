# Extraer coordenadas UTM de PDF ---update 2--- by WGHR.
from PyPDF2 import PdfFileReader
from conexion import borrar_db, crear_tabla, add_punto

# Extrae texto de PDF y lo devuelve como string
def leer_pdf(pdf_file="30197.pdf"):
    pdf_file, pdf_text = PdfFileReader(open(pdf_file, "rb")), ""
    for page in range(pdf_file.getNumPages()):
        pdf_text = pdf_text + pdf_file.getPage(page).extract_text() + " "
    return pdf_text

# Elimina los caracteres no deseados del string. Da formato a las coordenadas.
def formatear_texto(texto):
    texto = str(texto)
    texto = texto.replace("\n"," ")
    texto = texto.replace(" ","")
    texto = texto.replace("mEy","E")
    texto = texto.replace("mN","N")
    texto = texto.replace(",","")
    texto = texto.replace(";","")
    return texto

# Formato de coordenada UTM "000000000E0000000000N". Los ultimo 3 digitos es la parte decimal.
def obtener_puntos(texto):
    print(f"\nTexto en bruto:\n{texto}\n\nCoordenadas encontradas:")
    Este, Norte, Es_norte, orden = "", "", False, 1
    for letra in texto:
        try:
            int(letra)
            if len(Este) < 9 and Es_norte is False: Este = str(Este) + str(letra)
            if len(Norte) < 10 and Es_norte is True: Norte = str(Norte) + str(letra)            
        except:
            if len(Este) == 9 and letra == "E": Es_norte = True
            if len(Norte) == 10 and letra == "N" : # True: Coordenada completa!!!
                print(f"{orden}. {float(Este)/1000}E {float(Norte)/1000}N")
                add_punto(float(Este)/1000, float(Norte)/1000) #Añade a la tabla SQL
                Es_norte, orden = False, orden + 1
            if letra != "E": Este, Norte, Es_norte = "", "", False #Comprueba formato

borrar_db()
crear_tabla()
obtener_puntos((formatear_texto(leer_pdf())))