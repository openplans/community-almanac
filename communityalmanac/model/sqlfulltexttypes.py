from psycopg2.extensions import AsIs
from sqlalchemy.exc import DataError
from sqlalchemy.types import TypeEngine



class WeightedText(TypeEngine):
    """A weighted, tokenized representatin of text."""

    def __init__(self):
        super(WeightedText, self).__init__()

    def get_col_spec(self):
        return 'tsvector'

    def bind_processor(self, dialect):
        """Convert from Python type to database type."""
        def process(value):
            if value is None:
                return None
            raise DataError('WeightedText types don\'t yet support manual updates.')
        return process
