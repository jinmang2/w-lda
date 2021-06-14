import json
import copy
import torch
import numpy as np
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Union, Any


@dataclass(repr=False)
class TrainRecorder:
    loss_discriminator: float = field(default=0.0)
    loss_generator: float = field(default=0.0)
    loss_reconstruction: float = field(default=0.0)
    latent_max_distr: Union[np.ndarray, torch.Tensor, float] = field(default=0.0)
    latent_avg_entropy: float = field(default=0.0)
    latent_avg: Union[np.ndarray, torch.Tensor, float] = field(default=0.0)
    dirich_avg_entropy: float = field(default=0.0)
    loss_labeled: float = field(default=0.0)
    discriminator_z_confidence_true: float = field(default=0.0)
    discriminator_z_confidence_fake: float = field(default=0.0)
    discriminator_y_confidence_true: float = field(default=0.0)
    discriminator_y_confidence_fake: float = field(default=0.0)

    def save_to_json(self, json_path: str):
        json_string = json.dumps(asdict(self), indent=2, sort_keys=True) + "\n"
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(json_string)

    @classmethod
    def load_from_json(cls, json_path: str):
        with open(json_path, "r", encoding="utf-8") as f:
            text = f.read()
        return cls(**json.loads(text))

    def __repr__(self):
        cls_name = self.__class__.__qualname__
        field_values = self.__dataclass_fields__.values()
        contents = ", ".join(
            [f_value.name + ": " + str(f_value.type).split(".")[-1]
             for f_value in field_values]
        )
        return cls_name + "(" + contents + ")"

    def asdict(self):
        return asdict(self)

    def update(self, record: Dict[str, Union[float, torch.Tensor]]):
        for f_name, f_value in self.__dataclass_fields__.items():
            value = record.get(f_name, None)
            if value is not None:
                old_value = getattr(self, f_name)
                setattr(self, f_name, old_value + value)