from typing import Any


def get_reverse_choice(
        user_friendly_name: str,
        choice_attribute: Any
) -> str:
    choices = choice_attribute.field.choices
    for choice in choices:
        if user_friendly_name in choice:
            return choice[0]
    return ""
