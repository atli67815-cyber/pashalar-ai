from typing import Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from openai import AsyncOpenAI
from pydantic import BaseModel

app = FastAPI()

# Groq API anahtarını buraya yaz
client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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",
)


class ChatRequest(BaseModel):
  message: str
  image: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def read_root():
  try:
    with open("index.html", "r", encoding="utf-8") as f:
      return f.read()
  except FileNotFoundError:
    return "index.html dosyası bulunamadı!"


@app.post("/chat")
@app.post("/api/chat")
async def chat(request: ChatRequest):
  async def response_generator():
    try:
      user_content = request.message
      if request.image:
        user_content += " [Kullanıcı sohbete bir görsel ekledi/gönderdi]"

      stream = await client.chat.completions.create(
          model="openai/gpt-oss-120b",
          messages=[
              {
                  "role": "system",
                  "content": (
                      "Senin adın Pashalar AI. Sen gelişmiş, yetenekli ve"
                      " yardımcı bir yapay zeka asistanısın. Asla ChatGPT"
                      " olduğunu söyleme, kimliğin Pashalar AI'dır."
                  ),
              },
              {"role": "user", "content": user_content},
          ],
          stream=True,
      )
      async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
          yield content
    except Exception as e:
      print("HATA OLUŞTU:", str(e))
      yield f"Bağlantı hatası oluştu: {str(e)}"

  return StreamingResponse(response_generator(), media_type="text/plain")


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(app, host="127.0.0.1", port=8000)