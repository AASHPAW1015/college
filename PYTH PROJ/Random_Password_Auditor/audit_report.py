import pandas as pd
import matplotlib.pyplot as plt
import datetime

class AuditLogger:
    """Handles logging of audit events."""
    
    @staticmethod
    def log(message):
        """Simple logger that prints to console with timestamp."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")


class AuditReport:
    """Generates reports and visualizations."""

    def __init__(self, audit_data):
        self.audit_data = audit_data
        self.df = pd.DataFrame(audit_data)

    def save_to_csv(self, filename="audit_results.csv"):
        """Saves audit results to CSV."""
        try:
            self.df.to_csv(filename, index=False)
            AuditLogger.log(f"Results saved to {filename}")
        except Exception as e:
            AuditLogger.log(f"Error saving CSV: {e}")

    def generate_txt_report(self, filename="audit_report.txt"):
        """Generates a comprehensive text report."""
        total = len(self.df)
        strength_counts = self.df['Strength'].value_counts()
        avg_score = self.df['Score'].mean()
        
        strong_count = strength_counts.get("Strong", 0)
        medium_count = strength_counts.get("Medium", 0)
        weak_count = strength_counts.get("Weak", 0)
        
        weak_passwords = self.df[self.df['Strength'] == 'Weak'].head(5)
        
        report = f"""RANDOM PASSWORD AUDITOR
AUDIT SUMMARY:
Audit Date: {datetime.date.today()}
Total Passwords Tested: {total}

STRENGTH DISTRIBUTION:
Strong: {strong_count} ({strong_count/total*100:.1f}%)
Medium: {medium_count} ({medium_count/total*100:.1f}%)
Weak: {weak_count} ({weak_count/total*100:.1f}%)

WEAK PASSWORDS IDENTIFIED (Top 5):
"""
        for i, row in weak_passwords.iterrows():
            number = i + 1
            password = row["Password"]
            vulnerabilities = ", ".join(row["Vulnerabilities"])

            report += f'{number}. "{password}" - {vulnerabilities}\n'
            
        report += f"""
SECURITY SCORE: {int(avg_score)}/100

RECOMMENDATIONS:
1. All weak passwords must be changed.
2. Enforce minimum 12 character length.
3. Require special character usage.
4. Implement password expiry policy.

AUDIT CERTIFICATION:
Status: {'PASS' if weak_count == 0 else 'CONDITIONAL PASS' if weak_count < 5 else 'FAIL'}
Weak Passwords: {weak_count} (to be remediated)
"""
        try:
            with open(filename, 'w') as f:
                f.write(report)
            AuditLogger.log(f"Report saved to {filename}")
        except Exception as e:
            AuditLogger.log(f"Error saving TXT report: {e}")

    def create_visualizations(self):
        """Creates strength distribution chart."""
        if self.df.empty:
            return

        try:
            plt.figure(figsize=(8, 6))
            strength_counts = self.df['Strength'].value_counts()
            colors = {'Strong': 'green', 'Medium': 'orange', 'Weak': 'red'}
            
            # Map colors to the indices presented in strength_counts
            bar_colors = [colors.get(x, 'blue') for x in strength_counts.index]
            
            strength_counts.plot(kind='bar', color=bar_colors)
            plt.title('Password Strength Distribution')
            plt.xlabel('Strength Category')
            plt.ylabel('Count')
            plt.tight_layout()
            plt.savefig('strength_distribution.png')
            AuditLogger.log("Visualization saved to strength_distribution.png")
            plt.close()
        except Exception as e:
            AuditLogger.log(f"Error creating visualization: {e}")
