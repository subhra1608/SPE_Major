import pickle
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def load_model(model_path):
    # print("print ho rha")
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    logger.info("Model loaded successfully subhra.")
    return model

def load_scaler(scaler_path):
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    return scaler
