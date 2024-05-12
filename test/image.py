import os
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
)

response = client.images.generate(
  model="dall-e-2",
  prompt="a white siamese cat",
  size="256x256",
  quality="standard",
  n=1,
)
# response = client.images.generate(
#   model="dall-e-3",
#   prompt="a white siamese cat",
#   size="1024x1024",
#   quality="standard",
#   n=1,
# )

image_url = response.data[0].url
print(image_url)