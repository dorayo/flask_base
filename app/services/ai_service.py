from flask import current_app
import os
from openai import OpenAI

# GPT
API_KEY = os.getenv('GPT_KEY', '')
GPT_MODEL = 'gpt-4o'
client = OpenAI(
  api_key=API_KEY,
)

def call_gpt_api(model, messages, max_tokens=None):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
        if response.choices[0]:
            message = response.choices[0].message
            if message:
                gpt_result = message.content
        else:
            gpt_result = "GPTErr"
        current_app.logger.info(f'GPT返回值：{gpt_result}')
        return gpt_result
    except Exception as e:
        current_app.logger.error(f"GPT error: {e}")
        return "GPTErr"

def get_gpt_result_img(prompt, image_url):
    '''
    处理图片
    '''
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": image_url},
            ],
        }
    ]
    return call_gpt_api(GPT_MODEL, messages, max_tokens=300)

def get_gpt_result_text(system_prompt, user_prompt):
    '''
    处理文本
    '''
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    return call_gpt_api(GPT_MODEL, messages)
