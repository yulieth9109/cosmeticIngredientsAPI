import website.parameters as parameters

from openai import OpenAI

client = OpenAI(
  api_key = parameters.openAISecret,
)

def requestChatGPT(text):
    try:
        main_text = "Del siguiente texto extraer la lista de ingredientes solamente, la lista debe estar en formato CSV, el sepador será '++', cada ingrediente debe estar en mayuscula fija. Si no es posible encontrar ingredientes retorna solamente la palabra VACÍO. El texto es :"
        result = f"{main_text}\n{text}"
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": result,
                }
            ],
            model="gpt-3.5-turbo",
        )
    except ValueError as e:
        print(e)
        return "ERR: Los ingredientes no se pudieron procesar"

    return chat_completion.choices[0].message.content