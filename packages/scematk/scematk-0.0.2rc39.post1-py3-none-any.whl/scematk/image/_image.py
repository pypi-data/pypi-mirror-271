from abc import ABC, abstractmethod
from dask.array import Array
import matplotlib.pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar
import numpy as np
from numpy import ndarray
import os
from typing import List

class Image(ABC):
    def __init__(self, image: Array, info: dict, channel_names: List[str]) -> None:
        assert isinstance(image, Array), "image must be a dask array"
        assert image.ndim in [2, 3], "image must be 2D or 3D"
        assert isinstance(info, dict), "info must be a dictionary"
        if isinstance(channel_names, str):
            channel_names = [channel_names]
        assert isinstance(channel_names, list), "channel_names must be a list"
        assert all(isinstance(name, str) for name in channel_names), "all channel names must be strings"
        if image.ndim == 3:
            assert len(channel_names) == image.shape[2], "number of channel names must match number of channels in image"
        else:
            assert len(channel_names) == 1, "number of channel names must match number of channels in image"
        self.image = image
        self.info = info
        self.ndim = image.ndim
        self.shape = image.shape
        self.dtype = str(image.dtype)
        self.name = info.get('name', None)
        if 'mpp' in self.info:
            self.mpp = self.info['mpp']
        elif 'mpp-x' in self.info and 'mpp-y' in self.info:
            if self.info['mpp-x'] == self.info['mpp-y']:
                self.mpp = self.info['mpp-x']
        else:
            self.mpp = None
        self.channel_names = channel_names
        if 'channel_names' not in self.info:
            self.info['channel_names'] = self.channel_names

    def persist(self) -> None:
        return self.image.persist()

    def compute(self) ->  None:
        return self.image.compute()

    def rechunk(self, chunks: tuple) -> None:
        assert isinstance(chunks, tuple), "chunks must be a tuple"
        assert all(isinstance(chunk, int) for chunk in chunks), "all elements of chunks must be integers"
        assert len(chunks) == self.ndim, "length of chunks must match number of dimensions in image"
        assert all(chunk > 0 for chunk in chunks), "all elements of chunks must be positive"
        if self.ndim == 3:
            assert chunks[2] == len(self.channel_names), "third element of chunks must match number of channels in image"
        self.image = self.image.rechunk(chunks)

    def pixel_from_micron(self, micron: float) -> float:
        assert isinstance(micron, (int, float)), "micron must be a number"
        assert micron > 0, "micron must be positive"
        if not self.mpp or not isinstance(self.mpp, (int, float)):
            raise ValueError("Microns per pixel (mpp) not available")
        return micron / self.mpp

    def read_region(self, y_min: int, x_min: int, y_len: int, x_len: int, pad: bool = True, channel: str = None) -> ndarray:
        assert isinstance(y_min, int), "y_min must be an integer"
        assert isinstance(x_min, int), "x_min must be an integer"
        assert isinstance(y_len, int), "y_len must be an integer"
        assert isinstance(x_len, int), "x_len must be an integer"
        assert isinstance(pad, bool), "pad must be a boolean"
        assert isinstance(channel, (str, type(None))), "channel must be a string or None"
        assert y_min >= 0 or pad, "y_min must be non-negative if no padding is being applied"
        assert x_min >= 0 or pad, "x_min must be non-negative if no padding is being applied"
        assert y_len > 0, "y_len must be positive"
        assert x_len > 0, "x_len must be positive"
        assert y_min + y_len <= self.shape[0] or pad, "y_min + y_len must be less than or equal to the height of the image if no padding is being applied"
        assert x_min + x_len <= self.shape[1] or pad, "x_min + x_len must be less than or equal to the width of the image if no padding is being applied"
        assert channel is None or channel in self.channel_names, "channel must be one of the channel names"
        y_pad = [0, 0]
        x_pad = [0, 0]
        y_pad[0] = max(0, -y_min) if y_min < 0 else 0
        y_pad[1] = max(0, y_min + y_len - self.shape[0]) if y_min + y_len > self.shape[0] else 0
        x_pad[0] = max(0, -x_min) if x_min < 0 else 0
        x_pad[1] = max(0, x_min + x_len - self.shape[1]) if x_min + x_len > self.shape[1] else 0
        y_max = min(self.shape[0], y_min + y_len)
        x_max = min(self.shape[1], x_min + x_len)
        y_min = max(0, y_min)
        x_min = max(0, x_min)
        region = self.image[y_min:y_max, x_min:x_max].compute()
        if pad:
            if self.ndim == 2:
                region = np.pad(region, ((y_pad[0], y_pad[1]), (x_pad[0], x_pad[1])), mode='constant', constant_values=0)
            else:
                region = np.pad(region, ((y_pad[0], y_pad[1]), (x_pad[0], x_pad[1]), (0, 0)), mode='constant', constant_values=0)
        if channel:
            if self.ndim == 2:
                raise ValueError("Cannot specify channel for single channel image")
            channel_index = self.channel_names.index(channel)
            region = region[..., channel_index]
        return region

    def show_region(self, y_min: int, x_min: int, y_len: int, x_len:int, pad: bool = True, channel: str = None, scalebar: bool = True, scalebar_location: str = "lower right") -> None:
        assert isinstance(scalebar, bool), "scalebar must be a boolean"
        assert isinstance(scalebar_location, str), "scalebar_location must be a string"
        if not "mpp" in self.info:
            scalebar = False
        region = self.read_region(y_min, x_min, y_len, x_len, pad, channel)
        channel_names = self.channel_names
        if len(channel_names) == 1 or channel:
            region = np.squeeze(region)
            cmap = 'gray'
        elif len(channel_names) == 2 and not channel:
            region = np.pad(region, ((0, 0), (0, 0), (1, 0)), mode='constant', constant_values=0)
            cmap = None
        elif len(channel_names) == 3 and not channel:
            cmap = None
        else:
            raise NotImplementedError("Only 1, 2, or 3 channels supported")
        plt.imshow(region, cmap=cmap)
        if scalebar:
            scalebar = ScaleBar(self.mpp, units='µm', location=scalebar_location, length_fraction=0.1, border_pad=0.5)
            plt.gca().add_artist(scalebar)
        plt.axis('off')
        plt.show()

    @abstractmethod
    def get_thumb(self):
        pass

    @abstractmethod
    def show_thumb(self) ->  None:
        pass

    def _repr_html_(self) -> str:
        colour_map = {
            "Red": "#FF0000",
            "Green": "#00FF00",
            "Blue": "#0000FF",
            "Hematoxylin": "#2A2670",
            "Eosin": "#E63DB7",
            "DAB": "#813723"
        }
        channel_names = []
        for colour in self.channel_names:
            if colour in colour_map:
                channel_names.append(f'<span style="color: {colour_map[colour]};">{colour}</span>')
            else:
                channel_names.append(colour)
        total_width = 400
        icon_url = 'https://github.com/SCEMA-WSI/scematk/blob/main/src/scematk/image/_icons/temp_icon.png'
        html = f'''
        <div style="width: {total_width}px; background-color: #202020; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
            <h1>SCEMATK Image Object</h1>
            <div style="display: flex; justify-content: space-between;">
                <div style="flex: 2;">
                    <p>Name: {self.name if self.name else "SCEMATK Image"}</p>
                    <p>Format: {self.info.get('format', 'Unknown').title()}</p>
                    <p>Channels: {", ".join(channel_names)}</p>
                    <p>Dimensions: {" x ".join([f"{i:,}" for i in self.shape])}</p>
                    <p>Chunks: {" x ".join([f"{i:,}" for i in self.image.chunksize[:2]])}
                    <p>Data Type: {self.dtype}</p>
                </div>
                <div style="flex: 1;">
                    <img src="{icon_url}" style="max-width: 100%; height: auto; margin-top: 10px;">
                </div>
            </div>
        </div>
        '''
        return html
