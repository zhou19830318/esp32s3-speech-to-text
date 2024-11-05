# Text-to-Speech with ESP32 and ZhipuAI

This project uses an ESP32 microcontroller to convert AI-generated text into speech. It utilizes the **Baidu TTS API** for text-to-speech synthesis and plays the generated audio using an **I2S-based audio player**. The text-to-speech conversion is performed by sending requests to the **ZhipuAI API** for generating AI responses.

## Features

- Connects to a WiFi network using the ESP32.
- Sends a question to the **ZhipuAI API** and retrieves a response.
- Converts the AI-generated text into speech using the **Baidu TTS API**.
- Plays the audio using an I2S audio interface with the **MAX98357A** DAC.
- Handles audio in small chunks for memory efficiency.

## Requirements

- **Hardware:**
  - ESP32 development board.
  - MAX98357A I2S audio DAC or any compatible I2S-based audio output.
  - Active WiFi connection.

- **Software:**
  - MicroPython installed on the ESP32.
  - Python packages: `urequests`, `ujson`, `gc`, `network`, and `machine`.

- **APIs:**
  - ZhipuAI (for AI text generation).
  - Baidu TTS (for text-to-speech conversion).

## Setup

1. **Wi-Fi Configuration:**
   - Replace `'xxx'` in the `SSID` and `PASSWORD` constants with your actual WiFi credentials.

2. **API Keys:**
   - Replace `'xxx'` in the `API_KEY` variable with your **ZhipuAI** API key.
   - Replace `'xxx'` in the `api_key` and `secret_key` fields inside the `main()` function with your **Baidu TTS API** credentials.
   
3. **I2S Audio Configuration:**
   - The code is configured to use an **I2S** connection to a MAX98357A DAC. You can modify the `SCK_PIN`, `WS_PIN`, and `SD_PIN` variables to suit your hardware.
   - The audio sample rate is set to `8000Hz` (you can change it to 16000Hz or 24000Hz depending on your needs).

## How to Use

1. Flash the MicroPython firmware onto the ESP32 board if you haven't already.
2. Upload this Python script to the ESP32 using any appropriate method, such as **Thonny** or **WebREPL**.
3. Connect the ESP32 to a serial terminal or a REPL interface.
4. Run the script. It will first connect to the WiFi and prompt you to enter a question for the AI.
5. The ESP32 will:
   - Send the question to the **ZhipuAI** API and receive an AI-generated response.
   - Convert the response text to speech using the **Baidu TTS API**.
   - Play the generated audio in chunks through the connected I2S DAC.

### Example Interaction

