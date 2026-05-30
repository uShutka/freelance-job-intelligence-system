import re

from freelance_job_intelligence_system.config import PROFILE_SKILLS

RATE_RE = re.compile(r"(?:\$|€|eur\s*)\s?(\d{2,3})(?:\s?[-/]\s?(\d{2,3}))?\s?(?:/h|hr|hourly|per hour)?", re.IGNORECASE)
REMOTE_RE = re.compile(r"\b(remote|worldwide|anywhere|async)\b", re.IGNORECASE)
LOCATION_RE = re.compile(r"\b(US|EU|Europe|Estonia|Remote|Worldwide|UK|Germany|Canada)\b", re.IGNORECASE)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def extract_rate(text: str) -> int | None:
    match = RATE_RE.search(text or "")
    if not match:
        return None
    first = int(match.group(1))
    second = int(match.group(2)) if match.group(2) else first
    return round((first + second) / 2)


def extract_location(text: str) -> str:
    match = LOCATION_RE.search(text or "")
    if not match:
        return "not specified"
    value = match.group(1)
    return "remote" if value.lower() in {"remote", "worldwide", "anywhere", "async"} else value.upper()


def is_remote(text: str) -> bool:
    return bool(REMOTE_RE.search(text or ""))


def extract_skills(text: str, skills: list[str] | None = None) -> list[str]:
    haystack = normalize_text(text).lower()
    known_skills = skills or PROFILE_SKILLS
    found = []
    for skill in known_skills:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, haystack):
            found.append(skill)
    return sorted(set(found))


def classify_level(text: str) -> str:
    lower = normalize_text(text).lower()
    if re.search(r"\b(senior|lead|principal|8\+|7\+|staff)\b", lower):
        return "senior"
    if re.search(r"\b(junior|entry level|intern)\b", lower):
        return "junior"
    return "middle"
