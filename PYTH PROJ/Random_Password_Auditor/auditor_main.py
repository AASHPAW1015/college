import time
from password_class import PasswordAuditor
from audit_report import AuditReport, AuditLogger

def audit_decorator(func):
    """Decorator to log the start and end of the audit process."""
    def wrapper(*args, **kwargs):
        AuditLogger.log("Starting Security Audit...")
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        AuditLogger.log(f"Audit completed in {duration:.2f} seconds.")
        return result
    return wrapper

@audit_decorator
def main():
    try:
        # Initialize Auditor
        auditor = PasswordAuditor()
        
        # 1. Batch Password Generation
        count = 50
        AuditLogger.log(f"Generating {count} random passwords...")
        auditor.generate_random_passwords(count)
        
        # 2. Password Auditing
        AuditLogger.log("Analyzing password strength...")
        results = auditor.run_audit()
        
        # 3. Audit Reporting & Visualization
        AuditLogger.log("Generating reports...")
        reporter = AuditReport(results)
        
        reporter.save_to_csv("audit_results.csv")
        reporter.generate_txt_report("audit_report.txt")
        reporter.create_visualizations()
        
        AuditLogger.log("Audit process finished successfully.")
        
        # Print a snippet of the output to console for verification
        print("\n--- Snippet of Audit Results ---")
        print(reporter.df.head())
        print("--------------------------------")

    except Exception as e:
        AuditLogger.log(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    main()
