from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from app.predictor import forecast
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/api/forecast")
async def get_forecast_plot(number_of_days_to_forecast: int) -> StreamingResponse:

    plot_image = forecast(number_of_days_to_forecast)
    return StreamingResponse(plot_image, media_type="image/png")

@app.get("/", response_class=HTMLResponse)
async def start(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/forecast", response_class=HTMLResponse)
async def get_forecast(number_of_days_to_forecast: int, request: Request):
    plot_image = forecast(number_of_days_to_forecast)
    filename = f"{uuid4().hex}.png"
    file_path = f"app/static/images/{filename}"
    with open(file_path, "wb") as f:
        f.write(plot_image.getvalue())

    # Generate the URL for the image
    image_url = f"/static/images/{filename}"
    
    return templates.TemplateResponse(
        "forecast.html", {"request": request, "image_url": image_url})