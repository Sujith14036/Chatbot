import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Any
from .models import Course, StudentProfile

class CourseRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.course_features = None
        self.course_vectors = None
        
    def prepare_course_features(self, courses: List[Course]):
        """Prepare course features for vectorization"""
        course_texts = []
        for course in courses:
            # Combine various course attributes into a single text
            text = f"{course.title} {course.description} {' '.join(course.skills_covered)} {' '.join(course.prerequisites)}"
            course_texts.append(text)
        
        # Vectorize course features
        self.course_vectors = self.vectorizer.fit_transform(course_texts)
        self.course_features = courses
        
    def get_recommendations(self, 
                          student_profile: StudentProfile,
                          courses: List[Course],
                          num_recommendations: int = 5) -> List[Dict[str, Any]]:
        """
        Generate personalized course recommendations based on student profile
        """
        if self.course_vectors is None:
            self.prepare_course_features(courses)
            
        # Create student profile vector
        student_text = f"{' '.join(student_profile.academic_interests)} {' '.join(student_profile.career_goals)}"
        student_vector = self.vectorizer.transform([student_text])
        
        # Calculate similarity scores
        similarity_scores = cosine_similarity(student_vector, self.course_vectors).flatten()
        
        # Combine courses with their similarity scores
        course_scores = list(zip(courses, similarity_scores))
        
        # Sort by similarity score
        course_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Prepare recommendations
        recommendations = []
        for course, score in course_scores[:num_recommendations]:
            recommendations.append({
                "course": course,
                "match_score": float(score),
                "reasons": self._generate_recommendation_reasons(course, student_profile)
            })
            
        return recommendations
    
    def _generate_recommendation_reasons(self, course: Course, student_profile: StudentProfile) -> List[str]:
        """Generate personalized reasons for the recommendation"""
        reasons = []
        
        # Check for matching academic interests
        matching_interests = set(course.skills_covered) & set(student_profile.academic_interests)
        if matching_interests:
            reasons.append(f"Matches your interests in: {', '.join(matching_interests)}")
            
        # Check for matching career goals
        matching_goals = set(course.skills_covered) & set(student_profile.career_goals)
        if matching_goals:
            reasons.append(f"Supports your career goals in: {', '.join(matching_goals)}")
            
        # Check prerequisites
        if student_profile.past_courses:
            missing_prerequisites = set(course.prerequisites) - set(student_profile.past_courses)
            if missing_prerequisites:
                reasons.append(f"Note: You may need to complete these prerequisites: {', '.join(missing_prerequisites)}")
                
        return reasons 