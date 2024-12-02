from app import db as DBQueryRunner
from app.apis.TestAPI.repository import query

def get_data(id: int):
  # db_data = DBQueryRunner.run_query(
  #   query.TEST_FINDBY_ID,
  #   (id,)
  # )
  # return db_data

  return [
    {"message": "Hello, World1!"},
    {"message": "Hello, World2!"},
    {"message": "Hello, World3!"},
    {"message": "Hello, World4!"},
    {"message": "Hello, World5!"}
  ]

  