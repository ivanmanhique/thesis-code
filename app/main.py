from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from app.predictor import forecast
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/forecast")
async def get_forecast_plot(number_of_days_to_forecast: int) -> StreamingResponse:

    plot_image = forecast(number_of_days_to_forecast)
    return StreamingResponse(plot_image, media_type="image/png")
