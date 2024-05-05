# Used to abstract away concrete uses of MLflow model flavors.
# Based on the provided flavor from the FLOps SLA the specific MLflow model flavor will be used.

import os
import sys

from flops_utils.logging import logger
from flops_utils.types import MLModelFlavor

match MLModelFlavor(os.environ.get("ML_MODEL_FLAVOR")):
    case MLModelFlavor.KERAS:
        import mlflow.keras

        mlflow_model_flavor = mlflow.keras
    case MLModelFlavor.PYTORCH:
        import mlflow.pytorch

        mlflow_model_flavor = mlflow.pytorch
    case _:
        logger.exception("Provided MLModelFlavor is not supported yet.")
        sys.exit(1)
