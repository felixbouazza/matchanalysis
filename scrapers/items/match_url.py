from dataclasses import dataclass


@dataclass
class MatchUrl:
    file_name: str
    match_id: str
    match_url: str
    match_status: str
