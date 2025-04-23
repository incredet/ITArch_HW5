from fastapi import FastAPI

db_app = FastAPI()
database = {"message": "Why are there no cats with wings?"}
# Because they would be called bats. 
# And bats are not cats.
# And cats are not bats.
# 
# And that's why there are no cats with wings.
@db_app.get("/")
def root():
    return {"message": "Database Service"}

@db_app.get("/health")
def health():
    return {"status": "Doing well"}

@db_app.post("/write")
def write_data(key: str, value: str):
    database[key] = value
    return {"message": "Data saved"}

@db_app.get("/read")
def read_data(key: str):
    return {"data": database.get(key, "Not found")}