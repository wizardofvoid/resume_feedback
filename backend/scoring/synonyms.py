# synonyms.py
# Dictionary mapping common tech abbreviations and aliases to their canonical name.
SYNONYM_MAP = {
    # Programming Languages
    "py": "python",
    "python3": "python",
    "js": "javascript",
    "javascript": "javascript",
    "ts": "typescript",
    "typescript": "typescript",
    "cpp": "c++",
    "c plus plus": "c++",
    "golang": "go",
    "ipynb": "python",
    
    # Web Frameworks & Tech
    "react": "react",
    "reactjs": "react",
    "react.js": "react",
    "vue": "vue.js",
    "vuejs": "vue.js",
    "node": "node.js",
    "nodejs": "node.js",
    "django": "django",
    "flask": "flask",
    "angular": "angular",
    "angularjs": "angular",
    
    # Databases
    "postgres": "postgresql",
    "postgresql": "postgresql",
    "mysql": "mysql",
    "mongo": "mongodb",
    "mongodb": "mongodb",
    "sqlite3": "sqlite",
    "sqlite": "sqlite",
    
    # Cloud & DevOps
    "aws": "amazon web services",
    "amazon web services": "amazon web services",
    "gcp": "google cloud platform",
    "google cloud": "google cloud platform",
    "google cloud platform": "google cloud platform",
    "azure": "microsoft azure",
    "microsoft azure": "microsoft azure",
    "k8s": "kubernetes",
    "kubernetes": "kubernetes",
    "docker": "docker",
    "containers": "docker",
    "cicd": "ci/cd",
    "ci/cd": "ci/cd",
    "continuous integration": "ci/cd",
    "continuous deployment": "ci/cd",
    "sre": "devops",
    "site reliability engineering": "devops",
    
    # AI / ML / Data Science
    "ml": "machine learning",
    "machine-learning": "machine learning",
    "deep learning": "deep learning",
    "dl": "deep learning",
    "ai": "artificial intelligence",
    "artificial intelligence": "artificial intelligence",
    "nlp": "natural language processing",
    "natural language processing": "natural language processing",
    "cv": "computer vision",
    "computer vision": "computer vision",
    "stats": "statistics",
    "statistics": "statistics",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "tensor flow": "tensorflow",
    "tf": "tensorflow",
    "spark": "apache spark",
    "bi": "power bi",
    "powerbi": "power bi"
}

def get_canonical_name(skill: str) -> str:
    """
    Returns the normalized canonical name for a given skill.
    """
    s = skill.lower().strip()
    return SYNONYM_MAP.get(s, s)
