"""
Fire Drill Templates
===================

Define custom fire drill templates in a simple format.
Each template can specify:
- title: The incident title
- urgency: high, low, or critical
- description: Detailed description of the scenario
- expected_tta: Expected time to acknowledge (seconds)
- expected_ttr: Expected time to resolve (seconds)
- difficulty: easy, medium, or hard
- category: database, network, application, infrastructure, etc.

Template Format:
===============
TEMPLATE_NAME:
  title: "🔥 Fire Drill: [Scenario Description]"
  urgency: "high"
  description: "Detailed scenario description..."
  expected_tta: 300  # 5 minutes
  expected_ttr: 1800  # 30 minutes
  difficulty: "medium"
  category: "database"
"""

# Built-in templates
FIRE_DRILL_TEMPLATES = {
    "database_connection_failure": {
        "title": "🔥 Fire Drill: Database connection pool exhausted",
        "urgency": "high",
        "description": "The primary database connection pool has reached maximum capacity. Users are experiencing slow response times and some requests are failing.",
        "expected_tta": 300,  # 5 minutes
        "expected_ttr": 1800,  # 30 minutes
        "difficulty": "medium",
        "category": "database"
    },
    
    "cpu_spike": {
        "title": "🔥 Fire Drill: CPU usage at 95% on production servers",
        "urgency": "high",
        "description": "Multiple production servers are showing CPU usage above 95%. Response times are degrading and some services are becoming unresponsive.",
        "expected_tta": 180,  # 3 minutes
        "expected_ttr": 900,  # 15 minutes
        "difficulty": "medium",
        "category": "infrastructure"
    },
    
    "memory_leak": {
        "title": "🔥 Fire Drill: Memory leak detected in application pods",
        "urgency": "critical",
        "description": "Application pods are consuming memory at an alarming rate. Pods are being restarted frequently and user sessions are being lost.",
        "expected_tta": 120,  # 2 minutes
        "expected_ttr": 600,  # 10 minutes
        "difficulty": "hard",
        "category": "application"
    },
    
    "network_latency": {
        "title": "🔥 Fire Drill: High network latency between regions",
        "urgency": "high",
        "description": "Network latency between US-East and US-West regions has increased by 200ms. Cross-region API calls are timing out.",
        "expected_tta": 240,  # 4 minutes
        "expected_ttr": 1200,  # 20 minutes
        "difficulty": "medium",
        "category": "network"
    },
    
    "disk_space": {
        "title": "🔥 Fire Drill: Disk space at 95% on critical servers",
        "urgency": "critical",
        "description": "Multiple critical servers are running out of disk space. Log files are accumulating rapidly and services may stop functioning.",
        "expected_tta": 180,  # 3 minutes
        "expected_ttr": 900,  # 15 minutes
        "difficulty": "easy",
        "category": "infrastructure"
    },
    
    "api_rate_limit": {
        "title": "🔥 Fire Drill: External API rate limit exceeded",
        "urgency": "high",
        "description": "Third-party payment API is returning 429 errors. Payment processing is failing and customer transactions are being declined.",
        "expected_tta": 300,  # 5 minutes
        "expected_ttr": 1800,  # 30 minutes
        "difficulty": "medium",
        "category": "integration"
    },
    
    "ssl_certificate": {
        "title": "🔥 Fire Drill: SSL certificate expiring in 24 hours",
        "urgency": "critical",
        "description": "SSL certificate for production domain is expiring in 24 hours. Users will see security warnings and some browsers may block access.",
        "expected_tta": 600,  # 10 minutes
        "expected_ttr": 3600,  # 1 hour
        "difficulty": "easy",
        "category": "security"
    },
    
    "cache_miss": {
        "title": "🔥 Fire Drill: Redis cache cluster down",
        "urgency": "high",
        "description": "Redis cache cluster is completely down. All cache misses are hitting the database directly, causing severe performance degradation.",
        "expected_tta": 120,  # 2 minutes
        "expected_ttr": 600,  # 10 minutes
        "difficulty": "medium",
        "category": "infrastructure"
    },
    
    "load_balancer": {
        "title": "🔥 Fire Drill: Load balancer health checks failing",
        "urgency": "critical",
        "description": "Load balancer is marking all backend servers as unhealthy. Users cannot access the application and getting 502 errors.",
        "expected_tta": 60,  # 1 minute
        "expected_ttr": 300,  # 5 minutes
        "difficulty": "hard",
        "category": "infrastructure"
    },
    
    "database_deadlock": {
        "title": "🔥 Fire Drill: Database deadlock causing transaction failures",
        "urgency": "high",
        "description": "Database is experiencing frequent deadlocks. User transactions are failing and data consistency issues are occurring.",
        "expected_tta": 240,  # 4 minutes
        "expected_ttr": 1200,  # 20 minutes
        "difficulty": "hard",
        "category": "database"
    }
}

def get_template(template_name):
    """Get a specific template by name."""
    return FIRE_DRILL_TEMPLATES.get(template_name)

def get_all_templates():
    """Get all available templates."""
    return FIRE_DRILL_TEMPLATES

def get_templates_by_category(category):
    """Get all templates in a specific category."""
    return {name: template for name, template in FIRE_DRILL_TEMPLATES.items() 
            if template.get('category') == category}

def get_templates_by_difficulty(difficulty):
    """Get all templates of a specific difficulty."""
    return {name: template for name, template in FIRE_DRILL_TEMPLATES.items() 
            if template.get('difficulty') == difficulty}

def list_template_names():
    """Get a list of all template names."""
    return list(FIRE_DRILL_TEMPLATES.keys())

def validate_template(template):
    """Validate a template has all required fields."""
    required_fields = ['title', 'urgency', 'description']
    optional_fields = ['expected_tta', 'expected_ttr', 'difficulty', 'category']
    
    for field in required_fields:
        if field not in template:
            return False, f"Missing required field: {field}"
    
    if template['urgency'] not in ['low', 'high', 'critical']:
        return False, "Urgency must be 'low', 'high', or 'critical'"
    
    return True, "Template is valid"

def create_custom_template(name, title, urgency, description, **kwargs):
    """Create a custom template."""
    template = {
        'title': title,
        'urgency': urgency,
        'description': description,
        **kwargs
    }
    
    is_valid, message = validate_template(template)
    if not is_valid:
        raise ValueError(f"Invalid template: {message}")
    
    return template
