"""Phase 4: command line questionnaire that builds the student's search profile."""


def _ask_float(prompt, default=None):
    while True:
        raw = input(prompt).strip()
        if not raw and default is not None:
            return default
        try:
            return float(raw)
        except ValueError:
            print("  Please enter a number.")


def _ask_choice(prompt, options):
    """options: dict of accepted-input -> canonical value (keys are lowercase)."""
    option_hint = "/".join(options.keys())
    while True:
        raw = input(f"{prompt} ({option_hint}): ").strip().lower()
        if raw in options:
            return options[raw]
        print(f"  Please answer one of: {option_hint}")


def _ask_text(prompt):
    while True:
        raw = input(prompt).strip()
        if raw:
            return raw
        print("  Please enter a value.")


def run_intake():
    answers = {}

    answers["budget_max"] = _ask_float("1. What is your monthly budget maximum? $")

    answers["unit_type"] = _ask_choice(
        "2. Do you want the entire unit to yourself, or are you open to a shared house?",
        {"entire": "entire", "shared": "shared"},
    )

    if answers["unit_type"] == "shared":
        answers["room_privacy"] = _ask_choice(
            "3. Do you want a private room, or are you open to sharing a room?",
            {"private": "private", "shared": "shared"},
        )
        answers["bathroom_privacy"] = _ask_choice(
            "4. Do you want a private bathroom, or are you open to sharing a bathroom?",
            {"private": "private", "shared": "shared"},
        )
    else:
        answers["room_privacy"] = "private"
        answers["bathroom_privacy"] = "private"

    answers["unit_size"] = _ask_choice(
        "5. Unit size preference: studio, one bedroom, two bedroom, or three plus bedroom?",
        {
            "studio": "studio",
            "one bedroom": "1br", "1 bedroom": "1br", "1br": "1br", "one": "1br",
            "two bedroom": "2br", "2 bedroom": "2br", "2br": "2br", "two": "2br",
            "three plus bedroom": "3br+", "3+ bedroom": "3br+", "3br+": "3br+",
            "three plus": "3br+", "3plus": "3br+",
        },
    )

    answers["distance_max_miles"] = _ask_float(
        "6. Location anchor: max distance from USC in miles? [default 3]: ", default=3.0
    )

    answers["move_in_date"] = _ask_text("7. What is your move in date? ")

    answers["has_pet"] = _ask_choice(
        "8. Do you have a pet?",
        {"yes": True, "y": True, "no": False, "n": False},
    )

    return answers


if __name__ == "__main__":
    profile = run_intake()
    print("\n--- Stored intake answers ---")
    for key, value in profile.items():
        print(f"  {key}: {value!r}")
