from operator import and_
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from fastapi import Query, Request
from pydantic import BaseModel, model_validator
from pydantic.generics import GenericModel

from pydantic import BaseModel, Field

class PageParams(BaseModel):
    """Request query params for paginated API, including optional filters.
    Sample usage:
    page_params = PageParams(
    page=1,
    size=20,
    filters={
        "age": {"gte": 18},  # Age >= 18
        "joined_date": {"lte": "2025-01-01"},  # Date <= 2025-01-01
        "roles": ["admin", "editor"],  # List matching
        "email": "example.com"  # Partial match (email contains "example.com")
        }
    )\n
    """
    page: int = Field(default=1, ge=1, description="Page number (must be greater than or equal to 1)")
    size: int = Field(default=10, ge=1, le=100, description="Page size (must be between 1 and 100)")
    paginate: bool = Field(default=True, description="Whether to paginate the results")
    filters: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Dictionary of filters to apply to the query. Example: {'name': 'test', 'status': 'active'}"
    )

    @model_validator(mode='before')
    def debug_filters(cls, values):
        print(f"Incoming query parameters: {values}")
        return values


T = TypeVar("T")

class PagedResponseSchema(GenericModel, Generic[T]):
    """Response schema for any paged API."""

    total: int
    page: int
    size: int
    results: List[T]

class ResponseSchema(GenericModel, Generic[T]):
    """Response schema for any API."""

    status: str
    message: str
    code: int
    data: T


def paginate(
    page_params: PageParams,
    query: Query,
    model: Type,
    ResponseSchema: BaseModel
) -> PagedResponseSchema[T]:
    """Paginate the query after applying filters from PageParams."""
    
    # Apply filters if provided
    if page_params.filters:
        query = apply_filters(query, model, page_params.filters)

    # Perform pagination efficiently
    total_count = query.count()
    if page_params.paginate:
        query = query.offset((page_params.page - 1) * page_params.size).limit(page_params.size)

    paginated_query = query.all()

    # Return the paginated response
    return PagedResponseSchema[T](
        total=total_count,
        page=page_params.page,
        size=page_params.size,
        # results=[ResponseSchema(**item.__dict__) for item in paginated_query]
        results=[ResponseSchema.model_validate(item) for item in paginated_query],
    )


def apply_filters(
    query: Query,
    model: Type,
    filters: Dict[str, Any]
) -> Query:
    """
    Apply dynamic filters to an SQLAlchemy query.
    
    Args:
        query (Query): The SQLAlchemy query object.
        model (Type): The SQLAlchemy model to filter on.
        filters (Dict[str, Any]): Dictionary of filters where keys are column names and values are filter values.

    Returns:
        Query: The filtered SQLAlchemy query.
    """
    for field, value in filters.items():
        if value is None:
            continue

        if hasattr(model, field):
            column = getattr(model, field)

            # Handle range filtering for numeric or date fields
            if isinstance(value, dict):
                lower = value.get("gte")  # Greater than or equal to
                upper = value.get("lte")  # Less than or equal to
                if lower is not None and upper is not None:
                    query = query.filter(and_(column >= lower, column <= upper))
                elif lower is not None:
                    query = query.filter(column >= lower)
                elif upper is not None:
                    query = query.filter(column <= upper)

            # Partial matching for strings
            elif isinstance(value, str):
                query = query.filter(column.ilike(f"%{value}%"))  # Use ilike for case-insensitive matching

            # Exact matching for lists
            elif isinstance(value, list):
                query = query.filter(column.in_(value))

            # Exact matching for other types
            else:
                query = query.filter(column == value)

    return query


# def parse_page_params(request: Request) -> PageParams:
#     """Custom parser for PageParams to handle 'filters'."""
#     query_params = request.query_params
#     filters = {
#         key.split(".")[1]: value
#         for key, value in query_params.items()
#         if key.startswith("filters.")
#     }
#     # You can adapt this for bracket notation as well if needed
#     return PageParams(
#         page=int(query_params.get("page", 1)),
#         size=int(query_params.get("size", 10)),
#         filters=filters if filters else None
#     )

# def parse_page_params(request: Request) -> PageParams:
#     """Custom parser for PageParams to handle 'filters'."""
#     query_params = request.query_params
#     filters = {
#         key.split(".")[1]: value
#         for key, value in query_params.items()
#         if key.startswith("filters.")
#     }

#     # Convert range filters (e.g., "filters.field[gte]", "filters.field[lte]")
#     parsed_filters = {}
#     for key, value in filters.items():
#         if "[" in key and "]" in key:
#             field, operator = key.split("[")
#             operator = operator.strip("]")
#             if field not in parsed_filters:
#                 parsed_filters[field] = {}
#             parsed_filters[field][operator] = value
#         else:
#             parsed_filters[key] = value

#     return PageParams(
#         page=int(query_params.get("page", 1)),
#         size=int(query_params.get("size", 10)),
#         filters=parsed_filters if parsed_filters else None
#     )