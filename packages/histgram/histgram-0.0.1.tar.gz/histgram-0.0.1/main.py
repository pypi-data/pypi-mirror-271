from histogram.model.bpnet import BPNetModule
from histogram.model.chrombpnet import ChromBPNetModule
from histogram.data.data import HistoneDataModule

import lightning as L
from lightning.pytorch.cli import LightningCLI
from lightning.pytorch.loggers import TensorBoardLogger


class Model1(DemoModel):
    def configure_optimizers(self):
        print("⚡", "using Model1", "⚡")
        return super().configure_optimizers()


class Model2(DemoModel):
    def configure_optimizers(self):
        print("⚡", "using Model2", "⚡")
        return super().configure_optimizers()

def cli_main():
    cli = LightningCLI(seed_everything_default = 42, run=False)
                    #    parser_kwargs={"fit": {"default_config_files": ["config.yaml"]}}) 

if __name__ == '__main__':
    cli_main()
