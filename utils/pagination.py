from typing import Type, Any, Tuple, List
from sqlalchemy.orm import Session

def paginate_query(session: Session, model: Type, cursor_field: str = 'id', cursor: Any = 0, limit: int = 10) -> Tuple[List[Any], Any]:
    field = getattr(model, cursor_field)
    query = session.query(model).filter(field > cursor).order_by(field).limit(limit)
    results = query.all()
    next_cursor = getattr(results[-1], cursor_field) if results and len(results) == limit else None
    return results, next_cursor
