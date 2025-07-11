import simplejson
from sqlalchemy import create_engine, text


def json_encoder_ascii_false(d):
    return simplejson.dumps(d, ensure_ascii=False)


def get_engine(
    db_uri: str,
    /,
    *,
    echo_sql: bool = False,
    pool_size: int = 1,
    max_overflow: int = 0,
    connect_args: dict | None = None,
):
    engine = create_engine(
        db_uri,
        json_serializer=json_encoder_ascii_false,
        echo=echo_sql,
        pool_size=pool_size,
        max_overflow=max_overflow,
        connect_args=connect_args,
    )
    return engine


def get_by_statement(session, stmt: str, sql_params_dict: dict | None = None) -> list[dict]:
    return [
        {**x._mapping} for x in
        session.execute(
            text(stmt), sql_params_dict or {}
        ).all()
    ]
