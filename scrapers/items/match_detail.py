from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class MatchDetail:
    file_name: str
    match_id: str
    match_url: str
    match_status: str
    match_datetime: datetime
    has_rating: bool
    home_team: str
    outside_team: str
    home_team_score: int
    outside_team_score: int
    home_team_rating: Decimal
    draw_rating: Decimal
    outside_team_rating: Decimal
    championship_name: str
    country_name: str
    comment_number: int
