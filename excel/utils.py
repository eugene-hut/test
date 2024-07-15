from datetime import datetime
import openpyxl as opx

from .schemas.schemas import Excel


def get_workbook_and_path(data: Excel):
    data.file.filename = (
        datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + "---" + data.file.filename
    )
    file_path = f"files/{data.file.filename}"

    with open(file_path, "wb") as f:
        f.write(data.file.file.read())
    workbook = opx.open(filename=file_path)
    return workbook, file_path
