from collections.abc import Generator

import polars as pl


def read_mssql_batch(
    query: str,
    conn: str,
    batch_size: int = 1_000_000,
) -> Generator[tuple[pl.DataFrame, int], None, None]:
    """Read MSSQL by `arrow-odbc` lib for backend."""
    batch_num: int = 0
    for batch in pl.read_database(
        query=query,
        connection=conn,
        execute_options={
            "max_bytes_per_batch": 536_870_912,
        },
        iter_batches=True,
        batch_size=batch_size,
    ):
        yield batch, batch_num
        batch_num += 1


def write_mssql(): ...
