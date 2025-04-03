# Performance Improvement Plan (PIP) Agent

This repository contains an implementation of an AI-powered assistant that helps managers create structured and effective Performance Improvement Plans (PIPs) through an interactive, step-by-step process.

## Overview

The PIP Agent guides managers through the process of creating comprehensive Performance Improvement Plans by:

1. Collecting employee information
2. Analyzing performance gaps
3. Developing improvement plans
4. Identifying support resources
5. Generating a professional PIP document

The system uses a conversational approach, asking one question at a time and providing immediate feedback on the quality and completeness of the information provided.

## Components

The PIP Agent consists of several specialized tools:

### 1. Employee Info Extractor
- Collects essential employee details (job title, department)
- Asks one question at a time to gather information

### 2. Performance Gap Analyzer
- Analyzes performance gaps with a structured approach
- Collects and evaluates:
  - Gap Title (concise, 5-7 words)
  - Current Performance (2-3 line professional summary)
  - Examples (with date, context, and impact)
  - Expected Performance (starting with "The expected performance is...")
- Provides percentage-based feedback (25% per section)
- Always includes specific improvement suggestions

### 3. Improvement Plan Analyzer
- Collects improvement plans for each performance gap
- Focuses on two key aspects:
  - Goal (2-3 line outcome tied to Expected Performance)
  - Action Plans (SMART steps with specific timelines)
- Provides percentage-based feedback (50% per section)
- Always explains what accounts for any missing percentage points

### 4. Support Resources Identifier
- Identifies support resources for each performance gap
- Evaluates resources based on specificity, relevance, and variety
- Ensures resources come from different categories (training, mentoring, tools, materials)
- Provides percentage-based feedback with specific improvement suggestions

### 5. Comprehensive PIP Generator
- Combines all collected information into a professional PIP document
- Follows a standardized format with consistent sections
- Maintains privacy by using placeholders instead of actual names

## Workflow

The PIP creation process follows this workflow:

1. **Employee Information Collection**
   - Job title/role
   - Team/department

2. **Performance Gap Analysis** (for each gap)
   - Gap title
   - Current performance summary
   - Specific examples with dates and impact
   - Expected performance

3. **Improvement Plan Development** (for each gap)
   - Goal for improvement
   - Actionable steps with timelines

4. **Support Resources Identification** (for each gap)
   - Specific resources from different categories
   - Training, mentoring, tools, and materials

5. **PIP Document Generation**
   - Professionally formatted document
   - Consistent structure
   - Privacy-preserving placeholders

## Key Features

- **Interactive Guidance**: Step-by-step questions with immediate feedback
- **Structured Evaluation**: Clear criteria for evaluating each input
- **Percentage-Based Feedback**: Quantitative assessment of input quality
- **Specific Improvement Suggestions**: Always provides actionable feedback
- **Privacy Protection**: Never includes actual employee names in responses
- **Professional Formatting**: Consistent document structure

## Recent Improvements

- **Enhanced Feedback System**: All tools now provide percentage-based feedback with specific improvement suggestions
- **Streamlined Question Flow**: Reduced improvement plan questions from 3 to 2, combining timeline with actionable steps
- **Detailed Guidance**: Added descriptive examples to questions to guide better responses
- **Consistent Evaluation Criteria**: Standardized approach across all tools
- **Explicit Improvement Areas**: Always explains what accounts for any missing percentage points

## Usage

```bash
# Run the PIP Agent
python main.py
```

## Example Interaction

```
User: I need to create a PIP for an employee

Agent: What is the employee's job title/role?

User: Software Engineer

Agent: What is the employee's team/department?

User: Engineering

Agent: What is the performance gap title? Provide a concise and neutral title describing the gap, e.g., 'Timeliness in Task Response' or 'Accuracy in Project Delivery.'

User: Code Quality Issues

Agent: This gap title is at 80% match with our guidelines. It's concise and relevant, but could be more specific. The remaining 20% issue is that it could better describe the nature of the quality issues. I suggest: 'Inadequate Code Quality Standards' or 'Code Documentation Deficiencies'. Would you like to refine this gap title, or are you satisfied with it and ready to move to the next question?

...
```

## Requirements

- Python 3.8+
- Required packages listed in `requirements.txt`

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env` file (see `.env.example`)
4. Run the application: `python main.py`
