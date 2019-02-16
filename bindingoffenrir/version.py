import os
from bindingoffenrir.resources import RESOURCE_DIR

try:
    with open(os.path.join(RESOURCE_DIR, 'builddate'), 'r') as f:
        BUILD_DATE = f.read()
except Exception:
    BUILD_DATE = 'dev-build'
