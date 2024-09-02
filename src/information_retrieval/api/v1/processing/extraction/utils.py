from io import BytesIO

from PIL import Image

from information_retrieval.core.logger import app_logger as logger


def is_accepted_file_type(file_type: str, accepted_file_types: list[str]):
    logger.debug(f"Validating file type '{file_type}' is in allowed types {accepted_file_types}")
    return file_type in accepted_file_types


def normalize_image(image: Image) -> BytesIO:
    """
    Normalize the image by converting it to a standard format (JPEG) and resizing it if necessary.
    """
    max_size = (1024, 1024)  # Example size
    image.thumbnail(max_size)

    output = BytesIO()
    image.save(output, format="JPEG")
    output.seek(0)

    return output
