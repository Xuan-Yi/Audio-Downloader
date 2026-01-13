import subprocess
import threading
import time
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from pytubefix import YouTube
import os
import atexit

class PlayerSignals(QObject):
    state_changed = pyqtSignal(str, str)

class PreviewPlayer:
    def __init__(self):
        self.signals = PlayerSignals()
        self.process = None
        self.current_video_id = None
        self.current_url = None
        self._pending_id = None
        self._is_stopping = False
        self._is_paused = False
        self._state = "stopped"
        self._playback_position = 0.0
        self._play_start_time = None
        # Register atexit to ensure cleanup even if closeEvent is missed
        atexit.register(self.force_stop_all)

    def force_stop_all(self):
        """Forcefully kill any ffplay process started by the app."""
        try:
            # Kill by image name to be absolutely sure nothing remains
            subprocess.run(['taskkill', '/F', '/IM', 'ffplay.exe'], 
                         creationflags=0x08000000, capture_output=True)
        except:
            pass

    def play_preview(self, video_id, url, start_at: float = 0.0):
        self.stop()
        self._pending_id = video_id
        self._is_paused = False
        self._playback_position = max(0.0, start_at)
        self._play_start_time = time.monotonic() - self._playback_position
        self._set_buffering(video_id)
        
        thread = threading.Thread(
            target=self._fetch_and_start,
            args=(video_id, url, self._playback_position),
            daemon=True
        )
        thread.start()

    def _fetch_and_start(self, video_id, url, start_at: float):
        try:
            yt = YouTube(url)
            stream = yt.streams.get_audio_only()
            if stream and self._pending_id == video_id:
                cmd = ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet"]
                if start_at > 0:
                    cmd.extend(["-ss", f"{start_at:.3f}"])
                cmd.append(stream.url)
                creationflags = 0x08000000 # CREATE_NO_WINDOW
                
                if self._pending_id != video_id:
                    return

                proc = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=creationflags,
                )
                self.process = proc
                self.current_video_id = video_id
                self.current_url = url
                self._is_paused = False
                self._state = "playing"
                
                self.signals.state_changed.emit(video_id, "playing")
                
                proc.wait()

                if self.current_video_id == video_id and not self._is_stopping and self._state != "paused":
                    self._finalize_playback("ended", video_id)
            else:
                self._finalize_playback("stopped", video_id)
        except Exception as e:
            print(f"ffplay error: {e}")
            self._finalize_playback("stopped", video_id)

    def toggle(self, video_id, url):
        if self.current_video_id == video_id and self.current_url == url:
            if self.process:
                if self._state == "playing":
                    self.pause()
                elif self._state == "paused":
                    self._set_buffering(video_id)
                    self.resume()
                elif self._state == "buffering":
                    return
                else:
                    self.play_preview(video_id, url)
                return
            if self._state == "paused":
                self.play_preview(video_id, url, start_at=self._playback_position)
                return

        self.play_preview(video_id, url)

    def pause(self):
        if not self.process or self._is_paused or self._state != "playing":
            return
        try:
            self._is_paused = True
            if self._play_start_time is not None:
                self._playback_position = time.monotonic() - self._play_start_time
            if self.current_video_id:
                self._state = "paused"
                self.signals.state_changed.emit(self.current_video_id, "paused")
            pid = self.process.pid
            subprocess.run(['taskkill', '/F', '/T', '/PID', str(pid)],
                         creationflags=0x08000000, capture_output=True)
            self.process = None
            self._play_start_time = None
        except:
            pass

    def resume(self):
        if not self.process or not self._is_paused or self._state not in ("paused", "buffering"):
            return
        try:
            if self.process.stdin:
                self.process.stdin.write(b"p")
                self.process.stdin.flush()
            self._is_paused = False
            self._play_start_time = time.monotonic() - self._playback_position
            if self.current_video_id:
                self._state = "playing"
                self.signals.state_changed.emit(self.current_video_id, "playing")
        except:
            pass

    def stop(self):
        pending_id = self._pending_id
        self._pending_id = None
        if self._is_stopping:
            return
            
        self._is_stopping = True
        if self.process:
            try:
                pid = self.process.pid
                # Kill the specific process tree
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(pid)], 
                             creationflags=0x08000000, capture_output=True)
            except:
                pass
            self.process = None
            
        if self.current_video_id:
            self._finalize_playback("stopped", self.current_video_id)
        elif pending_id:
            self._finalize_playback("stopped", pending_id)
        
        self._is_stopping = False

    def _finalize_playback(self, state: str, video_id: str):
        if video_id:
            self.signals.state_changed.emit(video_id, state)
        self._pending_id = None
        self.process = None
        self.current_video_id = None
        self.current_url = None
        self._is_paused = False
        self._state = state
        self._play_start_time = None
        if state in ("stopped", "ended"):
            self._playback_position = 0.0

    def _set_buffering(self, video_id: str):
        self._state = "buffering"
        self.signals.state_changed.emit(video_id, "buffering")

    def get_playback_position(self, video_id: str):
        if self.current_video_id != video_id:
            return None
        if self._state == "playing" and self._play_start_time is not None:
            return max(0.0, time.monotonic() - self._play_start_time)
        if self._state in ("paused", "buffering"):
            return max(0.0, self._playback_position)
        return 0.0

# Global instance
preview_player = PreviewPlayer()
