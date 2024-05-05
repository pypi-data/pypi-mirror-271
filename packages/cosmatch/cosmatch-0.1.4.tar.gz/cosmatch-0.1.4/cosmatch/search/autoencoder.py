import torch
import pytorch_lightning as L
from torch.utils.data import Dataset
from torchvision import datasets
import torch.optim as optim
import torch.nn as nn
import numpy as np

from typing import Union, Tuple


class DeepAutoencoder(nn.Module):
    def __init__(self, shape_0: int) -> None:
        input_dim = shape_0
        hidden_dim1 = 20
        hidden_dim2 = 10
        latent_dim = 2
        super(DeepAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim1),
            nn.ReLU(),
            nn.Linear(hidden_dim1, hidden_dim2),
            nn.ReLU(),
            nn.Linear(hidden_dim2, latent_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim2),
            nn.ReLU(),
            nn.Linear(hidden_dim2, hidden_dim1),
            nn.ReLU(),
            nn.Linear(hidden_dim1, input_dim),
            nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.encoder(x)
        x = self.decoder(x)
        return x


class MyEncoder(nn.Module):

    def __init__(self, shapes: list, relu: bool = True, dropout: Union[float, None] = None) -> None:
        super().__init__()
        list_of_layers = []
        for i in range(len(shapes) - 2):
            list_of_layers.append(nn.Linear(shapes[i], shapes[i + 1]))
            if relu:
                list_of_layers.append(nn.ReLU())
            if dropout is not None:
                list_of_layers.append(nn.Dropout(p=dropout))
        list_of_layers.append(nn.Linear(shapes[-2], shapes[-1]))

        self.layers = nn.Sequential(*list_of_layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layers(x)


class MyDecoder(nn.Module):

    def __init__(self, shapes: list, relu: bool = True, dropout: Union[float, None] = None) -> None:
        super().__init__()
        list_of_layers = []
        for i in range(len(shapes) - 2):
            list_of_layers.append(nn.Linear(shapes[-i - 1], shapes[-i - 2]))
            if relu:
                list_of_layers.append(nn.ReLU())
            if dropout is not None:
                list_of_layers.append(nn.Dropout(p=dropout))
        list_of_layers.append(nn.Linear(shapes[1], shapes[0]))
        self.layers = nn.Sequential(*list_of_layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layers(x)


class MyAutoencoder(L.LightningModule):

    def __init__(self, shapes: list, relu: bool = True, dropout_en: Union[float, None] = None,
                 dropout_de: Union[float, None] = None) -> None:
        super().__init__()
        self.encoder = MyEncoder(shapes, relu, dropout_en)
        self.decoder = MyDecoder(shapes, relu, dropout_de)

        self.val_outputs: list = []
        self.train_outputs: list = []
        self.train_loss: list = []
        self.val_loss: list = []

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.encoder(x)
        x = self.decoder(x)
        return x

    def calc_loss(self, x: torch.Tensor, x_hat: torch.Tensor) -> torch.Tensor:
        loss = nn.functional.mse_loss(x_hat, x)
        return loss

    def training_step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> dict[str, torch.Tensor]:
        x, y = batch
        x = x.view(x.size(0), -1)
        y = y.view(y.size(0), -1)
        x_hat = self.forward(x)
        loss = self.calc_loss(x_hat, y)
        self.log("train_loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=False)
        self.train_outputs.append({'loss': loss})
        return {'loss': loss}

    def validation_step(self, batch: Tuple[torch.Tensor, torch.Tensor], batch_idx: int) -> dict[str, torch.Tensor]:
        with torch.no_grad():
            x, y = batch
            x = x.view(x.size(0), -1)
            x_hat = self.forward(x)
            loss = self.calc_loss(x_hat, y)
        self.log("val_loss", loss, prog_bar=True)
        self.val_outputs.append({'loss': loss})
        return {'loss': loss}

    def configure_optimizers_(self) -> Tuple[list[torch.optim.Optimizer], list[dict[str, Any]]]:
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3, weight_decay=5e-4)

        lr_scheduler = {
            'scheduler': torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=10, min_lr=1e-6, verbose=True),
            'monitor': 'val_loss',
        }

        return [optimizer], [lr_scheduler]

    def configure_optimizers(self) -> Tuple[list[torch.optim.Optimizer], list[dict[str, Any]]]:
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3, weight_decay=5e-4)

        # Define a custom lambda function for the sawtooth learning rate
        def lr_lambda(epoch: int) -> float:
            # Define the sawtooth shape for the learning rate
            cycle = 10  # Number of iterations in a cycle
            return 0.5 * (1 - abs(epoch % cycle - cycle // 2) / (cycle // 2))

        lr_scheduler = {
            'scheduler': torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda),
            'interval': 'epoch',
        }

        return [optimizer], [lr_scheduler]

    def on_validation_epoch_end(self) -> None:
        # здесь вы можете использовать self.train_outputs для доступа к выводам обучения
        avg_loss = torch.stack([x['loss'] for x in self.val_outputs]).mean()
        print(f"| Val Loss: {avg_loss:.3f}")
        self.log('val_loss', avg_loss, prog_bar=True, on_epoch=True, on_step=False)
        self.val_outputs = []
        self.val_loss.append(avg_loss)

    def on_train_epoch_end(self) -> None:
        # здесь вы можете использовать self.train_outputs для доступа к выводам обучения
        avg_loss = torch.stack([x['loss'] for x in self.train_outputs]).mean()
        print(f"| Train Loss: {avg_loss:.3f}")
        self.log('train_loss', avg_loss, prog_bar=True, on_epoch=True, on_step=False)
        self.train_outputs = []
        self.train_loss.append(avg_loss)


class MyDataset(Dataset):
    def __init__(self, dataset: np.ndarray) -> None:
        self.dataset = dataset
        self.dataset = torch.tensor(self.dataset, dtype=torch.float)

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.dataset[idx], self.dataset[idx]