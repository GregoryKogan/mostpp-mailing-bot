REGISTRATION_PERIOD = 2  # in months

# all of these keywords should be in the subject
REGISTRATION_SUBJECT_KEYWORDS = [
    "регистрация",
    "мероприятие",
]

REGISTRATIONS_CACHE_LIFETIME = 180  # in seconds

EVENTS_BASE_URL = "https://mostpp.ru"
FUTURE_EVENTS_PAGE_URL = f"{EVENTS_BASE_URL}/events"
PAST_EVENTS_PAGE_URL = f"{EVENTS_BASE_URL}/events/?filter=past"


# Project structure
PRE_EVENT_EMAIL_TEMPLATE_PATH = "assets/email_templates/pre-event-email-template.txt"
PRE_EVENT_EMAIL_SUBJECT_TEMPLATE_PATH = (
    "assets/email_templates/pre-event-email-subject-template.txt"
)
POST_EVENT_EMAIL_TEMPLATE_PATH = "assets/email_templates/post-event-email-template.txt"
POST_EVENT_EMAIL_SUBJECT_TEMPLATE_PATH = (
    "assets/email_templates/post-event-email-subject-template.txt"
)
