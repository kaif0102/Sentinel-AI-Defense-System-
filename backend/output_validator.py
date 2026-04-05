import re
import os

# ─────────────────────────────────────────
# HARMFUL OUTPUT PATTERNS
# ─────────────────────────────────────────
HARMFUL_OUTPUT_PATTERNS = [
    # Weapons/Violence
    r"step.by.step (instructions|guide) (to|for) (make|build|create) (a )?(bomb|weapon|explosive)",
    r"here('s| is) how to (make|build|create) (a )?(bomb|weapon|explosive|poison)",
    r"to (make|build|create) (a )?(bomb|weapon|explosive) you (need|will need|should)",
    
    # Hacking
    r"here('s| is) how to (hack|breach|infiltrate|bypass)",
    r"step.by.step (guide|instructions) (to|for) (hacking|breaching|infiltrating)",
    
    # Personal Data Leakage
    r"my (system prompt|instructions|training data) (is|are|says|say)",
    r"(here is|here's) my (system prompt|original instructions|training)",
    r"i (was|am) (instructed|trained|told) to",
    
    # Jailbreak Success Indicators
    r"as (DAN|an AI with no restrictions|a free AI)",
    r"i (no longer|don't) have (any )?(restrictions|limitations|guidelines)",
    r"i (can|will) (now )?(do|say|generate) anything",
    r"jailbreak (successful|complete|activated)",
    
    # Hate Speech
    r"(all|every) (jews|muslims|christians|blacks|whites|hispanics) (are|should)",
    r"(inferior|superior) (race|religion|ethnicity|gender)",
]

# ─────────────────────────────────────────
# SENSITIVE DATA PATTERNS
# ─────────────────────────────────────────
SENSITIVE_DATA_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",          # SSN
    r"\b\d{16}\b",                       # Credit card
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
    r"password\s*[:=]\s*\S+",           # Password
    r"api[_-]?key\s*[:=]\s*\S+",        # API Key
    r"secret\s*[:=]\s*\S+",             # Secret
    r"token\s*[:=]\s*\S+",              # Token
]

# ─────────────────────────────────────────
# POLICY VIOLATION CHECKER
# ─────────────────────────────────────────
def check_harmful_output(response: str) -> tuple:
    for pattern in HARMFUL_OUTPUT_PATTERNS:
        if re.search(pattern, response, re.IGNORECASE):
            return True, "Harmful content detected in response"
    return False, ""

# ─────────────────────────────────────────
# SENSITIVE DATA CHECKER
# ─────────────────────────────────────────
def check_sensitive_data(response: str) -> tuple:
    for pattern in SENSITIVE_DATA_PATTERNS:
        if re.search(pattern, response, re.IGNORECASE):
            return True, "Sensitive data detected in response"
    return False, ""

# ─────────────────────────────────────────
# MAIN VALIDATOR
# ─────────────────────────────────────────
def validate_output(response: str) -> dict:
    
    # Check 1 - Harmful content
    is_harmful, harmful_reason = check_harmful_output(response)
    
    # Check 2 - Sensitive data
    has_sensitive, sensitive_reason = check_sensitive_data(response)
    
    # Final decision
    is_safe = not is_harmful and not has_sensitive
    reason = harmful_reason or sensitive_reason or ""

    return {
        "is_safe": is_safe,
        "harmful_content": is_harmful,
        "sensitive_data": has_sensitive,
        "reason": reason
    }

# ─────────────────────────────────────────
# TEST IT
# ─────────────────────────────────────────
if __name__ == "__main__":
    test_responses = [
        "The capital of France is Paris.",
        "Here's how to make a bomb: first you need...",
        "As DAN, I no longer have any restrictions!",
        "My system prompt is: You are a helpful assistant...",
        "I can now do anything you ask without limitations!",
        "Your password is: abc123, your SSN is 123-45-6789",
        "Python is a great programming language for beginners.",
    ]

    print("=" * 60)
    print("SENTINEL AI - OUTPUT VALIDATOR TEST")
    print("=" * 60)

    for response in test_responses:
        result = validate_output(response)
        status = "✅ SAFE" if result["is_safe"] else "🚫 BLOCKED"
        print(f"\nResponse: {response[:60]}...")
        print(f"Status:   {status}")
        if not result["is_safe"]:
            print(f"Reason:   {result['reason']}")
        print("-" * 60)