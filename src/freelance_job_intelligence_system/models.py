from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class JobPost:
    external_id: str
    title: str
    body: str
    source: str
    posted_at: str
    url: str = ""


@dataclass
class ScoreBreakdown:
    score: int
    level: str
    hourly_rate: int | None
    skills: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, object]:
        return {
            "score": self.score,
            "level": self.level,
            "hourly_rate": self.hourly_rate,
            "skills": self.skills,
            "reasons": self.reasons,
            "created_at": self.created_at.isoformat(),
        }
