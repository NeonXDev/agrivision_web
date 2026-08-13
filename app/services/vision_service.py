"""Sends a plant photo to Groq's vision API and parses the response into
plant-identification data.

STAGE 4 fills this in with the official `groq` SDK (already in
requirements.txt). Rough shape of the real call:

    from groq import Groq
    client = Groq(api_key=current_app.config['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'])
    completion = client.chat.completions.create(
        model="...",  # a current vision-capable model — check
                       # console.groq.com/docs/vision, hosted models rotate
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Identify this plant. Reply as "
                                          "JSON with common_name, "
                                          "scientific_name, confidence "
                                          "(0-1), family, description, "
                                          "growing_tips (array)."},
                {"type": "image_url", "image_url": {"url": data_uri}},
            ],
        }],
        response_format={"type": "json_object"},
    )
    return json.loads(completion.choices[0].message.content)

Groq's vision models support JSON mode, so asking for structured JSON
directly (rather than parsing prose) is the reliable path here.
"""


def identify_plant(image_path: str) -> dict:
    """Returns a dict with keys: common_name, scientific_name, confidence
    (0.0-1.0), family, description, growing_tips (list[str]).

    Raises NotImplementedError until Stage 4.
    """
    raise NotImplementedError('vision_service.identify_plant — Stage 4')
