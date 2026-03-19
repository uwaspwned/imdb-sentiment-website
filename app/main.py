import logging
import pickle

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
import uvicorn


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="IMDB Sentiment Analysis API",
    description="API for movie review sentiment analysis (Logistic Regression model)",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler) #type: ignore

model = None
MODEL_PATH = "model.pkl"

def load_model():
    """Load the pre-trained model from a pickle file."""
    global model
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        logger.info("✅ Model successfully loaded")
    except FileNotFoundError:
        logger.error(f"❌ Model file not found at: {MODEL_PATH}")
        model = None
    except Exception as e:
        logger.error(f"❌ Error loading model: {e}")
        model = None

load_model()

class ReviewRequest(BaseModel):
    """Incoming request schema."""
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "text": "This movie was fantastic! I really enjoyed it."
        }
    })
    
    text: str = Field(..., min_length=1, max_length=2000)

class SentimentResponse(BaseModel):
    """API response schema."""
    sentiment: str
    confidence: float
    original_text: str

@app.get("/", tags=["Health"])
@app.get("/health", tags=["Health"])
async def health_check():
    """Check if the API and model are running properly."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "ok", "message": "API is running and model is loaded"}

@app.post("/predict", response_model=SentimentResponse, tags=["Prediction"])
@limiter.limit("100/minute")
async def predict_sentiment(request: Request, review: ReviewRequest):
    """
    Predict sentiment for a movie review.
    - **text**: Review text in English.
    
    Rate limits: 100 requests per minute per IP address
    """
    if model is None:
        logger.error("Prediction attempt failed: model not loaded")
        raise HTTPException(status_code=503, detail="Model not available")

    try:
        client_ip = get_remote_address(request)
        logger.info(f"Request from {client_ip}: {review.text[:50]}...")

        prediction_proba = model.predict_proba([review.text])[0]

        confidence_negative = float(prediction_proba[0])
        confidence_positive = float(prediction_proba[1])

        if confidence_positive > confidence_negative:
            sentiment = "positive"
            confidence = confidence_positive
        else:
            sentiment = "negative"
            confidence = confidence_negative

        response = SentimentResponse(
            sentiment=sentiment,
            confidence=round(confidence, 4),
            original_text=review.text
        )

        logger.info(f"Result for {client_ip}: {sentiment} with confidence {confidence:.4f}")
        
        return response

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/rate-limit-info", tags=["Info"])
async def rate_limit_info():
    """Get information about API rate limits."""
    return {
        "endpoint": "/predict",
        "limit": "100 requests per minute",
        "per": "IP address",
        "status": "active"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)