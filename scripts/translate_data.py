import openai
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Replace 'your_api_key' with your actual API key
openai.api_key = 'YOUR_API_KEY_COMES_HERE'

def translate_text(value):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Translate the following text to Portuguese: '{value}'"},
            ],
        max_tokens=1024,
        temperature=0,
        )
    return response.choices[0]["message"]["content"].strip()

def translate_item(item):
    translated_item = {}
    for key, value in item.items():
        if value:
            translated_value = translate_text(value)
            translated_item[key] = translated_value
        else:
            translated_item[key] = ''
    return translated_item

# Maximum number of parallel requests
MAX_PARALLEL_REQUESTS = 100

# Assuming the input JSON is in a file named 'input.json'
with open('alpaca_data.json', 'r') as f:
    data = json.load(f)

start = 40000
end = 55000
translated_data = []
data = data[start:end]

with ThreadPoolExecutor(max_workers=MAX_PARALLEL_REQUESTS) as executor:
    futures = {executor.submit(translate_item, item): item for item in data}
    
    for future in tqdm(as_completed(futures), total=len(futures), desc="Translating"):
        translated_data.append(future.result())

# Save the translated data to a new JSON file named 'translated_data.json'
with open(f'translated_data_up_to_{start}_to_{end}.json', 'w') as f:
    json.dump(translated_data, f, ensure_ascii=False, indent=4)

print(f"Translation complete. The translated data is saved in 'translated_data_from_{start}_to_{end}.json'")
