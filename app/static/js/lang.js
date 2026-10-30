// AgriVision Nepal - Client-side Bilingual (English / Nepali) Translation Engine
(function () {
  const STORAGE_KEY = 'agrivision-lang';

  const TRANSLATIONS = {
    en: {
      brand: "AgriVision Nepal",
      nav_home: "Home",
      nav_scan: "Identify Crop",
      nav_records: "Records",
      theme_dark: "Dark",
      theme_light: "Light",
      lang_btn: "नेपाली",
      home_translate_btn: "नेपालीमा हेर्नुहोस् (Translate to Nepali)",

      home_title: "AgriVision Nepal",
      home_subtitle: "Identify field crops, garden vegetables, and fruit plants from a photograph, and check today's wholesale rates from Kalimati and regional markets.",
      btn_open_cam: "Open Camera",
      btn_upload_photo: "Upload Photo",

      // Home Introduction & Guide
      home_about_title: "About AgriVision Nepal",
      home_about_p1: "AgriVision Nepal is an agricultural intelligence platform crafted specifically for farmers, growers, agronomists, and home gardeners across Nepal. By connecting plant visual recognition with Kalimati wholesale market data and Nepal-specific agronomic research, AgriVision bridges the gap between field observation and market economics.",
      home_about_p2: "Whether you are cultivating crops in the fertile Terai plains, mid-hill terraces, or river valleys, AgriVision helps you verify crop varieties, plan planting calendars, apply balanced fertilizers, protect against climate risks, and determine the most profitable seasons to harvest and sell.",
      how_to_use_title: "How to Use AgriVision (4 Easy Steps)",
      step1_title: "1. Capture or Upload a Photo",
      step1_desc: "Tap 'Open Camera' to take a live photo in your field or garden, or use 'Upload Photo' to select an image from your phone or computer. Ensure leaves, flowers, or fruit are clearly visible in natural daylight.",
      step2_title: "2. Instant Crop Identification",
      step2_desc: "Instantly discover the crop's local Nepali name (e.g. गोलभेंडा, फर्सी, काउली), standard English common name, scientific Latin classification, and botanical family.",
      step3_title: "3. Agronomy, Fertilizer & Climate Guide",
      step3_desc: "Check when to plant in Nepal (Falgun–Chaitra vs. Jestha–Ashadh), days to maturity, favorable temperatures, risk warnings (frost, waterlogging), and a step-by-step fertilizer plan (FYM, DAP, Potash, Urea).",
      step4_title: "4. Market Rates & Selling Strategy",
      step4_desc: "Review today's wholesale benchmark price from Kalimati Wholesale Market, Kathmandu. Discover peak profit months, off-season tunnel advantages, and storage advice to sell at highest rates.",

      features_section_title: "Core Features & Capabilities",
      feat1_title: "Crop Identification",
      feat1_desc: "Accurate visual identification of field crops, vegetables, fruits, and leafy greens across Nepal.",
      feat2_title: "Kalimati Wholesale Rates",
      feat2_desc: "Daily benchmark wholesale pricing (Min, Max, Average per kg) from Kathmandu's central market.",
      feat3_title: "Planting & Harvest Calendar",
      feat3_desc: "Seasonal timelines tailored for Terai, Valleys, and Mid-Hills (spring and monsoon seasons).",
      feat4_title: "Balanced Fertilizer Guide",
      feat4_desc: "Clear dosages for Farmyard Manure (FYM), DAP, Potash base application, and Urea top-dressing.",
      feat5_title: "Climate & Risk Warnings",
      feat5_desc: "Optimal growing temperatures (20°C–30°C) versus cold frost, waterlogging, and blight hazards.",
      feat6_title: "Market Timing & Profit Outlook",
      feat6_desc: "Insights into peak price months, festival demand windows, and off-season storage advantages.",

      tips_section_title: "Tips for Accurate Results",
      tip1_text: "Take photos in bright, natural daylight rather than in dim indoor light.",
      tip2_text: "Get close to distinctive plant parts like leaves, flowers, or fruit rather than a distant panorama.",
      tip3_text: "Switch anytime between English and Nepali using the toggle button in the top banner or navbar.",
      tip4_text: "Revisit your previous scans and price history anytime from the 'Records' page.",
      btn_get_started: "Start Identifying a Crop",

      how_it_works: "How it works",

      scan_title: "Identify Crop",
      scan_subtitle: "Take a photograph using your device camera or upload an image file.",
      tab_cam: "Camera",
      tab_upload: "Upload File",
      cam_error_title: "Camera access unavailable",
      cam_error_desc: "Allow camera permissions in browser settings or use file upload.",
      btn_switch_upload: "Switch to File Upload",
      drop_title: "Select or drop photo here",
      drop_desc: "Click to browse image files from your computer or phone",
      review_title: "Review photograph",
      btn_retake: "Retake",
      btn_submit_crop: "Identify & View Price",
      loading_title: "Processing photograph",
      loading_desc: "Matching botanical features and looking up market rates...",
      alert_take_photo_first: "Please take or upload an image first.",
      upload_failed_msg: "An error occurred while uploading. Please check connection and try again.",
      identify_failed_msg: "Could not identify this image. Please try again with a clearer photo.",

      back_to_scan: "← Identify another crop",
      match_label: "Match:",
      family_label: "Family:",
      recorded_date: "Recorded:",
      market_today_title: "Today's Wholesale Price (Nepal)",
      min_rate: "Min",
      max_rate: "Max",
      no_market_data_title: "Wholesale Market Rates",
      no_market_data_desc: "No commercial wholesale commodity trading data is recorded for this plant species.",
      crop_summary_title: "Crop Summary",
      agronomy_guide_title: "Cultivation & Agronomy Guide",
      quick_specs_title: "Key Farming Specifications",
      planting_season_label: "When to Grow",
      growth_duration_label: "Time to Harvest",
      climate_suitability_label: "Optimal Climate",
      profit_potential_label: "Profit Window",
      climate_guide_title: "Climate & Environmental Suitability",
      optimal_climate_title: "Favorable Climate (Where it grows properly)",
      unfavorable_climate_title: "Unfavorable Climate & Risk Factors (Where it fails)",
      fertilizer_guide_title: "Fertilizer & Soil Nutrition Guide",
      profitability_title: "Market Profitability & When to Sell",
      peak_profit_label: "Peak Wholesale Price Season:",
      off_season_label: "Off-Season Advantage:",
      selling_strategy_label: "Selling & Storage Strategy:",
      btn_identify_another: "Identify Another Crop",
      btn_view_records: "View All Records",
      unidentified_specimen: "Unidentified Specimen",
      empty_results_title: "No crop recorded yet",
      empty_results_desc: "Photograph or upload an image to view botanical details and Kalimati market prices.",
      btn_start_identifying: "Identify a Crop",

      records_title: "Crop Records",
      records_subtitle: "Previous crop identifications and Kalimati wholesale price snapshots.",
      btn_new_record: "+ New Record",
      btn_clear_all: "Clear all",
      clear_confirm: "Clear all recorded scans?",
      empty_records_title: "No records yet",
      empty_records_desc: "Take a photo or upload an image to create your first crop record."
    },
    ne: {
      brand: "एग्रिभिजन नेपाल",
      nav_home: "गृहपृष्ठ",
      nav_scan: "बाली पहिचान",
      nav_records: "अभिलेखहरू",
      theme_dark: "गाढा",
      theme_light: "उज्यालो",
      lang_btn: "English",
      home_translate_btn: "View in English (अंग्रेजीमा हेर्नुहोस्)",

      home_title: "एग्रिभिजन नेपाल",
      home_subtitle: "कुनै पनि बाली, तरकारी वा फलफूलको तस्विर खिचेर बिरुवा पहिचान गर्नुहोस् र कालिमाटी तथा स्थानीय थोक बजारको आजको दरभाउ हेर्नुहोस्।",
      btn_open_cam: "क्यामेरा खोल्नुहोस्",
      btn_upload_photo: "तस्विर अपलोड गर्नुहोस्",

      // Home Introduction & Guide
      home_about_title: "एग्रिभिजन नेपालको परिचय",
      home_about_p1: "एग्रिभिजन नेपाल नेपाली कृषक, कृषि प्राविधिक, विद्यार्थी तथा करेसाबारीका लागि तयार पारिएको एक भरपर्दो डिजिटल कृषि सहयोगी हो। यसले बिरुवा पहिचान, कालिमाटी थोक बजारको दरभाउ र नेपालको हावापानी सुहाउँदो प्राविधिक सल्लाहलाई एकै ठाउँमा उपलब्ध गराउँछ।",
      home_about_p2: "तराईको समथर फाँटदेखि मध्य पहाड र उपत्यकाका किसानहरूले बालीको नाम पहिचान गर्न, रोप्ने सही समय र मलखादको मात्रा बुझ्न, मौसम अनुसारको जोखिमबाट जोगिन र बढी नाफा हुने समयमा उत्पादन बेच्न यो उपयोगी छ।",
      how_to_use_title: "वेबसाइट कसरी प्रयोग गर्ने (४ सजिला चरणहरू)",
      step1_title: "१. बालीको तस्विर खिच्नुहोस् वा अपलोड गर्नुहोस्",
      step1_desc: "आफ्नो बारी वा खेतमा क्यामेरा खोलेर स्पष्ट तस्विर खिच्नुहोस् वा फोन/कम्प्युटरबाट फोटो अपलोड गर्नुहोस्। पात, फूल वा फल प्रस्ट देखिने गरी उज्यालोमा फोटो लिनुहोस्।",
      step2_title: "२. बिरुवा पहिचान र जात सम्बन्धी विवरण",
      step2_desc: "बालीको नेपाली नाम (उदा. गोलभेंडा, फर्सी, काउली), अंग्रेजी नाम, वैज्ञानिक वर्गीकरण र वनस्पति परिवार सम्बन्धी जानकारी तुरुन्त प्राप्त गर्नुहोस्।",
      step3_title: "३. खेती विधि, मलखाद र हावापानी सल्लाह",
      step3_desc: "नेपालको भूगोल अनुसार रोप्ने महिना, बाली पाक्ने दिन, गोबर तथा रासायनिक मलको मात्रा, र तुषारो वा पानी जम्ने जस्ता प्रतिकूल हावापानीका जोखिमहरू बुझ्नुहोस्।",
      step4_title: "४. बजार मूल्य र बढी नाफामा बेच्ने सल्लाह",
      step4_desc: "कालिमाटी फलफूल तथा तरकारी बजारको आजको थोक मूल्य हेर्नुहोस् र कुन महिनामा बढी भाउ पाइन्छ तथा कसरी बेच्दा अधिकतम फाइदा हुन्छ भन्ने रणनीति थाहा पाउनुहोस्।",

      features_section_title: "मुख्य सुविधाहरू र क्षमताहरू",
      feat1_title: "बाली तथा बिरुवा पहिचान",
      feat1_desc: "नेपालमा खेती गरिने तरकारी, फलफूल, खाद्यान्न र नगदे बालीहरूको द्रुत पहिचान।",
      feat2_title: "कालिमाटी थोक बजार दरभाउ",
      feat2_desc: "काठमाडौंको कालिमाटी बजारको दैनिक थोक न्यूनतम, अधिकतम र औसत दरभाउ प्रति के.जी.।",
      feat3_title: "रोप्ने र भित्र्याउने क्यालेन्डर",
      feat3_desc: "नेपालको तराई, उपत्यका र पहाड अनुसार रोप्ने र बाली भित्र्याउने उपयुक्त तालिका।",
      feat4_title: "सन्तुलित मलखाद तालिका",
      feat4_desc: "गोबर मल, डीएपी र पोटासको आधार मल तथा युरिया टप-ड्रेसिङको व्यावहारिक मात्रा।",
      feat5_title: "हावापानी र जोखिम चेतावनी",
      feat5_desc: "फस्टाउने उपयुक्त तापक्रम तथा तुषारो, पानी जम्ने समस्या र रोगको जोखिमबारे जानकारी।",
      feat6_title: "बजार अवसर र नाफा विश्लेषण",
      feat6_desc: "सबैभन्दा बढी भाउ पाइने महिना, चाडपर्वको माग र बेमौसमी भण्डारण फाइदाको विश्लेषण।",

      tips_section_title: "उत्तम नतिजाका लागि उपयोगी सुझावहरू",
      tip1_text: "मधुरो कोठाभन्दा बाहिर घाम वा उज्यालो प्राकृतिक प्रकाशमा फोटो खिच्नुहोस्।",
      tip2_text: "टाढाबाट पूरै खेतको फोटो लिनुभन्दा पात, फल वा फूल नजिकबाट प्रस्ट देखिने गरी खिच्नुहोस्।",
      tip3_text: "वेबसाइटको भाषा जुनसुकै बेला एक क्लिकमै अंग्रेजी वा नेपालीमा बदल्न सक्नुहुन्छ।",
      tip4_text: "पहिले पहिचान गरिएका बाली र मूल्यको अभिलेख 'अभिलेखहरू' मेनुमा हेर्न सक्नुहुन्छ।",
      btn_get_started: "बाली पहिचान सुरु गर्नुहोस्",

      how_it_works: "कसरी प्रयोग गर्ने",

      scan_title: "बाली पहिचान",
      scan_subtitle: "आफ्नो क्यामेराबाट तस्विर खिच्नुहोस् वा फाइल अपलोड गर्नुहोस्।",
      tab_cam: "क्यामेरा",
      tab_upload: "फाइल अपलोड",
      cam_error_title: "क्यामेरा उपलब्ध भएन",
      cam_error_desc: "कृपया ब्राउजरमा क्यामेरा अनुमति दिनुहोस् वा फाइल अपलोड प्रयोग गर्नुहोस्।",
      btn_switch_upload: "फाइल अपलोडमा जानुहोस्",
      drop_title: "यहाँ तस्विर छान्नुहोस् वा तान्नुहोस्",
      drop_desc: "कम्प्युटर वा मोबाइलबाट फोटो छान्नुहोस्",
      review_title: "तस्विर जाँच गर्नुहोस्",
      btn_retake: "पुनः खिच्नुहोस्",
      btn_submit_crop: "पहिचान र दरभाउ हेर्नुहोस्",
      loading_title: "तस्विर प्रशोधन हुँदैछ...",
      loading_desc: "बालीको पहिचान र कालिमाटी बजार दर खोजिँदैछ...",
      alert_take_photo_first: "कृपया पहिले तस्विर लिनुहोस् वा अपलोड गर्नुहोस्।",
      upload_failed_msg: "तस्विर पठाउँदा समस्या भयो। कृपया इन्टरनेट जाँचेर पुनः प्रयास गर्नुहोस्।",
      identify_failed_msg: "यस तस्विरबाट बाली पहिचान हुन सकेन। कृपया अझ स्पष्ट तस्विर लिएर प्रयास गर्नुहोस्।",

      back_to_scan: "← अर्को बाली पहिचान गर्नुहोस्",
      match_label: "सटीकता:",
      family_label: "वनस्पति परिवार:",
      recorded_date: "अभिलेख मिति:",
      market_today_title: "आजको थोक बजार मूल्य (नेपाल)",
      min_rate: "न्यूनतम",
      max_rate: "अधिकतम",
      no_market_data_title: "थोक बजार दरभाउ",
      no_market_data_desc: "यस वनस्पतिको व्यावसायिक थोक कारोबार दर उपलब्ध छैन।",
      crop_summary_title: "बाली सम्बन्धी जानकारी",
      agronomy_guide_title: "खेती तथा बाली व्यवस्थापन सल्लाह",
      quick_specs_title: "प्रमुख कृषि विवरण",
      planting_season_label: "रोप्ने उपयुक्त समय",
      growth_duration_label: "बाली तयार हुने समय",
      climate_suitability_label: "उपयुक्त हावापानी",
      profit_potential_label: "नाफा सम्भावना",
      climate_guide_title: "हावापानी र वातावरणीय अनुकूलता",
      optimal_climate_title: "उपयुक्त हावापानी (राम्रोसँग फस्टाउने अवस्था)",
      unfavorable_climate_title: "प्रतिकूल अवस्था र जोखिम (सप्रिन नसक्ने हावापानी)",
      fertilizer_guide_title: "मलखाद तथा माटो पोषण तालिका",
      profitability_title: "बजार नाफा र कहिले बेच्ने सल्लाह",
      peak_profit_label: "उच्च थोक मूल्य पाउने महिना:",
      off_season_label: "बेमौसमी खेतीको फाइदा:",
      selling_strategy_label: "बिक्री तथा भण्डारण रणनीति:",
      btn_identify_another: "अर्को बाली पहिचान गर्नुहोस्",
      btn_view_records: "सबै अभिलेख हेर्नुहोस्",
      unidentified_specimen: "पहिचान हुन नसकेको नमुना",
      empty_results_title: "कुनै बाली रेकर्ड गरिएको छैन",
      empty_results_desc: "बालीको विवरण र कालिमाटी बजार मूल्य हेर्न तस्विर लिनुहोस् वा अपलोड गर्नुहोस्।",
      btn_start_identifying: "बाली पहिचान गर्नुहोस्",

      records_title: "बाली अभिलेखहरू",
      records_subtitle: "पहिले पहिचान गरिएका बाली र कालिमाटी बजार दरको सूची।",
      btn_new_record: "+ नयाँ पहिचान",
      btn_clear_all: "सबै हटाउनुहोस्",
      clear_confirm: "के तपाईं सबै रेकर्ड मेटाउन चाहनुहुन्छ?",
      empty_records_title: "कुनै रेकर्ड छैन",
      empty_records_desc: "पहिलो रेकर्ड राख्न तस्विर लिनुहोस् वा अपलोड गर्नुहोस्।"
    }
  };

  function getCurrentLang() {
    return localStorage.getItem(STORAGE_KEY) || 'en';
  }

  function applyLanguage(lang) {
    if (!TRANSLATIONS[lang]) lang = 'en';

    document.documentElement.setAttribute('lang', lang === 'ne' ? 'ne' : 'en');
    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {}

    const dict = TRANSLATIONS[lang];

    // Update all elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (dict[key]) {
        el.textContent = dict[key];
      }
    });

    // Update dynamic bilingual text attributes if present
    document.querySelectorAll('[data-lang-en]').forEach(el => {
      const text = lang === 'ne' ? el.getAttribute('data-lang-ne') : el.getAttribute('data-lang-en');
      if (text) el.textContent = text;
    });

    // Update navbar language button text
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.textContent = dict.lang_btn;
      btn.setAttribute('title', lang === 'ne' ? 'Switch to English' : 'नेपालीमा हेर्नुहोस्');
    });

    // Update home translation button if present
    const homeBtnLabel = document.getElementById('home-lang-label');
    if (homeBtnLabel) {
      homeBtnLabel.textContent = dict.home_translate_btn;
    }
  }

  window.toggleAppLanguage = function () {
    const next = getCurrentLang() === 'ne' ? 'en' : 'ne';
    applyLanguage(next);
  };

  window.setAppLanguage = function (lang) {
    applyLanguage(lang);
  };

  // Expose dictionary for dynamic scripts
  window.getI18nText = function (key) {
    const lang = getCurrentLang();
    return (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) || TRANSLATIONS.en[key] || '';
  };

  document.addEventListener('DOMContentLoaded', () => {
    applyLanguage(getCurrentLang());
  });
})();

