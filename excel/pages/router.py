import os

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from starlette.responses import HTMLResponse, FileResponse

from excel.api.v1.handles import duplicate_rows, replace_photo
from excel.schemas.schemas import Duplicate, ReplacePhoto

router = APIRouter(
    prefix="/excel",
    tags=["Excel pages"],
)


templates = Jinja2Templates(directory="templates")


@router.get("/files")
async def get_files():
    try:
        file_path = "files"
        files = os.listdir(file_path)
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}


@router.delete("/files/{pass}")
async def delete_file(password: str):
    try:
        if password == "63":
            file_path = "files"
            for root, dirs, files in os.walk(file_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            return {"message": "File deleted"}
        return {"message": "???"}
    except Exception as e:
        return {"error": str(e)}


@router.get(
    path="/",
    response_class=HTMLResponse,
    name="excel",
)
async def get_base_excel_page(request: Request):
    try:
        return templates.TemplateResponse(
            request=request,
            name="excelpages/excel.html",
        )
    except Exception as e:
        return {"error": str(e)}


@router.get("/download/{filename}", response_class=FileResponse)
async def download_file(filename: str):
    try:
        file_path = f"files/{filename}"

        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type="multipart/form-data",
        )
    except Exception as e:
        return {"error": str(e)}


@router.get(
    path="/duplicate",
    response_class=HTMLResponse,
)
async def get_duplicate_page(request: Request):
    try:
        return templates.TemplateResponse(
            request=request,
            name="excelpages/forms/duplicate.html",
        )
    except Exception as e:
        return {"error": str(e)}


@router.post(
    path="/duplicate",
    response_class=HTMLResponse,
)
async def post_duplicate_page(request: Request):
    try:
        form = Duplicate(**(await request.form()))
        file = await duplicate_rows(form)
        link = f"/excel/download/{file.filename}"

        return templates.TemplateResponse(
            request=request,
            name="excelpages/forms/duplicate.html",
            context={
                "link": str(link),
            },
        )
    except Exception as e:
        return {"error": str(e)}


@router.get(
    path="/replace-photo",
    response_class=HTMLResponse,
)
async def get_replace_photo_page(request: Request):
    try:
        return templates.TemplateResponse(
            request=request,
            name="excelpages/forms/replace-photo.html",
        )
    except Exception as e:
        return {"error": str(e)}


@router.post(
    path="/replace-photo",
    response_class=HTMLResponse,
)
async def post_replace_photo_page(request: Request):
    try:
        form = ReplacePhoto(**(await request.form()))
        file = await replace_photo(form)
        print(form)
        link = f"/excel/download/{file.filename}"
        print(file.filename)

        return templates.TemplateResponse(
            request=request,
            name="excelpages/forms/replace-photo.html",
            context={
                "link": str(link),
            },
        )
    except Exception as e:
        return {"error": str(e)}
