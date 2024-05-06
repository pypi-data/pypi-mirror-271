import torch
import lightning as L

from bpnetlite.losses import MNLLLoss, log1pMSELoss
from bpnetlite.performance import calculate_performance_measures

from histomer.bpnet import BPNet
from histomer.chrombpnet import ChromBPNet




class EnformerModule(L.LightningModule):
    def __init__(self, n_outputs:int=2, n_control_tracks:int=2, trimming:int=(2114 - 1000) // 2):
        super().__init__()
        self.model = BPNet(n_outputs=n_outputs, n_control_tracks=n_control_tracks, trimming=trimming)