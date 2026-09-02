from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Comprehensive Master Mock Database covering States, Welfare, Scholarships, and Exams
MASTER_DATABASE = [
    {
        "id": "unia-01",
        "title": {
            "en": "UPSC Civil Services Examination Support & Fee Exemption",
            "hi": "यूपीएससी सिविल सेवा परीक्षा सहायता और शुल्क छूट",
            "mr": "यूपीएससी नागरी सेवा परीक्षा सहाय्य आणि शुल्क सूट"
        },
        "category": "All",
        "state": "All India",
        "type": "Competitive Exam",
        "age_limit": 32,
        "income_limit": 800000,
        "description": {
            "en": "National level examination for civil services with fee waivers for reserved categories.",
            "hi": "आरक्षित वर्ग के लिए शुल्क छूट के साथ सिविल सेवाओं के लिए राष्ट्रीय स्तर की परीक्षा।",
            "mr": "राखीव वर्गासाठी शुल्क माफीसह नागरी सेवांसाठी राष्ट्रीय स्तरावरील परीक्षा।"
        },
        "link": "https://upsc.gov.in/"
    },
    {
        "id": "unish-02",
        "title": {
            "en": "National Scholarship Portal (NSP) Higher Education Scheme",
            "hi": "राष्ट्रीय छात्रवृत्ति पोर्टल उच्च शिक्षा योजना",
            "mr": "राष्ट्रीय शिष्यवृत्ती पोर्टल उच्च शिक्षण योजना"
        },
        "category": "All",
        "state": "All India",
        "type": "Scholarship",
        "age_limit": 25,
        "income_limit": 450000,
        "description": {
            "en": "Central sector scholarship for college and university students.",
            "hi": "कॉलेज और विश्वविद्यालय के छात्रों के लिए केंद्रीय क्षेत्र की छात्रवृत्ति।",
            "mr": "कॉलेज आणि विद्यापीठ विद्यार्थ्यांसाठी केंद्रीय क्षेत्र शिष्यवृत्ती।"
        },
        "link": "https://scholarships.gov.in/"
    },
    {
        "id": "uniw-03",
        "title": {
            "en": "Pradhan Mantri Awas Yojana (PMAY) - Housing for All",
            "hi": "प्रधानमंत्री आवास योजना (पीएमएवाई) - सभी के लिए आवास",
            "mr": "प्रधानमंत्री आवास योजना (पीएमएवाय) - सर्वांसाठी घरे"
        },
        "category": "All",
        "state": "All India",
        "type": "Welfare Scheme",
        "age_limit": 70,
        "income_limit": 600000,
        "description": {
            "en": "Central credit-linked subsidy scheme for building or buying affordable houses.",
            "hi": "किफायती मकान बनाने या खरीदने के लिए केंद्रीय ऋण-संबद्ध सब्सिडी योजना।",
            "mr": "परवडणारी घरे बांधण्यासाठी किंवा खरेदी करण्यासाठी केंद्रीय अनुदान योजना।"
        },
        "link": "https://pmaymis.gov.in/"
    },
    {
        "id": "mah-04",
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
            "en": "State-backed financial assistance for post-matriculation studies in Maharashtra.",
            "hi": "महाराष्ट्र में पोस्ट-मैट्रिक पढ़ाई के लिए राज्य समर्थित वित्तीय सहायता।",
            "mr": "महाराष्ट्रातील उत्तर-मॅट्रिक अभ्यासासाठी राज्य-समर्थित आर्थिक सहाय्य."
        },
        "link": "https://mahadbtmahadbt.gov.in/"
    },
    {
        "id": "mah-05",
        "title": {
            "en": "Mahatma Jyotirao Phule Jan Arogya Yojana (Health Insurance)",
            "hi": "महात्मा ज्योतिराव फुले जन आरोग्य योजना (स्वास्थ्य बीमा)",
            "mr": "महात्मा ज्योतिराव फुले जन आरोग्य योजना"
        },
        "category": "All",
        "state": "Maharashtra",
        "type": "Welfare Scheme",
        "age_limit": 99,
        "income_limit": 1000000,
        "description": {
            "en": "Cashless health insurance coverage for eligible families in Maharashtra.",
            "hi": "महाराष्ट्र में पात्र परिवारों के लिए कैशलेस स्वास्थ्य बीमा कवरेज।",
            "mr": "महाराष्ट्रातील पात्र कुटुंबांसाठी कॅशलेस आरोग्य विमा संरक्षण."
        },
        "link": "https://www.jeevandayee.gov.in/"
    },
    {
        "id": "up-06",
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
            "en": "Research and governance fellowship supporting young professionals in UP.",
            "hi": "यूपी में युवा पेशेवरों का समर्थन करने वाली अनुसंधान और शासन फेलोशिप।",
            "mr": "यूपीमधील तरुण व्यावसायिकांचे समर्थन करणारी संशोधन आणि प्रशासन शिष्यवृत्ती."
        },
        "link": "https://up.gov.in/"
    },
    {
        "id": "up-07",
        "title": {
            "en": "UP Matritva Sahyog Yojana (Maternity Welfare)",
            "hi": "यूपी मातृत्व सहयोग योजना (मातृत्व कल्याण)",
            "mr": "यूपी मातृत्व सहयोग योजना"
        },
        "category": "All",
        "state": "Uttar Pradesh",
        "type": "Welfare Scheme",
        "age_limit": 45,
        "income_limit": 300000,
        "description": {
            "en": "Financial assistance for pregnant and lactating mothers for health nutrition.",
            "hi": "स्वास्थ्य पोषण के लिए गर्भवती और स्तनपान कराने वाली माताओं के लिए वित्तीय सहायता।",
            "mr": "आरोग्य पोषणासाठी गर्भवती आणि स्तनपान करणाऱ्या मातांना आर्थिक मदत."
        },
        "link": "https://up.gov.in/"
    },
    {
        "id": "del-08",
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
            "en": "Education loan scheme backed by the Delhi government for higher studies.",
            "hi": "उच्च अध्ययन के लिए दिल्ली सरकार द्वारा समर्थित शिक्षा ऋण योजना।",
            "mr": "उच्च अभ्यासासाठी दिल्ली सरकारद्वारे समर्थित शिक्षण कर्ज योजना."
        },
        "link": "https://delhi.gov.in/"
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
            const [income, setIncome] = React.useState(200000);
            const [state, setState] = React.useState('Maharashtra');
            const [category, setCategory] = React.useState('General');
            const [typeFilter, setTypeFilter] = React.useState('All');
            const [matches, setMatches] = React.useState([]);
            const [loading, setLoading] = React.useState(false);

            // UI Translation Dictionary
            const uiText = {
                en: {
                    title: "Haqdar",
                    subtitle: "All-India Schemes, Exams & Scholarships Engine",
                    langLabel: "Language:",
                    age: "Age",
                    income: "Annual Income (INR)",
                    state: "State / UT",
                    category: "Caste / Category",
                    type: "Opportunity Type",
                    searchBtn: "Find All Eligible Opportunities",
                    searching: "Scanning Policies...",
                    results: "Eligible Opportunities",
                    noResults: "No opportunities loaded yet. Run a search above.",
                    domicile: "Domicile",
                    cat: "Category",
                    portal: "Official Portal ↗",
                    types: { All: "All Types", Scholarship: "Scholarship", "Competitive Exam": "Competitive Exam", "Welfare Scheme": "Social Welfare Scheme" }
                },
                hi: {
                    title: "हक़दार",
                    subtitle: "अखिल भारतीय योजनाएं, परीक्षाएं और छात्रवृत्ति इंजन",
                    langLabel: "भाषा:",
                    age: "आयु",
                    income: "वार्षिक आय (रुपये)",
                    state: "राज्य / केंद्र शासित प्रदेश",
                    category: "जाति / श्रेणी",
                    type: "अवसर का प्रकार",
                    searchBtn: "सभी पात्र अवसर खोजें",
                    searching: "नीतियों की जाँच हो रही है...",
                    results: "पात्र अवसर",
                    noResults: "अभी तक कोई अवसर लोड नहीं हुआ है। ऊपर खोज चलाएं।",
                    domicile: "मूल निवास",
                    cat: "श्रेणी",
                    portal: "आधिकारिक पोर्टल ↗",
                    types: { All: "सभी प्रकार", Scholarship: "छात्रवृत्ति", "Competitive Exam": "प्रतियोगी परीक्षा", "Welfare Scheme": "सामाजिक कल्याण योजना" }
                },
                mr: {
                    title: "हक्दार",
                    subtitle: "अखिल भारतीय योजना, परीक्षा आणि शिष्यवृत्ती इंजिन",
                    langLabel: "भाषा:",
                    age: "वय",
                    income: "वार्षिक उत्पन्न (रुपये)",
                    state: "राज्य / केंद्रशासित प्रदेश",
                    category: "जात / प्रवर्ग",
                    type: "संधीचा प्रकार",
                    searchBtn: "सर्व पात्र संधी शोधा",
                    searching: "धोरणांची तपासणी होत आहे...",
                    results: "पात्र संधी",
                    noResults: "अद्याप कोणतीही संधी लोड केलेली नाही. वर शोध चालवा.",
                    domicile: "अधिवास",
                    cat: "प्रवर्ग",
                    portal: "अधिकृत संकेतस्थळ ↗",
                    types: { All: "सर्व प्रकार", Scholarship: "शिष्यवृत्ती", "Competitive Exam": "स्पर्धा परीक्षा", "Welfare Scheme": "समाज कल्याण योजना" }
                }
            };

            const t = uiText[lang] || uiText['en'];

            // All 28 States & 8 UTs of India
            const indianStates = [
                "All India", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", 
                "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", 
                "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", 
                "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
                "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", 
                "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands", 
                "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", 
                "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
            ];

            const languages = [
                { code: 'en', name: 'English' },
                { code: 'hi', name: 'हिन्दी (Hindi)' },
                { code: 'mr', name: 'मराठी (Marathi)' },
                { code: 'bn', name: 'বাংলা (Bengali)' },
                { code: 'te', name: 'తెలుగు (Telugu)' },
                { code: 'ta', name: 'தமிழ் (Tamil)' },
                { code: 'gu', name: 'ગુજરાતી (Gujarati)' },
                { code: 'kn', name: 'ಕನ್ನಡ (Kannada)' },
                { code: 'pa', name: 'ਪੰਜਾਬੀ (Punjabi)' }
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
        # Check eligibility limits
        if age <= item["age_limit"] and income <= item["income_limit"]:
            # Check state matching (All India matches everywhere, or exact state match)
            if item["state"] == "All India" or item["state"] == state:
                # Check category matching
                if item["category"] == "All" or item["category"] == category or category == "All":
                    # Check type filter
                    if scheme_type == "All" or item["type"] == scheme_type:
                        filtered.append(item)

    return jsonify({
        "success": True,
        "count": len(filtered),
        "matches": filtered
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
