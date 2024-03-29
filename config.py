from os import getenv

DB_USER = getenv("POSTGRES_USER", "postgres")
DB_USER_PASSWORD = getenv("POSTGRES_PASSWORD", "12345678")
IP_ADDRESS = "127.0.0.1"
PORT = "5432"
DB_NAME = getenv("POSTGRES_DB", "main")
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_USER_PASSWORD}@127.0.0.1:5432/{DB_NAME}"
MEET_DB_NAME = "1"
MEET_DB_URL = f"redis://127.0.0.1:6379/{MEET_DB_NAME}"
JWT_ALG = "HS256"
JWT_NAME = "JWT"
JWK_KEY = "ytXtB53Ku62pZdC-qBH3mJwgsxQThvBp4wfNHCUyS4HkUKA8Q9NEEzxy7Xl9oztmTpRheoG2008VEocBu7kqJw"
JWK_TYPE = "oct"
ENCODING = "utf-8"
USER_IMAGE_PLACEHOLDER_PATH = "utils/images/user_image_placeholder.jpg"
USER_IMAGE_FILE_STORAGE_PATH = "user_images/"
ADMIN_SECRET = "ed9666386acbe8709f63d751bc60ab4de0c9890f6395d082892c529460a1ec02"
MEET_AUTHORS_FILE_STORAGE_PATH = "meet_authors/"
MEET_AUTHORS_FILENAME = "meet_authors.txt"
CURRENT_VERSION_UPDATE_FILE_FILENAME = "current_version.txt"
ANDROID_UPDATE_FILENAME = "update_android.apk"
ANDROID_CLIENT_PLATFORM_NAME = "Android"
UPDATE_FILE_STORAGE_PATH = "update_files/"
FILE_MEDIA_TYPE_ANDROID = "application/vnd.android.package-archive"
SUPPORTED_PLATFORMS = [
    ANDROID_CLIENT_PLATFORM_NAME
]
SUPPORTED_UPDATE_FILE_CONTENT_TYPES = [
    FILE_MEDIA_TYPE_ANDROID
]
MIN_UPDATE_FILE_SIZE_BYTES = 1024
MAX_UPDATE_FILE_SIZE_BYTES = (1024 * 1024 * 1024) // 4
MIN_USER_IMAGE_WIDTH_PX = 100
MIN_USER_IMAGE_HEIGHT_PX = 100
MAX_USER_IMAGE_WIDTH_PX = 200
MAX_USER_IMAGE_HEIGHT_PX = 200
DATETIME_PATTERN = "%Y-%m-%d %H:%M:%S.%f"
NON_AUTH_REQUESTS: dict[str, list] = {
    "/docs": ["GET"],
    "/openapi.json": ["GET"],
    "/sign_up": ["POST"],
    "/sign_in": ["POST"],
    "/feedback": ["GET"],
    "/update": ["POST"],
    "/": ["GET", "POST", "DELETE", "PUT"]
}
ADMIN_REQUESTS = {
    "/feedback/all": ["GET"],
    "/update": ["POST"]
}
