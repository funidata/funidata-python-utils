#  Copyright (c) 2025 Funidata Oy.
#  All rights reserved.
# ------------------------------------------------------------------------------

import json

# SQLAlchemy is the optional `sql` extra. Import it lazily so that importing the `auth` and
# `sis_integration` packages (which reach this module through `DatabaseConfig`) works without it.


def json_encoder_ascii_false(d):
    return json.dumps(d, ensure_ascii=False)


def get_engine(
    db_uri: str,
    /,
    *,
    echo_sql: bool = False,
    pool_size: int = 1,
    max_overflow: int = 0,
    connect_args: dict | None = None,
):
    from sqlalchemy import create_engine

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
    from sqlalchemy import text

    return [
        {**x._mapping} for x in
        session.execute(
            text(stmt), sql_params_dict or {}
        ).all()
    ]
