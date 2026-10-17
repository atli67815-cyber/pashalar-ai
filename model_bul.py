import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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",
)


async def list_models():
  try:
    response = await client.models.list()
    print("\n--- HESABININ KULLANABİLDİĞİ MODELLER ---")
    for model in response.data:
      print(f"-> {model.id}")
    print("----------------------------------------\n")
  except Exception as e:
    print("Hata:", e)


asyncio.run(list_models())