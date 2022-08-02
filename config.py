DB_USER = "postgres"
DB_USER_PASSWORD = "12345678"
IP_ADDRESS = "127.0.0.1"
PORT = "5432"
DB_NAME = "main"
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_USER_PASSWORD}@{IP_ADDRESS}:{PORT}/{DB_NAME}"
MEET_DB_NAME = "1"
MEET_DB_URL = f"redis://{IP_ADDRESS}/{MEET_DB_NAME}"
JWT_ALG = "HS256"
JWT_NAME = "JWT"
JWK_KEY = "ytXtB53Ku62pZdC-qBH3mJwgsxQThvBp4wfNHCUyS4HkUKA8Q9NEEzxy7Xl9oztmTpRheoG2008VEocBu7kqJw"
JWK_TYPE = "oct"
ENCODING = "utf-8"
USER_IMAGE_PLACEHOLDER_PATH = "utils/images/user_image_placeholder.jpg"
USER_IMAGE_FILE_STORAGE_PATH = "user_images/"
MEET_AUTHOR_FILE_STORAGE_PATH = "meet_authors/"
MEET_AUTHOR_FILE_NAME = "meet_authors.txt"
MIN_USER_IMAGE_WIDTH_PX = 100
MIN_USER_IMAGE_HEIGHT_PX = 100
MAX_USER_IMAGE_WIDTH_PX = 200
MAX_USER_IMAGE_HEIGHT_PX = 200
