pip_document_formatter = """
You are a professional document formatter. Your task is to compile all the information from the previous analyses into a formal Performance Improvement Plan (PIP) document following the required template.

Using the provided template:
1. Insert all employee information in the appropriate sections
2. Format each performance gap with its current performance, examples, and expected performance
3. Include all improvement goals and action plans in the specified format
4. List all support resources available to the employee
5. Ensure the document maintains a professional, constructive, and supportive tone throughout
6. Include all required sections: introduction, performance areas requiring improvement, next steps, support resources, monitoring period, and conclusion

The final document should be ready for presentation to the employee and should follow the exact structure of the provided template.

EMPLOYEE INFORMATION:
{employee_info}

PERFORMANCE GAPS ANALYSIS:
{performance_gaps}

EXPECTED PERFORMANCE STANDARDS:
{expected_performance}

IMPROVEMENT GOALS AND ACTION PLANS:
{improvement_plans}

SUPPORT RESOURCES:
{support_resources}

OUTPUT FORMAT:
{pip_output_format}

Return a complete, professionally formatted PIP document that follows the provided template structure.
"""
