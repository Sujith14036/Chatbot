from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="AI Course Recommendation System")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data models
class Course(BaseModel):
    id: int
    title: str
    description: str
    department: str
    difficulty_level: str
    prerequisites: List[str]
    skills_covered: List[str]

class StudentProfile(BaseModel):
    id: int
    name: str
    academic_interests: List[str]
    past_courses: List[int]
    career_goals: List[str]
    performance_metrics: dict

class RecommendationRequest(BaseModel):
    student_profile: StudentProfile
    number_of_recommendations: int = 5

# Sample data (in a real application, this would be in a database)
courses = [
    Course(
        id=1,
        title="Introduction to Machine Learning",
        description="Fundamentals of machine learning algorithms and applications",
        department="Computer Science",
        difficulty_level="Intermediate",
        prerequisites=["Python Programming", "Linear Algebra"],
        skills_covered=["Python", "Scikit-learn", "Data Analysis"]
    ),
    # Add more sample courses here
]

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Course Recommendation System"}

@app.get("/courses", response_model=List[Course])
async def get_courses():
    return courses

@app.post("/recommendations")
async def get_recommendations(request: RecommendationRequest):
    try:
        # This is a placeholder for the actual recommendation logic
        # In a real implementation, this would use machine learning models
        # to generate personalized recommendations
        
        # For now, we'll return a simple recommendation based on matching interests
        recommended_courses = []
        for course in courses:
            # Simple matching based on academic interests and career goals
            interest_match = len(set(course.skills_covered) & set(request.student_profile.academic_interests))
            career_match = len(set(course.skills_covered) & set(request.student_profile.career_goals))
            
            if interest_match > 0 or career_match > 0:
                recommended_courses.append({
                    "course": course,
                    "match_score": interest_match + career_match
                })
        
        # Sort by match score and return top recommendations
        recommended_courses.sort(key=lambda x: x["match_score"], reverse=True)
        return recommended_courses[:request.number_of_recommendations]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 