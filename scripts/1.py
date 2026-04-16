
from backend.services import parsing_service as ps
resume = ps.parse_resume('John Doe\njohn@test.com\nSkills: Python, FastAPI')
jd = ps.parse_jd('Backend Engineer\nRequired: Python, FastAPI')
result = ps.match_resume_to_jd(resume, jd)
print(result.keys())
