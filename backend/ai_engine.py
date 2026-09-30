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
import cv2
from PIL import Image


def extract_video_frames(video_path, num_frames=3):
    """
    Extract a small number of representative frames from a video.
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Could not open video.")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        cap.release()
        raise ValueError("Video contains no readable frames.")

    frame_indices = [
        int(i * (total_frames - 1) / (num_frames - 1))
        for i in range(num_frames)
    ] if num_frames > 1 else [0]

    frames = []

    for index in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, index)

        success, frame = cap.read()

        if not success:
            continue

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        image = Image.fromarray(frame)

        # Keep images manageable for CPU inference
        image.thumbnail((768, 768))

        frames.append(image)

    cap.release()

    if not frames:
        raise ValueError("Could not extract frames from video.")

    return frames