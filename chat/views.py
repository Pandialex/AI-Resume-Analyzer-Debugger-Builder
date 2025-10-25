import json
import logging
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ARDAA.utils import call_gemini

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def chat_send(request):
    """Handle chat messages with STRICT short response instructions."""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        logger.info(f"📨 Chat request: {user_message}")
        
        if not user_message:
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        # ULTRA SHORT RESPONSE PROMPT
        short_prompt = f"""You are ARDAA AI Assistant created by Alex. Provide SHORT career advice.

CRITICAL RULES:
- MAXIMUM 2 SENTENCES
- NO BULLET POINTS
- NO LISTS
- BE DIRECT AND ACTIONABLE
- FOCUS ON 1-2 KEY POINTS
- PROFESSIONAL BUT CONCISE
- GET STRAIGHT TO THE POINT

Question: {user_message}

Short answer:"""
        
        logger.info("🤖 Calling AI with ultra-short instructions...")
        
        # Get AI response
        ai_response = call_gemini(short_prompt)
        
        # Force ultra-short response
        ai_response = make_ultra_short(ai_response)
        
        logger.info(f"✅ Final short response: {ai_response}")
        
        return JsonResponse({
            'reply': ai_response,
            'status': 'success'
        })
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON error: {e}")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

def make_ultra_short(text):
    """Force response to be ultra short and clean."""
    if not text:
        return "I can help with resume and career advice. What do you need?"
    
    # Remove bullet points and lists
    text = re.sub(r'[•\-]\s*', '', text)
    text = re.sub(r'\d+\.\s*', '', text)
    
    # Split into sentences and take only first 2
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) > 2:
        text = '. '.join(sentences[:2]) + '.'
    elif len(sentences) == 1:
        text = sentences[0]
        if not text.endswith('.'):
            text += '.'
    else:
        text = '. '.join(sentences) + '.'
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Ensure it's not too long
    if len(text) > 200:
        text = text[:200].rsplit(' ', 1)[0] + '...'
    
    return text

@csrf_exempt
@require_POST
def chat_suggestions(request):
    """Provide quick chat suggestions for short answers."""
    suggestions = [
        "Resume tips",
        "ATS keywords", 
        "Interview prep",
        "Job search",
        "Career advice",
        "Skills demand"
    ]
    return JsonResponse({'suggestions': suggestions})

@csrf_exempt
@require_POST 
def chat_widget_init(request):
    """Initialize chat widget."""
    return JsonResponse({
        'welcome_message': "Hi! I'm ARDAA AI by Alex. Short career advice. How can I help?",
        'status': 'ready'
    })