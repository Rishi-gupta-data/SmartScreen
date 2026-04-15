import re
from typing import List, Dict, Any, Optional, Tuple


# ---------------------------------------------------------------------------
# SKILL TAXONOMY
# ---------------------------------------------------------------------------
# Organised into categories so we can do category-level matching too.
# Each entry: canonical_name -> list of aliases (all lowercase, no leading/
# trailing spaces).  The canonical name is what gets stored.

SKILL_TAXONOMY: Dict[str, List[str]] = {
    # ── Languages ──────────────────────────────────────────────────────────
    "python":           ["python", "python3", "python 3"],
    "java":             ["java", "java8", "java 8", "java11", "java 11"],
    "javascript":       ["javascript", "js", "es6", "es2015", "ecmascript"],
    "typescript":       ["typescript", "ts"],
    "c":                [r"\bc\b"],
    "c++":              ["c++", "cpp", "c plus plus"],
    "c#":               ["c#", "csharp", "c sharp"],
    "go":               [r"\bgo\b", "golang"],
    "rust":             ["rust"],
    "kotlin":           ["kotlin"],
    "swift":            ["swift"],
    "scala":            ["scala"],
    "r":                [r"\br\b", r"\br programming"],
    "php":              ["php"],
    "ruby":             ["ruby"],
    "perl":             ["perl"],
    "bash":             ["bash", "shell scripting", "shell script"],
    "powershell":       ["powershell"],
    # ── Frontend ───────────────────────────────────────────────────────────
    "react":            ["react", "reactjs", "react.js"],
    "angular":          ["angular", "angularjs", "angular.js", "angular 2+"],
    "vue":              ["vue", "vuejs", "vue.js"],
    "nextjs":           ["nextjs", "next.js", "next js"],
    "nuxtjs":           ["nuxtjs", "nuxt.js"],
    "svelte":           ["svelte"],
    "html":             ["html", "html5"],
    "css":              ["css", "css3"],
    "sass":             ["sass", "scss"],
    "tailwindcss":      ["tailwind", "tailwindcss", "tailwind css"],
    "bootstrap":        ["bootstrap"],
    "jquery":           ["jquery"],
    "redux":            ["redux", "redux toolkit", "rtk"],
    # ── Backend ────────────────────────────────────────────────────────────
    "nodejs":           ["nodejs", "node.js", "node js", "express", "expressjs"],
    "django":           ["django"],
    "flask":            ["flask"],
    "fastapi":          ["fastapi", "fast api"],
    "spring":           ["spring", "spring boot", "springboot"],
    "rails":            ["rails", "ruby on rails", "ror"],
    "laravel":          ["laravel"],
    "asp.net":          ["asp.net", "aspnet", ".net core", "dotnet"],
    "graphql":          ["graphql"],
    "rest api":         ["rest api", "restful", "rest apis", "rest services"],
    "grpc":             ["grpc"],
    "websocket":        ["websocket", "websockets"],
    # ── Databases ──────────────────────────────────────────────────────────
    "sql":              [r"\bsql\b"],
    "mysql":            ["mysql"],
    "postgresql":       ["postgresql", "postgres", "psql"],
    "sqlite":           ["sqlite"],
    "oracle":           ["oracle db", "oracle database"],
    "mssql":            ["mssql", "sql server", "microsoft sql server"],
    "mongodb":          ["mongodb", "mongo"],
    "redis":            ["redis"],
    "elasticsearch":    ["elasticsearch", "elastic search", "elk"],
    "cassandra":        ["cassandra", "apache cassandra"],
    "dynamodb":         ["dynamodb", "dynamo db"],
    "neo4j":            ["neo4j"],
    "firebase":         ["firebase", "firestore"],
    # ── Cloud & DevOps ────────────────────────────────────────────────────
    "aws":              ["aws", "amazon web services"],
    "gcp":              ["gcp", "google cloud", "google cloud platform"],
    "azure":            ["azure", "microsoft azure"],
    "docker":           ["docker"],
    "kubernetes":       ["kubernetes", "k8s"],
    "terraform":        ["terraform"],
    "ansible":          ["ansible"],
    "jenkins":          ["jenkins"],
    "github actions":   ["github actions", "gh actions"],
    "gitlab ci":        ["gitlab ci", "gitlab ci/cd"],
    "circleci":         ["circleci", "circle ci"],
    "ci/cd":            ["ci/cd", "cicd", "continuous integration", "continuous deployment"],
    "linux":            ["linux", "ubuntu", "centos", "debian"],
    "nginx":            ["nginx"],
    "apache":           ["apache"],
    "git":              [r"\bgit\b"],
    "github":           ["github"],
    "gitlab":           ["gitlab"],
    # ── Data / ML / AI ───────────────────────────────────────────────────
    "machine learning": ["machine learning", "ml"],
    "deep learning":    ["deep learning", "dl"],
    "nlp":              ["nlp", "natural language processing"],
    "computer vision":  ["computer vision", r"\bcv\b"],
    "tensorflow":       ["tensorflow", "tf"],
    "pytorch":          ["pytorch", "torch"],
    "keras":            ["keras"],
    "scikit-learn":     ["scikit-learn", "sklearn", "scikit learn"],
    "pandas":           ["pandas"],
    "numpy":            ["numpy"],
    "matplotlib":       ["matplotlib"],
    "seaborn":          ["seaborn"],
    "spark":            ["spark", "apache spark", "pyspark"],
    "hadoop":           ["hadoop", "apache hadoop"],
    "airflow":          ["airflow", "apache airflow"],
    "dbt":              ["dbt", "data build tool"],
    "tableau":          ["tableau"],
    "power bi":         ["power bi", "powerbi"],
    # ── Architecture & Practices ─────────────────────────────────────────
    "microservices":    ["microservices", "microservice"],
    "system design":    ["system design"],
    "oop":              ["oop", "object oriented", "object-oriented"],
    "tdd":              ["tdd", "test driven", "test-driven"],
    "agile":            ["agile"],
    "scrum":            ["scrum"],
    "jira":             ["jira"],
    "confluence":       ["confluence"],
    # ── Mobile ────────────────────────────────────────────────────────────
    "android":          ["android"],
    "ios":              ["ios"],
    "react native":     ["react native"],
    "flutter":          ["flutter"],
    # ── Security ─────────────────────────────────────────────────────────
    "oauth":            ["oauth", "oauth2"],
    "jwt":              ["jwt", "json web token"],
    "ssl/tls":          ["ssl", "tls", "ssl/tls", "https"],
}

# Pre-compile patterns for performance
_SKILL_PATTERNS: List[Tuple[str, re.Pattern]] = []

def _build_skill_patterns():
    """Build compiled regex patterns for each skill alias."""
    global _SKILL_PATTERNS
    if _SKILL_PATTERNS:
        return
    for canonical, aliases in SKILL_TAXONOMY.items():
        for alias in aliases:
            # If alias already looks like a regex pattern (contains \b, etc.)
            if alias.startswith(r"\b") or alias.endswith(r"\b"):
                pattern = re.compile(alias, re.IGNORECASE)
            else:
                # Escape and add word boundary
                escaped = re.escape(alias)
                pattern = re.compile(r"\b" + escaped + r"\b", re.IGNORECASE)
            _SKILL_PATTERNS.append((canonical, pattern))

_build_skill_patterns()


# ---------------------------------------------------------------------------
# SECTION EXTRACTOR  (splits resume/JD into named sections)
# ---------------------------------------------------------------------------
SECTION_HEADERS = {
    "skills":          ["skills", "technical skills", "core competencies",
                        "technologies", "tech stack", "expertise", "proficiencies",
                        "tools", "tools & technologies"],
    "experience":      ["experience", "work experience", "professional experience",
                        "employment", "employment history", "work history",
                        "career history", "internship", "internships"],
    "education":       ["education", "academic background", "qualifications",
                        "academic qualifications", "educational background"],
    "projects":        ["projects", "personal projects", "key projects",
                        "academic projects", "side projects"],
    "certifications":  ["certifications", "certificates", "achievements",
                        "awards", "licenses"],
    "summary":         ["summary", "profile", "objective", "about me",
                        "professional summary", "career objective"],
    # JD-specific
    "responsibilities": ["responsibilities", "job responsibilities", "duties",
                         "role", "what you will do", "you will"],
    "requirements":    ["requirements", "required skills", "must have",
                        "qualifications required", "minimum qualifications",
                        "what we need"],
    "preferred":       ["preferred", "nice to have", "good to have",
                        "preferred qualifications", "bonus", "plus"],
}

def _extract_sections(text: str) -> Dict[str, str]:
    """
    Split text into sections based on common section headers.
    Returns dict of section_name -> section_content.
    """
    lines = text.split("\n")
    sections: Dict[str, str] = {"__header__": ""}
    current_section = "__header__"

    header_re = re.compile(
        r"^([A-Z][A-Za-z &/\-]{1,50})\s*[:|-]?\s*$"
    )

    for line in lines:
        stripped = line.strip()
        if not stripped:
            sections.setdefault(current_section, "")
            sections[current_section] += "\n"
            continue

        matched_section = None
        lower = stripped.lower().rstrip(":").strip()
        for section_name, headers in SECTION_HEADERS.items():
            if lower in headers:
                matched_section = section_name
                break

        if matched_section:
            current_section = matched_section
            sections[current_section] = ""
        else:
            sections.setdefault(current_section, "")
            sections[current_section] += stripped + "\n"

    return sections


# ---------------------------------------------------------------------------
# SKILL EXTRACTION  (section-aware)
# ---------------------------------------------------------------------------
def _extract_skills_from_text(text: str) -> List[str]:
    """Extract canonical skill names from any block of text."""
    found = set()
    for canonical, pattern in _SKILL_PATTERNS:
        if pattern.search(text):
            found.add(canonical)
    return sorted(found)


def extract_skills_from_resume(text: str) -> List[str]:
    """
    Extract skills, prioritising the 'skills' section if present,
    then falling back to full text.
    """
    sections = _extract_sections(text)
    skills_text = sections.get("skills", "")
    # Also include project/experience sections for implicit skills
    skills_text += " " + sections.get("projects", "")
    skills_text += " " + sections.get("experience", "")
    if not skills_text.strip():
        skills_text = text
    return _extract_skills_from_text(skills_text)


def extract_skills_for_jd(text: str, section: str = "requirements") -> List[str]:
    """
    Extract skills from a JD section.
    section = 'requirements' or 'preferred'
    """
    sections = _extract_sections(text)
    target_text = sections.get(section, "")
    if not target_text.strip():
        # Fallback: full text
        target_text = text
    return _extract_skills_from_text(target_text)


# ---------------------------------------------------------------------------
# NAME EXTRACTION
# ---------------------------------------------------------------------------
def extract_name(text: str) -> Optional[str]:
    """
    Multi-strategy name extraction.
    Strategy 1: Explicit 'Name:' label
    Strategy 2: First non-empty line that looks like a personal name
                (2-4 words, title-case or all-caps, no digits/special chars)
    """
    # Strategy 1
    name_label = re.search(r"(?:name\s*[:\-]\s*)([A-Za-z]+(?: [A-Za-z]+){1,3})",
                            text, re.IGNORECASE)
    if name_label:
        return name_label.group(1).strip().title()

    # Strategy 2
    lines = text.split("\n")
    name_pattern = re.compile(r"^[A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+){1,3}$")
    for line in lines[:10]:
        stripped = line.strip()
        if not stripped:
            continue
        # Skip lines with emails, phones, URLs
        if re.search(r"[@\d/\\|#]", stripped):
            continue
        # Skip section headers
        lower = stripped.lower()
        if any(lower.startswith(h) for h in
               ["resume", "cv", "curriculum", "profile", "objective", "summary"]):
            continue
        if name_pattern.match(stripped) or (stripped.isupper() and 2 <= len(stripped.split()) <= 4):
            return stripped.title()

    return None


# ---------------------------------------------------------------------------
# CONTACT EXTRACTION
# ---------------------------------------------------------------------------
def extract_email(text: str) -> Optional[str]:
    match = re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", text)
    return match.group(0).lower() if match else None


def extract_phone(text: str) -> Optional[str]:
    """
    Matches common international and Indian formats.
    Avoids matching plain integers like years.
    """
    patterns = [
        r"\+91[\s\-]?[6-9]\d{9}",                      # +91 Indian mobile
        r"\+?1[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}",  # US
        r"\+?[2-9]\d{1,3}[\s\-]?\d{4,6}[\s\-]?\d{4,6}", # generic intl
        r"\b[6-9]\d{9}\b",                               # Indian mobile (no country code)
        r"\b0\d{10}\b",                                  # 0XXXXXXXXXX
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(0).strip()
    return None


def extract_linkedin(text: str) -> Optional[str]:
    m = re.search(r"linkedin\.com/in/([A-Za-z0-9\-_%]+)", text, re.IGNORECASE)
    return f"linkedin.com/in/{m.group(1)}" if m else None


def extract_github(text: str) -> Optional[str]:
    m = re.search(r"github\.com/([A-Za-z0-9\-_%]+)", text, re.IGNORECASE)
    return f"github.com/{m.group(1)}" if m else None


# ---------------------------------------------------------------------------
# EXPERIENCE EXTRACTION
# ---------------------------------------------------------------------------
def extract_total_experience_years(text: str) -> Optional[float]:
    """
    Try to figure out total years of experience from the resume text.
    Strategies:
      1. Explicit "X years of experience" phrase
      2. Sum date ranges in experience section
    """
    # Strategy 1: explicit phrase
    exp_phrase = re.search(
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)",
        text, re.IGNORECASE
    )
    if exp_phrase:
        return float(exp_phrase.group(1))

    # Strategy 2: date ranges  e.g. "Jan 2020 – Dec 2022"
    date_range_pattern = re.compile(
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|"
        r"March|April|June|July|August|September|October|November|December)?\s*"
        r"(\d{4})\s*(?:–|-|to)\s*"
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|"
        r"March|April|June|July|August|September|October|November|December|Present|present|current)?\s*"
        r"(\d{4}|Present|present|current|now)",
        re.IGNORECASE
    )
    import datetime
    current_year = datetime.datetime.now().year
    total_months = 0
    for m in date_range_pattern.finditer(text):
        start_year = int(m.group(1))
        end_str = m.group(2)
        end_year = current_year if end_str.lower() in ("present", "current", "now") else int(end_str)
        if 1990 <= start_year <= current_year and start_year <= end_year <= current_year + 1:
            total_months += (end_year - start_year) * 12

    if total_months > 0:
        return round(total_months / 12, 1)

    return None


def extract_experience(text: str) -> List[Dict[str, str]]:
    """
    Extract experience entries by looking for company/role/date patterns.
    Returns structured list — far better than returning 'Unknown' for everything.
    """
    sections = _extract_sections(text)
    exp_text = sections.get("experience", text)  # fallback to full text

    entries = []

    # Date range pattern (covers most resume formats)
    date_re = re.compile(
        r"(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|"
        r"March|April|June|July|August|September|October|November|December)\s+)?"
        r"(\d{4})\s*(?:–|-|to)\s*"
        r"(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|January|February|"
        r"March|April|June|July|August|September|October|November|December)\s+)?"
        r"(\d{4}|Present|present|current|now)",
        re.IGNORECASE
    )

    lines = exp_text.split("\n")
    import datetime
    current_year = datetime.datetime.now().year
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        date_match = date_re.search(line)
        if date_match:
            start_y = date_match.group(1)
            end_y = date_match.group(2)
            duration = f"{start_y} – {end_y.capitalize()}"

            # Look for role/company in surrounding lines
            role = ""
            company = ""
            context = " ".join(lines[max(0, i-2):i+3])

            # Role indicators
            role_patterns = [
                r"(?:Software|Backend|Frontend|Full.?Stack|Data|ML|AI|Cloud|DevOps|"
                r"Senior|Junior|Lead|Principal|Staff|Associate)\s+\w+(?:\s+\w+)?",
                r"(?:Engineer|Developer|Analyst|Manager|Architect|Consultant|"
                r"Intern|Trainee|Scientist|Lead|Director)(?:\s+\w+)?",
            ]
            for rp in role_patterns:
                rm = re.search(rp, context, re.IGNORECASE)
                if rm:
                    role = rm.group(0).strip()
                    break

            # Company: look for "at <Company>" or "@ <Company>"
            at_match = re.search(r"(?:at|@)\s+([A-Z][A-Za-z0-9\s&.,]+)", context)
            if at_match:
                company = at_match.group(1).strip()

            entries.append({
                "company": company or "Not specified",
                "role": role or "Not specified",
                "duration": duration,
            })

        i += 1

    # Deduplicate
    seen = set()
    unique_entries = []
    for e in entries:
        key = e["duration"]
        if key not in seen:
            seen.add(key)
            unique_entries.append(e)

    return unique_entries if unique_entries else []


# ---------------------------------------------------------------------------
# EDUCATION EXTRACTION
# ---------------------------------------------------------------------------
DEGREE_PATTERNS = [
    (r"\bPh\.?D\.?\b", "PhD"),
    (r"\bM\.?Tech\.?\b|\bM\.?E\.?\b|\bMaster of Technology\b", "M.Tech"),
    (r"\bM\.?S\.?\b|\bMaster of Science\b", "M.S."),
    (r"\bMBA\b|\bMaster of Business\b", "MBA"),
    (r"\bM\.?C\.?A\.?\b", "MCA"),
    (r"\bB\.?Tech\.?\b|\bB\.?E\.?\b|\bBachelor of Technology\b|\bBachelor of Engineering\b", "B.Tech"),
    (r"\bB\.?S\.?\b|\bBachelor of Science\b", "B.S."),
    (r"\bBCA\b|\bBachelor of Computer Application\b", "BCA"),
    (r"\bB\.?C\.?A\.?\b", "BCA"),
    (r"\bB\.?Com\b", "B.Com"),
    (r"\bBBA\b", "BBA"),
    (r"\bDiploma\b", "Diploma"),
    (r"\bHigher Secondary\b|\bClass XII\b|\b12th\b|\bHSC\b", "12th / HSC"),
    (r"\bSecondary\b|\bClass X\b|\b10th\b|\bSSC\b|\bMatric\b", "10th / SSC"),
]


def extract_education(text: str) -> List[Dict[str, str]]:
    """
    Extract education entries with degree, institution, year, and field.
    """
    sections = _extract_sections(text)
    edu_text = sections.get("education", "")
    if not edu_text.strip():
        edu_text = text

    entries = []
    year_re = re.compile(r"\b(19|20)\d{2}\b")

    for pattern_str, degree_name in DEGREE_PATTERNS:
        degree_re = re.compile(pattern_str, re.IGNORECASE)
        for m in degree_re.finditer(edu_text):
            # Find surrounding context (±200 chars)
            start = max(0, m.start() - 200)
            end = min(len(edu_text), m.end() + 200)
            context = edu_text[start:end]

            # Year
            years = year_re.findall(context)
            year = years[-1] if years else "Not specified"

            # Institution: look for "University", "College", "Institute", "IIT", "NIT"
            inst_match = re.search(
                r"([A-Z][A-Za-z\s&'.,()]+(?:University|College|Institute|"
                r"Institution|School|Academy|IIT|NIT|BITS|VIT|SRM|MIT|"
                r"IIIT|IISC|IIM|XLRI|ISB)(?:\s+of\s+[A-Za-z\s]+)?)",
                context, re.IGNORECASE
            )
            institution = inst_match.group(1).strip() if inst_match else "Not specified"

            # Field of study
            field_match = re.search(
                r"(?:in|of)\s+(Computer Science|Information Technology|"
                r"Electronics|Electrical|Mechanical|Civil|Chemical|"
                r"Data Science|Artificial Intelligence|Machine Learning|"
                r"Mathematics|Physics|Commerce|Business Administration)",
                context, re.IGNORECASE
            )
            field = field_match.group(1).strip() if field_match else "Not specified"

            entries.append({
                "degree": degree_name,
                "institution": institution,
                "field": field,
                "year": year,
            })

    # Deduplicate by degree
    seen_degrees = set()
    unique = []
    for e in entries:
        if e["degree"] not in seen_degrees:
            seen_degrees.add(e["degree"])
            unique.append(e)

    return unique


# ---------------------------------------------------------------------------
# JD-SPECIFIC EXTRACTORS
# ---------------------------------------------------------------------------
JOB_TITLE_KEYWORDS = [
    "engineer", "developer", "architect", "analyst", "scientist", "manager",
    "lead", "head", "director", "consultant", "specialist", "designer",
    "administrator", "intern", "trainee", "associate", "principal", "staff",
]


def extract_job_title(text: str) -> Optional[str]:
    """
    Robust job title extraction.
    Strategy 1: Explicit "Position:" / "Role:" / "Title:" label
    Strategy 2: First line that contains a job title keyword
    Strategy 3: First non-empty, non-boilerplate line
    """
    # Strategy 1
    label_match = re.search(
        r"(?:Position|Role|Title|Job Title)\s*[:\-]\s*([^\n]{3,80})",
        text, re.IGNORECASE
    )
    if label_match:
        return label_match.group(1).strip()

    # Strategy 2
    lines = text.split("\n")
    for line in lines[:10]:
        stripped = line.strip()
        if not stripped or len(stripped) > 120:
            continue
        lower = stripped.lower()
        if any(kw in lower for kw in JOB_TITLE_KEYWORDS):
            # Clean up common prefixes
            stripped = re.sub(r"^(?:job|position|role|opening|vacancy)[:\s]+", "",
                               stripped, flags=re.IGNORECASE).strip()
            return stripped

    # Strategy 3: first meaningful line
    for line in lines[:5]:
        stripped = line.strip()
        if stripped and len(stripped) > 3:
            return stripped

    return None


def extract_company(text: str) -> Optional[str]:
    patterns = [
        r"Company\s*[:\-]\s*([^\n]{2,60})",
        r"Organization\s*[:\-]\s*([^\n]{2,60})",
        r"Employer\s*[:\-]\s*([^\n]{2,60})",
        r"(?:About|At)\s+([A-Z][A-Za-z0-9\s&.,]+(?:Ltd|Pvt|Inc|Corp|Technologies|"
        r"Solutions|Systems|Services|Software|Tech|Group|Global|Labs|Studio)?)",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def extract_experience_requirement(text: str) -> Optional[str]:
    """Extract experience requirement, handling ranges like '3-5 years'."""
    patterns = [
        r"(\d+)\s*[-–]\s*(\d+)\s*(?:\+)?\s*(?:years?|yrs?)",
        r"(\d+)\s*\+\s*(?:years?|yrs?)",
        r"(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp)",
        r"minimum\s+(\d+)\s*(?:years?|yrs?)",
        r"at\s+least\s+(\d+)\s*(?:years?|yrs?)",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            if m.lastindex and m.lastindex >= 2:
                try:
                    return f"{m.group(1)}-{m.group(2)} years"
                except IndexError:
                    pass
            return f"{m.group(1)}+ years"
    return None


def extract_salary(text: str) -> Optional[str]:
    """Extract salary range, supporting LPA (Indian) and $ formats."""
    patterns = [
        r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)\s*LPA",
        r"(\d+(?:\.\d+)?)\s*LPA",
        r"₹\s*[\d,]+\s*[-–to]+\s*₹?\s*[\d,]+(?:\s*per\s*(?:month|annum|year))?",
        r"\$\s*[\d,]+\s*[-–to]+\s*\$?\s*[\d,]+(?:\s*per\s*(?:month|year|annum))?",
        r"CTC\s*[:\-]?\s*[\d.]+\s*[-–]?\s*[\d.]*\s*(?:LPA|Lakhs?)",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(0).strip()
    return None


def extract_qualifications(text: str) -> List[str]:
    """Extract educational qualifications from JD."""
    qualifications = []
    sections = _extract_sections(text)
    target = sections.get("requirements", "") + " " + sections.get("education", "")
    if not target.strip():
        target = text

    checks = [
        (r"\bPh\.?D\b", "PhD"),
        (r"\bM\.?Tech\b|\bMaster'?s?\b", "Master's degree"),
        (r"\bB\.?Tech\b|\bBachelor'?s?\b|\bUnder.?graduate\b", "Bachelor's degree"),
        (r"\bDiploma\b", "Diploma"),
        (r"\bcertifi(?:ed|cation)\b", "Relevant certification"),
    ]
    for pattern, label in checks:
        if re.search(pattern, target, re.IGNORECASE):
            qualifications.append(label)

    return qualifications if qualifications else ["Bachelor's degree preferred"]


def extract_responsibilities(text: str) -> List[str]:
    """Extract responsibility lines from JD."""
    sections = _extract_sections(text)
    resp_text = sections.get("responsibilities", "")
    if not resp_text.strip():
        resp_text = text

    responsibilities = []
    bullet_re = re.compile(
        r"^[\s]*(?:[•\-–*▪◦‣➤▶→►]|\d+[.)]\s|\([a-z]\)\s)[^\S\n]*(.+)", re.MULTILINE
    )
    for m in bullet_re.finditer(resp_text):
        item = m.group(1).strip()
        if len(item) > 15:
            responsibilities.append(item)

    # Fallback: sentence-based extraction
    if not responsibilities:
        sentences = re.split(r"[.\n]", resp_text)
        for s in sentences:
            s = s.strip()
            if 20 <= len(s) <= 300:
                responsibilities.append(s)

    return responsibilities[:8] if responsibilities else []


# ---------------------------------------------------------------------------
# EXPERIENCE LEVEL CLASSIFIER
# ---------------------------------------------------------------------------
def classify_experience_level(years: Optional[float]) -> str:
    if years is None:
        return "Unknown"
    if years < 1:
        return "Fresher (< 1 year)"
    if years < 3:
        return "Junior (1-3 years)"
    if years < 6:
        return "Mid-Level (3-6 years)"
    if years < 10:
        return "Senior (6-10 years)"
    return "Staff / Principal (10+ years)"


# ---------------------------------------------------------------------------
# SKILL ALIASES  (for fuzzy matching in the matcher)
# ---------------------------------------------------------------------------
# Maps common abbreviations / alternative names back to canonical names
# so "node" in a resume matches "nodejs" in a JD etc.
_ALIAS_TO_CANONICAL: Dict[str, str] = {}
for _canonical, _aliases in SKILL_TAXONOMY.items():
    for _alias in _aliases:
        _clean = re.sub(r"\\b|\^|\$", "", _alias).strip().lower()
        _ALIAS_TO_CANONICAL[_clean] = _canonical
    _ALIAS_TO_CANONICAL[_canonical.lower()] = _canonical


def _normalize_skill(skill: str) -> str:
    s = skill.lower().strip()
    return _ALIAS_TO_CANONICAL.get(s, s)


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ SKILL ALIASES  (for fuzzy matching in the matcher)                      │
# └─────────────────────────────────────────────────────────────────────────┘

_ALIAS_TO_CANONICAL: Dict[str, str] = {}
for _canonical, _aliases in SKILL_TAXONOMY.items():
    for _alias in _aliases:
        _clean = re.sub(r"\\b|\^|\$", "", _alias).strip().lower()
        _ALIAS_TO_CANONICAL[_clean] = _canonical
    _ALIAS_TO_CANONICAL[_canonical.lower()] = _canonical


def _normalize_skill(skill: str) -> str:
    s = skill.lower().strip()
    return _ALIAS_TO_CANONICAL.get(s, s)


def _skill_importance_score(skill: str) -> int:
    """Rate skill importance by tier (lower = more critical)."""
    skill_lower = skill.lower()
    
    tier_1 = {"python", "java", "javascript", "react", "fastapi", "spring", "nodejs", "docker", "postgresql", "aws"}
    tier_2 = {"node", "typescript", "golang", "rust", "kubernetes", "azure", "gcp", "mongodb", "redis", "django"}
    tier_3 = {"html", "css", "jquery", "bootstrap", "sqlite", "git", "linux", "windows"}
    
    if skill_lower in tier_1:
        return 1  # Critical
    elif skill_lower in tier_2:
        return 2  # Important
    else:
        return 3  # Nice-to-have


def _count_relevant_experience(resume_roles: List[str], jd_title: str) -> int:
    """Count years of relevant experience where resume role matches JD title."""
    jd_title_lower = jd_title.lower() if jd_title else ""
    relevant_count = 0
    
    role_keywords = {
        "backend": {"backend", "api", "server", "service"},
        "frontend": {"frontend", "ui", "ux", "react", "vue", "angular"},
        "fullstack": {"fullstack", "full-stack", "fullstack engineer"},
        "devops": {"devops", "site reliability", "sre", "infrastructure"},
        "data": {"data engineer", "data scientist", "analytics", "ml", "machine learning"},
        "security": {"security", "infosec", "penetration"},
    }
    
    for role in resume_roles:
        role_lower = role.lower()
        for category, keywords in role_keywords.items():
            if any(kw in role_lower for kw in keywords) and any(kw in jd_title_lower for kw in keywords):
                relevant_count += 1
                break
    
    return relevant_count


def _match_education_level(resume_education: List[str], jd_qualifications: List[str]) -> float:
    """Match education level: higher degree = higher score."""
    degree_rank = {
        "phd": 5,
        "masters": 4,
        "bachelor": 3,
        "diploma": 2,
        "certificate": 1,
    }
    
    resume_highest = 0
    for edu in resume_education:
        edu_lower = edu.lower()
        for degree, rank in degree_rank.items():
            if degree in edu_lower:
                resume_highest = max(resume_highest, rank)
                break
    
    req_highest = 0
    for qual in jd_qualifications:
        qual_lower = qual.lower()
        for degree, rank in degree_rank.items():
            if degree in qual_lower:
                req_highest = max(req_highest, rank)
                break
    
    if req_highest == 0:
        return 100.0  # No requirement specified, assume met
    
    if resume_highest >= req_highest:
        return 100.0  # Meets or exceeds requirement
    elif resume_highest == req_highest - 1:
        return 85.0  # One level below
    else:
        return max(50.0, (resume_highest / req_highest) * 100)  # Significantly below


# ┌─────────────────────────────────────────────────────────────────────────┐
# │ MATCHING ENGINE (ENHANCED v2)                                           │
# └─────────────────────────────────────────────────────────────────────────┘
def match_resume_to_jd(
    resume_data: Dict[str, Any],
    jd_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Enhanced multi-dimensional matching with detailed breakdown:
      - Skill match        (weight 55%) - includes category matching
      - Experience        (weight 30%) - considers role progression
      - Education         (weight 15%) - degree level matching
    
    Returns comprehensive analysis with scores, gaps, and recommendations.
    """
    # ────────────────────────────────────────────────────────────────────────
    # 1. SKILL MATCH ANALYSIS (55%)
    # ────────────────────────────────────────────────────────────────────────
    resume_skills = set(_normalize_skill(s) for s in resume_data.get("skills", []))
    required_skills = set(_normalize_skill(s) for s in jd_data.get("required_skills", []))
    preferred_skills = set(_normalize_skill(s) for s in jd_data.get("preferred_skills", []))

    # Direct skill matches
    required_matched = resume_skills & required_skills
    preferred_matched = resume_skills & preferred_skills
    missing_required = required_skills - resume_skills
    missing_preferred = preferred_skills - resume_skills
    extra_skills = resume_skills - required_skills - preferred_skills

    # Base skill coverage score
    if required_skills:
        skill_score = (len(required_matched) / len(required_skills)) * 100
    else:
        skill_score = 100.0

    # Bonus for preferred skills (up to 15 points)
    preferred_bonus = 0.0
    if preferred_skills:
        pref_coverage = len(preferred_matched) / len(preferred_skills)
        preferred_bonus = pref_coverage * 15.0

    skill_score_final = min(skill_score + preferred_bonus, 100.0)
    
    # Penalty for critical skill gaps
    if missing_required and len(required_skills) > 0:
        criticality_factor = len(missing_required) / len(required_skills)
        if criticality_factor > 0.5:  # Over 50% of skills missing
            skill_score_final *= 0.85

    # ────────────────────────────────────────────────────────────────────────
    # 2. EXPERIENCE MATCH ANALYSIS (30%)
    # ────────────────────────────────────────────────────────────────────────
    resume_years = resume_data.get("total_experience_years")
    resume_level = resume_data.get("experience_level", "Unknown")
    required_exp_str = jd_data.get("experience_required", "")
    required_years = _parse_years_from_string(required_exp_str)

    exp_score = 100.0
    exp_detail = "Experience requirement not specified in JD"

    if required_years is not None:
        exp_detail = f"Required: {required_years}+ years {required_exp_str}"
        
        if resume_years is None:
            exp_score = 50.0
            exp_detail += " | Resume experience not clearly specified"
        else:
            years_diff = resume_years - required_years
            if years_diff >= 0:
                # Meets or exceeds requirement
                exp_score = min(100.0, 95.0 + (years_diff * 2))  # Cap at 100%
                exp_detail += f" | ✓ {resume_years} yrs ({years_diff:+.1f} yrs beyond requirement)"
            else:
                # Below requirement
                coverage_pct = (resume_years / required_years) * 100
                if coverage_pct >= 80:
                    exp_score = 80.0
                    exp_detail += f" | ⚠ {resume_years} yrs (–{abs(years_diff):.1f} yrs, {coverage_pct:.0f}% coverage)"
                elif coverage_pct >= 60:
                    exp_score = 60.0
                    exp_detail += f" | ✗ {resume_years} yrs (–{abs(years_diff):.1f} yrs, {coverage_pct:.0f}% coverage)"
                else:
                    exp_score = max(20.0, coverage_pct)
                    exp_detail += f" | ✗✗ {resume_years} yrs (significant gap, {coverage_pct:.0f}% coverage)"

        # Bonus: check if resume experience is in relevant roles
        resume_exp_list = resume_data.get("experience", [])
        if resume_exp_list and required_years:
            relevant_roles = _count_relevant_experience(resume_exp_list, jd_data.get("title", ""))
            if relevant_roles > 0:
                exp_score = min(exp_score + 5.0, 100.0)  # Bonus for relevant background

    # ────────────────────────────────────────────────────────────────────────
    # 3. EDUCATION MATCH ANALYSIS (15%)
    # ────────────────────────────────────────────────────────────────────────
    resume_education = resume_data.get("education", [])
    jd_qualifications = jd_data.get("qualifications", [])

    edu_score = 100.0
    edu_detail = "Education requirement not specified in JD"

    if jd_qualifications:
        edu_detail = f"JD requires: {', '.join(jd_qualifications)}"
        if not resume_education:
            edu_score = 60.0
            edu_detail += " | ⚠ No education details found in resume"
        else:
            resume_degrees = [e.get("degree", "").lower() for e in resume_education]
            degree_score = _match_education_level(resume_degrees, jd_qualifications)
            edu_score = degree_score
            found_degrees = [e.get("degree", "") for e in resume_education]
            
            if degree_score >= 90:
                edu_detail += f" | ✓ {', '.join(found_degrees)} (exceeds requirement)"
            elif degree_score >= 70:
                edu_detail += f" | ⚠ {', '.join(found_degrees)} (meets requirement)"
            else:
                edu_detail += f" | ✗ {', '.join(found_degrees)} (below requirement)"

    # ────────────────────────────────────────────────────────────────────────
    # 4. COMPOSITE MATCHING SCORE
    # ────────────────────────────────────────────────────────────────────────
    SKILL_WEIGHT = 0.55
    EXP_WEIGHT = 0.30
    EDU_WEIGHT = 0.15

    composite_score = (
        skill_score_final * SKILL_WEIGHT +
        exp_score * EXP_WEIGHT +
        edu_score * EDU_WEIGHT
    )
    composite_score = round(composite_score, 2)

    # ────────────────────────────────────────────────────────────────────────
    # 5. RECOMMENDATION & DETAIL
    # ────────────────────────────────────────────────────────────────────────
    recommendation, rec_detail = _generate_recommendation(
        composite_score, skill_score_final, exp_score, edu_score, missing_required
    )

    # ────────────────────────────────────────────────────────────────────────
    # 6. ACTIONABLE IMPROVEMENTS
    # ────────────────────────────────────────────────────────────────────────
    improvement_tips = _generate_improvement_tips(
        missing_required, preferred_matched, preferred_skills,
        resume_years, required_years
    )

    # ────────────────────────────────────────────────────────────────────────
    # 7. BUILD RESPONSE
    # ────────────────────────────────────────────────────────────────────────
    return {
        "match_score": composite_score,
        
        "breakdown": {
            "skill_score": round(skill_score_final, 2),
            "skill_score_detail": f"{len(required_matched)}/{len(required_skills)} required skills matched" if required_skills else "No required skills specified",
            "experience_score": round(exp_score, 2),
            "experience_score_detail": exp_detail,
            "education_score": round(edu_score, 2),
            "education_score_detail": edu_detail,
            "weights": {
                "skills": "55%",
                "experience": "30%",
                "education": "15%",
            },
        },
        
        "skill_match": {
            "required_matched": sorted(required_matched),
            "required_missing": sorted(missing_required),
            "preferred_matched": sorted(preferred_matched),
            "preferred_missing": sorted(missing_preferred),
            "extra_skills": sorted(extra_skills),
            "match_percentage": round(skill_score, 2),
            "summary": (
                f"{len(required_matched)}/{len(required_skills)} required, "
                f"{len(preferred_matched)} preferred" if required_skills else "No skills to match"
            ),
        },
        
        "experience_match": exp_detail,
        "education_match": edu_detail,
        
        "overall_recommendation": recommendation,
        "recommendation_detail": rec_detail,
        "improvement_tips": improvement_tips,
        
        "fitment_category": _categorize_fitment(composite_score),
    }


def _count_relevant_experience(
    experience_list: List[Dict[str, str]],
    job_title: str
) -> int:
    """Count how many resume entries are relevant to the JD job title."""
    if not job_title:
        return 0
    
    title_keywords = job_title.lower().split()
    relevant_count = 0
    
    for exp in experience_list:
        role = exp.get("role", "").lower()
        company = exp.get("company", "").lower()
        context = f"{role} {company}"
        
        if any(kw in context for kw in title_keywords if len(kw) > 3):
            relevant_count += 1
    
    return relevant_count


def _parse_years_from_string(exp_str: Optional[str]) -> Optional[float]:
    if not exp_str:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", str(exp_str))
    return float(m.group(1)) if m else None


def _categorize_fitment(score: float) -> Dict[str, Any]:
    """Categorize fitment with detailed breakdown."""
    if score >= 90:
        return {
            "category": "perfect_match",
            "label": "Perfect Match",
            "emoji": "🟢",
            "description": "Exceptional alignment across all dimensions"
        }
    elif score >= 80:
        return {
            "category": "excellent_match",
            "label": "Excellent Match",
            "emoji": "🟢",
            "description": "Strong fit with minimal gaps"
        }
    elif score >= 70:
        return {
            "category": "good_match",
            "label": "Good Match",
            "emoji": "🟡",
            "description": "Meets most requirements, manageable gaps"
        }
    elif score >= 60:
        return {
            "category": "fair_match",
            "label": "Fair Match",
            "emoji": "🟡",
            "description": "Meets some requirements, notable gaps"
        }
    elif score >= 50:
        return {
            "category": "weak_match",
            "label": "Weak Match",
            "emoji": "🔴",
            "description": "Significant gaps, requires consideration"
        }
    else:
        return {
            "category": "poor_match",
            "label": "Poor Match",
            "emoji": "🔴",
            "description": "Does not meet core requirements"
        }


DEGREE_RANK = {
    "phd": 5, "m.tech": 4, "m.s.": 4, "mba": 4, "mca": 4,
    "b.tech": 3, "b.s.": 3, "bca": 3, "b.com": 2, "bba": 2,
    "diploma": 1, "12th / hsc": 0, "10th / ssc": 0,
}


def _match_education_level(resume_degrees: List[str], jd_quals: List[str]) -> float:
    best_resume = max(
        (DEGREE_RANK.get(d.lower(), 0) for d in resume_degrees), default=0
    )
    required_rank = 0
    for q in jd_quals:
        q_lower = q.lower()
        if "phd" in q_lower or "doctor" in q_lower:
            required_rank = max(required_rank, 5)
        elif "master" in q_lower or "m.tech" in q_lower:
            required_rank = max(required_rank, 4)
        elif "bachelor" in q_lower or "b.tech" in q_lower or "graduate" in q_lower:
            required_rank = max(required_rank, 3)
        elif "diploma" in q_lower:
            required_rank = max(required_rank, 1)

    if required_rank == 0:
        return 100.0
    if best_resume >= required_rank:
        return 100.0
    if best_resume == required_rank - 1:
        return 70.0
    return max(0.0, (best_resume / required_rank) * 100)


def _generate_recommendation(
    composite: float,
    skill_score: float,
    exp_score: float,
    edu_score: float,
    missing_required: set,
) -> Tuple[str, str]:
    if composite >= 85:
        label = "Excellent Match — Strongly Recommended"
        detail = "Candidate is a strong fit. Skills, experience, and education align well."
    elif composite >= 70:
        label = "Good Match — Recommended"
        detail = "Candidate meets most requirements. Minor gaps exist but manageable."
    elif composite >= 55:
        label = "Moderate Match — Consider with Conditions"
        detail = "Candidate meets some requirements. Significant gaps need addressing."
    elif composite >= 40:
        label = "Weak Match — Not Recommended"
        detail = "Candidate lacks several key requirements."
    else:
        label = "Poor Match — Do Not Proceed"
        detail = "Candidate does not meet the core requirements for this role."

    if skill_score < 50 and composite >= 55:
        detail += " Note: Skill gap is a concern despite overall score."
    if exp_score < 50:
        detail += " Candidate is significantly under the experience requirement."

    return label, detail


def _generate_improvement_tips(
    missing_required: set,
    preferred_matched: set,
    preferred_skills: set,
    resume_years: Optional[float],
    required_years: Optional[float],
) -> List[str]:
    """Generate prioritized, actionable improvement suggestions."""
    tips = []

    # PRIORITY 1: Critical skill gaps
    if missing_required:
        # Prioritize common/important skills
        missing_sorted = sorted(missing_required, key=lambda x: _skill_importance_score(x))
        critical_skills = missing_sorted[:3]  # Top 3 critical gaps
        optional_skills = missing_sorted[3:5]  # Next gaps (if any)
        
        if critical_skills:
            skills_str = ", ".join(critical_skills)
            tips.append(
                f"🔴 CRITICAL: Develop these required skills immediately: {skills_str}. "
                f"These are non-negotiable for the role."
            )
        
        if optional_skills:
            tips.append(
                f"📌 Develop: {', '.join(optional_skills)} would complete the "
                f"skill set for this role."
            )

    # PRIORITY 2: Experience gap
    if required_years and resume_years is not None:
        if resume_years < required_years:
            gap = round(required_years - resume_years, 1)
            percentage = round((resume_years / required_years) * 100, 1)
            tips.append(
                f"⏰ EXPERIENCE: {percentage}% toward requirement. "
                f"Gain ~{gap} more years or compensate with strong projects/portfolio."
            )
        elif resume_years >= required_years * 1.2:
            tips.append(
                f"✓ EXPERIENCE: {resume_years} years significantly exceeds the {required_years}+ "
                f"requirement. Emphasize recent, relevant projects."
            )

    # PRIORITY 3: Preferred skills
    missing_preferred = preferred_skills - preferred_matched
    if missing_preferred:
        pref_list = ", ".join(sorted(missing_preferred)[:3])
        tips.append(
            f"⭐ BONUS: Learning {pref_list} would make the profile stand out "
            f"and increase competitiveness."
        )
    elif preferred_matched and len(preferred_matched) >= len(preferred_skills) * 0.5:
        tips.append(
            f"✓ PREFERRED SKILLS: Strong match on preferred qualifications. "
            f"Highlight these in resume."
        )

    # PRIORITY 4: Presentation/optimization
    if not tips or len(tips) < 2:
        tips.append(
            "💡 RESUME TIP: Use exact keywords from JD in your resume. "
            "ATS systems match on terminology — ensure all relevant skills are explicitly mentioned."
        )

    return tips[:4]  # Limit to 4 actionable tips


def _skill_importance_score(skill: str) -> int:
    """Rank skills by importance. Higher number = more important."""
    importance_tiers = {
        # CRITICAL (Tier 1)
        "python": 1, "java": 1, "javascript": 1, "react": 1, "fastapi": 1,
        "django": 1, "sql": 1, "aws": 1, "docker": 1, "kubernetes": 1,
        
        # IMPORTANT (Tier 2)
        "nodejs": 2, "angular": 2, "vue": 2, "spring": 2, "postgresql": 2,
        "mongodb": 2, "git": 2, "elasticsearch": 2, "redis": 2, "terraform": 2,
        
        # NICE-TO-HAVE (Tier 3)
        "html": 3, "css": 3, "bootstrap": 3, "jira": 3, "confluence": 3,
    }
    skill_lower = skill.lower()
    return importance_tiers.get(skill_lower, 99)  # Default to low importance


# ---------------------------------------------------------------------------
# PUBLIC API  (called by routes)
# ---------------------------------------------------------------------------
def parse_resume(resume_text: str) -> Dict[str, Any]:
    """Full resume parse — returns structured data."""
    total_exp = extract_total_experience_years(resume_text)
    return {
        "name":                    extract_name(resume_text),
        "email":                   extract_email(resume_text),
        "phone":                   extract_phone(resume_text),
        "linkedin":                extract_linkedin(resume_text),
        "github":                  extract_github(resume_text),
        "skills":                  extract_skills_from_resume(resume_text),
        "experience":              extract_experience(resume_text),
        "total_experience_years":  total_exp,
        "experience_level":        classify_experience_level(total_exp),
        "education":               extract_education(resume_text),
        "raw_text":                resume_text[:500],
    }


def parse_jd(jd_text: str) -> Dict[str, Any]:
    """Full JD parse — returns structured data."""
    return {
        "title":               extract_job_title(jd_text),
        "company":             extract_company(jd_text),
        "required_skills":     extract_skills_for_jd(jd_text, "requirements"),
        "preferred_skills":    extract_skills_for_jd(jd_text, "preferred"),
        "experience_required": extract_experience_requirement(jd_text),
        "salary_range":        extract_salary(jd_text),
        "qualifications":      extract_qualifications(jd_text),
        "responsibilities":    extract_responsibilities(jd_text),
        "raw_text":            jd_text[:500],
    }