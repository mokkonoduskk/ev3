from __future__ import annotations
from dataclasses import dataclass
import requests

from config.settings import Settings
from utils import validaciones as v
from utils.excepciones import ErrorServicioExterno

DIAS_PRONOSTICO = 5

VIENTO_MAX_KMH = 40
LLUVIA_PROB_MAX = 60
LLUIA_MAX_MM = 10
TEMP_MAX_C= 35
