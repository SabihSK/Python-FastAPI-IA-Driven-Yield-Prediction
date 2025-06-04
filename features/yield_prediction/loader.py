import pickle
import os

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")

models = {
    "fsd": pickle.load(open(os.path.join(MODEL_DIR, "fsd_model.pkl"), "rb")),
    "bhawalnagar": pickle.load(
        open(os.path.join(MODEL_DIR, "model_bhawalnagar.pkl"), "rb")
    ),
    "multan": pickle.load(open(os.path.join(MODEL_DIR, "model_Multan.pkl"), "rb")),
    "ryk": pickle.load(open(os.path.join(MODEL_DIR, "model_ryk.pkl"), "rb")),
}
