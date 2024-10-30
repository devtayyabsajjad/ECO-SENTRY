import openai
from config import Config
import numpy as np
from PIL import Image
import tensorflow as tf
import os
from groq import Groq  # Import Groq

# Initialize OpenAI API key
Groq.api_key = Config.OPENAI_API_KEY

# Initialize Groq client
groq_client = Groq(
    api_key="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"
)

def analyze_report(report_text):
    prompt = f"Analyze the following environmental report and provide insights:\n\n{report_text}\n\nInsights:"
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

def generate_recommendations(report_text):
    prompt = f"Based on the following environmental report, suggest actions to address the issue:\n\n{report_text}\n\nRecommendations:"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

def analyze_image(image_path):
    # Load a pre-trained model (this is a placeholder, you'd need to use a proper environmental analysis model)
    model = tf.keras.applications.MobileNetV2(weights='imagenet')
    
    # Load and preprocess the image
    img = Image.open(image_path)
    img = img.resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    
    # Make predictions
    predictions = model.predict(img_array)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
    
    # Format results
    results = [f"{label}: {confidence:.2f}%" for (_, label, confidence) in decoded_predictions]
    return results

def predict_environmental_trends(historical_data):
    prompt = f"Based on the following historical environmental data, predict future trends and potential issues:\n\n{historical_data}\n\nPredictions:"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

def explain_importance_of_fast_language_models():
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content  # Return the response content