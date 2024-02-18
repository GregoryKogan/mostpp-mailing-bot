import xlsxwriter
from dateutil.relativedelta import relativedelta
from datetime import datetime
import os

import config
from EventManagement.EventManager import RegistrationInfo


def generate_workbook(registrations: dict[str, list[RegistrationInfo]]) -> str:
    now = datetime.now()
    start_date = now - relativedelta(months=config.REGISTRATION_PERIOD)
    formatted_start_date = start_date.strftime("%d-%m-%Y")
    formatted_end_date = now.strftime("%d-%m-%Y")

    filename = f"registrations-from_{formatted_start_date}_to_{formatted_end_date}.xlsx"
    workbook = xlsxwriter.Workbook(filename)

    write_main_worksheet(workbook, registrations)

    for event, event_registrations in registrations.items():
        write_event_worksheet(workbook, event, event_registrations)

    workbook.close()

    return filename


def write_main_worksheet(workbook, registrations: list[RegistrationInfo]) -> None:
    main_worksheet = workbook.add_worksheet("Все регистрации")
    main_headers = [
        "Мероприятие",
        "Время регистрации",
        "Имя",
        "Номер телефона",
        "Email",
        "Компания",
        "Должность",
        "Комментарий",
    ]

    bold = workbook.add_format({"bold": True})
    for col in range(len(main_headers)):
        main_worksheet.write(0, col, main_headers[col], bold)

    current_row = 1
    for _, registrations in registrations.items():
        for registration in registrations:
            write_main_worksheet_row(main_worksheet, current_row, registration)
            current_row += 1

    main_worksheet.autofit()
    main_worksheet.set_column(0, 0, 30)


def write_main_worksheet_row(main_worksheet, current_row, registration):
    main_worksheet.write(current_row, 0, registration.event)
    main_worksheet.write(current_row, 1, registration.timestamp)
    main_worksheet.write(current_row, 2, registration.name)
    main_worksheet.write(current_row, 3, registration.phone)
    main_worksheet.write(current_row, 4, registration.email)
    main_worksheet.write(current_row, 5, registration.company)
    main_worksheet.write(current_row, 6, registration.position)
    main_worksheet.write(current_row, 7, registration.comment)


def write_event_worksheet(
    workbook, event: str, registrations: list[RegistrationInfo]
) -> None:
    invalid_chars = ["[", "]", ":", "*", "?", "/", "\\"]
    sheet_name = event
    for char in invalid_chars:
        sheet_name = sheet_name.replace(char, "")
    event_worksheet = workbook.add_worksheet(sheet_name[:31])

    event_headers = [
        "Время регистрации",
        "Имя",
        "Номер телефона",
        "Email",
        "Компания",
        "Должность",
        "Комментарий",
    ]

    bold = workbook.add_format({"bold": True})
    for col in range(len(event_headers)):
        event_worksheet.write(0, col, event_headers[col], bold)

    for current_row, registration in enumerate(registrations, start=1):
        write_event_sheet_row(event_worksheet, current_row, registration)

    event_worksheet.autofit()


def write_event_sheet_row(event_worksheet, current_row, registration):
    event_worksheet.write(current_row, 0, registration.timestamp)
    event_worksheet.write(current_row, 1, registration.name)
    event_worksheet.write(current_row, 2, registration.phone)
    event_worksheet.write(current_row, 3, registration.email)
    event_worksheet.write(current_row, 4, registration.company)
    event_worksheet.write(current_row, 5, registration.position)
    event_worksheet.write(current_row, 6, registration.comment)
