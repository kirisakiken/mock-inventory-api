import uvicorn

import app
from src.database.database_manager import metadata, engine


def main():
    metadata.create_all(engine)
    uvicorn.run(app.app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
