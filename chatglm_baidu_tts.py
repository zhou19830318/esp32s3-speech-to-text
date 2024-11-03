import network
import time
import urequests as requests
import ujson as json
import gc
from machine import I2S, Pin
#from play_audio import AudioPlayer

# Constants
SSID = 'xxx'  # replace with your wifi SSID
PASSWORD = 'xxx'  # replace with your wifi PWD
BUFFER_SIZE = 8192
API_KEY = "xxx"  # Replace with your ZhipuAI API key

# I2S configuration max98357
SCK_PIN = 2
WS_PIN = 3
SD_PIN = 4
SAMPLE_RATE = 8000  # Deepgram sample_rate options: 8000, 16000, 24000
BITS = 16  # 16 or 32 bits

# Initialize I2S
audio_out = I2S(0,
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
        if len(self.audio_buffer) >= BUFFER_SIZE * 8:  # 当缓存中的音频数据达到2秒时
            audio_out.write(self.audio_buffer)  # 播放缓存中的音频数据
        else:
            audio_out.write(self.audio_buffer)  # 播放缓存中的音频数据
        self.audio_buffer = b''  # 清空缓存
        #gc.collect()  # 播放每个音频块后释放内存
# Stream and play audio in chunks (manually read chunks from response)
# 在stream_and_play_audio_in_chunks函数中使用AudioPlayer类
class TextToAudio:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def url_encode(self, payload):
        """Manually URL encode the payload."""
        return '&'.join(f"{key}={value}" for key, value in payload.items())

    def get_access_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = f"grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}"
        response = requests.post(url, data=params)
        json_response = json.loads(response.content)
        return json_response.get("access_token", None)

    def convert_text_to_audio(self, text):
        url = "https://tsn.baidu.com/text2audio"
        
        access_token = self.get_access_token()
        if access_token:
            cuid = "xxxxx"
            payload = {
                'tok': access_token,
                'tex': text,
                'per': 0,
                'spd': 6,
                'pit': 5,
                'vol': 5,
                'aue': 5,  # Ensure this is set to return WAV format
                'cuid': cuid,
                'lan': 'zh',
                'ctp': 1
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*'
            }

            print("Payload:", payload)  # Debugging line
            encoded_payload = self.url_encode(payload).encode('utf-8')
            try:
                response = requests.post(url, headers=headers, data=encoded_payload)
                chunk_size = 1024  # 定义一个小的音频块大小来处理音频数据
                audio_player = AudioPlayer()  # 实例化AudioPlayer类
                print("Response Status Code:", response.status_code)
                if response.status_code == 200:
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
        "messages": [{"role": "user", "content": question}],
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
    api_key = "xxx"  # Deepgram API key
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
            api_key = "xxx"
            secret_key = "xxx"
            tta = TextToAudio(api_key, secret_key)
            tta.convert_text_to_audio(ai_response)
            gc.collect()  # Free up memory after each part
        else:
            print("Failed to get AI response. Please try again.")

        gc.collect()

if __name__ == "__main__":
    main()
