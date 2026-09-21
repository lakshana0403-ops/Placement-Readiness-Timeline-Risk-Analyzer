import re
import plotly.graph_objects as go

# Comprehensive List of Tech Skills
TECH_SKILLS = [
    # Languages
    "python", "java", "c++", "c#", "javascript", "typescript", "ruby", "php", "swift", "kotlin", "rust", "scala", "dart", "sql", "html", "css", "bash", "shell",
    # Frontend
    "react", "angular", "vue", "svelte", "next.js", "bootstrap", "tailwind", "material ui", "redux",
    # Backend & APIs
    "node.js", "express", "django", "flask", "fastapi", "spring boot", "asp.net", "ruby on rails", "laravel", "graphql", "rest api", "microservices",
    # Databases
    "mysql", "postgresql", "sqlite", "mongodb", "redis", "cassandra", "oracle", "firebase", "dynamodb", "elasticsearch",
    # DevOps & Cloud
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "jenkins", "github actions", "terraform", "ansible", "linux", "ci/cd", "git",
    # Data & ML
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "matplotlib", "seaborn", "tableau", "power bi", "machine learning", "deep learning", "nlp", "data analysis", "data structures", "algorithms",
    # Cybersecurity & Other
    "penetration testing", "cryptography", "blockchain", "agile", "scrum", "jira"
]

def analyze_skills(resume_text, job_desc):
    matched, missing = [], []
    
    # Pad texts with spaces to make edge-matching easier
    job_desc_padded = " " + job_desc.lower().replace('\n', ' ') + " "
    resume_text_padded = " " + resume_text.lower().replace('\n', ' ') + " "
    
    for skill in TECH_SKILLS:
        skill_lower = skill.lower()
        
        # Use regex to match the skill only if it is a distinct word (not surrounded by other letters)
        # We use a lookbehind and lookahead to ensure the skill isn't inside another word (e.g. "go" inside "algorithm")
        pattern = r"(?<![a-z])" + re.escape(skill_lower) + r"(?![a-z])"
        
        if re.search(pattern, job_desc_padded):
            if re.search(pattern, resume_text_padded):
                matched.append(skill)
            else:
                missing.append(skill)

    score = int((len(matched) / max(len(matched) + len(missing), 1)) * 100)
    return matched, missing, score


def learning_timeline(missing):
    phases = {
        "Phase 1: Core Fundamentals": {"time": "1-4 Weeks", "skills": []},
        "Phase 2: Problem Solving": {"time": "4-8 Weeks", "skills": []},
        "Phase 3: Backend & Integration": {"time": "2-4 Weeks", "skills": []},
        "Phase 4: Frontend & UI": {"time": "2-4 Weeks", "skills": []},
        "Phase 5: Databases & Storage": {"time": "2-3 Weeks", "skills": []},
        "Phase 6: Deployment & DevOps": {"time": "2-4 Weeks", "skills": []},
        "Phase 7: Advanced Topics (ML/Data)": {"time": "8-12+ Weeks", "skills": []}
    }
    
    skill_db = {
        # Core & Languages
        "python": ("Phase 1: Core Fundamentals", "Focus on: Data Types, OOP, Pandas, NumPy"),
        "java": ("Phase 1: Core Fundamentals", "Focus on: Spring Boot, Multithreading, JVM"),
        "c++": ("Phase 1: Core Fundamentals", "Focus on: Pointers, Memory Management, STL"),
        "c#": ("Phase 1: Core Fundamentals", "Focus on: .NET Core, LINQ, Entity Framework"),
        "javascript": ("Phase 1: Core Fundamentals", "Focus on: ES6+, DOM Manipulation, Async/Await"),
        "typescript": ("Phase 1: Core Fundamentals", "Focus on: Static Typing, Interfaces, Generics"),
        "ruby": ("Phase 1: Core Fundamentals", "Focus on: Object-oriented design, Ruby on Rails basics"),
        "php": ("Phase 1: Core Fundamentals", "Focus on: Server-side logic, Laravel, PDO"),
        "swift": ("Phase 1: Core Fundamentals", "Focus on: iOS SDK, SwiftUI, Optionals"),
        "kotlin": ("Phase 1: Core Fundamentals", "Focus on: Android SDK, Coroutines, Null Safety"),
        "go": ("Phase 1: Core Fundamentals", "Focus on: Goroutines, Channels, Microservices"),
        "rust": ("Phase 1: Core Fundamentals", "Focus on: Ownership, Borrowing, Concurrency"),
        "r": ("Phase 1: Core Fundamentals", "Focus on: Data wrangling, ggplot2, Statistical modeling"),
        "scala": ("Phase 1: Core Fundamentals", "Focus on: Functional Programming, Apache Spark"),
        "dart": ("Phase 1: Core Fundamentals", "Focus on: Flutter framework, Widget tree"),
        "bash": ("Phase 1: Core Fundamentals", "Focus on: Shell scripting, Automation, Grep/Awk"),
        "shell": ("Phase 1: Core Fundamentals", "Focus on: Shell scripting, Automation, Grep/Awk"),
        "html": ("Phase 1: Core Fundamentals", "Focus on: Semantic tags, Accessibility, DOM"),
        "css": ("Phase 1: Core Fundamentals", "Focus on: Flexbox, Grid, Responsive Design"),
        "git": ("Phase 1: Core Fundamentals", "Focus on: Branching, Merging, Rebase, GitHub Actions"),
        "agile": ("Phase 1: Core Fundamentals", "Focus on: Sprints, Standups, Jira, Scrum framework"),
        "scrum": ("Phase 1: Core Fundamentals", "Focus on: Sprints, Standups, Jira, Scrum framework"),
        "jira": ("Phase 1: Core Fundamentals", "Focus on: Issue tracking, Sprint boards, Kanban"),
        
        # Problem Solving
        "data structures": ("Phase 2: Problem Solving", "Focus on: Hash Maps, Trees, Graphs, Linked Lists"),
        "algorithms": ("Phase 2: Problem Solving", "Focus on: Sorting, Binary Search, Dynamic Programming"),
        
        # Backend
        "node.js": ("Phase 3: Backend & Integration", "Focus on: Event Loop, Express.js, Async/Await"),
        "express": ("Phase 3: Backend & Integration", "Focus on: Routing, Middleware, REST APIs"),
        "django": ("Phase 3: Backend & Integration", "Focus on: ORM, Views, Django REST Framework"),
        "flask": ("Phase 3: Backend & Integration", "Focus on: Routing, Blueprints, Jinja2"),
        "fastapi": ("Phase 3: Backend & Integration", "Focus on: Pydantic, Async Endpoints, Swagger UI"),
        "spring boot": ("Phase 3: Backend & Integration", "Focus on: Dependency Injection, JPA, REST"),
        "asp.net": ("Phase 3: Backend & Integration", "Focus on: MVC pattern, Web API, Middleware"),
        "ruby on rails": ("Phase 3: Backend & Integration", "Focus on: MVC pattern, Active Record, Routes"),
        "laravel": ("Phase 3: Backend & Integration", "Focus on: Eloquent ORM, Blade Templates, Routing"),
        "graphql": ("Phase 3: Backend & Integration", "Focus on: Schemas, Resolvers, Apollo, Mutations"),
        "rest api": ("Phase 3: Backend & Integration", "Focus on: HTTP Methods, Status Codes, JSON"),
        "microservices": ("Phase 3: Backend & Integration", "Focus on: Service Discovery, API Gateways, Docker"),
        
        # Frontend
        "react": ("Phase 4: Frontend & UI", "Focus on: Hooks, Functional Components, Context API"),
        "angular": ("Phase 4: Frontend & UI", "Focus on: Components, Services, RxJS, Dependency Injection"),
        "vue": ("Phase 4: Frontend & UI", "Focus on: Vue Instance, Directives, Vuex/Pinia"),
        "svelte": ("Phase 4: Frontend & UI", "Focus on: Reactive stores, Component lifecycle"),
        "next.js": ("Phase 4: Frontend & UI", "Focus on: SSR, SSG, API Routes, App Router"),
        "bootstrap": ("Phase 4: Frontend & UI", "Focus on: Grid System, Responsive Utility Classes"),
        "tailwind": ("Phase 4: Frontend & UI", "Focus on: Utility-first classes, Custom Configuration"),
        "material ui": ("Phase 4: Frontend & UI", "Focus on: Theming, MUI Components, Grid"),
        "redux": ("Phase 4: Frontend & UI", "Focus on: Store, Actions, Reducers, Redux Toolkit"),
        
        # Databases
        "sql": ("Phase 5: Databases & Storage", "Focus on: Joins, Subqueries, Normalization, Window Functions"),
        "mysql": ("Phase 5: Databases & Storage", "Focus on: Relational Schemas, InnoDB, Indexing"),
        "postgresql": ("Phase 5: Databases & Storage", "Focus on: Advanced JSONB, CTEs, Constraints"),
        "sqlite": ("Phase 5: Databases & Storage", "Focus on: Local storage, Mobile DBs, Relational queries"),
        "mongodb": ("Phase 5: Databases & Storage", "Focus on: NoSQL, Documents, Aggregation Pipeline"),
        "redis": ("Phase 5: Databases & Storage", "Focus on: In-memory caching, Pub/Sub, Data expiration"),
        "cassandra": ("Phase 5: Databases & Storage", "Focus on: Distributed architecture, Wide-column store"),
        "oracle": ("Phase 5: Databases & Storage", "Focus on: Enterprise SQL, PL/SQL, Triggers"),
        "firebase": ("Phase 5: Databases & Storage", "Focus on: Realtime DB, Firestore, Authentication"),
        "dynamodb": ("Phase 5: Databases & Storage", "Focus on: AWS NoSQL, Partition keys, Provisioned throughput"),
        "elasticsearch": ("Phase 5: Databases & Storage", "Focus on: Full-text search, Logstash, Kibana (ELK)"),
        
        # DevOps & Cloud
        "aws": ("Phase 6: Deployment & DevOps", "Focus on: EC2, S3, RDS, Lambda, IAM Roles"),
        "azure": ("Phase 6: Deployment & DevOps", "Focus on: Azure App Service, Virtual Machines, Azure SQL"),
        "gcp": ("Phase 6: Deployment & DevOps", "Focus on: Compute Engine, Cloud Storage, BigQuery"),
        "google cloud": ("Phase 6: Deployment & DevOps", "Focus on: Compute Engine, Cloud Storage, BigQuery"),
        "docker": ("Phase 6: Deployment & DevOps", "Focus on: Containers, Images, Docker Compose, Dockerfile"),
        "kubernetes": ("Phase 6: Deployment & DevOps", "Focus on: Pods, Deployments, Services, Helm charts"),
        "jenkins": ("Phase 6: Deployment & DevOps", "Focus on: Pipelines, Automated Builds, Plugins"),
        "github actions": ("Phase 6: Deployment & DevOps", "Focus on: Workflows, YAML configs, CI/CD runners"),
        "terraform": ("Phase 6: Deployment & DevOps", "Focus on: Infrastructure as Code (IaC), Providers, State"),
        "ansible": ("Phase 6: Deployment & DevOps", "Focus on: Playbooks, Inventory, Configuration Management"),
        "linux": ("Phase 6: Deployment & DevOps", "Focus on: Command line, Permissions, Cron jobs, SSH"),
        "ci/cd": ("Phase 6: Deployment & DevOps", "Focus on: Continuous Integration, Delivery pipelines"),
        
        # ML & Data
        "pandas": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Dataframes, GroupBy, Data Cleaning, Merging"),
        "numpy": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: N-dimensional arrays, Linear Algebra functions"),
        "scikit-learn": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Classification, Regression, Clustering, Pipelines"),
        "tensorflow": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Tensors, Deep Neural Networks, Keras API"),
        "pytorch": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Autograd, Neural Networks, PyTorch Lightning"),
        "keras": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Sequential API, Layers, Model Compilation"),
        "matplotlib": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Plotting, Subplots, Customizing visualizations"),
        "seaborn": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Statistical plots, Heatmaps, Pairplots"),
        "tableau": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Dashboards, Data Blending, Calculated Fields"),
        "power bi": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: DAX, Power Query, Data Modeling"),
        "machine learning": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Supervised/Unsupervised learning, Model evaluation"),
        "deep learning": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Neural Nets, CNNs for images, RNNs for text"),
        "nlp": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Tokenization, Embeddings, Transformers, HuggingFace"),
        "data analysis": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Exploratory Data Analysis (EDA), Statistics"),
        
        # Cyber
        "penetration testing": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Kali Linux, Metasploit, Nmap, Vulnerability scanning"),
        "cryptography": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Encryption algorithms, RSA, AES, Hashing"),
        "blockchain": ("Phase 7: Advanced Topics (ML/Data)", "Focus on: Distributed ledgers, Smart Contracts, Solidity, Web3")
    }

    for skill in missing:
        skill_lower = skill.lower()
        if skill_lower in skill_db:
            phase_name, reason = skill_db[skill_lower]
            phases[phase_name]["skills"].append(f"✅ **{skill.title()}**: {reason}")
        else:
            # Fallback for dynamic skills not strictly in the DB
            phases["Phase 1: Core Fundamentals"]["skills"].append(f"✅ **{skill.title()}**: Self-guided learning")
    
    timeline = {}
    for phase_name, data in phases.items():
        if data["skills"]:
            key = f"{phase_name} (⏳ {data['time']})"
            skills_text = "\n\n".join(data["skills"])
            timeline[key] = skills_text
            
    return timeline


def skill_radar_chart(matched, missing):
    if not matched and not missing:
        return None

    # Limit radar chart to top 12 skills max for visual clarity
    skills = (matched + missing)[:12]
    values = [1 if s in matched else 0 for s in skills]
    
    # If there are no skills to display, don't crash
    if not skills:
        return None

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=skills + [skills[0]],
        fill="toself"
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        height=420
    )
    return fig


def calculate_ats_score(resume_text, job_desc):
    import re
    # Filter out common english words and generic resume words to prevent inflated ATS scores
    stopwords = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'experience', 'skills', 'ability', 'required', 'preferred', 'years', 'team', 'working', 'knowledge', 'ideal', 'candidate', 'looking', 'role'}
    
    jd_words = set([w for w in re.findall(r"[a-zA-Z]{3,}", job_desc.lower()) if w not in stopwords])
    resume_words = set([w for w in re.findall(r"[a-zA-Z]{3,}", resume_text.lower()) if w not in stopwords])
    
    matched = jd_words.intersection(resume_words)
    score = (len(matched) / len(jd_words)) * 100 if jd_words else 0
    return round(score, 2), sorted(matched)
