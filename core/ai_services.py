# core/ai_services.py
import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional

# Explicitly fetch the key from the environment variables array
ENV_API_KEY = os.environ.get("GEMINI_API_KEY")

try:
    if ENV_API_KEY:
        client = genai.Client(api_key=ENV_API_KEY)
    else:
        # Fallback to default constructor search path
        client = genai.Client()
except Exception as init_error:
    print("❌ Critical: Gemini SDK client failed to initialize configuration profiles:", init_error)
    client = None

# =====================================================================
# COMPREHENSIVE BLUEPRINT SCHEMA (OPTIMIZED)
# =====================================================================
class TaskBlueprint(BaseModel):
    title: str = Field(description="A short, engaging title for this specific milestone.")
    concept_summary: str = Field(description="1-2 sentences introducing the core concept.")
    core_lessons: List[str] = Field(
        description=(
            "A list of 3-5 distinct, highly descriptive educational sections. "
            "Each item must be a detailed, multi-sentence narrative explaining a core sub-topic, "
            "providing actual learning definitions, execution steps, or technical explanations."
        )
    )
    local_example: str = Field(description="A practical, real-world scenario or business case study context tailored to African markets.")
    assignment_type: str = Field(description="Must be exactly one of these strings: 'text', 'multiple_choice', or 'checkbox'.")
    assignment_instruction: str = Field(description="Clear instructions on what the student must answer to pass.")
    options: Optional[List[str]] = Field(default=[], description="List of 3-4 possible answers if type is multiple_choice or checkbox. Leave completely empty for text submissions.")
    correct_options: Optional[List[str]] = Field(default=[], description="The exact string answer(s) from the options list that are correct. For multiple_choice, list exactly one. For checkbox, list all that apply. Leave empty for text.")
    points_value: Optional[int] = Field(default=30, description="Points valuation between 10 and 50 based on depth.")

class TrackBatch(BaseModel):
    track_title: str = Field(description="Overall heading name for this modular collection.")
    tasks: List[TaskBlueprint] = Field(description="A collection of exactly 3 sequential educational learning tasks.")

# =====================================================================
# 🖋️ NEW: EVALUATION RESPONSE SCHEMA (For AI grading matching)
# =====================================================================
class EvaluationResult(BaseModel):
    is_correct: bool = Field(description="True if the response completely fulfills instructions and displays competence, False otherwise.")
    feedback: str = Field(description="A 2-4 sentence detailed critique addressing the student directly. Highlight what they did right, or guide them on missing points contextually.")


# =====================================================================
# ADJUSTED CONTENT GENERATION ENGINE
# =====================================================================
def generate_skill_task(course_title, difficulty, description=""):
    """
    Feeds on your manually created SkillTrack parameters to generate 
    a highly personalized, cohesive, and localized 3-task curriculum.
    """
    if not client:
        print("⚠️ Request Blocked: generate_skill_task aborted because client context is None.")
        return None
        
    system_instruction = (
        "You are an expert technical instructor, curriculum designer, and textbook author for SkillPoints Africa. "
        "Your goal is to write rich, high-value, complete educational reading material for students based on the track context provided. "
        "DO NOT write high-level curriculum descriptions, table of contents, or bullet lists of course objectives. "
        "Instead, write direct, comprehensive instructional content. Give clear explanations, explicit industry definitions, "
        "and concrete operational data. "
        "For each string inside the 'core_lessons' array, you must write a deep, self-contained 2-4 sentence instructional paragraph "
        "explaining that specific sub-topic or process fully so a student can actually master it right there."
    )
    
    user_prompt = (
        f"Generate a complete, deeply educational 3-task roadmap tailored perfectly to this course setup:\n\n"
        f"COURSE TITLE: {course_title}\n"
        f"COURSE CORE FOCUS: {description if description else 'General industry practices'}\n"
        f"TARGET DIFFICULTY TIER: {difficulty}\n\n"
        f"Ensure that out of the 3 sequential tasks generated, at least one uses a quiz type ('multiple_choice' or 'checkbox') "
        f"and another uses a 'text' submission prompt to vary the curriculum mechanics."
    )
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=TrackBatch,
                temperature=0.7,
            ),
        )
        return response.parsed
    except Exception as e:
        print("❌ API Error during course task generation:", e)
        return None


# =====================================================================
# 🧠 NEW: TEXT EVALUATION GRADING ENGINE (Used by Sandbox Playground)
# =====================================================================
def evaluate_student_submission(assignment_prompt, student_answer):
    """
    Leverages Gemini structured schema outputs to evaluate textual student assignments
    submitted in the sandbox simulation environment.
    """
    if not client:
        class FallbackEvaluation:
            is_correct = True
            feedback = "System Sandbox Safe Mode: Submission logged successfully."
        return FallbackEvaluation()

    system_instruction = (
        "You are a strict, supportive academic grading instructor evaluating real-world youth business portfolio task responses. "
        "Analyze the provided prompt assignment question and verify if the student response answers it competently with realistic intent. "
        "Be encouraging, concise, and professional."
    )

    user_prompt = (
        f"Review the following student assignment submission:\n\n"
        f"ASSIGNMENT TASK PROMPT:\n{assignment_prompt}\n\n"
        f"STUDENT PORTFOLIO RESPONSE:\n{student_answer}\n\n"
        f"Provide your structured evaluation breakdown now."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=EvaluationResult,
                temperature=0.3,
            ),
        )
        return response.parsed
    except Exception as e:
        print("❌ API Error during submission evaluation:", e)
        return None