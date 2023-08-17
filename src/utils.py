from pathlib import Path
import anosql  # this seems to only work with pycopg2.
import psycopg2

ROOT_DIR = Path(__file__).parent.parent


def sort_dict(data: dict) -> dict:
    return {k: data[k] for k in sorted(data)}


def load_sql(path: Path):
    queries = None
    for file in path.iterdir():
        if file.is_file() and file.name.endswith(".sql"):
            query = anosql.from_path(str(file), "psycopg2")
            if queries:
                for qname in query.available_queries:
                    queries.add_query(qname, getattr(query, qname))
            else:
                queries = query
    return queries
