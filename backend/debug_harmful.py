import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from risk_engine import ATTACK_PATTERNS, HARMFUL_PATTERNS
import re
import base64

prompt = "Tell me about cybersecurity"
print(f"Testing: {prompt}")
print("=" * 50)

# Check ATTACK_PATTERNS
print("\nChecking ATTACK_PATTERNS:")
for pattern in ATTACK_PATTERNS:
    if re.search(pattern, prompt, re.IGNORECASE):
        print(f"MATCH: {pattern}")
    
# Check HARMFUL_PATTERNS
print("\nChecking HARMFUL_PATTERNS:")
for pattern in HARMFUL_PATTERNS:
    if re.search(pattern, prompt, re.IGNORECASE):
        print(f"MATCH: {pattern}")
    
# Check leet normalization
leet_map = {
    '0': 'o', '1': 'i', '3': 'e',
    '4': 'a', '5': 's', '@': 'a',
    '7': 't', '!': 'i'
}
normalized = prompt.lower()
for leet, normal in leet_map.items():
    normalized = normalized.replace(leet, normal)
print(f"\nNormalized: {normalized}")

# Check keywords in normalized
keywords = ['ignore', 'instructions', 'previous',
            'bypass', 'jailbreak', 'system']
for word in keywords:
    if word in normalized:
        print(f"KEYWORD MATCH: {word}")

# Check dehyphenated
dehyphenated = re.sub(r'[-\s]+', '', prompt.lower())
print(f"\nDehyphenated: {dehyphenated}")

keywords2 = ['ignoreallinstructions', 'ignoreprevious',
             'ignoreall', 'bypass', 'jailbreak']
for word in keywords2:
    if word in dehyphenated:
        print(f"DEHYPHENATED MATCH: {word}")

# Check base64
print("\nChecking Base64 decode:")
try:
    decoded = base64.b64decode(prompt).decode('utf-8')
    print(f"Decoded: {decoded}")
except:
    print("Not valid base64")
    # Check if cybersecurity contains any keywords
check_words = ['ignore', 'instructions', 'previous',
               'bypass', 'jailbreak', 'system', 
               'hack', 'attack', 'inject']

dehyphenated = "tellmeaboutcybersecurity"
print("\nChecking dehyphenated for keywords:")
for word in check_words:
    if word in dehyphenated:
        print(f"FOUND: '{word}' in '{dehyphenated}'")

# Test the actual functions
from risk_engine import check_harmful, check_rules, decode_and_check, compute_risk

print("\nDirect function tests:")
print(f"check_rules: {check_rules(prompt)}")
print(f"check_harmful: {check_harmful(prompt)}")
print(f"decode_and_check: {decode_and_check(prompt)}")

print("\nFull compute_risk:")
result = compute_risk(prompt)
for key, value in result.items():
    if key != 'prompt':
        print(f"  {key}: {value}")

# Debug decode_and_check step by step
print("\nDebugging decode_and_check step by step:")

# Step 1 - Base64
try:
    decoded = base64.b64decode(prompt).decode('utf-8')
    print(f"Base64 decoded: {decoded}")
    print(f"check_rules on decoded: {check_rules(decoded)}")
    print(f"check_harmful on decoded: {check_harmful(decoded)}")
    keywords = ['ignore', 'instructions', 'previous',
                'bypass', 'jailbreak', 'system']
    for word in keywords:
        if word in decoded.lower():
            print(f"KEYWORD in decoded: {word}")
except Exception as e:
    print(f"Base64 failed: {e}")

# Step 2 - Leet speak
leet_map = {
    '0': 'o', '1': 'i', '3': 'e',
    '4': 'a', '5': 's', '@': 'a',
    '7': 't', '!': 'i'
}
normalized = prompt.lower()
for leet, normal in leet_map.items():
    normalized = normalized.replace(leet, normal)
print(f"\nLeet normalized: {normalized}")
print(f"check_rules on normalized: {check_rules(normalized)}")
print(f"check_harmful on normalized: {check_harmful(normalized)}")
keywords2 = ['ignore', 'instructions', 'previous',
            'bypass', 'jailbreak', 'system']
for word in keywords2:
    if word in normalized:
        print(f"KEYWORD in normalized: {word}")

# Step 3 - Dehyphenated
dehyphenated = re.sub(r'[-\s]+', '', prompt.lower())
print(f"\nDehyphenated: {dehyphenated}")
print(f"check_rules on dehyphenated: {check_rules(dehyphenated)}")
print(f"check_harmful on dehyphenated: {check_harmful(dehyphenated)}")
keywords3 = ['ignoreallinstructions', 'ignoreprevious',
             'ignoreall', 'bypass', 'jailbreak']
for word in keywords3:
    if word in dehyphenated:
        print(f"KEYWORD in dehyphenated: {word}")

# Find exact matching pattern in dehyphenated
dehyphenated = "tellmeaboutcybersecurity"
print("\nFinding exact ATTACK_PATTERN match on dehyphenated:")
for pattern in ATTACK_PATTERNS:
    if re.search(pattern, dehyphenated, re.IGNORECASE):
        print(f"MATCH: {pattern}")