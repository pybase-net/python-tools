import os

# Get the directory name of the current file
current_dir = os.path.dirname(__file__)

# Construct the absolute path to the serviceAccountKey.json
FIREBASE_SERVICE_ACCOUNT_PATH = os.path.join(current_dir, '..', 'serviceAccountKey.json')

# Normalize the path (optional but recommended for cross-platform compatibility)
FIREBASE_SERVICE_ACCOUNT_PATH = os.path.normpath(FIREBASE_SERVICE_ACCOUNT_PATH)

FIREBASE_REALTIME_DATABASE_URL = 'https://drbaulderlocal-default-rtdb.asia-southeast1.firebasedatabase.app/'
