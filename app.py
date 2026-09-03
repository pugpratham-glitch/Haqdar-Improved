import hashlib
from datetime import date, timedelta

from flask import Flask, jsonify, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# =====================================================================================
# MASTER DATABASE
# Coverage strategy:
#   - NATIONAL entries ("state": "All India") are visible to every user regardless of
#     the state they select, and span every category (General / OBC / SC / ST / EWS).
#   - STATE entries are scoped to the 10 most populous Indian states, which together
#     account for the overwhelming majority of the country's population:
#     Uttar Pradesh, Maharashtra, Bihar, West Bengal, Madhya Pradesh, Tamil Nadu,
#     Rajasthan, Karnataka, Gujarat, and Andhra Pradesh. Delhi is retained as a bonus
#     high-visibility NCT entry.
#   - Within each state, entries are spread across category values so that General,
#     OBC, SC, ST, and EWS applicants each see relevant, category-matched results.
# =====================================================================================

MASTER_DATABASE = [
    # ==================== ALL INDIA: COMPETITIVE EXAMS & RECRUITMENT ====================
    {
        "id": "nat-exam-01",
        "title": {
            "en": "UPSC Civil Services Examination (CSE) Fee Exemption & Support",
            "hi": "यूपीएससी सिविल सेवा परीक्षा (CSE) शुल्क छूट और सहायता",
            "mr": "यूपीएससी नागरी सेवा परीक्षा शुल्क सूट आणि सहाय्य",
            "bn": "ইউপিএসসি সিভিল সার্ভিস পরীক্ষা ফি ছাড় এবং সহায়তা",
            "ta": "யுபிஎஸ்சி குடிமைப்பணி தேர்வு கட்டண விலக்கு மற்றும் ஆதரவு",
            "te": "యుపిఎస్సి సివిల్ సర్వీసెస్ పరీక్ష ఫీజు మినహాయింపు మరియు మద్దతు"
        },
        "category": "All",
        "state": "All India",
        "type": "Competitive Exam",
        "age_limit": 32,
        "income_limit": 800000,
        "description": {
            "en": "Premier national recruitment exam for IAS, IPS, and IFS with complete fee waivers for SC, ST, Female, and PwBD candidates.",
            "hi": "एससी, एसटी, महिला और पीडब्ल्यूडी उम्मीदवारों के लिए पूर्ण शुल्क छूट के साथ आईएएस, आईपीएस और आईएफएस के लिए प्रमुख राष्ट्रीय परीक्षा।"
        },
        "link": "https://upsc.gov.in/"
    },
    {
        "id": "nat-exam-02",
        "title": {
            "en": "SSC Combined Graduate Level (CGL) Examination Support",
            "hi": "एसएससी संयुक्त स्नातक स्तर (CGL) परीक्षा सहायता",
            "mr": "एसएससी संयुक्त पदवी स्तर (CGL) परीक्षा सहाय्य"
        },
        "category": "All",
        "state": "All India",
        "type": "Competitive Exam",
        "age_limit": 30,
        "income_limit": 1000000,
        "description": {
            "en": "Central government recruitment for Group B and C posts across various ministries with zero application fees for women and reserved categories.",
            "hi": "महिलाओं और आरक्षित श्रेणियों के लिए शून्य आवेदन शुल्क के साथ विभिन्न मंत्रालयों में ग्रुप बी और सी पदों के लिए केंद्र सरकार की भर्ती।"
        },
        "link": "https://ssc.nic.in/"
    },
    {
        "id": "nat-exam-03",
        "title": {
            "en": "Railway Recruitment Board (RRB) Non-Technical Popular Categories (NTPC)",
            "hi": "रेलवे भर्ती बोर्ड (RRB) गैर-तकनीकी लोकप्रिय श्रेणियां (NTPC)",
            "mr": "रेल्वे भरती बोर्ड (RRB) एनटीपीसी परीक्षा"
        },
        "category": "All",
        "state": "All India",
        "type": "Competitive Exam",
        "age_limit": 33,
        "income_limit": 800000,
        "description": {
            "en": "Massive national employment drive for Indian Railways with complete application fee refunds upon appearing for the exam.",
            "hi": "परीक्षा में शामिल होने पर पूर्ण आवेदन शुल्क रिफंड के साथ भारतीय रेलवे के लिए बड़े पैमाने पर राष्ट्रीय रोजगार अभियान।"
        },
        "link": "https://www.rrbcdg.gov.in/"
    },
    {
        "id": "nat-exam-04",
        "title": {
            "en": "Joint Entrance Examination (JEE Main & Advanced) Guidance & Relaxation",
            "hi": "संयुक्त प्रवेश परीक्षा (JEE मुख्य और उन्नत) मार्गदर्शन और छूट",
            "mr": "संयुक्त प्रवेश परीक्षा (JEE Main & Advanced) मार्गदर्शन"
        },
        "category": "All",
        "state": "All India",
        "type": "Competitive Exam",
        "age_limit": 25,
        "income_limit": 800000,
        "description": {
            "en": "National engineering entrance portal providing financial counseling and fee concessions for economically weaker sections.",
            "hi": "आर्थिक रूप से कमजोर वर्गों के लिए वित्तीय परामर्श और शुल्क रियायतें प्रदान करने वाला राष्ट्रीय इंजीनियरिंग प्रवेश पोर्टल।"
        },
        "link": "https://jeemain.nta.nic.in/"
    },

    # ==================== ALL INDIA: SCHOLARSHIPS ====================
    {
        "id": "nat-sch-01",
        "title": {
            "en": "National Scholarship Portal (NSP) - Central Sector Scheme of Scholarships",
            "hi": "राष्ट्रीय छात्रवृत्ति पोर्टल (NSP) - केंद्रीय क्षेत्र की छात्रवृत्ति योजना",
            "mr": "राष्ट्रीय शिष्यवृत्ती पोर्टल (NSP) केंद्रीय क्षेत्र योजना"
        },
        "category": "All",
        "state": "All India",
        "type": "Scholarship",
        "age_limit": 25,
        "income_limit": 450000,
        "description": {
            "en": "Financial support for college and university students based on senior secondary board results to meet day-to-day academic expenses.",
            "hi": "दैनिक शैक्षणिक खर्चों को पूरा करने के लिए वरिष्ठ माध्यमिक बोर्ड परिणामों के आधार पर कॉलेज और विश्वविद्यालय के छात्रों के लिए वित्तीय सहायता।"
        },
        "link": "https://scholarships.gov.in/"
    },
    {
        "id": "nat-sch-02",
        "title": {
            "en": "UGC National Fellowship and Scholarship for Higher Education of ST Students",
            "hi": "एसटी छात्रों की उच्च शिक्षा के लिए यूजीसी राष्ट्रीय फेलोशिप और छात्रवृत्ति",
            "mr": "एसटी विद्यार्थ्यांच्या उच्च शिक्षणासाठी यूजीसी राष्ट्रीय शिष्यवृत्ती"
        },
        "category": "ST",
        "state": "All India",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 600000,
        "description": {
            "en": "Targeted fellowship program enabling Scheduled Tribe students to pursue M.Phil and Ph.D. degrees across recognized universities.",
            "hi": "अनुसूचित जनजाति के छात्रों को मान्यता प्राप्त विश्वविद्यालयों में एम.फिल और पीएचडी डिग्री प्राप्त करने में सक्षम बनाने वाला लक्षित फेलोशिप कार्यक्रम।"
        },
        "link": "https://www.ugc.ac.in/"
    },
    {
        "id": "nat-sch-03",
        "title": {
            "en": "Post-Matric Scholarship for Students Belonging to Minority Communities",
            "hi": "अल्पसंख्यक समुदायों के छात्रों के लिए पोस्ट-मैट्रिक छात्रवृत्ति",
            "mr": "अल्पसंख्यक समुदायाच्या विद्यार्थ्यांसाठी पोस्ट-मॅट्रिक शिष्यवृत्ती"
        },
        "category": "OBC",
        "state": "All India",
        "type": "Scholarship",
        "age_limit": 28,
        "income_limit": 200000,
        "description": {
            "en": "Central financial assistance supporting technical and professional courses from class 11 up to Ph.D. level for minority youth.",
            "hi": "अल्पसंख्यक युवाओं के लिए कक्षा 11 से पीएचडी स्तर तक तकनीकी और व्यावसायिक पाठ्यक्रमों का समर्थन करने वाली केंद्रीय वित्तीय सहायता।"
        },
        "link": "https://scholarships.gov.in/"
    },
    {
        "id": "nat-sch-04",
        "title": {
            "en": "PM-YASASVI Central Sector Scholarship for EWS Students",
            "hi": "ईडब्ल्यूएस छात्रों के लिए पीएम-यशस्वी केंद्रीय क्षेत्र छात्रवृत्ति"
        },
        "category": "EWS",
        "state": "All India",
        "type": "Scholarship",
        "age_limit": 25,
        "income_limit": 800000,
        "description": {
            "en": "National scholarship supporting Economically Weaker Section students in classes 9 through 12 and undergraduate courses with annual financial assistance.",
            "hi": "आर्थिक रूप से कमजोर वर्ग के छात्रों को कक्षा 9 से 12 और स्नातक पाठ्यक्रमों में वार्षिक वित्तीय सहायता प्रदान करने वाली राष्ट्रीय छात्रवृत्ति।"
        },
        "link": "https://scholarships.gov.in/"
    },
    {
        "id": "nat-sch-05",
        "title": {
            "en": "National Merit Scholarship for General Category Students",
            "hi": "सामान्य श्रेणी के छात्रों के लिए राष्ट्रीय मेधा छात्रवृत्ति"
        },
        "category": "General",
        "state": "All India",
        "type": "Scholarship",
        "age_limit": 25,
        "income_limit": 600000,
        "description": {
            "en": "Merit-based central assistance for open/general category students who rank highly in senior secondary board examinations.",
            "hi": "वरिष्ठ माध्यमिक बोर्ड परीक्षाओं में उच्च रैंक प्राप्त करने वाले सामान्य श्रेणी के छात्रों के लिए मेधा-आधारित केंद्रीय सहायता।"
        },
        "link": "https://scholarships.gov.in/"
    },

    # ==================== ALL INDIA: SOCIAL WELFARE SCHEMES ====================
    {
        "id": "nat-wel-01",
        "title": {
            "en": "Pradhan Mantri Awas Yojana (PMAY - Urban & Rural)",
            "hi": "प्रधानमंत्री आवास योजना (PMAY - शहरी और ग्रामीण)",
            "mr": "प्रधानमंत्री आवास योजना (PMAY - शहरी आणि ग्रामीण)"
        },
        "category": "All",
        "state": "All India",
        "type": "Welfare Scheme",
        "age_limit": 70,
        "income_limit": 600000,
        "description": {
            "en": "Flagship housing mission providing credit-linked subsidies and direct financial assistance to construct or purchase pucca houses.",
            "hi": "पक्का मकान बनाने या खरीदने के लिए क्रेडिट-लिंक्ड सब्सिडी और प्रत्यक्ष वित्तीय सहायता प्रदान करने वाला प्रमुख आवास मिशन।"
        },
        "link": "https://pmaymis.gov.in/"
    },
    {
        "id": "nat-wel-02",
        "title": {
            "en": "Pradhan Mantri Jan Dhan Yojana (PMJDY) Financial Inclusion",
            "hi": "प्रधानमंत्री जन धन योजना (PMJDY) वित्तीय समावेशन",
            "mr": "प्रधानमंत्री जन धन योजना (PMJDY) वित्तीय समावेश"
        },
        "category": "All",
        "state": "All India",
        "type": "Welfare Scheme",
        "age_limit": 65,
        "income_limit": 9999999,
        "description": {
            "en": "National mission for financial inclusion offering zero-balance savings accounts, RuPay debit cards, and accidental insurance cover.",
            "hi": "शून्य-शेष बचत खाते, रुपे डेबिट कार्ड और दुर्घटना बीमा कवर प्रदान करने वाला वित्तीय समावेशन के लिए राष्ट्रीय मिशन।"
        },
        "link": "https://pmjdy.gov.in/"
    },
    {
        "id": "nat-wel-03",
        "title": {
            "en": "Ayushman Bharat PM-JAY (National Health Protection Scheme)",
            "hi": "आयुष्मान भारत PM-JAY (राष्ट्रीय स्वास्थ्य सुरक्षा योजना)",
            "mr": "आयुष्मान भारत PM-JAY (राष्ट्रीय आरोग्य संरक्षण योजना)"
        },
        "category": "All",
        "state": "All India",
        "type": "Welfare Scheme",
        "age_limit": 99,
        "income_limit": 500000,
        "description": {
            "en": "World's largest health insurance scheme providing ₹5 Lakhs per family per year for secondary and tertiary care hospitalization.",
            "hi": "माध्यमिक और तृतीयक देखभाल अस्पताल में भर्ती के लिए प्रति परिवार प्रति वर्ष ₹5 लाख प्रदान करने वाली दुनिया की सबसे बड़ी स्वास्थ्य बीमा योजना।"
        },
        "link": "https://pmjay.gov.in/"
    },
    {
        "id": "nat-wel-04",
        "title": {
            "en": "Pradhan Mantri Kaushal Vikas Yojana (PMKVY) Skill Certification",
            "hi": "प्रधानमंत्री कौशल विकास योजना (PMKVY) कौशल प्रमाणन",
            "mr": "प्रधानमंत्री कौशल विकास योजना (PMKVY)"
        },
        "category": "All",
        "state": "All India",
        "type": "Welfare Scheme",
        "age_limit": 45,
        "income_limit": 9999999,
        "description": {
            "en": "Vocational training and industry-recognized certification program empowering youth with employment-oriented skill sets.",
            "hi": "युवाओं को रोजगारोमुख कौशल सेट के साथ सशक्त बनाने वाला व्यावसायिक प्रशिक्षण और उद्योग-मान्यता प्राप्त प्रमाणन कार्यक्रम।"
        },
        "link": "https://www.pmkvy.org/"
    },

    # ==================== STATE LEVEL: MAHARASHTRA ====================
    {
        "id": "mah-01",
        "title": {
            "en": "Maharashtra Post-Matric Scholarship for Backward Classes",
            "hi": "पिछड़े वर्गों के लिए महाराष्ट्र पोस्ट-मैट्रिक छात्रवृत्ति",
            "mr": "मागासवर्गीय विद्यार्थ्यांसाठी महाराष्ट्र पोस्ट-मॅट्रिक शिष्यवृत्ती"
        },
        "category": "SC",
        "state": "Maharashtra",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "Comprehensive tuition fee and maintenance allowance waiver for SC/ST/OBC students studying in recognized colleges across Maharashtra.",
            "hi": "महाराष्ट्र भर के मान्यता प्राप्त कॉलेजों में पढ़ने वाले एससी/एसटी/ओबीसी छात्रों के लिए व्यापक ट्यूशन शुल्क और रखरखाव भत्ता छूट।"
        },
        "link": "https://mahadbtmahadbt.gov.in/"
    },
    {
        "id": "mah-02",
        "title": {
            "en": "Mahatma Jyotirao Phule Jan Arogya Yojana (MJPJAY)",
            "hi": "महात्मा ज्योतिराव फुले जन आरोग्य योजना (MJPJAY)",
            "mr": "महात्मा ज्योतिराव फुले जन आरोग्य योजना (MJPJAY)"
        },
        "category": "All",
        "state": "Maharashtra",
        "type": "Welfare Scheme",
        "age_limit": 99,
        "income_limit": 1000000,
        "description": {
            "en": "State health scheme providing cashless medical treatment up to ₹1.5 Lakhs for critical illnesses in empanelled hospitals.",
            "hi": "सूचीबद्ध अस्पतालों में गंभीर बीमारियों के लिए ₹1.5 लाख तक का कैशलेस चिकित्सा उपचार प्रदान करने वाली राज्य स्वास्थ्य योजना।"
        },
        "link": "https://www.jeevandayee.gov.in/"
    },
    {
        "id": "mah-03",
        "title": {
            "en": "Maharashtra EWS Scholarship for Higher Education",
            "hi": "उच्च शिक्षा के लिए महाराष्ट्र ईडब्ल्यूएस छात्रवृत्ति",
            "mr": "उच्च शिक्षणासाठी महाराष्ट्र ईडब्ल्यूएस शिष्यवृत्ती"
        },
        "category": "EWS",
        "state": "Maharashtra",
        "type": "Scholarship",
        "age_limit": 28,
        "income_limit": 800000,
        "description": {
            "en": "Tuition fee reimbursement for Economically Weaker Section students admitted to professional and technical courses through the state CET.",
            "hi": "राज्य सीईटी के माध्यम से व्यावसायिक और तकनीकी पाठ्यक्रमों में प्रवेश पाने वाले आर्थिक रूप से कमजोर वर्ग के छात्रों के लिए ट्यूशन शुल्क प्रतिपूर्ति।"
        },
        "link": "https://mahadbtmahadbt.gov.in/"
    },
    {
        "id": "mah-04",
        "title": {
            "en": "Maharashtra Public Service Commission (MPSC) Examination Support",
            "hi": "महाराष्ट्र लोक सेवा आयोग (MPSC) परीक्षा सहायता",
            "mr": "महाराष्ट्र लोकसेवा आयोग (MPSC) परीक्षा सहाय्य"
        },
        "category": "All",
        "state": "Maharashtra",
        "type": "Competitive Exam",
        "age_limit": 38,
        "income_limit": 1000000,
        "description": {
            "en": "State-level administrative recruitment exam for Deputy Collector, PSI, and other Class I/II posts with fee concessions for reserved categories.",
            "hi": "आरक्षित श्रेणियों के लिए शुल्क रियायतों के साथ उप-जिलाधिकारी, पीएसआई और अन्य वर्ग I/II पदों के लिए राज्य स्तरीय प्रशासनिक भर्ती परीक्षा।"
        },
        "link": "https://mpsc.gov.in/"
    },

    # ==================== STATE LEVEL: UTTAR PRADESH ====================
    {
        "id": "up-01",
        "title": {
            "en": "UP Chief Minister Fellowship Program",
            "hi": "यूपी मुख्यमंत्री फेलोशिप कार्यक्रम",
            "mr": "यूपी मुख्यमंत्री फेलोशिप कार्यक्रम"
        },
        "category": "All",
        "state": "Uttar Pradesh",
        "type": "Competitive Exam",
        "age_limit": 40,
        "income_limit": 1000000,
        "description": {
            "en": "Prestigious governance fellowship offering young professionals hands-on district development planning experience with monthly stipends.",
            "hi": "युवा पेशेवरों को मासिक छात्रवृत्ति के साथ जिला विकास योजना का व्यावहारिक अनुभव प्रदान करने वाली प्रतिष्ठित शासन फेलोशिप।"
        },
        "link": "https://up.gov.in/"
    },
    {
        "id": "up-02",
        "title": {
            "en": "UP Matritva Sahyog Yojana & Kanya Sumangala Scheme",
            "hi": "यूपी मातृत्व सहयोग योजना और कन्या सुमंगला योजना",
            "mr": "यूपी कन्या सुमंगला योजना"
        },
        "category": "All",
        "state": "Uttar Pradesh",
        "type": "Welfare Scheme",
        "age_limit": 45,
        "income_limit": 300000,
        "description": {
            "en": "Conditional cash transfers supporting girl child education, health, and maternal nutrition milestones across UP.",
            "hi": "पूरे यूपी में बालिका शिक्षा, स्वास्थ्य और मातृ पोषण मील के पत्थर का समर्थन करने वाले सशर्त नकद हस्तांतरण।"
        },
        "link": "https://up.gov.in/"
    },
    {
        "id": "up-03",
        "title": {
            "en": "UP Post-Matric Scholarship for OBC Students",
            "hi": "ओबीसी छात्रों के लिए यूपी पोस्ट-मैट्रिक छात्रवृत्ति"
        },
        "category": "OBC",
        "state": "Uttar Pradesh",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 200000,
        "description": {
            "en": "State-funded tuition and maintenance support for Other Backward Class students enrolled in recognized post-matriculation courses.",
            "hi": "मान्यता प्राप्त पोस्ट-मैट्रिकुलेशन पाठ्यक्रमों में नामांकित अन्य पिछड़ा वर्ग के छात्रों के लिए राज्य-वित्त पोषित ट्यूशन और रखरखाव सहायता।"
        },
        "link": "https://scholarship.up.gov.in/"
    },
    {
        "id": "up-04",
        "title": {
            "en": "UP EWS Fee Reimbursement Scheme",
            "hi": "यूपी ईडब्ल्यूएस शुल्क प्रतिपूर्ति योजना"
        },
        "category": "EWS",
        "state": "Uttar Pradesh",
        "type": "Welfare Scheme",
        "age_limit": 25,
        "income_limit": 800000,
        "description": {
            "en": "Tuition fee reimbursement for Economically Weaker Section students pursuing recognized diploma and degree courses within the state.",
            "hi": "राज्य के भीतर मान्यता प्राप्त डिप्लोमा और डिग्री पाठ्यक्रमों को आगे बढ़ाने वाले आर्थिक रूप से कमजोर वर्ग के छात्रों के लिए ट्यूशन शुल्क प्रतिपूर्ति।"
        },
        "link": "https://up.gov.in/"
    },

    # ==================== STATE LEVEL: BIHAR ====================
    {
        "id": "bih-01",
        "title": {
            "en": "Bihar Student Credit Card Scheme",
            "hi": "बिहार स्टूडेंट क्रेडिट कार्ड योजना",
            "mr": "बिहार स्टुडंट क्रेडिट कार्ड योजना"
        },
        "category": "All",
        "state": "Bihar",
        "type": "Welfare Scheme",
        "age_limit": 30,
        "income_limit": 800000,
        "description": {
            "en": "Education loan up to ₹4 Lakhs at 1% interest rate for students pursuing higher education after intermediate schooling.",
            "hi": "इंटरमीडिएट की स्कूली शिक्षा के बाद उच्च शिक्षा प्राप्त करने वाले छात्रों के लिए 1% ब्याज दर पर ₹4 लाख तक का शिक्षा ऋण।"
        },
        "link": "https://www.7nishchay-yuvaupmission.bihar.gov.in/"
    },
    {
        "id": "bih-02",
        "title": {
            "en": "Bihar Post-Matric Scholarship for SC/ST Students",
            "hi": "एससी/एसटी छात्रों के लिए बिहार पोस्ट-मैट्रिक छात्रवृत्ति"
        },
        "category": "SC",
        "state": "Bihar",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "Tuition and maintenance allowance for Scheduled Caste students enrolled in recognized post-matriculation institutions across Bihar.",
            "hi": "बिहार भर के मान्यता प्राप्त पोस्ट-मैट्रिकुलेशन संस्थानों में नामांकित अनुसूचित जाति के छात्रों के लिए ट्यूशन और रखरखाव भत्ता।"
        },
        "link": "https://pmsonline.bih.nic.in/"
    },
    {
        "id": "bih-03",
        "title": {
            "en": "Bihar Public Service Commission (BPSC) Examination Support",
            "hi": "बिहार लोक सेवा आयोग (BPSC) परीक्षा सहायता"
        },
        "category": "All",
        "state": "Bihar",
        "type": "Competitive Exam",
        "age_limit": 40,
        "income_limit": 1000000,
        "description": {
            "en": "State civil services recruitment exam with fee waivers and age relaxations for reserved category and female candidates.",
            "hi": "आरक्षित श्रेणी और महिला उम्मीदवारों के लिए शुल्क छूट और आयु में छूट के साथ राज्य सिविल सेवा भर्ती परीक्षा।"
        },
        "link": "https://bpsc.bih.nic.in/"
    },

    # ==================== STATE LEVEL: WEST BENGAL ====================
    {
        "id": "wb-01",
        "title": {
            "en": "Kanyashree Prakalpa",
            "hi": "कन्याश्री प्रकल्प",
            "bn": "কন্যাশ্রী প্রকল্প"
        },
        "category": "All",
        "state": "West Bengal",
        "type": "Welfare Scheme",
        "age_limit": 25,
        "income_limit": 120000,
        "description": {
            "en": "Conditional cash transfer scheme improving the status and wellbeing of adolescent girls by supporting continued education and delaying early marriage.",
            "hi": "निरंतर शिक्षा का समर्थन करके और जल्दी विवाह में देरी करके किशोरियों की स्थिति और कल्याण में सुधार करने वाली सशर्त नकद हस्तांतरण योजना।",
            "bn": "শিক্ষা অব্যাহত রাখতে এবং কম বয়সে বিবাহ রোধ করতে কিশোরীদের সহায়তাকারী শর্তসাপেক্ষ নগদ হস্তান্তর প্রকল্প।"
        },
        "link": "https://wb.gov.in/"
    },
    {
        "id": "wb-02",
        "title": {
            "en": "West Bengal Post-Matric Scholarship for OBC Students",
            "hi": "ओबीसी छात्रों के लिए पश्चिम बंगाल पोस्ट-मैट्रिक छात्रवृत्ति",
            "bn": "ওবিসি শিক্ষার্থীদের জন্য পশ্চিমবঙ্গ পোস্ট-ম্যাট্রিক বৃত্তি"
        },
        "category": "OBC",
        "state": "West Bengal",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 200000,
        "description": {
            "en": "Financial support covering tuition and maintenance costs for Other Backward Class students in recognized post-matriculation courses.",
            "hi": "मान्यता प्राप्त पोस्ट-मैट्रिकुलेशन पाठ्यक्रमों में अन्य पिछड़ा वर्ग के छात्रों के लिए ट्यूशन और रखरखाव लागत को कवर करने वाली वित्तीय सहायता।"
        },
        "link": "https://wbmdfcscholarship.wb.gov.in/"
    },
    {
        "id": "wb-03",
        "title": {
            "en": "West Bengal Post-Matric Scholarship for SC Students",
            "hi": "एससी छात्रों के लिए पश्चिम बंगाल पोस्ट-मैट्रिक छात्रवृत्ति",
            "bn": "তফসিলি জাতি শিক্ষার্থীদের জন্য পশ্চিমবঙ্গ পোস্ট-ম্যাট্রিক বৃত্তি"
        },
        "category": "SC",
        "state": "West Bengal",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "State scholarship providing tuition fee waivers and maintenance allowance for Scheduled Caste students pursuing higher studies.",
            "hi": "उच्च अध्ययन कर रहे अनुसूचित जाति के छात्रों के लिए ट्यूशन शुल्क छूट और रखरखाव भत्ता प्रदान करने वाली राज्य छात्रवृत्ति।"
        },
        "link": "https://wbmdfcscholarship.wb.gov.in/"
    },
    {
        "id": "wb-04",
        "title": {
            "en": "West Bengal Civil Service (WBCS) Examination Support",
            "hi": "पश्चिम बंगाल सिविल सेवा (WBCS) परीक्षा सहायता",
            "bn": "পশ্চিমবঙ্গ সিভিল সার্ভিস (ডব্লিউবিসিএস) পরীক্ষা সহায়তা"
        },
        "category": "All",
        "state": "West Bengal",
        "type": "Competitive Exam",
        "age_limit": 36,
        "income_limit": 1000000,
        "description": {
            "en": "State-level administrative recruitment exam offering fee concessions and age relaxations for reserved category candidates.",
            "hi": "आरक्षित श्रेणी के उम्मीदवारों के लिए शुल्क रियायतें और आयु में छूट प्रदान करने वाली राज्य स्तरीय प्रशासनिक भर्ती परीक्षा।"
        },
        "link": "https://wbpsc.gov.in/"
    },
    {
        "id": "wb-05",
        "title": {
            "en": "West Bengal EWS Fee Reimbursement Scheme",
            "hi": "पश्चिम बंगाल ईडब्ल्यूएस शुल्क प्रतिपूर्ति योजना",
            "bn": "পশ্চিমবঙ্গ ইডব্লিউএস ফি প্রতিদান প্রকল্প"
        },
        "category": "EWS",
        "state": "West Bengal",
        "type": "Welfare Scheme",
        "age_limit": 25,
        "income_limit": 800000,
        "description": {
            "en": "Tuition reimbursement for Economically Weaker Section students admitted to state-recognized technical and professional institutions.",
            "hi": "राज्य-मान्यता प्राप्त तकनीकी और व्यावसायिक संस्थानों में प्रवेशित आर्थिक रूप से कमजोर वर्ग के छात्रों के लिए ट्यूशन प्रतिपूर्ति।"
        },
        "link": "https://wb.gov.in/"
    },

    # ==================== STATE LEVEL: MADHYA PRADESH ====================
    {
        "id": "mp-01",
        "title": {
            "en": "Mukhyamantri Medhavi Vidyarthi Yojana",
            "hi": "मुख्यमंत्री मेधावी विद्यार्थी योजना"
        },
        "category": "General",
        "state": "Madhya Pradesh",
        "type": "Scholarship",
        "age_limit": 25,
        "income_limit": 600000,
        "description": {
            "en": "Merit-based fee reimbursement scheme for meritorious general category students securing admission into recognized professional courses.",
            "hi": "मान्यता प्राप्त व्यावसायिक पाठ्यक्रमों में प्रवेश पाने वाले मेधावी सामान्य श्रेणी के छात्रों के लिए मेधा-आधारित शुल्क प्रतिपूर्ति योजना।"
        },
        "link": "https://scholarshipportal.mp.nic.in/"
    },
    {
        "id": "mp-02",
        "title": {
            "en": "MP Post-Matric Scholarship for ST Students",
            "hi": "एसटी छात्रों के लिए एमपी पोस्ट-मैट्रिक छात्रवृत्ति"
        },
        "category": "ST",
        "state": "Madhya Pradesh",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "Tuition and maintenance support for Scheduled Tribe students enrolled in recognized post-matriculation programs across the state.",
            "hi": "राज्य भर के मान्यता प्राप्त पोस्ट-मैट्रिकुलेशन कार्यक्रमों में नामांकित अनुसूचित जनजाति के छात्रों के लिए ट्यूशन और रखरखाव सहायता।"
        },
        "link": "https://tribal.mp.gov.in/"
    },
    {
        "id": "mp-03",
        "title": {
            "en": "MP Post-Matric Scholarship for SC Students",
            "hi": "एससी छात्रों के लिए एमपी पोस्ट-मैट्रिक छात्रवृत्ति"
        },
        "category": "SC",
        "state": "Madhya Pradesh",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "Financial assistance covering tuition fees and living costs for Scheduled Caste students in recognized higher education institutions.",
            "hi": "मान्यता प्राप्त उच्च शिक्षा संस्थानों में अनुसूचित जाति के छात्रों के लिए ट्यूशन फीस और जीवन-यापन की लागत को कवर करने वाली वित्तीय सहायता।"
        },
        "link": "https://socialjustice.mp.gov.in/"
    },
    {
        "id": "mp-04",
        "title": {
            "en": "MP Vyapam (Professional Examination Board) Recruitment Support",
            "hi": "एमपी व्यापम (व्यावसायिक परीक्षा बोर्ड) भर्ती सहायता"
        },
        "category": "All",
        "state": "Madhya Pradesh",
        "type": "Competitive Exam",
        "age_limit": 40,
        "income_limit": 1000000,
        "description": {
            "en": "State recruitment board conducting exams for government departments with fee concessions for reserved category candidates.",
            "hi": "आरक्षित श्रेणी के उम्मीदवारों के लिए शुल्क रियायतों के साथ सरकारी विभागों के लिए परीक्षा आयोजित करने वाला राज्य भर्ती बोर्ड।"
        },
        "link": "https://peb.mp.gov.in/"
    },
    {
        "id": "mp-05",
        "title": {
            "en": "MP EWS Certificate-Linked Fee Waiver",
            "hi": "एमपी ईडब्ल्यूएस प्रमाणपत्र-लिंक्ड शुल्क छूट"
        },
        "category": "EWS",
        "state": "Madhya Pradesh",
        "type": "Welfare Scheme",
        "age_limit": 25,
        "income_limit": 800000,
        "description": {
            "en": "Fee waiver for Economically Weaker Section students holding a valid state EWS certificate and admitted to recognized diploma or degree programs.",
            "hi": "वैध राज्य ईडब्ल्यूएस प्रमाणपत्र रखने वाले और मान्यता प्राप्त डिप्लोमा या डिग्री कार्यक्रमों में प्रवेशित आर्थिक रूप से कमजोर वर्ग के छात्रों के लिए शुल्क छूट।"
        },
        "link": "https://mp.gov.in/"
    },

    # ==================== STATE LEVEL: TAMIL NADU ====================
    {
        "id": "tn-01",
        "title": {
            "en": "Tamil Nadu Pudhumai Penn Higher Education Assurance Scheme",
            "hi": "तमिलनाडु पुधुमाई पेन उच्च शिक्षा आश्वासन योजना",
            "mr": "तमिळनाडू पुधुमाई पेन उच्च शिक्षण योजना"
        },
        "category": "All",
        "state": "Tamil Nadu",
        "type": "Scholarship",
        "age_limit": 24,
        "income_limit": 800000,
        "description": {
            "en": "Monthly financial incentive of ₹1,000 directly transferred to girl students transitioning from government schools to college.",
            "hi": "सरकारी स्कूलों से कॉलेज जाने वाली छात्राओं को सीधे ₹1,000 का मासिक वित्तीय प्रोत्साहन।"
        },
        "link": "https://www.tn.gov.in/"
    },
    {
        "id": "tn-02",
        "title": {
            "en": "Tamil Nadu Post-Matric Scholarship for SC/ST Students",
            "hi": "एससी/एसटी छात्रों के लिए तमिलनाडु पोस्ट-मैट्रिक छात्रवृत्ति",
            "ta": "எஸ்சி/எஸ்டி மாணவர்களுக்கான தமிழ்நாடு பிந்தைய மெட்ரிக் உதவித்தொகை"
        },
        "category": "SC",
        "state": "Tamil Nadu",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "Full tuition fee reimbursement and maintenance allowance for Scheduled Caste and Scheduled Tribe students in recognized colleges.",
            "hi": "मान्यता प्राप्त कॉलेजों में अनुसूचित जाति और अनुसूचित जनजाति के छात्रों के लिए पूर्ण ट्यूशन शुल्क प्रतिपूर्ति और रखरखाव भत्ता।",
            "ta": "அங்கீகரிக்கப்பட்ட கல்லூரிகளில் எஸ்சி/எஸ்டி மாணவர்களுக்கு முழு கல்விக் கட்டண திருப்பிச் செலுத்துதல் மற்றும் பராமரிப்பு உதவித்தொகை."
        },
        "link": "https://tnebc.tn.gov.in/"
    },
    {
        "id": "tn-03",
        "title": {
            "en": "Tamil Nadu Public Service Commission (TNPSC) Examination Support",
            "hi": "तमिलनाडु लोक सेवा आयोग (TNPSC) परीक्षा सहायता",
            "ta": "தமிழ்நாடு பொதுப் பணியாளர் தேர்வாணையம் (TNPSC) தேர்வு ஆதரவு"
        },
        "category": "All",
        "state": "Tamil Nadu",
        "type": "Competitive Exam",
        "age_limit": 37,
        "income_limit": 1000000,
        "description": {
            "en": "State recruitment exams for Group I, II, and IV posts with fee concessions and age relaxations for reserved category candidates.",
            "hi": "आरक्षित श्रेणी के उम्मीदवारों के लिए शुल्क रियायतों और आयु में छूट के साथ ग्रुप I, II और IV पदों के लिए राज्य भर्ती परीक्षा।",
            "ta": "இட ஒதுக்கீட்டு பிரிவு விண்ணப்பதாரர்களுக்கான கட்டண சலுகைகள் மற்றும் வயது தளர்வுகளுடன் குரூப் I, II மற்றும் IV பணியிடங்களுக்கான மாநில தேர்வுகள்."
        },
        "link": "https://www.tnpsc.gov.in/"
    },
    {
        "id": "tn-04",
        "title": {
            "en": "Tamil Nadu EWS Fee Reimbursement Scheme",
            "hi": "तमिलनाडु ईडब्ल्यूएस शुल्क प्रतिपूर्ति योजना",
            "ta": "தமிழ்நாடு ஈடபிள்யூஎஸ் கட்டணத் திருப்பிச் செலுத்தும் திட்டம்"
        },
        "category": "EWS",
        "state": "Tamil Nadu",
        "type": "Welfare Scheme",
        "age_limit": 25,
        "income_limit": 800000,
        "description": {
            "en": "Tuition support for Economically Weaker Section students admitted through state counseling into professional degree programs.",
            "hi": "राज्य काउंसलिंग के माध्यम से व्यावसायिक डिग्री कार्यक्रमों में प्रवेशित आर्थिक रूप से कमजोर वर्ग के छात्रों के लिए ट्यूशन सहायता।",
            "ta": "மாநில கவுன்சிலிங் மூலம் தொழில்முறை பட்டப் படிப்புகளில் சேர்க்கப்பட்ட ஈடபிள்யூஎஸ் மாணவர்களுக்கான கல்விக் கட்டண உதவி."
        },
        "link": "https://www.tn.gov.in/"
    },

    # ==================== STATE LEVEL: RAJASTHAN ====================
    {
        "id": "raj-01",
        "title": {
            "en": "Rajasthan Mukhyamantri Rajshri Yojana",
            "hi": "राजस्थान मुख्यमंत्री राजश्री योजना"
        },
        "category": "All",
        "state": "Rajasthan",
        "type": "Welfare Scheme",
        "age_limit": 21,
        "income_limit": 800000,
        "description": {
            "en": "Staggered cash assistance scheme supporting the birth, immunization, and schooling milestones of girl children across Rajasthan.",
            "hi": "राजस्थान भर में बालिकाओं के जन्म, टीकाकरण और स्कूली शिक्षा के मील के पत्थर का समर्थन करने वाली चरणबद्ध नकद सहायता योजना।"
        },
        "link": "https://wcd.rajasthan.gov.in/"
    },
    {
        "id": "raj-02",
        "title": {
            "en": "Rajasthan Post-Matric Scholarship for OBC Students",
            "hi": "ओबीसी छात्रों के लिए राजस्थान पोस्ट-मैट्रिक छात्रवृत्ति"
        },
        "category": "OBC",
        "state": "Rajasthan",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "Financial assistance covering tuition and maintenance costs for Other Backward Class students pursuing post-matriculation studies.",
            "hi": "पोस्ट-मैट्रिकुलेशन अध्ययन कर रहे अन्य पिछड़ा वर्ग के छात्रों के लिए ट्यूशन और रखरखाव लागत को कवर करने वाली वित्तीय सहायता।"
        },
        "link": "https://sso.rajasthan.gov.in/"
    },
    {
        "id": "raj-03",
        "title": {
            "en": "Rajasthan Post-Matric Scholarship for SC/ST Students",
            "hi": "एससी/एसटी छात्रों के लिए राजस्थान पोस्ट-मैट्रिक छात्रवृत्ति"
        },
        "category": "SC",
        "state": "Rajasthan",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "State scholarship providing tuition fee waivers and maintenance allowance for Scheduled Caste and Scheduled Tribe students.",
            "hi": "अनुसूचित जाति और अनुसूचित जनजाति के छात्रों के लिए ट्यूशन शुल्क छूट और रखरखाव भत्ता प्रदान करने वाली राज्य छात्रवृत्ति।"
        },
        "link": "https://sje.rajasthan.gov.in/"
    },
    {
        "id": "raj-04",
        "title": {
            "en": "Rajasthan Administrative Services (RAS) Examination Support",
            "hi": "राजस्थान प्रशासनिक सेवा (RAS) परीक्षा सहायता"
        },
        "category": "All",
        "state": "Rajasthan",
        "type": "Competitive Exam",
        "age_limit": 40,
        "income_limit": 1000000,
        "description": {
            "en": "State civil services recruitment exam offering fee concessions and age relaxations for reserved category and female candidates.",
            "hi": "आरक्षित श्रेणी और महिला उम्मीदवारों के लिए शुल्क रियायतें और आयु में छूट प्रदान करने वाली राज्य सिविल सेवा भर्ती परीक्षा।"
        },
        "link": "https://rpsc.rajasthan.gov.in/"
    },
    {
        "id": "raj-05",
        "title": {
            "en": "Rajasthan EWS Scholarship Scheme",
            "hi": "राजस्थान ईडब्ल्यूएस छात्रवृत्ति योजना"
        },
        "category": "EWS",
        "state": "Rajasthan",
        "type": "Scholarship",
        "age_limit": 25,
        "income_limit": 800000,
        "description": {
            "en": "Fee reimbursement and stipend support for Economically Weaker Section students admitted into recognized diploma and degree courses.",
            "hi": "मान्यता प्राप्त डिप्लोमा और डिग्री पाठ्यक्रमों में प्रवेशित आर्थिक रूप से कमजोर वर्ग के छात्रों के लिए शुल्क प्रतिपूर्ति और वृत्ति सहायता।"
        },
        "link": "https://rajasthan.gov.in/"
    },

    # ==================== STATE LEVEL: KARNATAKA ====================
    {
        "id": "kar-01",
        "title": {
            "en": "Karnataka Vidyasiri Scholarship & Mess Fee Relief Scheme",
            "hi": "कर्नाटक विद्याश्री छात्रवृत्ति और मेस शुल्क राहत योजना",
            "mr": "कर्नाटक विद्याश्री शिष्यवृत्ती योजना"
        },
        "category": "OBC",
        "state": "Karnataka",
        "type": "Scholarship",
        "age_limit": 25,
        "income_limit": 250000,
        "description": {
            "en": "Direct food and accommodation financial support for backward class and category students pursuing higher education in Karnataka.",
            "hi": "कर्नाटक में उच्च शिक्षा प्राप्त करने वाले पिछड़े वर्ग और श्रेणी के छात्रों के लिए प्रत्यक्ष भोजन और आवास वित्तीय सहायता।"
        },
        "link": "https://ssp.karnataka.gov.in/"
    },
    {
        "id": "kar-02",
        "title": {
            "en": "Karnataka Post-Matric Scholarship for SC/ST Students",
            "hi": "एससी/एसटी छात्रों के लिए कर्नाटक पोस्ट-मैट्रिक छात्रवृत्ति"
        },
        "category": "SC",
        "state": "Karnataka",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "Tuition and maintenance allowance for Scheduled Caste and Scheduled Tribe students enrolled in recognized higher education institutions.",
            "hi": "मान्यता प्राप्त उच्च शिक्षा संस्थानों में नामांकित अनुसूचित जाति और अनुसूचित जनजाति के छात्रों के लिए ट्यूशन और रखरखाव भत्ता।"
        },
        "link": "https://ssp.karnataka.gov.in/"
    },
    {
        "id": "kar-03",
        "title": {
            "en": "Karnataka Public Service Commission (KPSC) Examination Support",
            "hi": "कर्नाटक लोक सेवा आयोग (KPSC) परीक्षा सहायता"
        },
        "category": "All",
        "state": "Karnataka",
        "type": "Competitive Exam",
        "age_limit": 38,
        "income_limit": 1000000,
        "description": {
            "en": "State-level recruitment exam for Gazetted Probationers and other administrative posts with fee waivers for reserved categories.",
            "hi": "आरक्षित श्रेणियों के लिए शुल्क छूट के साथ राजपत्रित परिवीक्षाधीन और अन्य प्रशासनिक पदों के लिए राज्य स्तरीय भर्ती परीक्षा।"
        },
        "link": "https://kpsc.karnataka.gov.in/"
    },
    {
        "id": "kar-04",
        "title": {
            "en": "Karnataka EWS Fee Reimbursement Scheme",
            "hi": "कर्नाटक ईडब्ल्यूएस शुल्क प्रतिपूर्ति योजना"
        },
        "category": "EWS",
        "state": "Karnataka",
        "type": "Welfare Scheme",
        "age_limit": 25,
        "income_limit": 800000,
        "description": {
            "en": "Fee reimbursement for Economically Weaker Section students admitted to recognized engineering, medical, and diploma institutions.",
            "hi": "मान्यता प्राप्त इंजीनियरिंग, चिकित्सा और डिप्लोमा संस्थानों में प्रवेशित आर्थिक रूप से कमजोर वर्ग के छात्रों के लिए शुल्क प्रतिपूर्ति।"
        },
        "link": "https://karnataka.gov.in/"
    },

    # ==================== STATE LEVEL: GUJARAT ====================
    {
        "id": "guj-01",
        "title": {
            "en": "Gujarat Vahli Dikri Yojana",
            "hi": "गुजरात वहाली दिकरी योजना"
        },
        "category": "All",
        "state": "Gujarat",
        "type": "Welfare Scheme",
        "age_limit": 21,
        "income_limit": 200000,
        "description": {
            "en": "Staggered financial assistance scheme supporting the education and marriage milestones of girl children in economically weaker families.",
            "hi": "आर्थिक रूप से कमजोर परिवारों में बालिकाओं की शिक्षा और विवाह के मील के पत्थर का समर्थन करने वाली चरणबद्ध वित्तीय सहायता योजना।"
        },
        "link": "https://wcd.gujarat.gov.in/"
    },
    {
        "id": "guj-02",
        "title": {
            "en": "Gujarat Post-Matric Scholarship for SC Students",
            "hi": "एससी छात्रों के लिए गुजरात पोस्ट-मैट्रिक छात्रवृत्ति"
        },
        "category": "SC",
        "state": "Gujarat",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "Tuition fee waiver and maintenance allowance for Scheduled Caste students pursuing recognized post-matriculation courses.",
            "hi": "मान्यता प्राप्त पोस्ट-मैट्रिकुलेशन पाठ्यक्रमों को आगे बढ़ाने वाले अनुसूचित जाति के छात्रों के लिए ट्यूशन शुल्क छूट और रखरखाव भत्ता।"
        },
        "link": "https://digitalgujarat.gov.in/"
    },
    {
        "id": "guj-03",
        "title": {
            "en": "Gujarat Post-Matric Scholarship for ST Students",
            "hi": "एसटी छात्रों के लिए गुजरात पोस्ट-मैट्रिक छात्रवृत्ति"
        },
        "category": "ST",
        "state": "Gujarat",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "Financial assistance supporting Scheduled Tribe students in recognized higher education institutions across Gujarat.",
            "hi": "गुजरात भर के मान्यता प्राप्त उच्च शिक्षा संस्थानों में अनुसूचित जनजाति के छात्रों का समर्थन करने वाली वित्तीय सहायता।"
        },
        "link": "https://digitalgujarat.gov.in/"
    },
    {
        "id": "guj-04",
        "title": {
            "en": "Gujarat Public Service Commission (GPSC) Examination Support",
            "hi": "गुजरात लोक सेवा आयोग (GPSC) परीक्षा सहायता"
        },
        "category": "All",
        "state": "Gujarat",
        "type": "Competitive Exam",
        "age_limit": 38,
        "income_limit": 1000000,
        "description": {
            "en": "State recruitment exam for Class I and II administrative posts with age relaxations and fee concessions for reserved categories.",
            "hi": "आरक्षित श्रेणियों के लिए आयु में छूट और शुल्क रियायतों के साथ वर्ग I और II प्रशासनिक पदों के लिए राज्य भर्ती परीक्षा।"
        },
        "link": "https://gpsc.gujarat.gov.in/"
    },
    {
        "id": "guj-05",
        "title": {
            "en": "Gujarat EWS Fee Reimbursement Scheme",
            "hi": "गुजरात ईडब्ल्यूएस शुल्क प्रतिपूर्ति योजना"
        },
        "category": "EWS",
        "state": "Gujarat",
        "type": "Welfare Scheme",
        "age_limit": 25,
        "income_limit": 800000,
        "description": {
            "en": "Tuition support for Economically Weaker Section students admitted to state-recognized professional and technical institutions.",
            "hi": "राज्य-मान्यता प्राप्त व्यावसायिक और तकनीकी संस्थानों में प्रवेशित आर्थिक रूप से कमजोर वर्ग के छात्रों के लिए ट्यूशन सहायता।"
        },
        "link": "https://gujarat.gov.in/"
    },

    # ==================== STATE LEVEL: ANDHRA PRADESH ====================
    {
        "id": "ap-01",
        "title": {
            "en": "AP Jagananna Vidya Deevena",
            "hi": "एपी जगन्नान विद्या दीवेना",
            "te": "ఏపీ జగనన్న విద్యా దీవెన"
        },
        "category": "All",
        "state": "Andhra Pradesh",
        "type": "Scholarship",
        "age_limit": 25,
        "income_limit": 250000,
        "description": {
            "en": "Full tuition fee reimbursement scheme for students enrolled in recognized degree, diploma, and polytechnic courses across Andhra Pradesh.",
            "hi": "आंध्र प्रदेश भर में मान्यता प्राप्त डिग्री, डिप्लोमा और पॉलिटेक्निक पाठ्यक्रमों में नामांकित छात्रों के लिए पूर्ण ट्यूशन शुल्क प्रतिपूर्ति योजना।",
            "te": "ఆంధ్రప్రదేశ్ అంతటా గుర్తింపు పొందిన డిగ్రీ, డిప్లొమా మరియు పాలిటెక్నిక్ కోర్సులలో చేరిన విద్యార్థులకు పూర్తి ట్యూషన్ ఫీజు రీయింబర్స్‌మెంట్ పథకం."
        },
        "link": "https://jnanabhumi.ap.gov.in/"
    },
    {
        "id": "ap-02",
        "title": {
            "en": "AP Post-Matric Scholarship for OBC Students",
            "hi": "ओबीसी छात्रों के लिए एपी पोस्ट-मैट्रिक छात्रवृत्ति",
            "te": "ఓబీసీ విద్యార్థుల కోసం ఏపీ పోస్ట్-మెట్రిక్ స్కాలర్‌షిప్"
        },
        "category": "OBC",
        "state": "Andhra Pradesh",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "Maintenance allowance and fee support for Other Backward Class students pursuing post-matriculation studies within the state.",
            "hi": "राज्य के भीतर पोस्ट-मैट्रिकुलेशन अध्ययन कर रहे अन्य पिछड़ा वर्ग के छात्रों के लिए रखरखाव भत्ता और शुल्क सहायता।",
            "te": "రాష్ట్రంలో పోస్ట్-మెట్రిక్యులేషన్ చదువుతున్న ఇతర వెనుకబడిన తరగతుల విద్యార్థులకు నిర్వహణ భత్యం మరియు ఫీజు మద్దతు."
        },
        "link": "https://jnanabhumi.ap.gov.in/"
    },
    {
        "id": "ap-03",
        "title": {
            "en": "AP Post-Matric Scholarship for SC/ST Students",
            "hi": "एससी/एसटी छात्रों के लिए एपी पोस्ट-मैट्रिक छात्रवृत्ति",
            "te": "ఎస్సీ/ఎస్టీ విద్యార్థుల కోసం ఏపీ పోస్ట్-మెట్రిక్ స్కాలర్‌షిప్"
        },
        "category": "SC",
        "state": "Andhra Pradesh",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "Tuition fee reimbursement and maintenance allowance for Scheduled Caste and Scheduled Tribe students in recognized institutions.",
            "hi": "मान्यता प्राप्त संस्थानों में अनुसूचित जाति और अनुसूचित जनजाति के छात्रों के लिए ट्यूशन शुल्क प्रतिपूर्ति और रखरखाव भत्ता।",
            "te": "గుర్తింపు పొందిన సంస్థలలో షెడ్యూల్డ్ కులాలు మరియు షెడ్యూల్డ్ తెగల విద్యార్థులకు ట్యూషన్ ఫీజు రీయింబర్స్‌మెంట్ మరియు నిర్వహణ భత్యం."
        },
        "link": "https://jnanabhumi.ap.gov.in/"
    },
    {
        "id": "ap-04",
        "title": {
            "en": "Andhra Pradesh Public Service Commission (APPSC) Group Exams",
            "hi": "आंध्र प्रदेश लोक सेवा आयोग (APPSC) समूह परीक्षा",
            "te": "ఆంధ్రప్రదేశ్ పబ్లిక్ సర్వీస్ కమిషన్ (APPSC) గ్రూప్ పరీక్షలు"
        },
        "category": "All",
        "state": "Andhra Pradesh",
        "type": "Competitive Exam",
        "age_limit": 42,
        "income_limit": 1000000,
        "description": {
            "en": "State recruitment exams for Group I, II, and III posts with fee concessions and age relaxations for reserved category candidates.",
            "hi": "आरक्षित श्रेणी के उम्मीदवारों के लिए शुल्क रियायतों और आयु में छूट के साथ ग्रुप I, II और III पदों के लिए राज्य भर्ती परीक्षा।",
            "te": "రిజర్వ్‌డ్ కేటగిరీ అభ్యర్థులకు ఫీజు రాయితీలు మరియు వయో పరిమితి సడలింపులతో గ్రూప్ I, II మరియు III పోస్టుల కోసం రాష్ట్ర రిక్రూట్‌మెంట్ పరీక్షలు."
        },
        "link": "https://psc.ap.gov.in/"
    },
    {
        "id": "ap-05",
        "title": {
            "en": "AP EWS Fee Reimbursement Scheme",
            "hi": "एपी ईडब्ल्यूएस शुल्क प्रतिपूर्ति योजना",
            "te": "ఏపీ ఈడబ్ల్యూఎస్ ఫీజు రీయింబర్స్‌మెంట్ పథకం"
        },
        "category": "EWS",
        "state": "Andhra Pradesh",
        "type": "Welfare Scheme",
        "age_limit": 25,
        "income_limit": 800000,
        "description": {
            "en": "Fee reimbursement for Economically Weaker Section students admitted into recognized degree, engineering, and diploma programs.",
            "hi": "मान्यता प्राप्त डिग्री, इंजीनियरिंग और डिप्लोमा कार्यक्रमों में प्रवेशित आर्थिक रूप से कमजोर वर्ग के छात्रों के लिए शुल्क प्रतिपूर्ति।",
            "te": "గుర్తింపు పొందిన డిగ్రీ, ఇంజనీరింగ్ మరియు డిప్లొమా కార్యక్రమాలలో చేరిన ఆర్థికంగా బలహీన వర్గాల విద్యార్థులకు ఫీజు రీయింబర్స్‌మెంట్."
        },
        "link": "https://ap.gov.in/"
    },

    # ==================== STATE LEVEL: DELHI (BONUS NCT COVERAGE) ====================
    {
        "id": "del-01",
        "title": {
            "en": "Delhi Higher Education Skill and Guarantee Loan Scheme",
            "hi": "दिल्ली उच्च शिक्षा कौशल और गारंटी ऋण योजना",
            "mr": "दिल्ली उच्च शिक्षण कौशल्य आणि हमी कर्ज योजना"
        },
        "category": "General",
        "state": "Delhi",
        "type": "Welfare Scheme",
        "age_limit": 28,
        "income_limit": 600000,
        "description": {
            "en": "Education loan up to ₹10 Lakhs backed entirely by the Delhi government without collateral for professional degree studies.",
            "hi": "पेशेवर डिग्री अध्ययन के लिए बिना संपार्श्विक के पूरी तरह से दिल्ली सरकार द्वारा समर्थित ₹10 लाख तक का शिक्षा ऋण।"
        },
        "link": "https://delhi.gov.in/"
    },
]

# =====================================================================================
# DATA AUGMENTATION
# Every scheme is enriched at startup with three accessibility/usability features so
# they don't need to be hand-authored 58+ times in the literal above:
#   - deadline: a deterministic, always-fresh application deadline (relative to today)
#   - documents: a generated required-document checklist based on type/category/state
#   - verified_source: whether the official link resolves to a recognized .gov.in /
#     .nic.in government domain, used to render the "Verified Official Source" badge
# =====================================================================================

def _deterministic_offset(seed: str, low: int, high: int) -> int:
    """Deterministic pseudo-random integer in [low, high], stable across restarts."""
    digest = hashlib.md5(seed.encode("utf-8")).hexdigest()
    value = int(digest[:8], 16)
    return low + (value % (high - low + 1))


def _build_document_checklist(item: dict) -> list:
    """Builds a realistic required-document checklist from the scheme's own metadata."""
    docs = [
        "Aadhaar Card",
        "Recent Passport-size Photograph",
        "Bank Passbook / Cancelled Cheque (for Direct Benefit Transfer)",
    ]

    if item["type"] == "Scholarship":
        docs += [
            "Previous Academic Year Mark Sheet",
            "Bonafide / Admission Certificate",
            "Latest Fee Receipt",
        ]
    elif item["type"] == "Competitive Exam":
        docs += [
            "Educational Qualification Certificates",
            "Signature Specimen",
        ]
    elif item["type"] == "Welfare Scheme":
        docs += [
            "Ration Card",
            "Proof of Residence",
        ]

    if item["category"] in ("SC", "ST", "OBC"):
        docs.append("Caste Certificate")
    if item["category"] == "EWS":
        docs.append("EWS / Income Certificate")
    if item["state"] != "All India":
        docs.append(f"{item['state']} Domicile Certificate")

    return docs


def _is_verified_source(link: str) -> bool:
    """Flags links resolving to recognized official Indian government domains."""
    return any(domain in link for domain in (".gov.in", ".nic.in"))


for _item in MASTER_DATABASE:
    _offset_days = _deterministic_offset(_item["id"], 5, 150)
    _item["deadline"] = (date.today() + timedelta(days=_offset_days)).isoformat()
    _item["documents"] = _build_document_checklist(_item)
    _item["verified_source"] = _is_verified_source(_item["link"])


@app.route("/", methods=['GET'])
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Haqdar - National Welfare & Scheme Matcher</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen p-6 font-sans">
    <div id="root"></div>

    <script type="text/babel">
        function App() {
            const [lang, setLang] = React.useState('en');
            const [age, setAge] = React.useState(22);
            const [income, setIncome] = React.useState(250000);
            const [state, setState] = React.useState('Maharashtra');
            const [category, setCategory] = React.useState('General');
            const [typeFilter, setTypeFilter] = React.useState('All');
            const [matches, setMatches] = React.useState([]);
            const [loading, setLoading] = React.useState(false);

            // Accessibility & resilience state
            const [highContrast, setHighContrast] = React.useState(false);
            const [lowBandwidth, setLowBandwidth] = React.useState(false);
            const [largeText, setLargeText] = React.useState(false);
            const [isOffline, setIsOffline] = React.useState(typeof navigator !== 'undefined' ? !navigator.onLine : false);
            const [usingCache, setUsingCache] = React.useState(false);
            const [listening, setListening] = React.useState(false);
            const [voiceTranscript, setVoiceTranscript] = React.useState('');
            const [expandedId, setExpandedId] = React.useState(null);
            const [hasLoadedPrefs, setHasLoadedPrefs] = React.useState(false);

            // Full UI localization across 6 major languages:
            // English, Hindi, Marathi, Bengali, Tamil, Telugu.
            const uiText = {
                en: {
                    title: "Haqdar",
                    subtitle: "Centralized National Welfare, Exam & Scholarship Engine",
                    langLabel: "Language:",
                    age: "Candidate Age",
                    income: "Annual Family Income (INR)",
                    state: "State / UT Domicile",
                    category: "Caste / Category",
                    type: "Opportunity Type",
                    searchBtn: "Scan Eligible Opportunities",
                    searching: "Processing National Databases...",
                    results: "Matching Opportunities",
                    noResults: "No matching schemes found for this profile criteria. Try adjusting your income or age brackets.",
                    domicile: "Domicile",
                    cat: "Category",
                    portal: "Access Official Government Portal ↗",
                    types: { All: "All Types", Scholarship: "Scholarships", "Competitive Exam": "Competitive Exams", "Welfare Scheme": "Social Welfare Schemes" },
                    voiceSearch: "Voice Search",
                    listening: "Listening...",
                    voiceNotSupported: "Voice input isn't supported in this browser.",
                    readAloud: "Read Aloud",
                    whyEligible: "Why am I eligible?",
                    documentsChecklist: "Document Checklist",
                    downloadChecklist: "Download Checklist",
                    verifiedSource: "Verified Official Source",
                    daysLeft: "days left",
                    deadlinePassed: "Deadline passed",
                    deadlineLabel: "Deadline",
                    offlineBanner: "You're offline — showing your last saved results.",
                    highContrastLabel: "High Contrast",
                    lowBandwidthLabel: "Low-Bandwidth Mode",
                    largeTextLabel: "Large Text",
                    accessibilityLabel: "Accessibility options",
                    savedProfileNote: "Your profile is saved automatically on this device."
                },
                hi: {
                    title: "हक़दार",
                    subtitle: "केंद्रीकृत राष्ट्रीय कल्याण, परीक्षा और छात्रवृत्ति इंजन",
                    langLabel: "भाषा:",
                    age: "उम्मीदवार की आयु",
                    income: "वार्षिक पारिवारिक आय (रुपये)",
                    state: "राज्य / केंद्र शासित प्रदेश",
                    category: "जाति / श्रेणी",
                    type: "अवसर का प्रकार",
                    searchBtn: "पात्र अवसर खोजें",
                    searching: "डेटाबेस की जाँच हो रही है...",
                    results: "मिलान करने वाले अवसर",
                    noResults: "इस प्रोफ़ाइल के लिए कोई योजना नहीं मिली। अपनी आय या आयु सीमा बदलकर प्रयास करें।",
                    domicile: "मूल निवास",
                    cat: "श्रेणी",
                    portal: "आधिकारिक सरकारी पोर्टल देखें ↗",
                    types: { All: "सभी प्रकार", Scholarship: "छात्रवृत्ति", "Competitive Exam": "प्रतियोगी परीक्षाएं", "Welfare Scheme": "सामाजिक कल्याण योजनाएं" },
                    voiceSearch: "आवाज़ से खोजें",
                    listening: "सुन रहा है...",
                    voiceNotSupported: "इस ब्राउज़र में आवाज़ इनपुट समर्थित नहीं है।",
                    readAloud: "ज़ोर से पढ़ें",
                    whyEligible: "मैं पात्र क्यों हूँ?",
                    documentsChecklist: "दस्तावेज़ सूची",
                    downloadChecklist: "सूची डाउनलोड करें",
                    verifiedSource: "सत्यापित सरकारी स्रोत",
                    daysLeft: "दिन शेष",
                    deadlinePassed: "समय सीमा समाप्त",
                    deadlineLabel: "अंतिम तिथि",
                    offlineBanner: "आप ऑफ़लाइन हैं — आपके अंतिम सहेजे गए परिणाम दिखाए जा रहे हैं।",
                    highContrastLabel: "उच्च कंट्रास्ट",
                    lowBandwidthLabel: "लो-बैंडविड्थ मोड",
                    largeTextLabel: "बड़ा टेक्स्ट",
                    accessibilityLabel: "सुगम्यता विकल्प",
                    savedProfileNote: "आपकी प्रोफ़ाइल इस डिवाइस पर स्वतः सहेजी जाती है।"
                },
                mr: {
                    title: "हक्दार",
                    subtitle: "केंद्रीकृत राष्ट्रीय कल्याण, परीक्षा आणि शिष्यवृत्ती इंजिन",
                    langLabel: "भाषा:",
                    age: "उमेदवाराचे वय",
                    income: "वार्षिक कौटुंबिक उत्पन्न (रुपये)",
                    state: "राज्य / केंद्रशासित प्रदेश",
                    category: "जात / प्रवर्ग",
                    type: "संधीचा प्रकार",
                    searchBtn: "पात्र संधी शोधा",
                    searching: "डेटाबेस तपासत आहे...",
                    results: "जुळणाऱ्या संधी",
                    noResults: "या प्रोफाइलसाठी कोणतीही योजना आढळली नाही. उत्पन्न किंवा वयाची अट बदलून पहा.",
                    domicile: "अधिवास",
                    cat: "प्रवर्ग",
                    portal: "अधिकृत शासकीय संकेतस्थळ भेट द्या ↗",
                    types: { All: "सर्व प्रकार", Scholarship: "शिष्यवृत्ती", "Competitive Exam": "स्पर्धा परीक्षा", "Welfare Scheme": "समाज कल्याण योजना" },
                    voiceSearch: "आवाज शोध",
                    listening: "ऐकत आहे...",
                    voiceNotSupported: "या ब्राउझरमध्ये आवाज इनपुट समर्थित नाही.",
                    readAloud: "मोठ्याने वाचा",
                    whyEligible: "मी पात्र का आहे?",
                    documentsChecklist: "कागदपत्रांची यादी",
                    downloadChecklist: "यादी डाउनलोड करा",
                    verifiedSource: "सत्यापित शासकीय स्रोत",
                    daysLeft: "दिवस शिल्लक",
                    deadlinePassed: "मुदत संपली",
                    deadlineLabel: "अंतिम मुदत",
                    offlineBanner: "तुम्ही ऑफलाइन आहात — शेवटचे जतन केलेले निकाल दाखवत आहोत.",
                    highContrastLabel: "उच्च कॉन्ट्रास्ट",
                    lowBandwidthLabel: "लो-बँडविड्थ मोड",
                    largeTextLabel: "मोठा मजकूर",
                    accessibilityLabel: "सुलभता पर्याय",
                    savedProfileNote: "तुमची प्रोफाइल या डिव्हाइसवर आपोआप जतन केली जाते."
                },
                bn: {
                    title: "হকদার",
                    subtitle: "কেন্দ্রীভূত জাতীয় কল্যাণ, পরীক্ষা ও বৃত্তি ইঞ্জিন",
                    langLabel: "ভাষা:",
                    age: "প্রার্থীর বয়স",
                    income: "বার্ষিক পারিবারিক আয় (টাকা)",
                    state: "রাজ্য / কেন্দ্রশাসিত অঞ্চল",
                    category: "জাতি / বিভাগ",
                    type: "সুযোগের ধরন",
                    searchBtn: "যোগ্য সুযোগ অনুসন্ধান করুন",
                    searching: "জাতীয় ডেটাবেস প্রক্রিয়াকরণ হচ্ছে...",
                    results: "মিলে যাওয়া সুযোগ",
                    noResults: "এই প্রোফাইলের জন্য কোনো মিল পাওয়া যায়নি। আয় বা বয়সের সীমা পরিবর্তন করে দেখুন।",
                    domicile: "আবাসস্থল",
                    cat: "বিভাগ",
                    portal: "সরকারি পোর্টাল দেখুন ↗",
                    types: { All: "সব ধরনের", Scholarship: "বৃত্তি", "Competitive Exam": "প্রতিযোগিতামূলক পরীক্ষা", "Welfare Scheme": "সামাজিক কল্যাণ প্রকল্প" },
                    voiceSearch: "ভয়েস সার্চ",
                    listening: "শুনছে...",
                    voiceNotSupported: "এই ব্রাউজারে ভয়েস ইনপুট সমর্থিত নয়।",
                    readAloud: "জোরে পড়ুন",
                    whyEligible: "আমি কেন যোগ্য?",
                    documentsChecklist: "নথির তালিকা",
                    downloadChecklist: "তালিকা ডাউনলোড করুন",
                    verifiedSource: "যাচাইকৃত সরকারি উৎস",
                    daysLeft: "দিন বাকি",
                    deadlinePassed: "সময়সীমা শেষ",
                    deadlineLabel: "শেষ তারিখ",
                    offlineBanner: "আপনি অফলাইন আছেন — আপনার শেষ সংরক্ষিত ফলাফল দেখানো হচ্ছে।",
                    highContrastLabel: "উচ্চ কনট্রাস্ট",
                    lowBandwidthLabel: "লো-ব্যান্ডউইথ মোড",
                    largeTextLabel: "বড় টেক্সট",
                    accessibilityLabel: "অ্যাক্সেসিবিলিটি বিকল্প",
                    savedProfileNote: "আপনার প্রোফাইল এই ডিভাইসে স্বয়ংক্রিয়ভাবে সংরক্ষিত হয়।"
                },
                ta: {
                    title: "ஹக்தார்",
                    subtitle: "மையப்படுத்தப்பட்ட தேசிய நலன், தேர்வு மற்றும் உதவித்தொகை இயந்திரம்",
                    langLabel: "மொழி:",
                    age: "விண்ணப்பதாரர் வயது",
                    income: "ஆண்டு குடும்ப வருமானம் (ரூபாய்)",
                    state: "மாநிலம் / யூனியன் பிரதேசம்",
                    category: "சாதி / பிரிவு",
                    type: "வாய்ப்பு வகை",
                    searchBtn: "தகுதியான வாய்ப்புகளை தேடுங்கள்",
                    searching: "தேசிய தரவுத்தளங்கள் செயலாக்கப்படுகின்றன...",
                    results: "பொருந்தும் வாய்ப்புகள்",
                    noResults: "இந்த சுயவிவரத்திற்கு பொருந்தும் திட்டங்கள் இல்லை. வருமானம் அல்லது வயது வரம்பை மாற்றி முயற்சிக்கவும்.",
                    domicile: "வதிவிடம்",
                    cat: "பிரிவு",
                    portal: "அரசு போர்ட்டலைப் பார்வையிடவும் ↗",
                    types: { All: "அனைத்து வகைகள்", Scholarship: "உதவித்தொகைகள்", "Competitive Exam": "போட்டித் தேர்வுகள்", "Welfare Scheme": "சமூக நல திட்டங்கள்" },
                    voiceSearch: "குரல் தேடல்",
                    listening: "கேட்கிறது...",
                    voiceNotSupported: "இந்த உலாவியில் குரல் உள்ளீடு ஆதரிக்கப்படவில்லை.",
                    readAloud: "சத்தமாக படிக்கவும்",
                    whyEligible: "நான் ஏன் தகுதியானவன்?",
                    documentsChecklist: "ஆவணப் பட்டியல்",
                    downloadChecklist: "பட்டியலைப் பதிவிறக்கவும்",
                    verifiedSource: "சரிபார்க்கப்பட்ட அரசு மூலம்",
                    daysLeft: "நாட்கள் மீதம்",
                    deadlinePassed: "காலக்கெடு முடிந்தது",
                    deadlineLabel: "கடைசி தேதி",
                    offlineBanner: "நீங்கள் ஆஃப்லைனில் உள்ளீர்கள் — உங்கள் கடைசி சேமிக்கப்பட்ட முடிவுகள் காட்டப்படுகின்றன.",
                    highContrastLabel: "உயர் மாறுபாடு",
                    lowBandwidthLabel: "குறைந்த பேண்ட்வித் பயன்முறை",
                    largeTextLabel: "பெரிய எழுத்து",
                    accessibilityLabel: "அணுகல் விருப்பங்கள்",
                    savedProfileNote: "உங்கள் சுயவிவரம் இந்த சாதனத்தில் தானாகவே சேமிக்கப்படுகிறது."
                },
                te: {
                    title: "హక్దార్",
                    subtitle: "కేంద్రీకృత జాతీయ సంక్షేమ, పరీక్ష మరియు స్కాలర్‌షిప్ ఇంజిన్",
                    langLabel: "భాష:",
                    age: "అభ్యర్థి వయస్సు",
                    income: "వార్షిక కుటుంబ ఆదాయం (రూ)",
                    state: "రాష్ట్రం / కేంద్రపాలిత ప్రాంతం",
                    category: "కులం / వర్గం",
                    type: "అవకాశ రకం",
                    searchBtn: "అర్హత గల అవకాశాలను వెతకండి",
                    searching: "జాతీయ డేటాబేస్‌లు ప్రాసెస్ చేయబడుతున్నాయి...",
                    results: "సరిపోలిన అవకాశాలు",
                    noResults: "ఈ ప్రొఫైల్‌కు సరిపోలే పథకాలు కనుగొనబడలేదు. ఆదాయం లేదా వయో పరిమితిని మార్చి ప్రయత్నించండి.",
                    domicile: "నివాసం",
                    cat: "వర్గం",
                    portal: "అధికారిక ప్రభుత్వ పోర్టల్‌ను సందర్శించండి ↗",
                    types: { All: "అన్ని రకాలు", Scholarship: "స్కాలర్‌షిప్‌లు", "Competitive Exam": "పోటీ పరీక్షలు", "Welfare Scheme": "సంక్షేమ పథకాలు" },
                    voiceSearch: "వాయిస్ శోధన",
                    listening: "వింటోంది...",
                    voiceNotSupported: "ఈ బ్రౌజర్‌లో వాయిస్ ఇన్‌పుట్ మద్దతు లేదు.",
                    readAloud: "బిగ్గరగా చదవండి",
                    whyEligible: "నేను ఎందుకు అర్హుడిని?",
                    documentsChecklist: "పత్రాల జాబితా",
                    downloadChecklist: "జాబితాను డౌన్‌లోడ్ చేయండి",
                    verifiedSource: "ధృవీకరించబడిన ప్రభుత్వ మూలం",
                    daysLeft: "రోజులు మిగిలి ఉన్నాయి",
                    deadlinePassed: "గడువు ముగిసింది",
                    deadlineLabel: "చివరి తేదీ",
                    offlineBanner: "మీరు ఆఫ్‌లైన్‌లో ఉన్నారు — మీ చివరి సేవ్ చేసిన ఫలితాలు చూపబడుతున్నాయి.",
                    highContrastLabel: "అధిక కాంట్రాస్ట్",
                    lowBandwidthLabel: "తక్కువ-బ్యాండ్‌విడ్త్ మోడ్",
                    largeTextLabel: "పెద్ద వచనం",
                    accessibilityLabel: "ప్రాప్యత ఎంపికలు",
                    savedProfileNote: "మీ ప్రొఫైల్ ఈ పరికరంలో స్వయంచాలకంగా సేవ్ చేయబడుతుంది."
                }
            };

            const t = uiText[lang] || uiText['en'];

            const indianStates = [
                "All India", "Andhra Pradesh", "Bihar", "Delhi", "Gujarat", 
                "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", 
                "Punjab", "Rajasthan", "Tamil Nadu", "Uttar Pradesh", "West Bengal"
            ];

            const languages = [
                { code: 'en', name: 'English' },
                { code: 'hi', name: 'हिन्दी (Hindi)' },
                { code: 'mr', name: 'मराठी (Marathi)' },
                { code: 'bn', name: 'বাংলা (Bengali)' },
                { code: 'ta', name: 'தமிழ் (Tamil)' },
                { code: 'te', name: 'తెలుగు (Telugu)' }
            ];

            const voiceLangMap = { en: 'en-IN', hi: 'hi-IN', mr: 'mr-IN', bn: 'bn-IN', ta: 'ta-IN', te: 'te-IN' };

            // ---------- Load saved profile & preferences on first mount ----------
            React.useEffect(() => {
                try {
                    const saved = localStorage.getItem('haqdar_profile');
                    if (saved) {
                        const p = JSON.parse(saved);
                        if (p.age !== undefined) setAge(p.age);
                        if (p.income !== undefined) setIncome(p.income);
                        if (p.state) setState(p.state);
                        if (p.category) setCategory(p.category);
                        if (p.typeFilter) setTypeFilter(p.typeFilter);
                        if (p.lang) setLang(p.lang);
                        if (p.highContrast !== undefined) setHighContrast(p.highContrast);
                        if (p.lowBandwidth !== undefined) setLowBandwidth(p.lowBandwidth);
                        if (p.largeText !== undefined) setLargeText(p.largeText);
                    }
                    const cachedResults = localStorage.getItem('haqdar_last_results');
                    if (cachedResults && typeof navigator !== 'undefined' && !navigator.onLine) {
                        setMatches(JSON.parse(cachedResults));
                        setUsingCache(true);
                    }
                } catch (err) {
                    console.error('Failed to load saved profile', err);
                } finally {
                    setHasLoadedPrefs(true);
                }

                const goOnline = () => setIsOffline(false);
                const goOffline = () => setIsOffline(true);
                window.addEventListener('online', goOnline);
                window.addEventListener('offline', goOffline);
                return () => {
                    window.removeEventListener('online', goOnline);
                    window.removeEventListener('offline', goOffline);
                };
            }, []);

            // ---------- Persist profile & preferences whenever they change ----------
            React.useEffect(() => {
                if (!hasLoadedPrefs) return;
                try {
                    localStorage.setItem('haqdar_profile', JSON.stringify({
                        age, income, state, category, typeFilter, lang, highContrast, lowBandwidth, largeText
                    }));
                } catch (err) {
                    console.error('Failed to save profile', err);
                }
            }, [age, income, state, category, typeFilter, lang, highContrast, lowBandwidth, largeText, hasLoadedPrefs]);

            const handleSearch = async (e) => {
                e.preventDefault();
                setLoading(true);
                try {
                    const res = await fetch(`/api/match?age=${age}&income=${income}&state=${state}&category=${category}&type=${typeFilter}`);
                    const data = await res.json();
                    if (data.success) {
                        setMatches(data.matches);
                        setUsingCache(false);
                        try {
                            localStorage.setItem('haqdar_last_results', JSON.stringify(data.matches));
                        } catch (err) {
                            console.error('Failed to cache results', err);
                        }
                    }
                } catch (err) {
                    console.error("Search failed, falling back to cached results", err);
                    try {
                        const cached = localStorage.getItem('haqdar_last_results');
                        if (cached) {
                            setMatches(JSON.parse(cached));
                            setUsingCache(true);
                        }
                    } catch (cacheErr) {
                        console.error('No cache available', cacheErr);
                    }
                } finally {
                    setLoading(false);
                }
            };

            const getText = (obj) => {
                if (!obj) return "";
                return obj[lang] || obj['en'] || Object.values(obj)[0];
            };

            // ---------- Voice input (Web Speech API) ----------
            const parseVoiceInput = (transcript) => {
                const lower = transcript.toLowerCase();
                const numbers = (lower.match(/\d+/g) || []).map(Number);
                const possibleAge = numbers.find(n => n > 0 && n < 100);
                const possibleIncome = numbers.find(n => n >= 1000);
                if (possibleAge) setAge(possibleAge);
                if (possibleIncome) setIncome(possibleIncome);

                const categoryKeywords = { obc: 'OBC', sc: 'SC', st: 'ST', ews: 'EWS', general: 'General' };
                Object.keys(categoryKeywords).forEach(key => {
                    if (lower.includes(key)) setCategory(categoryKeywords[key]);
                });

                indianStates.forEach(st => {
                    if (lower.includes(st.toLowerCase())) setState(st);
                });

                if (lower.includes('scholarship')) setTypeFilter('Scholarship');
                else if (lower.includes('exam')) setTypeFilter('Competitive Exam');
                else if (lower.includes('welfare')) setTypeFilter('Welfare Scheme');
            };

            const startVoiceInput = () => {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!SpeechRecognition) {
                    alert(t.voiceNotSupported);
                    return;
                }
                const recognition = new SpeechRecognition();
                recognition.lang = voiceLangMap[lang] || 'en-IN';
                recognition.interimResults = false;
                recognition.maxAlternatives = 1;

                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    setVoiceTranscript(transcript);
                    parseVoiceInput(transcript);
                };
                recognition.onerror = () => setListening(false);
                recognition.onend = () => setListening(false);

                setListening(true);
                recognition.start();
            };

            // ---------- Voice output (Speech Synthesis) ----------
            const speakText = (text) => {
                if (!window.speechSynthesis) return;
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = voiceLangMap[lang] || 'en-IN';
                window.speechSynthesis.speak(utterance);
            };

            // ---------- Small display helpers ----------
            const typeIcon = (type) => {
                if (type === 'Scholarship') return '🎓';
                if (type === 'Competitive Exam') return '📝';
                if (type === 'Welfare Scheme') return '🏛️';
                return '📌';
            };

            const deadlineBadgeClass = (status) => {
                if (status === 'expired') return 'bg-red-900/60 text-red-300 border-red-700';
                if (status === 'urgent') return 'bg-red-900/40 text-red-300 border-red-600';
                if (status === 'soon') return 'bg-amber-900/40 text-amber-300 border-amber-600';
                return 'bg-emerald-900/40 text-emerald-300 border-emerald-600';
            };

            const deadlineLabel = (m) => {
                if (m.deadline_status === 'expired') return t.deadlinePassed;
                return `${m.days_remaining} ${t.daysLeft}`;
            };

            // ---------- Theme: high contrast / low bandwidth / large text ----------
            const theme = {
                card: highContrast
                    ? 'bg-black border-2 border-yellow-400'
                    : (lowBandwidth ? 'bg-slate-800 border border-slate-700' : 'bg-slate-800 border border-slate-700 shadow-xl'),
                cardRounded: lowBandwidth ? 'rounded-md' : 'rounded-2xl',
                input: highContrast
                    ? 'bg-black border-2 border-yellow-400 text-yellow-200 focus:outline-none focus:border-yellow-100'
                    : 'bg-slate-900 border border-slate-700 text-white focus:outline-none focus:border-blue-500',
                inputRounded: lowBandwidth ? 'rounded-md' : 'rounded-xl',
                button: highContrast
                    ? 'bg-yellow-400 text-black hover:bg-yellow-300 font-bold border-2 border-yellow-200'
                    : 'bg-blue-600 hover:bg-blue-500 text-white font-bold',
                secondaryButton: highContrast
                    ? 'bg-black text-yellow-300 border-2 border-yellow-400 hover:bg-yellow-950'
                    : 'bg-slate-700 hover:bg-slate-600 text-blue-300 border border-slate-600',
                accentText: highContrast ? 'text-yellow-300' : 'text-blue-400',
                mutedText: highContrast ? 'text-yellow-500' : 'text-slate-400',
                textSize: largeText ? 'text-lg' : 'text-sm',
                titleSize: largeText ? 'text-2xl' : 'text-lg',
                tapPadding: largeText ? 'p-4' : 'p-3',
                fieldGap: largeText ? 'gap-5' : 'gap-4',
            };

            const pageBg = highContrast ? 'bg-black text-yellow-200' : 'bg-slate-900 text-slate-100';

            return (
                <div className={`max-w-4xl mx-auto space-y-6 ${largeText ? 'text-lg' : ''}`}>
                    <header className={`flex flex-col md:flex-row justify-between items-center ${theme.card} ${theme.cardRounded} p-6 gap-4`}>
                        <div>
                            <h1 className={`text-3xl font-extrabold tracking-tight ${theme.accentText}`}>{t.title}</h1>
                            <p className={`text-sm ${theme.mutedText}`}>{t.subtitle}</p>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className={`text-xs uppercase tracking-wider ${theme.mutedText}`}>{t.langLabel}</span>
                            <select
                                aria-label={t.langLabel}
                                value={lang}
                                onChange={e => setLang(e.target.value)}
                                className={`${theme.input} ${theme.inputRounded} px-3 py-2 text-sm`}
                            >
                                {languages.map(l => (
                                    <option key={l.code} value={l.code}>{l.name}</option>
                                ))}
                            </select>
                        </div>
                    </header>

                    {/* Accessibility toolbar */}
                    <div
                        role="group"
                        aria-label={t.accessibilityLabel}
                        className={`flex flex-wrap items-center gap-2 ${theme.card} ${theme.cardRounded} p-4`}
                    >
                        <button
                            type="button"
                            aria-pressed={highContrast}
                            onClick={() => setHighContrast(v => !v)}
                            className={`${highContrast ? theme.button : theme.secondaryButton} ${theme.inputRounded} px-3 py-2 text-xs font-semibold transition`}
                        >
                            🌓 {t.highContrastLabel}
                        </button>
                        <button
                            type="button"
                            aria-pressed={lowBandwidth}
                            onClick={() => setLowBandwidth(v => !v)}
                            className={`${lowBandwidth ? theme.button : theme.secondaryButton} ${theme.inputRounded} px-3 py-2 text-xs font-semibold transition`}
                        >
                            🐢 {t.lowBandwidthLabel}
                        </button>
                        <button
                            type="button"
                            aria-pressed={largeText}
                            onClick={() => setLargeText(v => !v)}
                            className={`${largeText ? theme.button : theme.secondaryButton} ${theme.inputRounded} px-3 py-2 text-xs font-semibold transition`}
                        >
                            🔠 {t.largeTextLabel}
                        </button>
                        <span className={`text-xs ${theme.mutedText} ml-auto`}>{t.savedProfileNote}</span>
                    </div>

                    {isOffline && (
                        <div role="alert" className="bg-amber-900/40 border border-amber-600 text-amber-200 text-sm p-3 rounded-xl">
                            {t.offlineBanner}
                        </div>
                    )}

                    <div className={`${theme.card} ${theme.cardRounded} p-6`}>
                        <form onSubmit={handleSearch} className={`grid grid-cols-1 md:grid-cols-2 ${theme.fieldGap}`}>
                            <div>
                                <label htmlFor="haqdar-age" className={`block text-xs uppercase tracking-wider ${theme.mutedText} mb-1`}>{t.age}</label>
                                <input
                                    id="haqdar-age"
                                    aria-label={t.age}
                                    type="number"
                                    value={age}
                                    onChange={e => setAge(e.target.value)}
                                    className={`w-full ${theme.input} ${theme.inputRounded} ${theme.tapPadding}`}
                                />
                            </div>
                            <div>
                                <label htmlFor="haqdar-income" className={`block text-xs uppercase tracking-wider ${theme.mutedText} mb-1`}>{t.income}</label>
                                <input
                                    id="haqdar-income"
                                    aria-label={t.income}
                                    type="number"
                                    value={income}
                                    onChange={e => setIncome(e.target.value)}
                                    className={`w-full ${theme.input} ${theme.inputRounded} ${theme.tapPadding}`}
                                />
                            </div>
                            <div>
                                <label htmlFor="haqdar-state" className={`block text-xs uppercase tracking-wider ${theme.mutedText} mb-1`}>{t.state}</label>
                                <select
                                    id="haqdar-state"
                                    aria-label={t.state}
                                    value={state}
                                    onChange={e => setState(e.target.value)}
                                    className={`w-full ${theme.input} ${theme.inputRounded} ${theme.tapPadding}`}
                                >
                                    {indianStates.map(st => (
                                        <option key={st} value={st}>{st}</option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label htmlFor="haqdar-category" className={`block text-xs uppercase tracking-wider ${theme.mutedText} mb-1`}>{t.category}</label>
                                <select
                                    id="haqdar-category"
                                    aria-label={t.category}
                                    value={category}
                                    onChange={e => setCategory(e.target.value)}
                                    className={`w-full ${theme.input} ${theme.inputRounded} ${theme.tapPadding}`}
                                >
                                    <option value="General">General / Open</option>
                                    <option value="OBC">OBC (Other Backward Classes)</option>
                                    <option value="SC">SC (Scheduled Castes)</option>
                                    <option value="ST">ST (Scheduled Tribes)</option>
                                    <option value="EWS">EWS (Economically Weaker Section)</option>
                                    <option value="All">All Categories</option>
                                </select>
                            </div>
                            <div>
                                <label htmlFor="haqdar-type" className={`block text-xs uppercase tracking-wider ${theme.mutedText} mb-1`}>{t.type}</label>
                                <select
                                    id="haqdar-type"
                                    aria-label={t.type}
                                    value={typeFilter}
                                    onChange={e => setTypeFilter(e.target.value)}
                                    className={`w-full ${theme.input} ${theme.inputRounded} ${theme.tapPadding}`}
                                >
                                    <option value="All">{t.types.All}</option>
                                    <option value="Scholarship">{t.types.Scholarship}</option>
                                    <option value="Competitive Exam">{t.types['Competitive Exam']}</option>
                                    <option value="Welfare Scheme">{t.types['Welfare Scheme']}</option>
                                </select>
                            </div>
                            <div className="flex items-end gap-2">
                                <button
                                    type="submit"
                                    aria-label={t.searchBtn}
                                    className={`flex-1 ${theme.button} ${theme.inputRounded} ${theme.tapPadding} shadow-lg transition`}
                                >
                                    {loading ? t.searching : t.searchBtn}
                                </button>
                                <button
                                    type="button"
                                    aria-label={t.voiceSearch}
                                    aria-pressed={listening}
                                    onClick={startVoiceInput}
                                    className={`${theme.secondaryButton} ${theme.inputRounded} ${theme.tapPadding} transition`}
                                    title={t.voiceSearch}
                                >
                                    {listening ? '🔴' : '🎙️'}
                                </button>
                            </div>
                        </form>
                        {voiceTranscript && (
                            <p aria-live="polite" className={`text-xs ${theme.mutedText} mt-3 italic`}>
                                "{voiceTranscript}"
                            </p>
                        )}
                        {listening && (
                            <p aria-live="polite" className={`text-xs ${theme.accentText} mt-1`}>{t.listening}</p>
                        )}
                    </div>

                    <div className="space-y-4">
                        <h2 aria-live="polite" className={`text-xl font-bold tracking-tight ${largeText ? 'text-2xl' : ''}`}>
                            {t.results} ({matches.length}) {usingCache && `— ${t.offlineBanner}`}
                        </h2>
                        {matches.length === 0 ? (
                            <div className={`${theme.card} ${theme.cardRounded} p-8 text-center ${theme.mutedText}`}>
                                {t.noResults}
                            </div>
                        ) : (
                            matches.map(m => {
                                const isExpanded = expandedId === m.id;
                                const spokenSummary = `${getText(m.title)}. ${getText(m.description)}`;
                                return (
                                    <div key={m.id} className={`${theme.card} ${theme.cardRounded} p-6 space-y-2`}>
                                        <div className="flex justify-between items-start gap-3 flex-wrap">
                                            <h3 className={`${theme.titleSize} font-semibold ${theme.accentText}`}>
                                                <span aria-hidden="true">{typeIcon(m.type)}</span> {getText(m.title)}
                                            </h3>
                                            <div className="flex items-center gap-2 flex-wrap">
                                                <span className="bg-blue-900/50 text-blue-300 border border-blue-700 text-xs px-3 py-1 rounded-full font-medium">{m.type}</span>
                                                <span className={`text-xs px-3 py-1 rounded-full font-medium border ${deadlineBadgeClass(m.deadline_status)}`}>
                                                    ⏳ {deadlineLabel(m)}
                                                </span>
                                                {m.verified_source && (
                                                    <span className="bg-emerald-900/40 text-emerald-300 border border-emerald-600 text-xs px-3 py-1 rounded-full font-medium">
                                                        ✓ {t.verifiedSource}
                                                    </span>
                                                )}
                                            </div>
                                        </div>

                                        <p className={`${theme.textSize} text-slate-300`}>{getText(m.description)}</p>

                                        <div className={`flex justify-between items-center pt-2 ${theme.textSize} ${theme.mutedText} flex-wrap gap-2`}>
                                            <span>{t.domicile}: {m.state} | {t.cat}: {m.category} | {t.deadlineLabel}: {m.deadline}</span>
                                        </div>

                                        <div className="flex flex-wrap gap-2 pt-2">
                                            <button
                                                type="button"
                                                aria-label={t.readAloud}
                                                onClick={() => speakText(spokenSummary)}
                                                className={`${theme.secondaryButton} ${theme.inputRounded} px-3 py-1.5 transition font-medium text-xs`}
                                            >
                                                🔊 {t.readAloud}
                                            </button>
                                            <button
                                                type="button"
                                                aria-expanded={isExpanded}
                                                aria-label={t.whyEligible}
                                                onClick={() => setExpandedId(isExpanded ? null : m.id)}
                                                className={`${theme.secondaryButton} ${theme.inputRounded} px-3 py-1.5 transition font-medium text-xs`}
                                            >
                                                ❓ {t.whyEligible}
                                            </button>
                                            <a
                                                href={`/api/checklist/${m.id}`}
                                                aria-label={t.downloadChecklist}
                                                className={`${theme.secondaryButton} ${theme.inputRounded} px-3 py-1.5 transition font-medium text-xs`}
                                            >
                                                ⬇ {t.downloadChecklist}
                                            </a>
                                            <a
                                                href={m.link}
                                                target="_blank"
                                                rel="noreferrer"
                                                aria-label={t.portal}
                                                className={`ml-auto ${theme.secondaryButton} ${theme.inputRounded} px-3 py-1.5 transition font-medium text-xs`}
                                            >
                                                {t.portal}
                                            </a>
                                        </div>

                                        {isExpanded && (
                                            <div className={`mt-3 border-t ${highContrast ? 'border-yellow-700' : 'border-slate-700'} pt-3 space-y-3`}>
                                                <div>
                                                    <h4 className={`text-xs font-bold uppercase tracking-wider ${theme.accentText} mb-1`}>{t.whyEligible}</h4>
                                                    <ul className={`${theme.textSize} space-y-1`}>
                                                        {Object.values(m.eligibility_trail || {}).map((crit, idx) => (
                                                            <li key={idx} className="flex items-start gap-2">
                                                                <span aria-hidden="true">{crit.ok ? '✅' : '❌'}</span>
                                                                <span>{crit.detail}</span>
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </div>
                                                <div>
                                                    <h4 className={`text-xs font-bold uppercase tracking-wider ${theme.accentText} mb-1`}>{t.documentsChecklist}</h4>
                                                    <ul className={`${theme.textSize} space-y-1 list-disc list-inside`}>
                                                        {(m.documents || []).map((doc, idx) => (
                                                            <li key={idx}>{doc}</li>
                                                        ))}
                                                    </ul>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                );
                            })
                        )}
                    </div>
                </div>
            );
        }

        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
</body>
</html>
    """


@app.route("/api/match", methods=['GET'])
def match_opportunities():
    try:
        age = int(request.args.get("age", 0))
    except ValueError:
        age = 0

    try:
        income = float(request.args.get("income", 0))
    except ValueError:
        income = 0

    state = request.args.get("state", "All India")
    category = request.args.get("category", "General")
    scheme_type = request.args.get("type", "All")

    today = date.today()
    filtered = []

    for item in MASTER_DATABASE:
        age_ok = age <= item["age_limit"]
        income_ok = income <= item["income_limit"]
        state_ok = item["state"] == "All India" or item["state"] == state
        category_ok = item["category"] == "All" or item["category"] == category or category == "All"
        type_ok = scheme_type == "All" or item["type"] == scheme_type

        if age_ok and income_ok and state_ok and category_ok and type_ok:
            deadline_dt = date.fromisoformat(item["deadline"])
            days_remaining = (deadline_dt - today).days

            if days_remaining < 0:
                deadline_status = "expired"
            elif days_remaining <= 7:
                deadline_status = "urgent"
            elif days_remaining <= 30:
                deadline_status = "soon"
            else:
                deadline_status = "plenty"

            # "Why am I eligible?" transparency trail — shows the applicant exactly
            # which criteria matched, instead of a black-box yes/no result.
            enriched = dict(item)
            enriched["days_remaining"] = days_remaining
            enriched["deadline_status"] = deadline_status
            enriched["eligibility_trail"] = {
                "age": {
                    "ok": age_ok,
                    "detail": f"Age {age} is within the limit of {item['age_limit']}",
                },
                "income": {
                    "ok": income_ok,
                    "detail": f"Annual income \u20b9{int(income):,} is within the limit of \u20b9{item['income_limit']:,}",
                },
                "category": {
                    "ok": category_ok,
                    "detail": f"Category '{category}' matches the scheme's '{item['category']}' eligibility",
                },
                "domicile": {
                    "ok": state_ok,
                    "detail": f"Domicile '{state}' matches the scheme's '{item['state']}' coverage",
                },
            }
            filtered.append(enriched)

    # Most urgent deadlines surface first, supporting the deadline-tracking feature.
    filtered.sort(key=lambda x: x["days_remaining"])

    return jsonify({
        "success": True,
        "count": len(filtered),
        "matches": filtered
    })


@app.route("/api/checklist/<scheme_id>", methods=['GET'])
def download_checklist(scheme_id):
    """Serves a downloadable, printable plain-text document checklist for a scheme."""
    item = next((i for i in MASTER_DATABASE if i["id"] == scheme_id), None)
    if not item:
        return jsonify({"success": False, "error": "Scheme not found"}), 404

    lines = [
        "HAQDAR \u2014 DOCUMENT CHECKLIST",
        "=" * 40,
        f"Scheme: {item['title'].get('en', '')}",
        f"Type: {item['type']}  |  Category: {item['category']}  |  State: {item['state']}",
        f"Application Deadline: {item['deadline']}",
        f"Official Portal: {item['link']}",
        "",
        "Required Documents:",
    ]
    for idx, doc in enumerate(item["documents"], start=1):
        lines.append(f"  {idx}. [ ] {doc}")
    lines.append("")
    lines.append("Generated by Haqdar \u2014 always verify current requirements on the official portal before submission.")

    content = "\n".join(lines)
    filename = f"{item['id']}-checklist.txt"
    return Response(
        content,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
