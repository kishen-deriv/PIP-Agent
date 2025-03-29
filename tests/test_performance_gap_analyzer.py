"""
Test script for the Performance Gap Analyzer tool
"""

import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from tools.performance_gap_analyzer import PerformanceGapAnalyzerTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_performance_gap_analyzer():
    """Test the performance gap analyzer tool with a sample input"""
    
    # Sample input from real_sample_2.txt
    sample_input = """
Timestamp:
12/31/2024 16:45:42

Email Address:
sean@regentmarkets.com

Your Name:
Sean 

Employee's Name:
Shane

Employee's Role:
QA TL

Slack Channel Name:
pip-dubai-indulekha_pottakkatt

What is the specific performance gap?
Lack of Progress and Proactive Action on the Visual Automation Tool Evaluation

Provide specific examples of how this gap reflects in the employee's work performance
Throughout Q4, there were no regular progress updates provided until specifically requested. This lack of initiative in communicating progress made it difficult to assess the status of the project and delayed decision-making.

Detail how these concerns have been raised with the employee previously. 
On November 12, 2024, during our catch-up call, I raised concerns about the lack of progress on the visual automation tool evaluation. I instructed you to create a clear comparison sheet documenting the tools tested, including a list of must-have features. I provided an example of a comparison sheet for reference. During the call, I also emphasized the need for consistent progress updates and instructed you to provide status updates every Thursday or, at the latest, by Friday.

On November 15, 2024, the comparison sheet was still not completed. I sent a reminder via Slack, reiterating to provide consistent updates on the evaluation progress by the end of each Thursday. You acknowledged this and agreed to give consistent updates on the evaluation progress.

What is the expected level of performance regarding the gap above?
The expected performance is to evaluate and finalize the visual automation tool by the end of Q4. During the evaluation, you are expected to proactively communicate with vendors and team members to ensure milestones are met. As a team lead, you must address technical challenges and provide regular, concise, and accurate progress updates. By the end of Q4, you should have completed the evaluation and selected a visual automation tool based on the outcome.
"""
    
    # Initialize the tool
    performance_gap_tool = PerformanceGapAnalyzerTool()
    
    # Run the tool with the sample input
    result = performance_gap_tool._run(sample_input)
    
    # Print the result
    print("\n=== Performance Gap Analysis Result ===\n")
    print(result)
    print("\n=====================================\n")
    
    return result

if __name__ == "__main__":
    test_performance_gap_analyzer()
