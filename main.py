from volumes import TotalPartnerVolume
from fastapi import FastAPI
from fastapi.responses import Response
from utils import get_response_data
import uvicorn


app = FastAPI()



@app.get('/')
async def hello():
    return {
        'message': 'Тестовое задание для должности Разработчик Python - Greenway.\nДля работы ввеедите в адресную строку \docs'
    }


@app.post('/get_total_volume')
async def get_total_volume(partners_path: str, orders_path: str, footer=True):
        tpv = TotalPartnerVolume(partners_path=partners_path, orders_path=orders_path)
        df = tpv.get_total_sales_volume(footer)
        data = get_response_data(df)
        if footer:
            headers = {
                'content-disposition':
                'attachment; filename="total_sales_volumes.xlsx"'
            }
        else:
            headers = {
                'content-disposition':
                'attachment; filename="total_sales_volumes_without_footer.xlsx"'
            }
        return Response(content=data, headers=headers)


if __name__ == "__main__":
    uvicorn.run("main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level='info'
    )