import json
from openai import OpenAI


class GptModelService:
    def __model(self):
       return OpenAI()

    @classmethod
    def generate_text(self, questions: str) -> dict:
        response = self.__model(self).chat.completions.create(
            model="gpt-4o-mini",
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "response",
                    "schema": {
                        "type": "object",
                        "properties": {
                          "result": {
                            "type": "array",
                            "items": {
                              "question_number": {
                                  "type": "number",
                              },
                              "question": {
                                "type": "string",
                              },
                              "response": {
                                  "type": "string",
                              },
                              "explanation": {
                                  "type": "string"
                              }
                            }
                          }
                        },
                        "required": ["question_number", "question", "response", "explanation"]
                      },
                }
              },
              messages=[
                {
                    "role": "user",
                    "strict": True,
                    "content": [
                    {
                        "type": "text",
                        "text": f"Eu preciso que você assuma o papel de um consultor especialista em cibersegurança e me ajude a entender como posso melhorar a segurança da minha empresa. Tenho perguntas e respostas separadas em pilares captadas através de um formulário para usar como base.",
                    },
                    {
                        "type": "text",
                        "text": f"{questions}"
                    },
                    ],
                },
                {
                    "role": 'system',
                    "content":
                        'Agora, preciso que você me ajude a entender como posso melhorar a segurança da minha empresa. Me de 5 sugestões de melhorias para cada pilar. Retornar em JSON',
                },
            ],
            max_tokens=900,
        )
        return self.__response_to_json(response)

    @classmethod
    def __response_to_json(self, response) -> dict:
        return json.loads(response.choices[0].message.content)['result']

