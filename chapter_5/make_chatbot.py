from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from bs4 import BeautifulSoup
import requests
import spacy

# Cargar el modelo específico de spaCy
nlp = spacy.load("en_core_web_sm")
import en_core_web_sm
nlp = en_core_web_sm.load()
doc = nlp("This is a sentence.")
print([(w.text, w.pos_) for w in doc])

print("spaCy cargado correctamente.")

print(type(nlp))


# Crear un objeto ChatBot
chatbot = ChatBot("CyberLaunch")

# Crear un entrenador para el chatbot
trainer = ListTrainer(chatbot)

# Obtener datos del sitio web (suponiendo que 'https://www.zoho.com/desk/knowledge-management-software.html' está activo)
page = requests.get('https://www.zoho.com/desk/knowledge-management-software.html')
#print('web_scan_page:',page)

soup = BeautifulSoup(page.content, 'lxml')

# Encontrar todos los elementos h2 que contienen preguntas
h2_elements = soup.find_all('h2', text=lambda text: text and text.strip().endswith('?'))
preguntas = [h2.get_text(strip=True) for h2 in h2_elements]

# Encontrar las respuestas que siguen a cada h2
respuestas = []
for h2 in h2_elements:
    # Obtener todos los elementos hermanos siguientes hasta el siguiente h2
    siguientes_elementos = h2.find_next_siblings()
    
    # Recolectar texto de los elementos hermanos hasta el siguiente h2 o párrafo
    respuesta_texto = ""
    for siguiente_elemento in siguientes_elementos:
        if siguiente_elemento.name == 'h2':
            break
        elif siguiente_elemento.name == 'p':
            
            respuesta_texto = siguiente_elemento.get_text(strip=True)
            break
        else:
            respuesta_texto += str(siguiente_elemento)
    # Replace empty answers with "Vacio"
    if not respuesta_texto:
        respuesta_texto = 'Null'



    respuestas.append(respuesta_texto.strip())
    #print('respuesta: -->',respuestas)

# Lista para almacenar preguntas y respuestas
# Lista para almacenar preguntas y respuestas
data = []

# Imprimir preguntas y respuestas
for i, (pregunta, respuesta) in enumerate(zip(preguntas, respuestas), 1):
    print(f"Pregunta {i}: {pregunta}")
    print(f"Respuesta {i}: {respuesta}\n")

    # Agregar pregunta y respuesta a la lista
    data.append(pregunta)
    data.append(respuesta)
    # Entrenar al chatbot
    #trainer.train(data)
    
    #trainer.train([pregunta])


print("##############################################################")

# Reemplazar campos vacíos con 'NA'
data = ['NA' if not item else item for item in data]
conversations = [[data[i], data[i + 1]] for i in range(0, len(data), 2)]

print("Contenido de data:", conversations)
trainer.train(conversations)

# Hacer preguntas de muestra al chatbot
for _ in range(2):
    pregunta = input('¿En qué puedo ayudarte?\n')
    respuesta = chatbot.get_response(pregunta)
    print(respuesta)

"""
#print('soup', soup)
faq_entries = soup.find_all(class_="content-wrap")
#print('faq:',faq_entries)
# Parsear y entrenar el chatbot
for entry in faq_entries:
    qa = entry.get_text().replace('\xa0', '').split('  \n\n')
    question = qa[0].replace('\n', '')
    answer = qa[1].replace('\n', ' ').replace('   ', '')

    # Imprimir preguntas y respuestas
    print(question)
    print(answer)

    # Entrenar al chatbot
    trainer.train([question, answer])

# Hacer preguntas de muestra al chatbot
for _ in range(2):
    question = input('¿En qué puedo ayudarte?\n')
    response = chatbot.get_response(question)
    print(response)
"""