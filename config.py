DB_USER = "postgres"
DB_USER_PASSWORD = "12345678"
IP_ADDRESS = "127.0.0.1"
PORT = "5432"
DB_NAME = "main"
DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_USER_PASSWORD}@{IP_ADDRESS}:{PORT}/{DB_NAME}"
REDIS_DB_NAME = "1"
REDIS_DB_URL = f"redis://{IP_ADDRESS}/{REDIS_DB_NAME}"
JWT_ALG = "HS256"
JWT_NAME = "JWT"
JWK = "ytXtB53Ku62pZdC-qBH3mJwgsxQThvBp4wfNHCUyS4HkUKA8Q9NEEzxy7Xl9oztmTpRheoG2008VEocBu7kqJw"
JWK_TYPE = "oct"
ENCODING = "utf-8"
