from pydantic import BaseModel, Field


class GrammarFeedback(BaseModel):
    score: int = Field(ge=0, le=100)
    issues: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)


class ResumeAnalysisResult(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    ats_score: int = Field(ge=0, le=100)
    profession: str = Field(min_length=1, max_length=150)
    summary_feedback: str
    experience_feedback: str
    projects_feedback: str
    skills_feedback: str
    education_feedback: str
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    grammar: GrammarFeedback
    recruiter_feedback: str
    interview_probability: int = Field(ge=0, le=100)
    recommendations: list[str] = Field(default_factory=list)


class ResumeAnalysisView(BaseModel):
    id: int
    original_filename: str
    provider: str
    model_name: str
    analysis: ResumeAnalysisResult
