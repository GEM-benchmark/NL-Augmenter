import re
from typing import List

from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


def weekday_month_abbreviate(text, max_outputs=1):
    abbdreviations = {
        "Monday": "Mon.",
        "Tuesday": "Tue.",
        "Wednesday": "Wed.",
        "Thursday": "Thu.",
        "Friday": "Fri.",
        "Saturday": "Sat.",
        "Sunday": "Sun.",
        "January": "Jan.",
        "February": "Feb.",
        "March": "Mar.",
        "April": "Apr.",
        "May": "May",
        "June": "Jun.",
        "July": "Jul.",
        "August": "Aug.",
        "September": "Sep.",
        "October": "Oct.",
        "November": "Nov.",
        "December": "Dec.",
    }

    expansions = {
        "Mon.": "Monday",
        "Tue.": "Tuesday",
        "Wed.": "Wednesday",
        "Thu.": "Thursday",
        "Fri.": "Friday",
        "Sat.": "Saturday",
        "Sun.": "Sunday",
        "Jan.": "January",
        "Feb.": "February",
        "Mar.": "March",
        "Apr.": "April",
        "May": "May",
        "Jun.": "June",
        "Jul.": "July",
        "Aug.": "August",
        "Sep.": "September",
        "Oct.": "October",
        "Nov.": "November",
        "Dec.": "December",
    }

    regex = re.compile(
        "(%s)"
        % (
            "|".join([x + "(?!s)" for x in abbdreviations.keys()])
            + "|"
            + "|".join([x.replace(".", "\\.") for x in expansions.keys()])
        )
    )

    return [
        regex.sub(
            lambda y: {**abbdreviations, **expansions}[
                y.string[y.start() : y.end()]
            ],
            text,
        )
    ]


class WeekdayMonthAbbreviation(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self):
        super().__init__()

    def generate(self, sentence: str) -> List[str]:
        perturbed_texts = weekday_month_abbreviate(text=sentence)
        return perturbed_texts
