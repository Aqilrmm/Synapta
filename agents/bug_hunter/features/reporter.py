# reporter.py

"""
Reporter Module for Bug Hunter Agent
Handles reporting of scan results and issues found during analysis
"""

import logging
from typing import List, Dict

class Reporter:
    """Handles reporting of findings from the bug hunter agent"""

    def __init__(self):
        self.logger = logging.getLogger("bug_hunter.reporter")

    def report_findings(self, findings: List[Dict[str, str]]):
        """Report findings from the bug scan"""
        if not findings:
            self.logger.info("No findings to report.")
            return
        
        self.logger.info("Reporting findings:")
        for finding in findings:
            self.logger.info(f"🔍 Finding: {finding.get('issue')}, Severity: {finding.get('severity')}")
    
    def generate_report(self, findings: List[Dict[str, str]]) -> str:
        """Generate a summary report of findings"""
        report_lines = ["Bug Hunter Report", "=" * 20]
        for finding in findings:
            report_lines.append(f"Issue: {finding.get('issue')}, Severity: {finding.get('severity')}")
        
        report = "\n".join(report_lines)
        self.logger.info("Report generated successfully.")
        return report

    def save_report(self, report: str, file_path: str):
        """Save the report to a file"""
        try:
            with open(file_path, 'w') as file:
                file.write(report)
            self.logger.info(f"Report saved to {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to save report: {e}")
