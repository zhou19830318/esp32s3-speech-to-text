Table of Contents
Prerequisites
Hardware Setup
Software Setup
Running the System
Customization
Troubleshooting
Prerequisites
Before starting, ensure you have the following:

ESP32 Development Board (e.g., ESP32 DevKitC)
MAX98357 I2S DAC (or compatible I2S audio output device)
Microphone or speaker connected via I2S for audio output
WiFi credentials (SSID and password)
API keys:
ZhipuAI API key (for AI response generation)
Deepgram API key (for text-to-speech conversion)
Software Dependencies
MicroPython installed on your ESP32.
uRequests and uJSON modules for HTTP requests and JSON parsing.
Machine module for I2S control.
Hardware Setup
ESP32 Pin Configuration:
Pin	Function
GPIO22	I2S Clock (SCK)
GPIO35	I2S Word Select (WS)
GPIO21	I2S Serial Data (SD)
Connect your I2S DAC (e.g., MAX98357) to these pins on your ESP32.
Software Setup
Step 1: Install MicroPython
Download and flash MicroPython firmware onto your ESP32. Refer to the official MicroPython documentation for ESP32 for installation instructions.

Set up a terminal to interact with the ESP32 using a serial terminal such as Thonny, PuTTY, or screen.

Step 2: Upload the Code
Open the provided Python script in your editor.
Upload the code to the ESP32 using Thonny or ampy.
Ensure you replace the placeholder API keys (********) in the script with your actual API keys for ZhipuAI and Deepgram.
Step 3: Install Dependencies
Ensure your MicroPython environment includes the following libraries:

uRequests for HTTP requests
uJSON for JSON parsing
gc for garbage collection
These libraries are usually built-in for MicroPython. If not, you can manually install them.

Step 4: I2S Audio Player
This script uses I2S to output audio from your ESP32. If you're using a different I2S DAC or audio hardware, ensure it's configured correctly and supports 8 kHz, 16-bit mono audio.

Running the System
WiFi Connection: On boot, the system will attempt to connect to WiFi using the SSID and password defined in the script.
AI Question: Once connected, you'll be prompted to enter a question. The system will then send the question to the ZhipuAI service and receive an AI-generated response.
Text-to-Speech: The response is then sent to the Deepgram API for text-to-speech conversion. Audio data is streamed in chunks and played through the I2S audio output.
Loop: This process continues, asking for new questions until 'q' is entered to quit the program.
Customization
1. Change WiFi Credentials:
Update the SSID and PASSWORD constants with your WiFi credentials to enable the system to connect to the network.

2. Change API Keys:
Replace the placeholder API_KEY with your ZhipuAI API key.
Replace Deepgram API key in the stream_and_play_audio_in_chunks function to match your Deepgram account.
3. Adjust Audio Parameters:
The audio is streamed at 8 kHz with 16-bit depth. To change the sample rate or format, adjust the SAMPLE_RATE and BITS constants.

4. Modify AI Model:
You can modify the request payload in the get_ai_response() function to ask different types of questions or interact with other APIs if needed.

Troubleshooting
WiFi Connection Issue:

Ensure that your SSID and password are correctly entered.
Check that the ESP32 is in range of the WiFi network.
Audio Not Playing:

Double-check the I2S wiring between the ESP32 and the audio output device.
Make sure that the correct pins for SCK, WS, and SD are configured in the script.
AI Response Error:

Verify that your API key for ZhipuAI is correct.
Ensure your internet connection is stable and capable of making requests to the API.
Conclusion
This project demonstrates how to use an ESP32 to interface with an AI-powered chat service and convert the responses into speech, which is then outputted through an I2S audio device. The system can be easily customized and extended to include additional features such as more advanced TTS options, user-specific AI models, and improved memory management.
