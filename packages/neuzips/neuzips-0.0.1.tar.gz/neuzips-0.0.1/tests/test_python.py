import logging


import torch
from neuzips import compress_model


logging.basicConfig(level=logging.DEBUG)


def test_compress_model():
    model = torch.nn.Sequential(
        torch.nn.Linear(10, 10),
        torch.nn.Linear(10, 10),
    )

    uncompressed = sum((n.data.numel() * n.data.element_size()) for n in model.parameters())

    cmodel = compress_model(model)

    compressed = sum((n.data.numel() * n.data.element_size()) for n in cmodel.parameters())

    assert compressed < uncompressed
