import uuid
from typing import Tuple

from flask import Response, jsonify
from smarttesting.bik.score.analysis.score_analyzer import ScoreAnalyzer
from smarttesting.bik.score.domain.pesel import Pesel


def score(pesel: str, score_analyzer: ScoreAnalyzer) -> Tuple[Response, int]:
    if score_analyzer.should_grant_loan(Pesel(pesel)):
        return (
            jsonify(
                user_id=str(uuid.uuid4()),
                status="VERIFICATION_PASSED",
            ),
            200,
        )

    return jsonify(user_id=str(uuid.uuid4()), status="VERIFICATION_FAILED"), 403
