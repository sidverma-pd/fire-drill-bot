# 🔥 Custom Fire Drill Templates Guide

Create your own fire drill templates to simulate realistic scenarios your team might face.

## Template Format

Templates are defined in `fire_drill_templates.py` using this format:

```python
"template_name": {
    "title": "🔥 Fire Drill: [Scenario Description]",
    "urgency": "high",  # low, high, or critical
    "description": "Detailed scenario description...",
    "expected_tta": 300,  # Expected time to acknowledge (seconds)
    "expected_ttr": 1800,  # Expected time to resolve (seconds)
    "difficulty": "medium",  # easy, medium, or hard
    "category": "database"  # database, infrastructure, network, etc.
}
```

## Required Fields

- **title**: The incident title that appears in PagerDuty
- **urgency**: How urgent the incident is (affects PagerDuty priority)
- **description**: Detailed description of what's happening

## Optional Fields

- **expected_tta**: Expected time to acknowledge in seconds
- **expected_ttr**: Expected time to resolve in seconds  
- **difficulty**: How challenging the scenario is
- **category**: What type of incident this is

## Example Template

```python
"payment_processor_down": {
    "title": "🔥 Fire Drill: Payment processor API completely down",
    "urgency": "critical",
    "description": "Third-party payment processor is returning 500 errors for all requests. No payments can be processed and customers are getting errors during checkout.",
    "expected_tta": 120,  # 2 minutes
    "expected_ttr": 900,  # 15 minutes
    "difficulty": "hard",
    "category": "integration"
}
```

## Adding Your Template

1. Open `fire_drill_templates.py`
2. Add your template to the `FIRE_DRILL_TEMPLATES` dictionary
3. Restart the Flask app
4. Use `/trigger-template payment_processor_down` to test it

## Template Categories

- **database**: Database-related issues
- **infrastructure**: Server, CPU, memory issues
- **network**: Connectivity, latency issues
- **application**: Code, deployment issues
- **integration**: Third-party API issues
- **security**: SSL, authentication issues
- **general**: Other scenarios

## Difficulty Levels

- **easy**: Simple issues that should be resolved quickly
- **medium**: Standard issues with moderate complexity
- **hard**: Complex issues requiring investigation and coordination

## Scoring Impact

Templates with `expected_tta` and `expected_ttr` values will:
- Reduce scoring penalties if teams respond within expected times
- Provide more realistic performance expectations
- Help teams understand what "good" response times look like

## Best Practices

1. **Be realistic**: Base scenarios on real incidents your team has faced
2. **Vary difficulty**: Include easy, medium, and hard scenarios
3. **Set expectations**: Use expected_tta/ttr to define reasonable response times
4. **Be specific**: Detailed descriptions help teams understand the scenario
5. **Test regularly**: Update templates based on team feedback and performance
