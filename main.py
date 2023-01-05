import pyaudio
import speech_recognition as sr
import requests

# Inicializa o objeto de reconhecimento de fala
r = sr.Recognizer()

# Inicializa o PyAudio
p = pyaudio.PyAudio()

# Seleciona o dispositivo de entrada (microfone)
device_index = None
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    if device_info["name"].lower() in ["microfone", "input"]:
        device_index = i
        break

if device_index is None:
    print("Não foi possível encontrar um dispositivo de entrada (microfone)")
    exit()

# Inicializa o motor de síntese de fala
engine = pyttsx3.init()

# Inicia o laço infinito
while True:
    # Inicializa o stream de áudio
    stream = p.open(
        input_device_index=device_index,
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024
    )

    # Lê os dados do stream
    data = stream.read(1024)

    # Fecha o stream
    stream.stop_stream()
    stream.close()

    # Converte os dados em um objeto AudioData
    audio_data = sr.AudioData(data, 44100, 2)

    # Reconhece o áudio
    text = r.recognize_google(audio_data)
    print(text)

    # Faz a requisição para o chatgpt
    response = requests.post('https://api.chatgpt.com/', json={'prompt': text})

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Obtém a resposta do chatgpt
        resposta = response.json()['response']
    else:
        resposta = f'Erro {response.status_code}: {response.text}'

    # Emite o som da resposta do chatgpt
    engine.say(resposta)
    engine.runAndWait()
