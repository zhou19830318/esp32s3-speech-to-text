import network
import time
import urequests as requests
import ujson as json
import gc
from machine import I2S, Pin
from play_audio import AudioPlayer

# Constants
SSID = '********'  # replace with your wifi SSID
PASSWORD = '********'  # replace with your wifi PWD
BUFFER_SIZE = 8192
API_KEY = "******************"  # Replace with your ZhipuAI API key

# I2S configuration max98357
SCK_PIN = 22
WS_PIN = 35
SD_PIN = 21
SAMPLE_RATE = 8000  # Deepgram sample_rate options: 8000, 16000, 24000
BITS = 16  # 16 or 32 bits

# Initialize I2S
audio_out = I2S(1,
                sck=Pin(SCK_PIN),
                ws=Pin(WS_PIN),
                sd=Pin(SD_PIN),
                mode=I2S.TX,
                bits=BITS,
                format=I2S.MONO,
                rate=SAMPLE_RATE,
                ibuf=BUFFER_SIZE * 2)

# WiFi connection
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to', SSID)
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print('Connected to', SSID)
    print('IP Address:', wlan.ifconfig()[0])

class AudioPlayer:
    def __init__(self):
        self.audio_buffer = b''  # 初始化音频缓存

    def play_audio_chunk(self, chunk):
        self.audio_buffer += chunk  # 将音频数据添加到缓存中
        if len(self.audio_buffer) >= BUFFER_SIZE * 4:  # 当缓存中的音频数据达到设定值时
            audio_out.write(self.audio_buffer)  # 播放缓存中的音频数据
        else:
            audio_out.write(self.audio_buffer)  # 播放缓存中的音频数据
        self.audio_buffer = b''  # 清空缓存
        #gc.collect()  # 播放每个音频块后释放内存
# Stream and play audio in chunks (manually read chunks from response)
# 在stream_and_play_audio_in_chunks函数中使用AudioPlayer类
def stream_and_play_audio_in_chunks(text, api_key):
    url = "https://api.deepgram.com/v1/speak?model=aura-asteria-en&encoding=linear16&sample_rate=8000"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {api_key}"
    }
    data = {
        "text": text
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        #if response.status_code == 200:
            #print("Streaming and playing audio in chunks...")
        chunk_size = 1024  # 定义一个小的音频块大小来处理音频数据
        audio_player = AudioPlayer()  # 实例化AudioPlayer类

        while True:
            audio_chunk = response.raw.read(chunk_size)  # 逐块读取响应中的音频数据
            if not audio_chunk:
                break  # 音频流结束
            audio_player.play_audio_chunk(audio_chunk)  # 使用AudioPlayer类播放每个音频块
            gc.collect()  # 播放每个音频块后释放内存
        #else:
            #print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        response.close()

# Split the AI response into manageable chunks
"""
def process_and_stream_tts(response_text, api_key):
    sentences = response_text.split('.')
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            #print(f"Generating and playing speech for: {sentence}")
            stream_and_play_audio_in_chunks(sentence, api_key)
            gc.collect()  # Free up memory after each part
"""
# Get AI response
def get_ai_response(question):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    payload = json.dumps({
        "model": "glm-4-flash",
        "messages": [{"role": "user", "content": question + " Answer without special symbols."}],
        "temperature": 0.7,
        "top_p": 1,
        "n": 1,
        "stream": False,
        "max_tokens": 1024,
        "presence_penalty": 0,
        "frequency_penalty": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=30)
        print("Status Code:", response.status_code)
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    
    except requests.exceptions.Timeout:
        print("Request to AI API timed out. Please try again.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    finally:
        response.close()
        gc.collect()

# Main loop
def main():
    api_key = "***************"  # replace by your Deepgram API key
    connect_wifi()

    while True:
        open_ai_question = input("Enter your question (or 'q' to quit): ")
        if open_ai_question.lower() == 'q':
            break

        print("Processing your question...")
        print("Getting AI response...")
        ai_response = get_ai_response(open_ai_question)
        if ai_response:
            print(f'AI Response: {ai_response}')
            #process_and_stream_tts(ai_response, api_key)
            stream_and_play_audio_in_chunks(ai_response, api_key)
            gc.collect()  # Free up memory after each part
        else:
            print("Failed to get AI response. Please try again.")

        gc.collect()

if __name__ == "__main__":
    main()
