from pathlib import Path

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from ultima_scraper_detector.ultima_scraper_detector import UltimaScraperDetector


class USDRClient(FastAPI):
    ultima_detector = UltimaScraperDetector()

    def __init__(self):
        super().__init__()


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


class Item(BaseModel):
    filepaths: list[str]


@router.post("/activate_gui")
def activate_gui():
    USDRClient.ultima_detector.activate_gui()
    return True


@router.post("/detect")
def detect(item: Item):
    ultima_detector = USDRClient.ultima_detector
    ultima_detector.detect([Path(filepath) for filepath in item.filepaths])
    return ultima_detector.detections


@router.post("/predict_sex")
def predict_sex():
    return USDRClient.ultima_detector.predict_sex()


@router.post("/reset_detections")
def reset_detections():
    return USDRClient.ultima_detector.reset_detections()
