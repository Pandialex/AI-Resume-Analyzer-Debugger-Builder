import os
import json
import time
import logging
from typing import Dict, Any
import requests
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# --- Gemini / API config ---
API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
HEADERS = {"Content-Type": "application/json", "X-goog-api-key": API_KEY}

# HTTP call config
HTTP_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 2.0

def call_gemini(prompt: str) -> str:
    """Call Gemini API with the given prompt and return raw text response."""
    if not API_KEY:
        logger.error("GEMINI_API_KEY is not set. Set it in your .env file.")
        return "⚠️ Gemini API key missing. Please configure GEMINI_API_KEY."

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 2048,
        }
    }

    last_exc = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.post(ENDPOINT, headers=HEADERS, json=payload, timeout=HTTP_TIMEOUT)
            
            if resp.status_code == 200:
                data = resp.json()
                try:
                    return data["candidates"][0]["content"]["parts"][0]["text"].strip()
                except (KeyError, IndexError) as e:
                    logger.error("Unexpected Gemini response structure: %s", data)
                    return "⚠️ Error parsing AI response. Please try again."
            
            elif resp.status_code == 429:
                wait_time = RETRY_DELAY * (attempt + 1)
                logger.warning("Rate limit hit, waiting %s seconds", wait_time)
                time.sleep(wait_time)
                continue
                
            else:
                logger.error("Gemini API error %s: %s", resp.status_code, resp.text)
                if 500 <= resp.status_code < 600 and attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                    continue
                return f"⚠️ API Error {resp.status_code}: Please try again later."
                
        except requests.RequestException as e:
            logger.warning("Network error (attempt %d): %s", attempt + 1, e)
            last_exc = e
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
                continue
            return "⚠️ Network error. Please check your connection and try again."
    
    return f"⚠️ Failed after {MAX_RETRIES} attempts: {last_exc}"

def _extract_json_from_text(text: str) -> tuple:
    """Attempt to find and parse a JSON object inside `text`."""
    if not text:
        return False, {}

    text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    
    if start == -1 or end == -1 or end < start:
        return False, {}

    candidate = text[start:end + 1]
    
    try:
        parsed = json.loads(candidate)
        return True, parsed
    except json.JSONDecodeError:
        try:
            import re
            candidate = re.sub(r',\s*}', '}', candidate)
            candidate = re.sub(r',\s*]', ']', candidate)
            parsed = json.loads(candidate)
            return True, parsed
        except Exception:
            logger.error("Failed to parse JSON from: %s", candidate[:200])
            return False, {}

def analyze_resume(resume_text: str, job_desc: str) -> Dict[str, Any]:
    """
    Analyze resume against job description using Gemini API.
    Returns comprehensive analysis data including AI tips.
    """
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) resume analyzer. 
    Analyze the resume against the job description and provide a JSON response with the following structure:
    
    {{
        "ats_score": 85,
        "grammar": ["List of grammar issues found"],
        "feedback": ["List of general feedback points"],
        "suggestions": ["List of improvement suggestions"],
        "ai_tips": ["List of AI-powered optimization tips"]
    }}
    
    IMPORTANT: 
    - ats_score should be an integer between 0-100
    - All arrays should contain strings
    - Be constructive and specific in your feedback
    - Focus on ATS compatibility, keywords, and formatting
    - For ai_tips, provide advanced AI-specific optimization strategies
    
    RESUME:
    {resume_text[:3000]}
    
    JOB DESCRIPTION:
    {job_desc[:2000]}
    
    Provide ONLY the JSON response, no additional text.
    """

    raw_response = call_gemini(prompt)
    
    # Default response structure
    default_response = {
        'ats_score': 50,
        'grammar': ["AI service temporarily unavailable"],
        'feedback': ["Please try again later"],
        'suggestions': ["Check your connection and retry"],
        'ai_tips': [
            "Optimize your resume with relevant keywords from the job description",
            "Use quantifiable achievements to demonstrate impact",
            "Ensure your resume is ATS-friendly with standard formatting",
            "Highlight transferable skills that match the job requirements"
        ]
    }
    
    if raw_response.startswith("⚠️"):
        logger.error("Gemini API call failed: %s", raw_response)
        return default_response
    
    ok, parsed = _extract_json_from_text(raw_response)
    
    if not ok:
        logger.error("Failed to parse AI response: %s", raw_response[:500])
        return default_response
    
    # Extract and validate data with defaults
    try:
        ats_score = min(100, max(0, int(parsed.get("ats_score", 50))))
    except (ValueError, TypeError):
        ats_score = 50

    def _safe_list_extract(key, default=None):
        if default is None:
            default = []
        value = parsed.get(key, default)
        if isinstance(value, list):
            return [str(item) for item in value if item]
        return [str(value)] if value else default

    # Ensure all required fields are present
    result = {
        'ats_score': ats_score,
        'grammar': _safe_list_extract("grammar", ["No major grammar issues found"]),
        'feedback': _safe_list_extract("feedback", ["Review completed successfully"]),
        'suggestions': _safe_list_extract("suggestions", ["Add more relevant keywords from job description"]),
        'ai_tips': _safe_list_extract("ai_tips", [
            "Optimize your resume with relevant keywords from the job description",
            "Use quantifiable achievements to demonstrate impact",
            "Ensure your resume is ATS-friendly with standard formatting",
            "Highlight transferable skills that match the job requirements"
        ])
    }
    
    return result