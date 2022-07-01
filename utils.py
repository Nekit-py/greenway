
from time import perf_counter
from functools import wraps
from io import BytesIO
import pandas as pd
import logging


logging.basicConfig(level='INFO')


def timeit(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        start = perf_counter()
        res = method(self, *args, **kwargs)
        logging.info(f'Total time -> {round(perf_counter() - start, 2)} sec.')
        return res
    return wrapper


def get_response_data(df: pd.DataFrame) -> bytes:
    with BytesIO() as buffer:
        with pd.ExcelWriter(path=buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        data = buffer.getvalue()
    return data