from .model_system import ModelSystem
from .noise_models import (
    DataDependentNoise,
    ZeroNoise,
    ConstantNoise,
    ProportionalNoise,
    SumNoise,
    parse_noise_model,
    noise_model_factory,
)
from .branin_hoo import branin, branin_no_noise
from .color_pH import color_pH
from .gold_map import gold_map
from .gold_map_with_wells import gold_map_with_wells
from .hart3 import hart3, hart3_no_noise
from .hart6 import hart6, hart6_no_noise
from .poly2 import poly2, poly2_no_noise
from .peaks import peaks, peaks_no_noise

__all__ = [
    "branin",
    "branin_no_noise",
    "color_pH",
    "ModelSystem",
    "DataDependentNoise",
    "ZeroNoise",
    "ConstantNoise",
    "ProportionalNoise",
    "SumNoise",
    "parse_noise_model",
    "noise_model_factory",
    "hart3",
    "hart3_no_noise",
    "hart6",
    "hart6_no_noise",
    "poly2",
    "poly2_no_noise",
    "peaks",
    "peaks_no_noise",
    "gold_map",
    "gold_map_with_wells",
]
