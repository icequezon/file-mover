import os

from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

from src.logger import logger


def extract_date_info(file_path):
    try:
        image = Image.open(file_path)
        exif = image._getexif()
        for tag, value in exif.items():
            if TAGS.get(tag) == "DateTimeOriginal":
                date = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                monthName = date.strftime("%B")
                return {
                    "year": date.year,
                    "month": f"{date.month:02d}",
                    "monthName": f"{monthName}",
                    "day": f"{date.day}",
                }
    except Exception:
        error_message = (
            "Cannot extract exif data from file. Using time created from the file."
        )
        logger.error(error_message)

    ts = os.path.getmtime(file_path)
    date = datetime.fromtimestamp(ts)
    monthName = date.strftime("%B")

    return {
        "year": date.year,
        "month": f"{date.month:02d}",
        "monthName": f"{monthName}",
        "day": f"{date.day}",
    }
