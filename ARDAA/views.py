import os
import io
import uuid
import json
import fitz
import logging
from docx import Document
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.files.storage import default_storage
from django.contrib import messages
from django.conf import settings
from django.http import Http404, JsonResponse
from .forms import ResumeUploadForm
from .utils import analyze_resume, call_gemini

# Setup logging
logger = logging.getLogger(__name__)

# Temporary directory for file storage
TEMP_DIR = "temp_resumes"

def _ensure_temp_dir():
    """Create temp directory if it doesn't exist."""
    base = os.path.join(settings.MEDIA_ROOT, TEMP_DIR)
    os.makedirs(base, exist_ok=True)
    return base

def extract_text(file_bytes, ext):
    """Extract text from different file formats."""
    ext = ext.lower()
    try:
        if ext == "pdf":
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = "\n".join([page.get_text("text") for page in doc])
            doc.close()
            return text
        elif ext == "docx":
            doc = Document(io.BytesIO(file_bytes))
            return "\n".join([p.text for p in doc.paragraphs])
        elif ext in ("txt", "text"):
            return file_bytes.decode("utf-8", errors="ignore")
        else:
            return ""
    except Exception as e:
        logger.error(f"Text extraction error: {e}")
        return ""

def index(request):
    """Home page view."""
    form = ResumeUploadForm()
    return render(request, "ARDAA/index.html", {"form": form})
def analyze(request):
    """Analyze resume against job description - NO LOGIN REQUIRED."""
    if request.method == "POST":
        print("🚀 DEBUG: Analyze view called - POST request")
        
        form = ResumeUploadForm(request.POST, request.FILES)
        
        if not form.is_valid():
            print("❌ DEBUG: Form validation failed")
            for field, errors in form.errors.items():
                print(f"❌ {field}: {errors}")
            messages.error(request, "Please check the form fields.")
            return render(request, "ARDAA/index.html", {"form": form})

        resume_file = form.cleaned_data["resume"]
        job_desc = form.cleaned_data["job_desc"].strip()

        print(f"📄 DEBUG: Resume file: {resume_file.name}")
        print(f"📝 DEBUG: Job desc length: {len(job_desc)}")

        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.txt']
        file_ext = os.path.splitext(resume_file.name)[1].lower()
        if file_ext not in allowed_extensions:
            print(f"❌ DEBUG: Invalid file extension: {file_ext}")
            messages.error(request, "Please upload PDF, DOCX, or TXT files only.")
            return render(request, "ARDAA/index.html", {"form": form})

        # Validate job description
        if not job_desc or len(job_desc) < 30:
            print("❌ DEBUG: Job description too short or empty")
            messages.error(request, "Please provide a detailed job description (at least 30 characters).")
            return render(request, "ARDAA/index.html", {"form": form})

        # Process analysis for BOTH authenticated and unauthenticated users
        try:
            print("🔍 DEBUG: Starting resume processing...")
            
            # Read and extract text from resume
            file_data = resume_file.read()
            ext = resume_file.name.split(".")[-1].lower()
            resume_text = extract_text(file_data, ext)

            if not resume_text.strip():
                print("❌ DEBUG: Could not extract text from file")
                messages.error(request, "Could not extract text from the file. Please try another file.")
                return render(request, "ARDAA/index.html", {"form": form})

            print(f"📊 DEBUG: Extracted text length: {len(resume_text)}")
            print("🤖 DEBUG: Calling AI analysis...")

            # Perform AI analysis
            analysis_result = analyze_resume(resume_text, job_desc)
            
            print(f"✅ DEBUG: Analysis complete - Score: {analysis_result.get('ats_score')}")

            # Store comprehensive results in session
            request.session['analysis_results'] = {
                "ats_score": analysis_result.get('ats_score', 50),
                "grammar": analysis_result.get('grammar', ["No grammar issues found"]),
                "feedback": analysis_result.get('feedback', ["Analysis completed successfully"]),
                "suggestions": analysis_result.get('suggestions', ["Add more relevant keywords from job description"]),
                "ai_tips": analysis_result.get('ai_tips', [
                    "Optimize your resume with relevant keywords from the job description",
                    "Use quantifiable achievements to demonstrate impact",
                    "Ensure your resume is ATS-friendly with standard formatting",
                    "Highlight transferable skills that match the job requirements"
                ]),
                "resume_text": resume_text[:1000],
                "job_desc": job_desc[:500],
            }
            request.session.modified = True

            print("🎯 DEBUG: Redirecting to result page...")
            return redirect("ARDAA:result_page")

        except Exception as e:
            print(f"💥 DEBUG: Analysis error: {str(e)}")
            logger.error(f"Analysis error: {str(e)}")
            messages.error(request, f"Analysis failed: {str(e)}")
            return render(request, "ARDAA/index.html", {"form": form})

    # GET request - show form
    print("🔍 DEBUG: Analyze view - GET request")
    form = ResumeUploadForm()
    return render(request, "ARDAA/index.html", {"form": form})



# def after_login(request):
#     """Continue analysis after user login."""
#     if not request.user.is_authenticated:
#         print("❌ DEBUG: User not authenticated in after_login")
#         return redirect('accounts:login')

#     temp_resume_path = request.session.get("temp_resume_path")
#     job_desc = request.session.get("temp_job_desc")

#     print(f"🔍 DEBUG: after_login - temp_resume_path: {temp_resume_path}")
#     print(f"🔍 DEBUG: after_login - job_desc exists: {bool(job_desc)}")

#     if not temp_resume_path or not job_desc:
#         print("❌ DEBUG: Session data missing in after_login")
#         messages.error(request, "Your session has expired. Please upload your resume again.")
#         return redirect("ARDAA:index")

#     try:
#         print("🔍 DEBUG: Processing stored resume file...")
        
#         # Read stored file
#         with default_storage.open(temp_resume_path, 'rb') as f:
#             file_data = f.read()
        
#         # Extract text
#         ext = temp_resume_path.split('.')[-1]
#         resume_text = extract_text(file_data, ext)

#         if not resume_text.strip():
#             print("❌ DEBUG: Could not read stored resume file")
#             messages.error(request, "Could not read the resume file. Please try again.")
#             return redirect("ARDAA:index")

#         print(f"📊 DEBUG: Stored resume text length: {len(resume_text)}")
#         print("🤖 DEBUG: Calling AI analysis for stored resume...")

#         # Perform AI analysis
#         analysis_result = analyze_resume(resume_text, job_desc)
        
#         print(f"✅ DEBUG: Stored resume analysis complete - Score: {analysis_result.get('ats_score')}")

#         # Store results in session
#         request.session['analysis_results'] = {
#             "ats_score": analysis_result.get('ats_score', 50),
#             "grammar": analysis_result.get('grammar', ["No grammar issues found"]),
#             "feedback": analysis_result.get('feedback', ["Analysis completed successfully"]),
#             "suggestions": analysis_result.get('suggestions', ["Add more relevant keywords from job description"]),
#             "ai_tips": analysis_result.get('ai_tips', [
#                 "Optimize your resume with relevant keywords from the job description",
#                 "Use quantifiable achievements to demonstrate impact",
#                 "Ensure your resume is ATS-friendly with standard formatting",
#                 "Highlight transferable skills that match the job requirements"
#             ]),
#             "resume_text": resume_text[:1000],
#             "job_desc": job_desc[:500],
#         }
#         request.session.modified = True

#         # Clean up temporary files
#         try:
#             request.session.pop("temp_resume_path", None)
#             request.session.pop("temp_job_desc", None)
#             default_storage.delete(temp_resume_path)
#             print("🧹 DEBUG: Temporary files cleaned up")
#         except Exception as e:
#             print(f"⚠️ DEBUG: Cleanup error: {e}")

#         print("🎯 DEBUG: Redirecting to result page from after_login...")
#         return redirect("ARDAA:result_page")

#     except Exception as e:
#         print(f"💥 DEBUG: after_login error: {str(e)}")
#         logger.error(f"After login error: {str(e)}")
#         messages.error(request, f"An error occurred during analysis: {str(e)}")
#         return redirect("ARDAA:index")
def after_login(request):
    """Redirect to index since login is no longer required for analysis."""
    messages.info(request, "You can now analyze resumes without logging in!")
    return redirect("ARDAA:index")

def result_view(request):
    """Display analysis results."""
    print("🔍 DEBUG: Result view accessed")
    
    # Get results from session
    results = request.session.get('analysis_results')
    print(f"🔍 DEBUG: Session results exists: {bool(results)}")
    
    if not results:
        print("❌ DEBUG: No analysis results found in session")
        messages.error(request, "No analysis results found. Please upload and analyze a resume first.")
        return redirect("ARDAA:index")
    
    # Ensure all required fields are present with defaults
    required_fields = {
        'ats_score': 50,
        'grammar': ["No grammar analysis available"],
        'feedback': ["No feedback available"],
        'suggestions': ["No suggestions available"],
        'ai_tips': ["Optimize with job description keywords"]
    }
    
    for field, default in required_fields.items():
        if field not in results or not results[field]:
            print(f"⚠️ DEBUG: Missing field {field}, using default")
            results[field] = default
    
    print(f"📊 DEBUG: Displaying results - ATS Score: {results.get('ats_score')}")
    print(f"📊 DEBUG: Grammar issues: {len(results.get('grammar', []))}")
    print(f"📊 DEBUG: Suggestions: {len(results.get('suggestions', []))}")
    print(f"📊 DEBUG: AI Tips: {len(results.get('ai_tips', []))}")
    
    # Clear the session after displaying (optional - keep if you want users to refresh)
    # request.session.pop('analysis_results', None)
    # request.session.modified = True
    
    return render(request, "ARDAA/result.html", results)

def aboutus(request):
    """About us page."""
    return render(request, "ARDAA/aboutus.html")

# Chat functionality (if you want to keep it in ARDAA app)
def chat_send(request):
    """Handle chat messages - SHORT RESPONSES."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            
            print(f"💬 DEBUG: Chat message: {message}")
            
            if not message:
                return JsonResponse({'error': 'Message is required'}, status=400)
            
            # SHORT RESPONSE PROMPT
            short_prompt = f"""You are ARDAA AI Assistant created by Alex. Provide SHORT career advice.

RULES:
- MAXIMUM 2 SENTENCES
- NO BULLET POINTS
- BE DIRECT AND ACTIONABLE
- FOCUS ON 1-2 KEY POINTS

Question: {message}

Short answer:"""
            
            # Get AI response
            ai_response = call_gemini(short_prompt)
            
            # Ensure short response
            def make_short(text):
                sentences = text.split('. ')
                if len(sentences) > 2:
                    text = '. '.join(sentences[:2]) + '.'
                return text.replace('•', '').replace('-', '')
            
            ai_response = make_short(ai_response)
            
            print(f"💬 DEBUG: Chat response: {ai_response}")
            
            return JsonResponse({
                'reply': ai_response,
                'status': 'success'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(f"💥 DEBUG: Chat error: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
