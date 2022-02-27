"""Main survey file.
"""
import os

import numpy as np
from flask_login import current_user
from hemlock import User, Page, utils
from hemlock.functional import compile, validate, test_response
from hemlock.questions import Check, Input, Label, Range, Select, Textarea
from hemlock_ax import Assigner
from sqlalchemy_mutable.utils import partial

assigner = Assigner({"color": ("red", "green", "blue"), "body": ("car", "truck")})
wtp_color = {
    "red": 0,
    "green": -200,
    "blue": 200
}
wtp_body = {
    "car": 10000,
    "truck": 15000
}


@User.route("/survey")
def seed():
    """Creates the main survey branch.

    Returns:
        List[Page]: List of pages shown to the user.
    """
    assignment = assigner.assign_user()
    return [
        Page(
            Input(
                f"How much would you pay for a {assignment['color']} {assignment['body']}?",
                prepend="$",
                append=".00",
                input_tag={"type": "number", "min": 0},
                variable="target",
                test_response=max(0, wtp_color[assignment["color"]] + wtp_body[assignment["body"]] + np.random.normal(0, 5000))
            )
        ),
        Page(
            Label("Thanks for participating!"),
        )
    ]
