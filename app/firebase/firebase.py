import json

import firebase_admin
from firebase_admin import credentials, App, db, auth
from ..config import FIREBASE_SERVICE_ACCOUNT_PATH, FIREBASE_REALTIME_DATABASE_URL


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class FirebaseConnector(metaclass=SingletonMeta):
    firebase_admin_instance: App

    def connect(self):
        try:
            with open(FIREBASE_SERVICE_ACCOUNT_PATH) as f:
                firebase_service_account_config = json.load(f)
            if firebase_service_account_config:
                cred = credentials.Certificate(firebase_service_account_config)
                self.firebase_admin_instance = firebase_admin.initialize_app(cred, {
                    'databaseURL': FIREBASE_REALTIME_DATABASE_URL,
                })
                print("Firebase initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Firebase: {e}")

    def check_and_create_collection(self):
        ref = db.reference('users')
        snapshot = ref.get(shallow=True)  # Efficiently check for the existence of the node
        if snapshot is None:
            print("Collection 'users' does not exist. Creating new collection.")
            ref.set({})
        else:
            print("Collection 'users' already exists.")

    def add_user_if_not_exists(self, user_id):
        try:
            user_ref = db.reference(f'users/{user_id}')
            user_snapshot = user_ref.get()

            if user_snapshot is None:
                print(f"User {user_id} does not exist. Creating new user.")
                user_ref.set({"numberOfUnNotifiedMessages": 0})
                print(f"User {user_id} created successfully.")
            else:
                print(f"User {user_id} already exists.")
        except Exception as e:
            print(f"Failed to check or add user {user_id}: {e}")

    def add_new_users(self, user_ids):
        try:
            ref = db.reference('users')
            existing_users = ref.get(shallow=True)  # Efficiently check existing users
            new_users_data = {}
            for user_id in user_ids:
                user_id_str = str(user_id)
                if existing_users is None:
                    new_users_data[user_id_str] = {"numberOfUnNotifiedMessages": 0}
                elif user_id_str not in existing_users:
                    new_users_data[user_id_str] = {"numberOfUnNotifiedMessages": 0}

            if new_users_data:
                ref.update(new_users_data)
                print(f"New users added successfully: {new_users_data}")
            else:
                print("No new users to add.")
        except Exception as e:
            print(f"Failed to add new users: {e}")

    def update_user_notifications(self, user_id, number_of_unnotified_messages):
        try:
            user_ref = db.reference(f'users/{user_id}')
            user_snapshot = user_ref.get()

            if user_snapshot is None:
                print(f"User {user_id} does not exist. Creating new user.")
                user_ref.set({"numberOfUnNotifiedMessages": number_of_unnotified_messages})
                print(
                    f"User {user_id} created successfully with numberOfUnNotifiedMessages: {number_of_unnotified_messages}")
            else:
                print(f"User {user_id} already exists. Updating numberOfUnNotifiedMessages.")
                user_ref.update({"numberOfUnNotifiedMessages": number_of_unnotified_messages})
                print(
                    f"User {user_id} updated successfully with numberOfUnNotifiedMessages: {number_of_unnotified_messages}")
        except Exception as e:
            print(f"Failed to check or update user {user_id}: {e}")


    def create_custom_token(self, uid, additional_claims=None):
        try:
            custom_token = auth.create_custom_token(uid, additional_claims)
            print(f"Custom token created successfully: {custom_token.decode('utf-8')}")
            return custom_token.decode('utf-8')
        except Exception as e:
            print(f"Failed to create custom token for user {uid}: {e}")
            return None

