import soundfile
import tempfile
import shutil
import os
import json
from datetime import datetime
import numpy as np


class AFile(soundfile.SoundFile):
    def __init__(self, afile_path:str, mode:str="r", samplerate:int=None, channels:int=None, temp:bool=False) -> None:
        """The AFile class handles .wav sound files. Metadata is used to store and load additional settings.
        It is recommended to open AFile's in a with statement.

        Args:
            afile_path (str): Path to .wav file.
            mode ({"r", "r+", "w", "w+"}, optional): File open mode.
            samplerate (int, optional): Samplerate, only used in write mode.
            channels (int, optional): Channel count, only used in write mode.
            temp (bool): Set file temporary (deleted on close). Only used in write mode.

        Example:
            ```python linenums="1" title="Load a file"
            from asmu import AFile

            with AFile(AFILE_PATH) as afile:
                print(afile.data.shape)
            ```
        """
        self._afile_path = afile_path
        self.settings = {}
        if mode == "r":
            super().__init__(afile_path, mode=mode)
            # load settings
            if self.comment:
                self.settings = json.loads(self.comment)
        else:
            _name = os.path.split(afile_path)[1].replace(".wav", "")
            if temp:
                self._tmp = tempfile.NamedTemporaryFile(prefix=_name, suffix='.wav', dir="", delete=True)
                super().__init__(self._tmp, mode=mode, samplerate=samplerate, channels=channels, subtype="PCM_24", format="WAV")
            else:
                super().__init__(afile_path, mode=mode, samplerate=samplerate, channels=channels, subtype="PCM_24", format="WAV")
            now = datetime.now()
            # set wav metadata
            self.title = _name
            self.date = now.strftime("%d/%m/%Y %H:%M:%S")
    
    # store settings as json string in metadata "comment"
    @property
    def settings(self) -> dict:
        """Additional JSON settings in the metadata's comment field."""
        return self._settings
    @settings.setter
    def settings(self, value: dict) -> None:
        self._settings = value

    @property
    def latency(self) -> int:
        """Latency in samples."""
        try:
            return int(self.settings["latency"])
        except KeyError:
            return None
    @latency.setter
    def latency(self, value: int) -> None:
        self.settings["latency"] = int(value)

    @property
    def data(self) -> np.ndarray:
        """Data of AFile as numpy array of shape ("samples" x "channels")."""
        self.flush()
        self.seek(0)
        return self.read(dtype="float32", always_2d=True)
    
    def __exit__(self, *args):
        try:
            self.comment = json.dumps(self.settings)
        except soundfile.LibsndfileError:
            pass
        self.close()

    def cal_latency(self, time):
        """Calculate and store loopback latency without physical connection.

        !!! warning
            Dont rely on this method, as it only calculates the ADC/DAC's internal latency. 
            Use [latency_from_rec.py](../examples.md/#latency_from_recpy) to compare this result with the real loopback calibration.

        Args:
            time (CData): The time object given in the Interface callback function.
        """
        self.latency = round((time.outputBufferDacTime-time.inputBufferAdcTime)*self.samplerate + 1) # the +1 was measured experimentally (could be the cable?)
