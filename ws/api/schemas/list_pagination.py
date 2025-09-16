from pydantic import BaseModel


class ListPaginationSchema(BaseModel):
    """This schema will use for 'get_batch' method in repository"""

    limit: int
    offset: int
