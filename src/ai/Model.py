from pathlib import Path
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
from . import FeatureMap
from src.util import classproperty, Img

NORM_MEAN = [0.485, 0.456, 0.406]
NORM_STD = [0.229, 0.224, 0.225]

CLASSES = [
            "unselected"
          ] + [
            f"slot_{i:02d}"
            for i in range(FeatureMap.SLOT_CAPACITY)
          ]

def _freeze_params(params) -> None:
        for param in params:
            param.requires_grad = False

def _unfreeze_params(params) -> None:
    for param in params:
        param.requires_grad = True

class Model:
    def __init__(self, training=False, fine_tuning=False, state=None):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = models.resnet18(weights='IMAGENET1K_V1').to(device)        

        inputs_len = model.fc.in_features
        outputs_len = len(CLASSES)
        model.fc = nn.Linear(inputs_len, outputs_len).to(device)
        
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(NORM_MEAN, NORM_STD)
        ])

        def to_tensor(imgs: list[Img]):
            tensors = [transform(img.raw_data) for img in imgs]
            return torch.stack(tensors)
        
        if state is not None:
            model.load_state_dict(state)

        if training:
            model.train()
            self._criterion = nn.CrossEntropyLoss()
            self._optimizer = optim.Adam(model.parameters(), lr=0.0001)
            
            if fine_tuning:
              _unfreeze_params(model.parameters())
            else:
              _freeze_params(model.parameters())
            
            _unfreeze_params(model.fc.parameters())
        else:
            model.eval()

        self._model = model
        self._device = device
        self._training = training
        self._fine_tuning = fine_tuning
        self._to_tensor = to_tensor
  
    @property
    def DEVICE(self):
        return self._device
    
    @property
    def FINE_TUNING(self):
        return self._fine_tuning

    @classproperty
    def CLASSES(cls):
        return CLASSES
    
    def train(self, imgs: list[Img], labels: torch.Tensor) -> float:
        if not self._training:
            raise RuntimeError("Model is not in training mode.")

        inputs = self._to_tensor(imgs).to(self._device)
        labels = labels.to(self._device)

        self._optimizer.zero_grad()
        outputs = self._model(inputs)
        loss = self._criterion(outputs, labels)
        loss.backward()
        self._optimizer.step()
        return loss.item()
    
    def save(self, path: Path):
        torch.save(self._model.state_dict(), path)
    
    @classmethod
    def from_file(cls, path: Path, training=False, fine_tuning=False) -> "Model":
        if not path.exists():
            raise FileNotFoundError(f"Model file not found at {path}")

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        state = torch.load(path, map_location=device)
        return cls(training, fine_tuning, state)