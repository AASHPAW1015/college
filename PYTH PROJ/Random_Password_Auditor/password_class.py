import random
import string
import re

class SecurityAnalyzer:
    """Evaluates password strength and identifies vulnerabilities."""

    @staticmethod
    def calculate_score(password):
        """Calculates a security score (0-100) using lambda logic."""
        score = 0
        
        # Criteria checks using lambdas
        length_score = (lambda p: min(len(p) * 4, 40))(password)  # Up to 40 pts for length
        upper_score = (lambda p: 10 if any(c.isupper() for c in p) else 0)(password)
        lower_score = (lambda p: 10 if any(c.islower() for c in p) else 0)(password)
        digit_score = (lambda p: 20 if any(c.isdigit() for c in p) else 0)(password)
        special_score = (lambda p: 20 if any(c in string.punctuation for c in p) else 0)(password)
        
        score = length_score + upper_score + lower_score + digit_score + special_score
        return min(score, 100)

    @staticmethod
    def identify_vulnerabilities(password):
        """Identifies specific weaknesses in the password."""
        issues = []
        if len(password) < 8:
            issues.append("Too short (< 8 chars)")
        if not any(c.isdigit() for c in password):
            issues.append("Missing numbers")
        if not any(c.isupper() for c in password):
            issues.append("Missing uppercase")
        if not any(c in string.punctuation for c in password):
            issues.append("Missing special characters")
        
        # Simple pattern checks
        common_patterns = ["123", "abc", "password", "admin", "test"]
        if any(pat in password.lower() for pat in common_patterns):
            issues.append("Predictable pattern found")
            
        return issues

    @staticmethod
    def evaluate_strength(score):
        """Categorizes score into Weak, Medium, Strong."""
        if score < 50:
            return "Weak"
        elif score < 80:
            return "Medium"
        else:
            return "Strong"


class PasswordAuditor:
    """Generates and tests passwords."""

    def __init__(self):
        self.passwords = []
        self.audit_results = []

    def generate_random_passwords(self, count=50):
        """Generates a batch of random passwords with varying complexity."""
        self.passwords = []
        chars = string.ascii_letters + string.digits + string.punctuation
        
        for _ in range(count):
            # Randomize length between 6 and 16 to ensure a mix of weak/strong
            length = random.randint(6, 16)
            
            # Occasionally create intentionally weak passwords for demonstration
            if random.random() < 0.2:
                p = "".join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(4, 8)))
            else:
                p = "".join(random.choices(chars, k=length))
            
            self.passwords.append(p)
        return self.passwords

    def run_audit(self):
        """Audits the generated passwords using SecurityAnalyzer."""
        self.audit_results = []
        for pwd in self.passwords:
            score = SecurityAnalyzer.calculate_score(pwd)
            strength = SecurityAnalyzer.evaluate_strength(score)
            vulns = SecurityAnalyzer.identify_vulnerabilities(pwd)
            
            self.audit_results.append({
                "Password": pwd,
                "Score": score,
                "Strength": strength,
                "Vulnerabilities": vulns
            })
        return self.audit_results
