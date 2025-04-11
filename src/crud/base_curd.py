from sqlalchemy.orm import Session
# from sqlmodel import  Session

class BaseCRUD:
    def __init__(self, db_session: Session): #, project_id: str
        self.db_session = db_session
        # self.project_id = project_id

    # def set_schema(self):
    #     """
    #      Method to set the schema name to the session connection
    #      To support multi-tenancy, where common set of tables are in multiple schemas.
    #      ProjectId is the runtime schema name.
    #      This is done to execute the query on the correct Postgres schema
    #      https://docs.sqlalchemy.org/en/20/core/connections.html#translation-of-schema-names
    #     """
    #     self.db_session.connection(execution_options={"schema_translate_map": {"runtime_schema_name": self.project_id}})
