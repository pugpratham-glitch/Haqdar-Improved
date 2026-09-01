from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Comprehensive Master Mock Database
MASTER_DATABASE = [
    {
        "id": "unia-01",
        "title": {
            "en": "UPSC Civil Services Examination Support & Fee Exemption",
            "hi": "यूपीएससी सिविल सेवा परीक्षा सहायता और शुल्क छूट",
            "bn": "ইউপিএসসি সিভিল সার্ভিস পরীক্ষা সহায়তা এবং ফি ছাড়",
            "mr": "यूपीएससी नागरी सेवा परीक्षा सहाय्य आणि शुल्क सूट",
            "ta": "யுபிஎஸ்சி குடிமைப்பணி தேர்வு ஆதரவு மற்றும் கட்டண விலக்கு",
            "te": "యూపీఎస్సీ సివిల్ సర్వీసెస్ పరీక్ష మద్దతు మరియు ఫీజు మినహాయింపు"
        },
        "category": "All",
        "state": "All India",
        "type": "Competitive Exam",
        "age_limit": 32,
        "income_limit": 800000,
        "description": {
            "en": "National level examination for civil services with fee waivers for reserved categories.",
            "hi": "आरक्षित वर्ग के लिए शुल्क माफ के साथ सिविल सेवाओं के लिए राष्ट्रीय स्तर की परीक्षा।",
            "bn": "সংরক্ষিত শ্রেণীর জন্য ফি ছাড় সহ সিভিল সার্ভিসের জন্য জাতীয় স্তরের পরীক্ষা।",
            "mr": "राखीव वर्गासाठी शुल्क माफीसह नागरी सेवांसाठी राष्ट्रीय स्तरावरील परीक्षा।"
        },
        "link": "https://upsc.gov.in/"
    },
    {
        "id": "unish-02",
        "title": {
            "en": "National Scholarship Portal (NSP) Higher Education Scheme",
            "hi": "राष्ट्रीय छात्रवृत्ति पोर्टल उच्च शिक्षा योजना",
            "bn": "জাতীয় স্কলারশিপ পোর্টাল উচ্চ শিক্ষা স্কিম",
            "mr": "राष्ट्रीय शिष्यवृत्ती पोर्टल उच्च शिक्षण योजना",
            "ta": "தேசிய கல்வி உதவித்தொகை தளம் உயர் கல்வி திட்டம்"
        },
        "category": "All",
        "state": "All India",
        "type": "Scholarship",
        "age_limit": 25,
        "income_limit": 450000,
        "description": {
            "en": "Central sector scholarship for college and university students.",
            "hi": "कॉलेज और विश्वविद्यालय के छात्रों के लिए केंद्रीय क्षेत्र की छात्रवृत्ति।",
            "bn": "কলেজ এবং বিশ্ববিদ্যালয়ের শিক্ষার্থীদের জন্য কেন্দ্রীয় খাতের স্কলারশিপ।"
        },
        "link": "https://scholarships.gov.in/"
    },
    {
        "id": "mah-03",
        "title": {
            "en": "Maharashtra Post-Matric Scholarship for SC/ST/OBC",
            "hi": "महाराष्ट्र एससी/एसटी/ओबीसी के लिए पोस्ट-मैट्रिक छात्रवृत्ति",
            "mr": "महाराष्ट्र एससी/एसटी/ओबीसीसाठी पोस्ट-मॅट्रिक शिष्यवृत्ती"
        },
        "category": "SC",
        "state": "Maharashtra",
        "type": "Scholarship",
        "age_limit": 30,
        "income_limit": 250000,
        "description": {
            "en": "State-backed financial assistance for post-matriculation studies in Maharashtra.",
            "mr": "महाराष्ट्रातील उत्तर-मॅट्रिक अभ्यासासाठी राज्य-समर्थित आर्थिक सहाय्य."
        },
        "link": "https://mahadbtmahadbt.gov.in/"
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
    <title>Haqdar - 22-Language Welfare Matcher</title>
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
            const [state, setState] = React.useState('All India');
            const [category, setCategory] = React.useState('All');
            const [typeFilter, setTypeFilter] = React.useState('All');
            const [matches, setMatches] = React.useState([]);
            const [loading, setLoading] = React.useState(false);

            // All 22 Official Scheduled Languages of India
            const languages = [
                { code: 'en', name: 'English' },
                { code: 'hi', name: 'हिन्दी (Hindi)' },
                { code: 'bn', name: 'বাংলা (Bengali)' },
                { code: 'mr', name: 'मराठी (Marathi)' },
                { code: 'te', name: 'తెలుగు (Telugu)' },
                { code: 'ta', name: 'தமிழ் (Tamil)' },
                { code: 'gu', name: 'ગુજરાતી (Gujarati)' },
                { code: 'ur', name: 'اردو (Urdu)' },
                { code: 'kn', name: 'ಕನ್ನಡ (Kannada)' },
                { code: 'ml', name: 'മലയാളം (Malayalam)' },
                { code: 'pa', name: 'ਪੰਜਾਬੀ (Punjabi)' },
                { code: 'or', name: 'ଓଡ଼ିଆ (Odia)' },
                { code: 'as', name: 'অসমীয়া (Assamese)' },
                { code: 'mai', name: 'मैथिली (Maithili)' },
                { code: 'sat', name: 'संथाली (Santali)' },
                { code: 'ks', name: 'कॉशुर (Kashmiri)' },
                { code: 'ne', name: 'नेपाली (Nepali)' },
                { code: 'sd', name: 'سنڌي (Sindhi)' },
                { code: 'kok', name: 'कोंकणी (Konkani)' },
                { code: 'doi', name: 'डोगरी (Dogri)' },
                { code: 'mni', name: 'মৈতৈলোন্ (Manipuri)' },
                { code: 'sa', name: 'संस्कृतम् (Sanskrit)' }
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
                            <h1 className="text-3xl font-extrabold tracking-tight text-blue-400">Haqdar</h1>
                            <p className="text-sm text-slate-400">All-India Schemes, Exams & Scholarships Engine</p>
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="text-xs text-slate-400 uppercase tracking-wider">Language:</span>
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
                                <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1">Age / आयु</label>
                                <input type="number" value={age} onChange={e => setAge(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500" />
                            </div>
                            <div>
                                <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1">Annual Income (INR) / वार्षिक आय</label>
                                <input type="number" value={income} onChange={e => setIncome(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500" />
                            </div>
                            <div>
                                <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1">State / राज्य</label>
                                <select value={state} onChange={e => setState(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500">
                                    <option value="All India">All India / राष्ट्रीय</option>
                                    <option value="Maharashtra">Maharashtra</option>
                                    <option value="Delhi">Delhi</option>
                                    <option value="Uttar Pradesh">Uttar Pradesh</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-xs uppercase tracking-wider text-slate-400 mb-1">Category / श्रेणी</label>
                                <select value={category} onChange={e => setCategory(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-blue-500">
                                    <option value="All">All Categories / सभी</option>
                                    <option value="SC">SC</option>
                                    <option value="ST">ST</option>
                                    <option value="OBC">OBC</option>
                                    <option value="General">General</option>
                                </select>
                            </div>
                            <div className="md:col-span-2">
                                <button type="submit" className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold p-3 rounded-xl transition shadow-lg">
                                    {loading ? 'Scanning Policies...' : 'Find All Eligible Opportunities'}
                                </button>
                            </div>
                        </form>
                    </div>

                    <div className="space-y-4">
                        <h2 className="text-xl font-bold tracking-tight text-slate-200">Eligible Opportunities ({matches.length})</h2>
                        {matches.length === 0 ? (
                            <div className="bg-slate-800 p-8 rounded-2xl border border-slate-700 text-center text-slate-400">
                                Run a search above to discover matching schemes, exams, and scholarships.
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
                                        <span>Domicile: {m.state} | Category: {m.category}</span>
                                        <a href={m.link} target="_blank" rel="noreferrer" className="bg-slate-700 hover:bg-slate-600 text-blue-300 px-3 py-1.5 rounded-lg border border-slate-600 transition font-medium">
                                            Official Portal ↗
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
    category = request.args.get("category", "All")
    scheme_type = request.args.get("type", "All")

    filtered = []
    for item in MASTER_DATABASE:
        if age <= item["age_limit"] and income <= item["income_limit"]:
            if item["state"] == "All India" or item["state"] == state:
                if item["category"] == "All" or item["category"] == category:
                    filtered.append(item)

    return jsonify({
        "success": True,
        "count": len(filtered),
        "matches": filtered
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)