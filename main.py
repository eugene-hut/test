import uvicorn
from fastapi import FastAPI

from excel.api import router as api_v1_excel_router


app = FastAPI()

app.include_router(router=api_v1_excel_router)


@app.get("/")
async def root():
    return {"message": "Hello from server!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
