import matplotlib.pyplot as plt
from src.config.logs_config import setup_log, auto_logger
from pathlib import Path

logger = setup_log(name="File Helper", filename="utils")

@auto_logger(logger)
def show_img_exists(filepath, size):
    img = plt.imread(filepath)
    plt.figure(figsize=size)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

@auto_logger(logger)
def is_cache(save_path, isredraw=True, size=(12,10)) -> bool:
    if save_path.exists():
        logger.info(f"Img {save_path.name} has exist")
        if isredraw:
            logger.info(f"RELOAD IMAGE {save_path.name}")
            show_img_exists(save_path, size)
            return True
    return False


