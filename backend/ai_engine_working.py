from transformers import Qwen3VLForConditionalGeneration, AutoProcessor
import torch

MODEL_NAME = "Qwen/Qwen3-VL-2B-Instruct"

print("Loading FieldMind AI model...")

model = Qwen3VLForConditionalGeneration.from_pretrained(
    MODEL_NAME
)

processor = AutoProcessor.from_pretrained(
    MODEL_NAME
)

print("FieldMind AI model loaded.")


def analyze_image(
    image,
    question="What do you see in this image?"
):

    fieldmind_prompt = f"""
You are FieldMind AI, a practical AI field assistant.

The user has provided an image and a question.

USER QUESTION:
{question}

Analyze the image carefully and answer the user's question.

Use exactly this format:

OBSERVATION:
Describe only what you can clearly see in the image.

POSSIBLE ISSUE:
Identify any visible problem, abnormality, damage, or unusual condition.
If no obvious issue is visible, say:
"No obvious issue detected."

RECOMMENDED ACTION:
Give a practical next step based only on what can reasonably be determined from the image.

SAFETY NOTE:
Mention any relevant safety precaution.
If no specific safety concern can be determined, say:
"No specific safety concern identified from the image."

IMPORTANT:
- Do not invent information.
- Do not claim certainty when the image is unclear.
- Clearly distinguish visible facts from possible issues.
- Keep the answer concise and practical.
"""

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image
                },
                {
                    "type": "text",
                    "text": fieldmind_prompt
                }
            ]
        }
    ]

    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = processor(
        text=[text],
        images=[image],
        return_tensors="pt"
    )

    with torch.inference_mode():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=60,
            do_sample=False
    )

    generated_ids_trimmed = [
        output_ids[len(input_ids):]
        for input_ids, output_ids in zip(
            inputs.input_ids,
            generated_ids
        )
    ]

    output = processor.batch_decode(
        generated_ids_trimmed,
        skip_special_tokens=True
    )[0]

    return output