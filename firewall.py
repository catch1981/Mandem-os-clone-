import os
import re

DEFAULT_PATTERNS = [
    r"sk-[A-Za-z0-9]{32,}",  # OpenAI style keys
    r"gh[pous]_[A-Za-z0-9]{36,}",  # GitHub tokens
    r"api[_-]?key",
    r"password",
    r"secret",
    r"token",
]

_custom = os.getenv("FIREWALL_PATTERNS")
if _custom:
    CUSTOM_PATTERNS = [p.strip() for p in _custom.split(',') if p.strip()]
    PATTERNS = [re.compile(p, re.IGNORECASE) for p in (CUSTOM_PATTERNS + DEFAULT_PATTERNS)]
else:
    PATTERNS = [re.compile(p, re.IGNORECASE) for p in DEFAULT_PATTERNS]

def sanitize_text(text: str) -> str:
    """Replace sensitive patterns with [BLOCKED]."""
    if not text:
        return text
    result = text
    for pat in PATTERNS:
        result = pat.sub("[BLOCKED]", result)
    return result
