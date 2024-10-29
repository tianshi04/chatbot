from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load .env file
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 1024,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="Bạn là một người bạn hỗ trợ tui học về ngôn ngữ python. Bạn đôi khi hài hước, lấy những ví dụ trực quan dễ hiều, gần gủi",
)
 
chat_session = model.start_chat(
  history=[

  ]
)

