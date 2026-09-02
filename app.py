from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Exhaustive Master Database: Comprehensive National + Core State Policies
MASTER_DATABASE = [
    # ==================== ALL INDIA: COMPETITIVE EXAMS & RECRUITMENT ====================
    {
        "id": "nat-exam-01",
        "title": {
            "en": "UPSC Civil Services Examination (CSE) Fee Exemption & Support",
            "hi": "यूपीएससी सिविल सेवा परीक्षा (CSE) शुल्क छूट और सहायता",
            "mr": "यूपीएससी नागरी सेवा परीक्षा शुल्क सूट आणि सहाय्य",
            "bn": "ইউপিএসসি সিভিল সার্ভিস পরীক্ষা ফি ছাড় এবং সহায়তা",
            "ta": "யுபிஎஸ்சி குடிமைப்பணி தேர்வு கட்டண விலக்கு மற்றும் ஆதரவு"
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

    # ==================== STATE LEVEL: DELHI ====================
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
    }
]

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

            // Clean, High-Quality UI Localization Dictionaries
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
                    types: { All: "All Types", Scholarship: "Scholarships", "Competitive Exam": "Competitive Exams", "Welfare Scheme": "Social Welfare Schemes" }
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
                    types: { All: "सभी प्रकार", Scholarship: "छात्रवृत्ति", "Competitive Exam": "प्रतियोगी परीक्षाएं", "Welfare Scheme": "सामाजिक कल्याण योजनाएं" }
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
                    types: { All: "सर्व प्रकार", Scholarship: "शिष्यवृत्ती", "Competitive Exam": "स्पर्धा परीक्षा", "Welfare Scheme": "समाज कल्याण योजना" }
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
                { code: 'mr', name: 'मराठी (Marathi)' }
            ];

            const handleSearch = async (e) => {
                e.preventDefault();
                setLoading(true);
                try {
                    const res = await fetch(`/api/match?age=${age}&income=${income}&state=${state}&category=${category}&type=${typeFilter}`);
                    const data = await res.json();
                    if(data.success) {
                        setMatches(data.matches);
                    }
                } catch (err) {
                    console.error("Search failed", err);
                } finally {
                    setLoading(false);
                }
            };

            const getText = (obj) => {
                if (!obj) return "";
                return obj[lang] || obj['en'] || Object.values(obj)[0];
            };

            return (
                <div className="max-w-4xl mx-auto space-y-6">
                    <header className="flex flex-col md:flex-row justify-between items-center bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl gap-4">
                        <div>
                            <h1 className="text-3xl font-extrabold tracking-tight text-blue-400">{t.title}</h1>
                            <p className="text-sm text-slate-400">{t.subtitle}</p>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="text-xs text-slate-400 uppercase tracking-wider">{t.langLabel}</span>
                            <select value={lang} onChange={e => setLang(e.target.value)} className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500">
                                {languages.map(l => (
                                    <option key={l.code} value={l.code}>{l.name}</option>
                                ))}
                            </select>
                        </div>
                    </header>

                    <div className="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl">
                        <form onSubmit={handleSearch} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1">{t.age}</label>
                                <input type="number" value={age} onChange={e => setAge(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500" />
                            </div>
                            <div>
                                <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1">{t.income}</label>
                                <input type="number" value={income} onChange={e => setIncome(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500" />
                            </div>
                            <div>
                                <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1">{t.state}</label>
                                <select value={state} onChange={e => setState(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500">
                                    {indianStates.map(st => (
                                        <option key={st} value={st}>{st}</option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1">{t.category}</label>
                                <select value={category} onChange={e => setCategory(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500">
                                    <option value="General">General / Open</option>
                                    <option value="OBC">OBC (Other Backward Classes)</option>
                                    <option value="SC">SC (Scheduled Castes)</option>
                                    <option value="ST">ST (Scheduled Tribes)</option>
                                    <option value="EWS">EWS (Economically Weaker Section)</option>
                                    <option value="All">All Categories</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1">{t.type}</label>
                                <select value={typeFilter} onChange={e => setTypeFilter(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500">
                                    <option value="All">{t.types.All}</option>
                                    <option value="Scholarship">{t.types.Scholarship}</option>
                                    <option value="Competitive Exam">{t.types['Competitive Exam']}</option>
                                    <option value="Welfare Scheme">{t.types['Welfare Scheme']}</option>
                                </select>
                            </div>
                            <div className="flex items-end">
                                <button type="submit" className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold p-3 rounded-xl transition shadow-lg">
                                    {loading ? t.searching : t.searchBtn}
                                </button>
                            </div>
                        </form>
                    </div>

                    <div className="space-y-4">
                        <h2 className="text-xl font-bold tracking-tight text-slate-200">{t.results} ({matches.length})</h2>
                        {matches.length === 0 ? (
                            <div className="bg-slate-800 p-8 rounded-2xl border border-slate-700 text-center text-slate-400">
                                {t.noResults}
                            </div>
                        ) : (
                            matches.map(m => (
                                <div key={m.id} className="bg-slate-800 p-6 rounded-2xl border border-slate-700 shadow-xl space-y-2">
                                    <div className="flex justify-between items-start">
                                        <h3 className="text-lg font-semibold text-blue-400">{getText(m.title)}</h3>
                                        <span className="bg-blue-900/50 text-blue-300 border border-blue-700 text-xs px-3 py-1 rounded-full font-medium">{m.type}</span>
                                    </div>
                                    <p className="text-sm text-slate-300">{getText(m.description)}</p>
                                    <div className="flex justify-between items-center pt-2 text-xs text-slate-400">
                                        <span>{t.domicile}: {m.state} | {t.cat}: {m.category}</span>
                                        <a href={m.link} target="_blank" rel="noreferrer" className="bg-slate-700 hover:bg-slate-600 text-blue-300 px-3 py-1.5 rounded-lg border border-slate-600 transition font-medium">
                                            {t.portal}
                                        </a>
                                    </div>
                                </div>
                            ))
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

    filtered = []
    for item in MASTER_DATABASE:
        if age <= item["age_limit"] and income <= item["income_limit"]:
            if item["state"] == "All India" or item["state"] == state:
                if item["category"] == "All" or item["category"] == category or category == "All":
                    if scheme_type == "All" or item["type"] == scheme_type:
                        filtered.append(item)

    return jsonify({
        "success": True,
        "count": len(filtered),
        "matches": filtered
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
