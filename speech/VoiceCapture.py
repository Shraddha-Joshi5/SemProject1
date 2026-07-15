import pyaudio
import wave
import os
from datetime import datetime
from faster_whisper import WhisperModel


class VoiceCapture:
    """
    Captures audio from microphone and transcribes using faster-whisper.
    Optimized for CPU inference with int8 quantization.
    """
    def __init__(self, model_size='base', device='cpu', compute_type='int8', language='ne'):
        self.model_size = model_size
        self.device = device
        self.language = language
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.audio_dir = 'data/audio'
        os.makedirs(self.audio_dir, exist_ok=True)

    def __repr__(self):
        return f"VoiceCapture(model={self.model_size}, device={self.device}, lang={self.language})"

    def record_audio(self, duration=5, sample_rate=16000, channels=1, chunk=1024):
        """
        Records audio from microphone for specified duration.
        Returns: audio file path
        """
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk
        )
        frames = []
        try:
            print(f"Recording for {duration}s...")
            for _ in range(int(sample_rate / chunk * duration)):
                data = stream.read(chunk, exception_on_overflow=False)
                frames.append(data)
            print("Done.")
        finally:
            stream.stop_stream()
            stream.close()
            sample_width = p.get_sample_size(pyaudio.paInt16)
            p.terminate()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_path = os.path.join(self.audio_dir, f"audio_{timestamp}.wav")
        with wave.open(audio_path, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
        return audio_path

    def transcribe_audio(self, audio_path):
        """
        Convert audio file to text using Whisper.
        Returns: transcript string
        """
        segments, info = self.model.transcribe(
            audio_path,
            language=self.language,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )
        transcript = " ".join(segment.text for segment in segments)
        return transcript, info.language, info.language_probability

    def capture_and_transcribe(self, duration=5):
        """
        Complete workflow: record audio and transcribe it.
        Returns: (transcript, audio_file_path)
        """
        audio_path = self.record_audio(duration=duration)
        transcript, lang, confidence = self.transcribe_audio(audio_path)
        if confidence < 0.8:
            print(f"Warning: low language confidence ({confidence:.2f}), detected as '{lang}'")
        return transcript, audio_path