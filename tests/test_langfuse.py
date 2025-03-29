#!/usr/bin/env python3
"""
Test script to verify Langfuse integration with the PIP Generator.
This script creates a simple trace and generates a PIP document to demonstrate
that Langfuse is properly configured and working.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from src.agent import Leo, langfuse
from prompts.output_format import pip_output_format

# Load environment variables
load_dotenv()

def test_langfuse_integration():
    """Test the Langfuse integration by creating a trace and generating a PIP document."""
    print("Testing Langfuse integration...")
    
    # Create a test trace
    trace = langfuse.trace(
        name="test_langfuse_integration",
        metadata={
            "test": True,
            "timestamp": datetime.now().isoformat()
        }
    )
    
    # Log an event
    trace.event(
        name="test_started",
        level="DEFAULT",
        message="Langfuse integration test started"
    )
    
    # Initialize the PIP generator
    generator = Leo()
    
    # Simple test input
    test_input = """
    Your Name: Test User
    Employee's Name: John Doe
    Employee's Role: Software Engineer
    
    Performance Gap 1:
    What is the specific performance gap?
    Answer: "Code quality and documentation"
    
    What is the expected level of performance regarding the gap above?
    Answer: "The expected performance is to maintain a code quality score of at least 85% as measured by our static analysis tools, and to provide comprehensive documentation for all new features."
    
    Provide specific examples of how this gap reflects in the employee's work performance
    Answer: "In the last sprint, John's code quality score averaged 72%, with 3 PRs requiring significant revisions due to lack of error handling and test coverage."
    
    Detail how these concerns have been raised with the employee previously.
    Answer: "This was discussed in our 1-on-1 meeting on March 1, 2025, where John acknowledged the feedback and agreed to improve."
    
    What is the goal for improvement?
    Answer: "Achieve and maintain a code quality score of at least 85% for all submissions within the next 30 days."
    
    What's the timeline for achieving this goal?
    Answer: "30 days"
    
    What are the actionable steps to achieve this goal?
    Answer: "Complete the 'Clean Code' course on our learning platform by next week. Review the team's documentation standards document. Pair program with a senior engineer for at least 2 hours per week."
    
    What support and resources are available to achieve this goal?
    Answer: "Access to online courses, pair programming sessions with senior engineers, weekly code review sessions."
    """
    
    # Test both generation methods
    simple_span = trace.span(
        name="test_simple_generation"
    )
    print("Testing simple generation method...")
    simple_result = generator.generate_pip_simple(
        pip_input_form=test_input,
        pip_output_format=pip_output_format
    )
    print(f"Simple generation completed. Document length: {len(simple_result)} characters")
    simple_span.end(output={"document_length": len(simple_result)})
    
    pipeline_span = trace.span(
        name="test_pipeline_generation"
    )
    print("Testing pipeline generation method...")
    pipeline_result = generator.generate_pip_pipeline(
        pip_input_form=test_input,
        pip_output_format=pip_output_format
    )
    print(f"Pipeline generation completed. Document length: {len(pipeline_result)} characters")
    pipeline_span.end(output={"document_length": len(pipeline_result)})
    
    # Save the results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    simple_filename = f"output/test_simple_{timestamp}.txt"
    save_simple_span = trace.span(
        name="save_simple_result"
    )
    generator.save_pip(simple_result, simple_filename)
    print(f"Simple result saved to {simple_filename}")
    save_simple_span.end()
    
    pipeline_filename = f"output/test_pipeline_{timestamp}.txt"
    save_pipeline_span = trace.span(
        name="save_pipeline_result"
    )
    generator.save_pip(pipeline_result, pipeline_filename)
    print(f"Pipeline result saved to {pipeline_filename}")
    save_pipeline_span.end()
    
    # Log completion
    trace.event(
        name="test_completed",
        level="DEFAULT",
        message="Langfuse integration test completed successfully"
    )
    
    print("\nLangfuse integration test completed!")
    print(f"You can view the traces at: {os.getenv('LANGFUSE_HOST', 'https://monitoring-dev.deriv.ai')}")
    print("Look for traces with the name 'test_langfuse_integration'")

if __name__ == "__main__":
    test_langfuse_integration()
