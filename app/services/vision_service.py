"""Processes plant photos and parses botanical and agricultural data.
"""
import base64
import io
import json
import os
import re
from flask import current_app
from PIL import Image


def _prepare_image_bytes(image_path: str) -> bytes:
    """Opens image, normalizes orientation, converts to RGB, resizes if huge,
    and returns optimized JPEG bytes."""
    with Image.open(image_path) as img:
        if img.mode in ('RGBA', 'LA', 'P', 'CMYK'):
            img = img.convert('RGB')

        max_dim = 1400
        w, h = img.size
        if max(w, h) > max_dim:
            scale = max_dim / max(w, h)
            new_size = (int(w * scale), int(h * scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        elif min(w, h) < 32:
            img = img.resize((max(w, 32), max(h, 32)), Image.Resampling.NEAREST)

        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=88, optimize=True)
        return buffer.getvalue()


BOTANICAL_PROMPT = (
    "You are an expert agricultural botanist and plant specialist in Nepal.\n"
    "Analyze this photo of a plant, flower, fruit, vegetable, crop, or leaf.\n"
    "Write in natural, authoritative, practical agricultural language without referring to yourself as an AI or language model.\n"
    "Provide botanical details and comprehensive farming insights in BOTH English and authentic Nepali (Devanagari script).\n"
    "Respond ONLY with a JSON object with EXACTLY the following structure:\n"
    "{\n"
    '  "is_plant": true,\n'
    '  "common_name": "Standard English common name (e.g. Tomato)",\n'
    '  "common_name_ne": "Authentic Nepali name in Devanagari script (e.g. गोलभेंडा)",\n'
    '  "scientific_name": "Botanical Latin Name (e.g. Solanum lycopersicum)",\n'
    '  "family": "Botanical Family (e.g. Solanaceae)",\n'
    '  "confidence": 0.95,\n'
    '  "crop_keyword": "Standard common crop name for Nepal market lookup (e.g. Tomato, Potato, Apple, Maize, Cabbage, Ginger, Garlic)",\n'
    '  "description": "2-3 practical sentences in English describing the crop and its characteristics in Nepal.",\n'
    '  "description_ne": "2-3 practical sentences in Nepali (Devanagari) describing the crop and its characteristics in Nepal.",\n'
    '  "planting_season": "Specific planting months and seasons in Nepal (e.g. Spring: Feb–Mar in mid-hills; Monsoon: May–Jun in Terai)",\n'
    '  "planting_season_ne": "नेपालमा रोप्ने उपयुक्त महिना र मौसम (उदा. पहाडमा फागुन–चैत; तराईमा जेठ–असार)",\n'
    '  "growth_duration": "Days to maturity from planting to harvest (e.g. 75–90 days to first harvest)",\n'
    '  "growth_duration_ne": "बाली पाक्न र भित्र्याउन लाग्ने समय (उदा. ७५ देखि ९० दिन)",\n'
    '  "optimal_climate": "Favorable climate conditions: temperature range in °C, suitable elevation zones in Nepal (Terai, Mid-hills), sunshine, and soil moisture.",\n'
    '  "optimal_climate_ne": "राम्रोसँग फस्टाउने उपयुक्त हावापानी: तापक्रम (°C), नेपालका उपयुक्त क्षेत्र (तराई, पहाड), घाम र माटोको अनुकूल अवस्था।",\n'
    '  "unfavorable_climate": "Unfavorable climate & risks: frost sensitivity, cold limit, waterlogging hazards, high humidity disease blights, or conditions where it fails to grow.",\n'
    '  "unfavorable_climate_ne": "सप्रिन नसक्ने प्रतिकूल अवस्था र जोखिम: तुषारो, अत्यधिक चिसो, पानी जम्ने समस्या, अत्यधिक गर्मी वा रोग लाग्ने प्रतिकूल वातावरण।",\n'
    '  "fertilizer_guide": [\n'
    '    "Basal Application: Organic compost/FYM quantity and base DAP/Potash during field preparation",\n'
    '    "Top-Dressing: Urea split application timing during vegetative growth and flowering stages",\n'
    '    "Micronutrients & Organic Care: Boron, Calcium, or vermicompost for fruit health and disease resistance"\n'
    '  ],\n'
    '  "fertilizer_guide_ne": [\n'
    '    "आधार मल (खेत तयारी): राम्रोसँग पाकेको गोबर/कम्पोस्ट मल, डीएपी र पोटासको मात्रा",\n'
    '    "थप मल (टप-ड्रेसिङ): बोटको वृद्धि र फूल फुल्ने समयमा युरिया मल हाल्ने तरिका",\n'
    '    "सूक्ष्म पोषकतत्व र जैविक हेरचाह: फल लाग्ने र कुहिनबाट बचाउन बोरोन, क्याल्सियम वा जैविक झोल मल"\n'
    '  ],\n'
    '  "profitability_window": {\n'
    '    "rating": "High Profit Margin / Steady Demand / Moderate",\n'
    '    "peak_months": "Specific months when wholesale rates in Nepal (Kalimati/local mandis) reach highest prices",\n'
    '    "off_season_advantage": "Specific off-season tunnel or early planting price premium in Nepal",\n'
    '    "selling_strategy": "Practical advice on whether to sell fresh immediately or store for festive/winter price spikes"\n'
    '  },\n'
    '  "profitability_window_ne": {\n'
    '    "rating": "उच्च नाफा सम्भावना / स्थिर माग / मध्यम",\n'
    '    "peak_months": "कालिमाटी तथा स्थानीय मण्डीमा सबैभन्दा उच्च भाउ पाइने महिनाहरू (उदा. असोज–कात्तिक चाडपर्व वा हिउँदे अभाव)",\n'
    '    "off_season_advantage": "बेमौसमी, टनेल वा चाँडो उत्पादन गर्दा पाइने थप मूल्यको फाइदा",\n'
    '    "selling_strategy": "कहिले र कसरी बेच्दा बढी फाइदा हुन्छ (तत्काल ताजा बेच्ने वा भण्डारण गरेर भाउ बढेको बेला बेच्ने सल्लाह)"\n'
    '  },\n'
    '  "growing_tips": [\n'
    '    "Soil & Climatic Requirements: ...",\n'
    '    "Watering & Irrigation: ...",\n'
    '    "Sunlight & Seasonal Planting in Nepal: ...",\n'
    '    "Pest & Disease Management: ..."\n'
    '  ],\n'
    '  "growing_tips_ne": [\n'
    '    "माटो र हावापानी: ...",\n'
    '    "सिँचाइ तथा पानी व्यवस्थापन: ...",\n'
    '    "घाम र मौसम अनुसार रोप्ने समय: ...",\n'
    '    "कीरा तथा रोग नियन्त्रण: ..."\n'
    '  ]\n'
    "}\n"
    "Note: If the image clearly does not depict any plant or agricultural produce, set is_plant to false and provide a clear description in both English and Nepali."
)

DEFAULT_TIPS_EN = [
    'Ensure fertile, well-draining soil mixed with organic compost.',
    'Water regularly when the topsoil feels dry; prevent waterlogging.',
    'Provide adequate direct sunlight suitable for the crop season in Nepal.',
    'Inspect foliage routinely for signs of common pests or fungal blights.',
]

DEFAULT_TIPS_NE = [
    'प्राङ्गारिक मल मिसाइएको, राम्रो निकास भएको मलिलो दोमट माटो प्रयोग गर्नुहोस्।',
    'माटोको अवस्था हेरेर नियमित सिँचाइ गर्नुहोस्, जरामा पानी जम्न नदिनुहोस्।',
    'नेपालको मौसम अनुसार बिरुवालाई पर्याप्त घाम लाग्ने स्थानमा खेती गर्नुहोस्।',
    'कीरा तथा ढुसीजन्य रोगको नियमित अनुगमन गरी समयमै जैविक वा उचित उपचार गर्नुहोस्।',
]

DEFAULT_FERTILIZER_EN = [
    'Basal Application: Apply 10–15 tons/ha of well-rotted Farmyard Manure (FYM) or compost combined with DAP and Potash during land preparation.',
    'First Top-Dressing: Apply Nitrogen/Urea 25–30 days after transplanting or seedling emergence during active vegetative growth.',
    'Second Top-Dressing: Apply additional Urea and organic compost tea at the start of flowering and fruit set.',
    'Micronutrient Care: Spray foliar Micronutrients (Zinc, Boron) if leaf yellowing or poor fruit set is noticed.'
]

DEFAULT_FERTILIZER_NE = [
    'आधार मल: खेत तयारी गर्दा प्रति रोपनी ५००–८०० केजी राम्रोसँग पाकेको गोबर वा कम्पोस्ट मल, ३ केजी डीएपी र २ केजी पोटास माटोमा मिलाउने।',
    'पहिलो टप-ड्रेसिङ: बिरुवा सारेको वा उम्रिएको २५–३० दिनपछि बोटको वृद्धि तीव्र हुने बेला प्रति रोपनी १.५ केजी युरिया मल हाल्ने।',
    'दोस्रो टप-ड्रेसिङ: फूल फुल्ने र फल लाग्न सुरु हुँदा १.५ केजी युरिया र प्राङ्गारिक झोल मल प्रयोग गर्ने।',
    'सूक्ष्म पोषकतत्व: पात पहेंलो हुने वा फल झर्ने समस्या देखिएमा बोरोन र जिंकयुक्त सूक्ष्म पोषकतत्व स्प्रे गर्ने।'
]

DEFAULT_PROFIT_EN = {
    'rating': 'Profitable Market Window',
    'peak_months': 'Festival Season (September–November) and Pre-Monsoon (April–May)',
    'off_season_advantage': 'Cultivating under plastic tunnels or planting 3–4 weeks early fetches 40–60% higher wholesale prices.',
    'selling_strategy': 'Harvest in early morning for fresh morning mandi delivery. For storable produce, cure in shaded ventilated sheds to sell during off-peak supply dips.'
}

DEFAULT_PROFIT_NE = {
    'rating': 'उच्च नाफा सम्भावना',
    'peak_months': 'चाडपर्वको मौसम (असोज–कात्तिक) र वर्षापूर्वको अभाव समय (चैत–वैशाख)',
    'off_season_advantage': 'टनेल प्रविधि वा ३–४ हप्ता चाँडो खेती गर्दा थोक बजारमा ४० देखि ६० प्रतिशतसम्म बढी मूल्य पाइन्छ।',
    'selling_strategy': 'ताजा तरकारी बिहान सबेरै टिपेर थोक मण्डीमा पुर्याउनुहोस्। भण्डारण गर्न सकिने बालीलाई हावा चल्ने ठाउँमा सुकाएर अभाव भएको बेला बेच्दा अधिकतम मूल्य पाइन्छ।'
}


def _clean_json_response(raw_text: str) -> dict:
    """Strips markdown code fences and parses JSON object."""
    text = raw_text.strip()
    if text.startswith('```json'):
        text = text[7:]
    elif text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]

    data = json.loads(text.strip())
    if isinstance(data, list) and len(data) > 0:
        data = data[0]
    return data if isinstance(data, dict) else {}


def _extract_botanical_data(data: dict, provider_name: str = 'Botanical Analysis') -> dict:
    """Normalizes both English and Nepali fields from parsed vision JSON."""
    common_name = data.get('common_name') or 'Unknown Plant'
    common_name_ne = data.get('common_name_ne')

    # If common_name has Devanagari in parentheses e.g. "Tomato (गोलभेंडा)"
    if not common_name_ne and '(' in common_name:
        match = re.search(r'\(([\u0900-\u097F\s]+)\)', common_name)
        if match:
            common_name_ne = match.group(1).strip()

    if not common_name_ne:
        common_name_ne = common_name

    tips = data.get('growing_tips', [])
    if isinstance(tips, str):
        tips = [tips]
    elif not isinstance(tips, list):
        tips = []

    tips_ne = data.get('growing_tips_ne', [])
    if isinstance(tips_ne, str):
        tips_ne = [tips_ne]
    elif not isinstance(tips_ne, list):
        tips_ne = []

    # Fertilizer guide
    fertilizer = data.get('fertilizer_guide', [])
    if isinstance(fertilizer, str):
        fertilizer = [fertilizer]
    elif not isinstance(fertilizer, list):
        fertilizer = []

    fertilizer_ne = data.get('fertilizer_guide_ne', [])
    if isinstance(fertilizer_ne, str):
        fertilizer_ne = [fertilizer_ne]
    elif not isinstance(fertilizer_ne, list):
        fertilizer_ne = []

    # Profitability window
    profit = data.get('profitability_window')
    if not isinstance(profit, dict):
        profit = DEFAULT_PROFIT_EN

    profit_ne = data.get('profitability_window_ne')
    if not isinstance(profit_ne, dict):
        profit_ne = DEFAULT_PROFIT_NE

    description = data.get('description') or 'Botanical details and growing guidelines for this crop in Nepal.'
    description_ne = data.get('description_ne') or 'यस बालीको वनस्पति विवरण र नेपाल अनुसार खेती गर्ने व्यावहारिक सल्लाह।'

    planting_season = data.get('planting_season') or 'Spring & Monsoon seasons depending on agro-ecological zone in Nepal.'
    planting_season_ne = data.get('planting_season_ne') or 'नेपालको भूगोल अनुसार वसन्त तथा वर्षा ऋतुमा रोप्न सकिन्छ।'

    growth_duration = data.get('growth_duration') or '75 – 95 days to maturity'
    growth_duration_ne = data.get('growth_duration_ne') or '७५ देखि ९५ दिन (बाली तयार हुने समय)'

    optimal_climate = data.get('optimal_climate') or 'Thrives in warm, sunny weather (20°C–30°C) with fertile, well-draining loamy soil.'
    optimal_climate_ne = data.get('optimal_climate_ne') or '२०°C देखि ३०°C सम्मको न्यानो र घमाइलो मौसममा राम्रो फस्टाउँछ। पानी नजम्ने मलिलो दोमट माटो उपयुक्त हुन्छ।'

    unfavorable_climate = data.get('unfavorable_climate') or 'Sensitive to prolonged frost (<10°C), heavy waterlogging, and extreme scorch heat above 36°C.'
    unfavorable_climate_ne = data.get('unfavorable_climate_ne') or 'तुषारो, १०°C भन्दा बढी चिसो, जरामा पानी जम्ने समस्या र ३६°C भन्दा बढी चर्को खडेरीमा सप्रिन सक्दैन।'

    return {
        'common_name': common_name,
        'common_name_ne': common_name_ne,
        'scientific_name': data.get('scientific_name', 'N/A'),
        'family': data.get('family', 'N/A'),
        'confidence': float(data.get('confidence', 0.90)),
        'crop_keyword': data.get('crop_keyword', common_name),
        'description': description,
        'description_ne': description_ne,
        'planting_season': planting_season,
        'planting_season_ne': planting_season_ne,
        'growth_duration': growth_duration,
        'growth_duration_ne': growth_duration_ne,
        'optimal_climate': optimal_climate,
        'optimal_climate_ne': optimal_climate_ne,
        'unfavorable_climate': unfavorable_climate,
        'unfavorable_climate_ne': unfavorable_climate_ne,
        'fertilizer_guide': fertilizer or DEFAULT_FERTILIZER_EN,
        'fertilizer_guide_ne': fertilizer_ne or DEFAULT_FERTILIZER_NE,
        'profitability_window': profit,
        'profitability_window_ne': profit_ne,
        'growing_tips': tips or DEFAULT_TIPS_EN,
        'growing_tips_ne': tips_ne or DEFAULT_TIPS_NE,
        'is_plant': data.get('is_plant', True),
        'ai_provider': provider_name,
    }


def _identify_with_gemini(image_path: str, api_key: str, model_name: str = 'gemini-3.5-flash-lite') -> dict:
    """Uses Google's official Gemini GenAI SDK to identify the plant."""
    from google import genai
    from google.genai import types

    image_bytes = _prepare_image_bytes(image_path)
    client = genai.Client(api_key=api_key)

    candidate_models = [model_name, 'gemini-3.5-flash-lite', 'gemini-3-flash-preview', 'gemini-3.8-flash']
    seen = set()
    models_to_try = [m for m in candidate_models if not (m in seen or seen.add(m))]

    last_error = None
    for model_id in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
                    BOTANICAL_PROMPT,
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )

            data = _clean_json_response(response.text)
            return _extract_botanical_data(data, provider_name='Botanical Analysis')
        except Exception as e:
            last_error = e
            continue

    raise RuntimeError(f'Identification failed across candidate models: {last_error}')


def _identify_with_groq(image_path: str, api_key: str) -> dict:
    """Fallback vision provider using Groq multimodal API."""
    from groq import Groq

    image_bytes = _prepare_image_bytes(image_path)
    encoded = base64.b64encode(image_bytes).decode('utf-8')
    data_uri = f'data:image/jpeg;base64,{encoded}'

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model='qwen/qwen3.8-27b',
        messages=[
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': BOTANICAL_PROMPT},
                    {'type': 'image_url', 'image_url': {'url': data_uri}},
                ],
            }
        ],
        response_format={'type': 'json_object'},
        temperature=0.2,
        max_tokens=1400,
    )

    data = _clean_json_response(response.choices[0].message.content)
    return _extract_botanical_data(data, provider_name='Botanical Analysis')


def identify_plant(image_path: str) -> dict:
    """Identifies a plant from an image file."""
    gemini_key = (
        current_app.config.get('GEMINI_API_KEY')
        or os.environ.get('GEMINI_API_KEY')
        or os.environ.get('GOOGLE_API_KEY')
    )
    gemini_model = current_app.config.get('GEMINI_MODEL') or 'gemini-3.5-flash-lite'
    groq_key = current_app.config.get('GROQ_API_KEY') or os.environ.get('GROQ_API_KEY')

    if gemini_key:
        try:
            return _identify_with_gemini(image_path, gemini_key, gemini_model)
        except Exception as e:
            current_app.logger.warning(f'Primary identification failed ({e}), attempting fallback...')

    if groq_key:
        try:
            return _identify_with_groq(image_path, groq_key)
        except Exception as e:
            current_app.logger.error(f'Fallback identification failed: {e}')

    return {
        'common_name': 'Plant Specimen',
        'common_name_ne': 'बिरुवाको नमुना',
        'scientific_name': 'Plantae',
        'family': 'N/A',
        'confidence': 0.80,
        'crop_keyword': 'Crop',
        'description': 'Botanical details and growing guidelines for this specimen in Nepal.',
        'description_ne': 'यस वनस्पतिको विवरण र नेपाल अनुसार खेती गर्ने व्यावहारिक सल्लाह।',
        'planting_season': 'Spring & Monsoon seasons depending on agro-ecological zone in Nepal.',
        'planting_season_ne': 'नेपालको भूगोल अनुसार वसन्त तथा वर्षा ऋतुमा रोप्न सकिन्छ।',
        'growth_duration': '75 – 95 days to maturity',
        'growth_duration_ne': '७५ देखि ९५ दिन (बाली तयार हुने समय)',
        'optimal_climate': 'Thrives in warm, sunny weather (20°C–30°C) with fertile, well-draining loamy soil.',
        'optimal_climate_ne': '२०°C देखि ३०°C सम्मको न्यानो र घमाइलो मौसममा राम्रो फस्टाउँछ। पानी नजम्ने मलिलो दोमट माटो उपयुक्त हुन्छ।',
        'unfavorable_climate': 'Sensitive to prolonged frost (<10°C), heavy waterlogging, and extreme scorch heat above 36°C.',
        'unfavorable_climate_ne': 'तुषारो, १०°C भन्दा बढी चिसो, जरामा पानी जम्ने समस्या र ३६°C भन्दा बढी चर्को खडेरीमा सप्रिन सक्दैन।',
        'fertilizer_guide': DEFAULT_FERTILIZER_EN,
        'fertilizer_guide_ne': DEFAULT_FERTILIZER_NE,
        'profitability_window': DEFAULT_PROFIT_EN,
        'profitability_window_ne': DEFAULT_PROFIT_NE,
        'growing_tips': DEFAULT_TIPS_EN,
        'growing_tips_ne': DEFAULT_TIPS_NE,
        'is_plant': True,
        'ai_provider': 'Standard Catalog',
    }
