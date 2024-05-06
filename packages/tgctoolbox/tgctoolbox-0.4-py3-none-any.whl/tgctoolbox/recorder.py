try:
    import pyaudio

    PyAudio = pyaudio.PyAudio
except ImportError:
    PyAudio = None
import websocket
import threading
import time
from .logger import setup_custom_logger as TGCLoggerSetup

if PyAudio is None:
    raise ImportError(
        "The 'audio' extras are required to use this feature. "
        "Install them with: pip install tgctoolbox[audio]"
    )

# Constants for audio recording
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 16000  # Sampling rate
CHUNK = 1024  # Frames per buffer

# WebSocket URL
ws_url = "ws://localhost:8000/ws/transcribe_aai"

# Initialize PyAudio
audio = pyaudio.PyAudio()

logger = TGCLoggerSetup("recorder")


# WebSocket client
class WSClient(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.ws = websocket.WebSocketApp(
            url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ws.on_open = self.on_open
        logger.info(f"WebSocket client initialized: {self.ws.__dict__}")

    def run(self):
        self.ws.run_forever()

    def send_audio(self, data):
        if self.ws.sock and self.ws.sock.connected:
            self.ws.send(data, opcode=websocket.ABNF.OPCODE_BINARY)
        else:
            logger.info("WebSocket is not open. Cannot send data.")

    def on_message(self, ws, message):
        logger.info(f"Received: {message}")

    def on_error(self, ws, error):
        logger.error(error, exc_info=True)

    def on_close(self, ws, close_status_code, close_reason):
        logger.info("### closed ###")

    def on_open(self, ws):
        logger.info("WebSocket opened")
        logger.info("WebSocket opened")


def record_audio(ws_client):
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    logger.info("Recording...")

    try:
        while True:
            data = stream.read(CHUNK)
            ws_client.send_audio(data)

    except KeyboardInterrupt:
        logger.warning("Recording stopped by user request. Exiting...")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        ws_client.ws.close()


if __name__ == "__main__":
    ws_client = WSClient(ws_url)
    ws_client.start()

    time.sleep(1)  # Wait for the WebSocket connection to establish
    record_audio(ws_client)
