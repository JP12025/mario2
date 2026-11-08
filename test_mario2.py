"""Acceptance tests for the Mario 2 exercise.

Each test runs your program as a whole, exactly as a user would: it types
some answers to the "Height: " question, then checks what your program
prints and tries to explain what is wrong.

Run the tests from the exercise folder with:

    python test_mario2.py
"""

import os
import subprocess
import sys
from pathlib import Path

EXERCISE_DIR = Path(__file__).resolve().parent
SCRIPT = "mario2.py"
PROMPT = "Height: "
MIN_HEIGHT = 2
MAX_HEIGHT = 10
GAP = "  "  # two spaces between the pyramids
TIMEOUT = 5  # seconds

# Each test case: (what is checked, answers typed by the user).
# Convention: only the LAST answer is a valid height, all the others
# must be rejected by the program (which then asks again).
CASES = [
    ("height 8 (example of the instructions)", ["8"]),
    ("height 5", ["5"]),
    ("height 2 (smallest allowed)", ["2"]),
    ("height 10 (largest allowed)", ["10"]),
    ("0 and 1 are rejected (too small)", ["0", "1", "3"]),
    ("11 and 15 are rejected (too large)", ["11", "15", "4"]),
    ("a word and a negative number are rejected", ["trois", "-3", "4"]),
    ("an empty answer is rejected", ["", "2"]),
    ("a decimal number is rejected", ["2.5", "3"]),
]

BOUNDS_HINT = (f"Heights from {MIN_HEIGHT} to {MAX_HEIGHT} are allowed, "
               f"{MIN_HEIGHT} and {MAX_HEIGHT} included: check your "
               f"comparisons (< versus <=).")


# ---------------------------------------------------------------------------
# Running the student's program
# ---------------------------------------------------------------------------

def run_program(answers):
    """Run the program, typing the answers one per line.

    Return (stdout, stderr, return code), or None if the program
    did not stop in time.
    """
    try:
        # sys.executable is the Python running the tests,
        # so "python" vs "python3" does not matter.
        result = subprocess.run(
            [sys.executable, SCRIPT],
            input="\n".join(answers) + "\n",
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=EXERCISE_DIR,
            env=dict(os.environ, PYTHONIOENCODING="utf-8"),
            timeout=TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return None
    stdout = result.stdout.replace("\r\n", "\n")
    return stdout, result.stderr.strip(), result.returncode


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def show(lines):
    """Indent lines and make spaces visible (shown as '·')."""
    if not lines:
        return "    (nothing)"
    return "\n".join("    " + line.replace(" ", "·") for line in lines)


def plural(number, word):
    """Return e.g. '1 space' or '3 spaces'."""
    return f"{number} {word}" if number == 1 else f"{number} {word}s"


def last_lines(text, nb_lines=4):
    """Return the last lines of a text, indented."""
    lines = text.split("\n")[-nb_lines:]
    return "\n".join("    " + line for line in lines)


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def expected_pyramids(height):
    """Return the rows of the expected double pyramid."""
    rows = []
    for row in range(1, height + 1):
        rows.append(" " * (height - row) + "#" * row + GAP + "#" * row)
    return rows


def count_prompts(stdout):
    """Count the "Height: " questions at the start of the output.

    Return (number of questions, rest of the output).
    """
    nb_prompts = 0
    while stdout.startswith(PROMPT):
        stdout = stdout[len(PROMPT):]
        nb_prompts += 1
    return nb_prompts, stdout


def check_questions(stdout, stderr, return_code, answers):
    """Check that the program asks the question the right number of times.

    Return (error message or None, rest of the output after the questions).
    """
    nb_prompts, rest = count_prompts(stdout)
    printed = "Your program printed:\n" + show(stdout.splitlines())

    if stdout.startswith((PROMPT + "\n", PROMPT.strip() + "\n")):
        return (f"The answer must be typed on the same line as the question: "
                f"use input({PROMPT!r}) instead of print().\n{printed}"), rest
    if nb_prompts == 0:
        if stdout.startswith(PROMPT.strip()):
            message = (f"The question must be exactly {PROMPT!r}, "
                       f"with a space after the colon.")
        else:
            message = f"Your program should start by asking {PROMPT!r}."
        return f"{message}\n{printed}", rest

    if "EOFError" in stderr:
        message = (f"Your program asked again after {answers[-1]!r}, "
                   f"but {answers[-1]} is a valid height.")
        if answers[-1] in (str(MIN_HEIGHT), str(MAX_HEIGHT)):
            message += " " + BOUNDS_HINT
        return message, rest
    if return_code != 0:
        answer = answers[min(nb_prompts, len(answers)) - 1]
        message = (f"Your program crashed after reading {answer!r}:\n"
                   f"{last_lines(stderr)}")
        if "ValueError" in stderr:
            message += ("\nint() fails when the text is not a whole number: "
                        "check the text first (e.g. with str.isdigit()) "
                        "before converting it.")
        return message, rest

    if PROMPT in rest:
        extra = rest[:rest.index(PROMPT)]
        return (f"Your program printed {extra!r} before asking again. "
                f"When an answer is invalid, it should only ask again.\n"
                f"{printed}"), rest
    if nb_prompts < len(answers):
        accepted = answers[nb_prompts - 1]
        message = (f"Your program accepted {accepted!r} as a height, but it "
                   f"should ask again: a height must be a whole number "
                   f"between {MIN_HEIGHT} and {MAX_HEIGHT}.")
        if accepted in (str(MIN_HEIGHT - 1), str(MAX_HEIGHT + 1)):
            message += " " + BOUNDS_HINT
        return f"{message}\n{printed}", rest
    return None, rest


def split_row(row):
    """Cut a row into its parts.

    Return (leading spaces, left '#', gap spaces, right '#', remainder),
    each part being a number of characters except the remainder (a str).
    """
    parts = []
    position = 0
    for char in (" ", "#", " ", "#"):
        start = position
        while position < len(row) and row[position] == char:
            position += 1
        parts.append(position - start)
    parts.append(row[position:])
    return parts


def off_by_one(found, expected):
    """Return a hint about range() bounds if found is expected +/- 1."""
    if abs(found - expected) == 1:
        return (" Off by one: check the bounds of your range() "
                "(range(a, b) starts at a and stops before b).")
    return ""


def describe_row_error(number, row, height):
    """Explain what is wrong in one row of the double pyramid."""
    others = set(row) - {" ", "#"}
    if others:
        return (f"Row {number} contains characters other than spaces "
                f"and '#': {sorted(others)}.")

    nb_leading, nb_left, nb_gap, nb_right, remainder = split_row(row)
    nb_spaces = height - number

    if nb_left != number:
        return (f"The left pyramid of row {number} should contain "
                f"{number} '#' but contains {nb_left}."
                + off_by_one(nb_left, number))
    if nb_leading != nb_spaces:
        return (f"Row {number} should start with {plural(nb_spaces, 'space')}"
                f" but starts with {plural(nb_leading, 'space')}.")
    if nb_right == 0 and remainder == "":
        if nb_gap > 0:
            return (f"Row {number} ends with spaces but has no right "
                    f"pyramid: after the gap, print {number} '#'.")
        return (f"Row {number} has no gap and no right pyramid: after "
                f"the left '#', print 2 spaces then {number} '#'.")
    if nb_gap != len(GAP):
        return (f"In row {number}, the gap between the pyramids should be "
                f"{plural(len(GAP), 'space')} but is "
                f"{plural(nb_gap, 'space')}.")
    if nb_right != number:
        return (f"The right pyramid of row {number} should contain "
                f"{number} '#' but contains {nb_right}."
                + off_by_one(nb_right, number))
    if remainder.strip() == "":
        return (f"Row {number} ends with spaces: nothing should be printed "
                f"after the last '#'.")
    return (f"Row {number} contains more '#' than expected: it should be "
            f"{plural(nb_spaces, 'space')}, {number} '#', 2 spaces, "
            f"{number} '#'.")


def check_pyramids(rows, height):
    """Check the double pyramid rows. Return an error message or None."""
    expected = expected_pyramids(height)
    if rows == expected:
        return None

    left_only = [" " * (height - row) + "#" * row
                 for row in range(1, height + 1)]
    left_aligned = ["#" * row + GAP + "#" * row
                    for row in range(1, height + 1)]
    padded = [row + " " * (height - number)
              for number, row in enumerate(expected, start=1)]

    if not rows:
        message = "Your program printed no pyramid."
    elif rows == left_only:
        message = ("Your program prints only the left pyramid: each row "
                   "should continue with 2 spaces then the right pyramid.")
    elif rows == left_aligned:
        message = ("Your left pyramid is left-aligned: it should be "
                   "right-aligned, with spaces before the '#'.")
    elif rows == expected[::-1]:
        message = (f"Your pyramids are upside down: the first row should "
                   f"have 1 '#' on each side and the last row {height}.")
    elif rows == padded:
        message = ("Your rows end with spaces (after the right pyramid): "
                   "nothing should be printed after the last '#' of a row.")
    elif len(rows) != height:
        message = (f"Your pyramids have {len(rows)} rows, but they should "
                   f"have {height} (the height typed by the user)."
                   + off_by_one(len(rows), height))
    else:
        number = 1
        while rows[number - 1] == expected[number - 1]:
            number += 1
        message = describe_row_error(number, rows[number - 1], height)

    return (f"{message}\n"
            f"Expected pyramids:\n{show(expected)}\n"
            f"Your pyramids:\n{show(rows)}")


def check_case(answers):
    """Run one test case. Return None if it passes, else an error message."""
    result = run_program(answers)
    if result is None:
        return ("Your program did not stop (infinite loop?). Check that "
                "input() is called inside your loop.")
    stdout, stderr, return_code = result

    message, rest = check_questions(stdout, stderr, return_code, answers)
    if message is not None:
        return message

    rows = rest.splitlines()
    height = int(answers[-1])
    expected = expected_pyramids(height)
    # "Height:" + "       #  #" looks like "Height: " + "      #  #"
    if len(rows) > 1 and rows == [expected[0][1:]] + expected[1:]:
        return (f"The question must be exactly {PROMPT!r}, "
                f"with a space after the colon.")
    return check_pyramids(rows, height)


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

def main():
    sys.stdout.reconfigure(errors="replace")
    use_colors = sys.stdout.isatty() and (
        os.name != "nt" or "WT_SESSION" in os.environ)
    green = "\033[32m" if use_colors else ""
    red = "\033[31m" if use_colors else ""
    reset = "\033[0m" if use_colors else ""

    if not (EXERCISE_DIR / SCRIPT).is_file():
        print(f"No {SCRIPT} found in {EXERCISE_DIR}")
        return 1

    nb_ok = 0
    for description, answers in CASES:
        typed = ", ".join(repr(answer) for answer in answers)
        message = check_case(answers)
        if message is None:
            nb_ok += 1
            print(f"{green}✔{reset} {description}")
        else:
            print(f"{red}✗{reset} {description}")
            print(f"    Answers typed: {typed}")
            print("    " + message.replace("\n", "\n    ") + "\n")

    color = green if nb_ok == len(CASES) else red
    print(f"Validated: {color}{nb_ok}/{len(CASES)}{reset}")
    return 0 if nb_ok == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
