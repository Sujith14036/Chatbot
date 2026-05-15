from pydantic import BaseModel
from typing import List, Dict, Optional

class Course(BaseModel):
    id: int
    title: str
    description: str
    department: str
    difficulty_level: str
    prerequisites: List[str]
    skills_covered: List[str]
    credits: int
    instructor: str
    schedule: str
    capacity: int
    current_enrollment: int

class StudentProfile(BaseModel):
    id: int
    name: str
    academic_interests: List[str]
    past_courses: List[int]
    career_goals: List[str]
    performance_metrics: Dict[str, float]
    major: Optional[str] = None
    year: Optional[str] = None
    gpa: Optional[float] = None

class RecommendationRequest(BaseModel):
    student_profile: StudentProfile
    number_of_recommendations: int = 5
    filters: Optional[Dict[str, List[str]]] = None

class RecommendationResponse(BaseModel):
    course: Course
    match_score: float
    reasons: List[str]

class CourseEnrollment(BaseModel):
    student_id: int
    course_id: int
    semester: str
    grade: Optional[str] = None
    feedback: Optional[str] = None 