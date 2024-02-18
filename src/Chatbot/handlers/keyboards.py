from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from Chatbot.CallbackHasher import CallbackType, build_event_action_callback


def select_event(events: list[str]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    event,
                    callback_data=build_event_action_callback(
                        CallbackType.EVENT_REGISTRATIONS, event
                    ),
                )
            ]
            for event in events
        ]
    )


def select_mail_type(event: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Напоминания",
                    callback_data=build_event_action_callback(
                        CallbackType.EVENT_INFO_BEFORE_SENDING_CONFIRMATIONS, event
                    ),
                ),
                InlineKeyboardButton(
                    "Благодарности",
                    callback_data=build_event_action_callback(
                        CallbackType.EVENT_INFO_BEFORE_SENDING_THANKS, event
                    ),
                ),
            ]
        ]
    )


def build_email_or_change_event(event: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Создать пиьсмо",
                    callback_data=build_event_action_callback(
                        CallbackType.GENERATE_EMAIL, event
                    ),
                ),
                InlineKeyboardButton(
                    "Изменить",
                    callback_data=build_event_action_callback(
                        CallbackType.CHANGE_EVENT_DATA, event
                    ),
                ),
            ]
        ]
    )


def select_field_to_change(event: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Изменить ссылку",
                    callback_data=build_event_action_callback(
                        CallbackType.CHANGE_EVENT_LINK, event
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    "Изменить дату",
                    callback_data=build_event_action_callback(
                        CallbackType.CHANGE_EVENT_DATE, event
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    "Изменить время",
                    callback_data=build_event_action_callback(
                        CallbackType.CHANGE_EVENT_TIME, event
                    ),
                ),
            ],
            [
                InlineKeyboardButton(
                    "Назад",
                    callback_data=build_event_action_callback(
                        CallbackType.GO_BACK_FROM_CHANGING_EVENT_DATA, event
                    ),
                ),
            ],
        ]
    )


def send_email_or_cancel(event: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Отправить",
                    callback_data=build_event_action_callback(
                        CallbackType.SEND_EMAIL, event
                    ),
                ),
                InlineKeyboardButton(
                    "Отменить",
                    callback_data=build_event_action_callback(
                        CallbackType.CANCEL_SENDING_EMAIL, event
                    ),
                ),
            ]
        ]
    )
