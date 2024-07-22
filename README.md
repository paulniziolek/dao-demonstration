# MySQL DB Test

A sample MySQL database project with FastAPI integration.

## Environmental Variables

To connect to the MySQL database, the following environmental variables need to be set:

- `DB_HOST`: The host address of the MySQL database.
- `DB_PORT`: The port number of the MySQL database.
- `DB_USER`: The username for accessing the MySQL database.
- `DB_PASS`: The password for accessing the MySQL database.
- `DB_NAME`: The name of the MySQL database.

The values for the current local environment can be set using `source setenv.sh`.

## Future Fixes

- Support asynchronocity for our DB transactions, either with DB connection pooling or some alternate method.
- Store our environmental variables as a config JSON instead.
- Validation Logic should be handled at the service/handler layer, not the DAO layer. Also, consider using Pydantic for validation features instead
- Error handling and exception logic should (maybe) be moved to the service/handler layer, not the DAO layer. (look into this)
- When using the above exception logic, try to specify exact exception, not just `except Exception: ...`.
- Improved logging system
- In internal/domains/mysqldb/db.py, include a wrapper util func for getting environ variables and asserting when they are none.
- Improve unit testing with better mocking, especially for the UserDAO. 
