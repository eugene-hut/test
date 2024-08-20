from typing import Annotated

from openpyxl.styles.numbers import FORMAT_NUMBER
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from excel.schemas.schemas import ReplacePhoto, Duplicate
from excel.utils import get_workbook_and_path


router = APIRouter(
    tags=["Excel"],
)


@router.post(
    path="/replace-photo/",
    summary="Замена фото",
)
async def replace_photo(
    data: Annotated[ReplacePhoto, Depends()],
):
    try:
        wb, file_path = get_workbook_and_path(data)
        sheet = wb.active
        for row in sheet.rows:
            for cell in row:
                cell_value = cell.value.split(";")
                new_value = cell_value[0] + data.text
                if cell_value[-1].endswith(".mp4"):
                    new_value += ";" + cell_value[-1]
                cell.value = new_value
        wb.save(file_path)
        return FileResponse(
            file_path,
            filename=data.file.filename,
            media_type="multipart/form-data",
        )
    except Exception as e:
        return {"error": str(e)}


@router.post(
    path="/duplicate",
    summary="Дублирование строк",
)
async def duplicate_rows(data: Annotated[Duplicate, Depends()]):
    try:
        wb, file_path = get_workbook_and_path(data)
        sheet_original = wb.active
        sheet_result = wb.create_sheet(title=f"Result-{sheet_original.title}")

        for row, row_orig in enumerate(sheet_original.iter_rows(values_only=True), 1):
            row_orig = list(row_orig)
            row_orig[0] = row
            print(row_orig)

            for _ in range(data.quantity):
                sheet_result.append(row_orig)

        for cell in sheet_result["C"]:
            cell.number_format = FORMAT_NUMBER
        wb.save(file_path)
        return FileResponse(
            file_path,
            filename=data.file.filename,
            media_type="multipart/form-data",
        )
    except Exception as e:
        return {"error": str(e)}
