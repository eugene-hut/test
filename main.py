import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from excel.api import router as api_v1_excel_router

from excel.pages.router import templates
from excel.pages.router import router as pages_router

app = FastAPI()

app.include_router(router=api_v1_excel_router)
app.include_router(router=pages_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get(
    path="/",
    response_class=HTMLResponse,
    name="index",
)
async def get_base_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
