import torch
import warnings, logging

from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import get_image_colorizer


class Model:

    def __init__(self):
        torch.hub.set_dir('models')
        device.set(device=DeviceId.CPU)
        warnings.filterwarnings('ignore')
        logging.disable(logging.CRITICAL)
        torch.backends.cudnn.benchmark = True
        self.model = get_image_colorizer(artistic=True)

    def colorize(self, path):
        params = {'render_factor': 35, 'watermarked': False}
        self.model.get_transformed_image(path, **params).save(path)