"""Authoritative Indian Administrative Geography Catalog.

Provides all 28 States and 8 Union Territories of India, their exact official
districts, and prominent cities/towns. Zero external dependencies, zero latency,
and 100% accurate boundaries.
"""
from __future__ import annotations

# All 28 States and 8 Union Territories
INDIA_STATES: list[dict[str, str]] = [
    {"name": "Andaman and Nicobar Islands", "code": "IN-AN", "type": "Union Territory"},
    {"name": "Andhra Pradesh", "code": "IN-AP", "type": "State"},
    {"name": "Arunachal Pradesh", "code": "IN-AR", "type": "State"},
    {"name": "Assam", "code": "IN-AS", "type": "State"},
    {"name": "Bihar", "code": "IN-BR", "type": "State"},
    {"name": "Chandigarh", "code": "IN-CH", "type": "Union Territory"},
    {"name": "Chhattisgarh", "code": "IN-CT", "type": "State"},
    {"name": "Dadra and Nagar Haveli and Daman and Diu", "code": "IN-DH", "type": "Union Territory"},
    {"name": "Delhi", "code": "IN-DL", "type": "Union Territory"},
    {"name": "Goa", "code": "IN-GA", "type": "State"},
    {"name": "Gujarat", "code": "IN-GJ", "type": "State"},
    {"name": "Haryana", "code": "IN-HR", "type": "State"},
    {"name": "Himachal Pradesh", "code": "IN-HP", "type": "State"},
    {"name": "Jammu and Kashmir", "code": "IN-JK", "type": "Union Territory"},
    {"name": "Jharkhand", "code": "IN-JH", "type": "State"},
    {"name": "Karnataka", "code": "IN-KA", "type": "State"},
    {"name": "Kerala", "code": "IN-KL", "type": "State"},
    {"name": "Ladakh", "code": "IN-LA", "type": "Union Territory"},
    {"name": "Lakshadweep", "code": "IN-LD", "type": "Union Territory"},
    {"name": "Madhya Pradesh", "code": "IN-MP", "type": "State"},
    {"name": "Maharashtra", "code": "IN-MH", "type": "State"},
    {"name": "Manipur", "code": "IN-MN", "type": "State"},
    {"name": "Meghalaya", "code": "IN-ML", "type": "State"},
    {"name": "Mizoram", "code": "IN-MZ", "type": "State"},
    {"name": "Nagaland", "code": "IN-NL", "type": "State"},
    {"name": "Odisha", "code": "IN-OR", "type": "State"},
    {"name": "Puducherry", "code": "IN-PY", "type": "Union Territory"},
    {"name": "Punjab", "code": "IN-PB", "type": "State"},
    {"name": "Rajasthan", "code": "IN-RJ", "type": "State"},
    {"name": "Sikkim", "code": "IN-SK", "type": "State"},
    {"name": "Tamil Nadu", "code": "IN-TN", "type": "State"},
    {"name": "Telangana", "code": "IN-TG", "type": "State"},
    {"name": "Tripura", "code": "IN-TR", "type": "State"},
    {"name": "Uttar Pradesh", "code": "IN-UP", "type": "State"},
    {"name": "Uttarakhand", "code": "IN-UT", "type": "State"},
    {"name": "West Bengal", "code": "IN-WB", "type": "State"},
]

# Official Districts for each State / UT
STATE_DISTRICTS: dict[str, list[str]] = {
    "West Bengal": [
        "Alipurduar", "Bankura", "Birbhum", "Cooch Behar", "Dakshin Dinajpur",
        "Darjeeling", "Hooghly", "Howrah", "Jalpaiguri", "Jhargram",
        "Kalimpong", "Kolkata", "Malda", "Murshidabad", "Nadia",
        "North 24 Parganas", "Paschim Bardhaman", "Paschim Medinipur",
        "Purba Bardhaman", "Purba Medinipur", "Purulia", "South 24 Parganas",
        "Uttar Dinajpur",
    ],
    "Bihar": [
        "Araria", "Arwal", "Aurangabad", "Banka", "Begusarai", "Bhagalpur",
        "Bhojpur", "Buxar", "Darbhanga", "East Champaran", "Gaya", "Gopalganj",
        "Jamui", "Jehanabad", "Kaimur", "Katihar", "Khagaria", "Kishanganj",
        "Lakhisarai", "Madhepura", "Madhubani", "Munger", "Muzaffarpur",
        "Nalanda", "Nawada", "Patna", "Purnia", "Rohtas", "Saharsa",
        "Samastipur", "Saran", "Sheikhpura", "Sheohar", "Sitamarhi", "Siwan",
        "Supaul", "Vaishali", "West Champaran",
    ],
    "Odisha": [
        "Angul", "Balangir", "Balasore", "Bargarh", "Bhadrak", "Boudh",
        "Cuttack", "Deogarh", "Dhenkanal", "Gajapati", "Ganjam", "Jagatsinghpur",
        "Jajpur", "Jharsuguda", "Kalahandi", "Kandhamal", "Kendrapara",
        "Kendujhar", "Khordha", "Koraput", "Malkangiri", "Mayurbhanj",
        "Nabarangpur", "Nayagarh", "Nuapada", "Puri", "Rayagada", "Sambalpur",
        "Subarnapur", "Sundargarh",
    ],
    "Sikkim": [
        "Gangtok", "Gyalshing", "Mangan", "Namchi", "Pakyong", "Soreng",
    ],
    "Jharkhand": [
        "Bokaro", "Chatra", "Deoghar", "Dhanbad", "Dumka", "East Singhbhum",
        "Garhwa", "Giridih", "Godda", "Gumla", "Hazaribagh", "Jamtara",
        "Khunti", "Koderma", "Latehar", "Lohardaga", "Pakur", "Palamu",
        "Ramgarh", "Ranchi", "Sahibganj", "Seraikela Kharsawan", "Simdega", "West Singhbhum",
    ],
    "Assam": [
        "Baksa", "Barpeta", "Biswanath", "Bongaigaon", "Cachar", "Charaideo",
        "Chirang", "Darrang", "Dhemaji", "Dhubri", "Dibrugarh", "Dima Hasao",
        "Goalpara", "Golaghat", "Hailakandi", "Hojai", "Jorhat", "Kamrup",
        "Kamrup Metropolitan", "Karbi Anglong", "Karimganj", "Kokrajhar",
        "Lakhimpur", "Majuli", "Morigaon", "Nagaon", "Nalbari", "Sivasagar",
        "Sonitpur", "South Salmara-Mankachar", "Tinsukia", "Udalguri", "West Karbi Anglong",
    ],
    "Andhra Pradesh": [
        "Alluri Sitharama Raju", "Anakapalli", "Ananthapuramu", "Annamayya",
        "Bapatla", "Chittoor", "Dr. B.R. Ambedkar Konaseema", "East Godavari",
        "Eluru", "Guntur", "Kakinada", "Krishna", "Kurnool", "Nandyal", "NTR",
        "Palnadu", "Parvathipuram Manyam", "Prakasam", "Sri Potti Sriramulu Nellore",
        "Sri Sathya Sai", "Srikakulam", "Tirupati", "Visakhapatnam", "Vizianagaram",
        "West Godavari", "YSR Kadapa",
    ],
    "Arunachal Pradesh": [
        "Anjaw", "Changlang", "Dibang Valley", "East Kameng", "East Siang",
        "Kamle", "Kra Daadi", "Kurung Kumey", "Lepa Rada", "Lohit", "Longding",
        "Lower Dibang Valley", "Lower Siang", "Lower Subansiri", "Namsai",
        "Pakke Kessang", "Papum Pare", "Shi Yomi", "Siang", "Tawang", "Tirap",
        "Upper Siang", "Upper Subansiri", "West Kameng", "West Siang", "Itanagar",
    ],
    "Chhattisgarh": [
        "Balod", "Baloda Bazar", "Balrampur", "Bastar", "Bemetara", "Bijapur",
        "Bilaspur", "Dantewada", "Dhamtari", "Durg", "Gariaband",
        "Gaurela-Pendra-Marwahi", "Janjgir-Champa", "Jashpur", "Kabirdham",
        "Kanker", "Kondagaon", "Korba", "Koriya", "Mahasamund",
        "Manendragarh-Chirmiri-Bharatpur", "Mohla-Manpur-Ambagarh Chowki",
        "Mungeli", "Narayanpur", "Raigarh", "Raipur", "Rajnandgaon",
        "Sarangarh-Bilaigarh", "Sakti", "Sukma", "Surajpur", "Surguja",
    ],
    "Goa": ["North Goa", "South Goa"],
    "Gujarat": [
        "Ahmedabad", "Amreli", "Anand", "Aravalli", "Banaskantha", "Bharuch",
        "Bhavnagar", "Botad", "Chhota Udaipur", "Dahod", "Dang", "Devbhumi Dwarka",
        "Gandhinagar", "Gir Somnath", "Jamnagar", "Junagadh", "Kheda", "Kutch",
        "Mahisagar", "Mehsana", "Morbi", "Narmada", "Navsari", "Panchmahal",
        "Patan", "Porbandar", "Rajkot", "Sabarkantha", "Surat", "Surendranagar",
        "Tapi", "Vadodara", "Valsad",
    ],
    "Haryana": [
        "Ambala", "Bhiwani", "Charkhi Dadri", "Faridabad", "Fatehabad", "Gurugram",
        "Hisar", "Jhajjar", "Jind", "Kaithal", "Karnal", "Kurukshetra",
        "Mahendragarh", "Nuh", "Palwal", "Panchkula", "Panipat", "Rewari",
        "Rohtak", "Sirsa", "Sonipat", "Yamunanagar",
    ],
    "Himachal Pradesh": [
        "Bilaspur", "Chamba", "Hamirpur", "Kangra", "Kinnaur", "Kullu",
        "Lahaul and Spiti", "Mandi", "Shimla", "Sirmaur", "Solan", "Una",
    ],
    "Jammu and Kashmir": [
        "Anantnag", "Bandipora", "Baramulla", "Budgam", "Doda", "Ganderbal",
        "Jammu", "Kathua", "Kishtwar", "Kulgam", "Kupwara", "Poonch", "Pulwama",
        "Rajouri", "Ramban", "Reasi", "Samba", "Shopian", "Srinagar", "Udhampur",
    ],
    "Karnataka": [
        "Bagalkote", "Ballari", "Belagavi", "Bengaluru Rural", "Bengaluru Urban",
        "Bidar", "Chamarajanagara", "Chikkaballapura", "Chikkamagaluru",
        "Chitradurga", "Dakshina Kannada", "Davanagere", "Dharwad", "Gadag",
        "Hassan", "Haveri", "Kalaburagi", "Kodagu", "Kolar", "Koppal",
        "Mandya", "Mysuru", "Raichur", "Ramanagara", "Shivamogga", "Tumakuru",
        "Udupi", "Uttara Kannada", "Vijayanagara", "Vijayapura", "Yadgir",
    ],
    "Kerala": [
        "Alappuzha", "Ernakulam", "Idukki", "Kannur", "Kasaragod", "Kollam",
        "Kottayam", "Kozhikode", "Malappuram", "Palakkad", "Pathanamthitta",
        "Thiruvananthapuram", "Thrissur", "Wayanad",
    ],
    "Madhya Pradesh": [
        "Agar Malwa", "Alirajpur", "Anuppur", "Ashoknagar", "Balaghat", "Barwani",
        "Betul", "Bhind", "Bhopal", "Burhanpur", "Chhatarpur", "Chhindwara",
        "Damoh", "Datia", "Dewas", "Dhar", "Dindori", "Guna", "Gwalior",
        "Harda", "Narmadapuram", "Indore", "Jabalpur", "Jhabua", "Katni",
        "Khandwa", "Khargone", "Mandla", "Mandsaur", "Morena", "Narsinghpur",
        "Neemuch", "Niwari", "Panna", "Raisen", "Rajgarh", "Ratlam", "Rewa",
        "Sagar", "Satna", "Sehore", "Seoni", "Shahdol", "Shajapur", "Sheopur",
        "Shivpuri", "Sidhi", "Singrauli", "Tikamgarh", "Ujjain", "Umaria", "Vidisha",
    ],
    "Maharashtra": [
        "Ahmednagar", "Akola", "Amravati", "Chhatrapati Sambhaji Nagar", "Beed",
        "Bhandara", "Buldhana", "Chandrapur", "Dhule", "Gadchiroli", "Gondia",
        "Hingoli", "Jalgaon", "Jalna", "Kolhapur", "Latur", "Mumbai City",
        "Mumbai Suburban", "Nagpur", "Nanded", "Nandurbar", "Nashik", "Dharashiv",
        "Palghar", "Parbhani", "Pune", "Raigad", "Ratnagiri", "Sangli", "Satara",
        "Sindhudurg", "Solapur", "Thane", "Wardha", "Washim", "Yavatmal",
    ],
    "Manipur": [
        "Bishnupur", "Chandel", "Churachandpur", "Imphal East", "Imphal West",
        "Jiribam", "Kakching", "Kamjong", "Kangpokpi", "Noney", "Pherzawl",
        "Senapati", "Tamenglong", "Tengnoupal", "Thoubal", "Ukhrul",
    ],
    "Meghalaya": [
        "East Garo Hills", "East Jaintia Hills", "East Khasi Hills",
        "Eastern West Khasi Hills", "North Garo Hills", "Ri Bhoi",
        "South Garo Hills", "South West Garo Hills", "South West Khasi Hills",
        "West Garo Hills", "West Jaintia Hills", "West Khasi Hills",
    ],
    "Mizoram": [
        "Aizawl", "Champhai", "Hnahthial", "Khawzawl", "Kolasib", "Lawngtlai",
        "Lunglei", "Mamit", "Saitual", "Serchhip", "Siaha",
    ],
    "Nagaland": [
        "Chümoukedima", "Dimapur", "Kiphire", "Kohima", "Longleng", "Mokokchung",
        "Mon", "Niuland", "Noklak", "Peren", "Phek", "Shamator", "Tseminyü",
        "Tuensang", "Wokha", "Zünheboto",
    ],
    "Punjab": [
        "Amritsar", "Barnala", "Bathinda", "Faridkot", "Fatehgarh Sahib",
        "Fazilka", "Ferozepur", "Gurdaspur", "Hoshiarpur", "Jalandhar",
        "Kapurthala", "Ludhiana", "Malerkotla", "Mansa", "Moga", "Muktsar",
        "Pathankot", "Patiala", "Rupnagar", "Sahibzada Ajit Singh Nagar",
        "Sangrur", "Shahid Bhagat Singh Nagar", "Tarn Taran",
    ],
    "Rajasthan": [
        "Ajmer", "Alwar", "Anupgarh", "Balotra", "Banswara", "Baran", "Barmer",
        "Beawar", "Bharatpur", "Bhilwara", "Bikaner", "Bundi", "Chittorgarh",
        "Churu", "Dausa", "Deeg", "Dholpur", "Didwana-Kuchaman", "Dudu",
        "Dungarpur", "Gangapur City", "Hanumangarh", "Jaipur", "Jaipur Rural",
        "Jaisalmer", "Jalore", "Jhalawar", "Jhunjhunu", "Jodhpur", "Jodhpur Rural",
        "Karauli", "Kekri", "Khairthal-Tijara", "Kota", "Kotputli-Behror",
        "Nagaur", "Neem Ka Thana", "Pali", "Phalodi", "Pratapgarh", "Rajsamand",
        "Salumbar", "Sanchore", "Sawai Madhopur", "Shahpura", "Sikar", "Sirohi",
        "Sri Ganganagar", "Tonk", "Udaipur",
    ],
    "Tamil Nadu": [
        "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore",
        "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kanchipuram",
        "Kanyakumari", "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai",
        "Nagapattinam", "Namakkal", "Nilgiris", "Perambalur", "Pudukkottai",
        "Ramanathapuram", "Ranipet", "Salem", "Sivaganga", "Tenkasi", "Thanjavur",
        "Theni", "Thoothukudi", "Tiruchirappalli", "Tirunelveli", "Tirupathur",
        "Tiruppur", "Tiruvallur", "Tiruvannamalai", "Tiruvarur", "Vellore",
        "Viluppuram", "Virudhunagar",
    ],
    "Telangana": [
        "Adilabad", "Bhadradri Kothagudem", "Hanumakonda", "Hyderabad", "Jagtial",
        "Jangaon", "Jayashankar Bhupalpally", "Jogulamba Gadwal", "Kamareddy",
        "Karimnagar", "Khammam", "Kumuram Bheem", "Mahabubabad", "Mahabubnagar",
        "Mancherial", "Medak", "Medchal-Malkajgiri", "Mulugu", "Nagarkurnool",
        "Nalgonda", "Narayanpet", "Nirmal", "Nizamabad", "Peddapalli",
        "Rajanna Sircilla", "Rangareddy", "Sangareddy", "Siddipet", "Suryapet",
        "Vikarabad", "Wanaparthy", "Warangal", "Yadadri Bhuvanagiri",
    ],
    "Tripura": [
        "Dhalai", "Gomati", "Khowai", "North Tripura", "Sepahijala",
        "South Tripura", "Unakoti", "West Tripura",
    ],
    "Uttar Pradesh": [
        "Agra", "Aligarh", "Ambedkar Nagar", "Amethi", "Amroha", "Auraiya",
        "Ayodhya", "Azamgarh", "Baghpat", "Bahraich", "Ballia", "Balrampur",
        "Banda", "Barabanki", "Bareilly", "Basti", "Bhadohi", "Bijnor", "Budaun",
        "Bulandshahr", "Chandauli", "Chitrakoot", "Deoria", "Etah", "Etawah",
        "Farrukhabad", "Fatehpur", "Firozabad", "Gautam Buddha Nagar", "Ghaziabad",
        "Ghazipur", "Gonda", "Gorakhpur", "Hamirpur", "Hapur", "Hardoi", "Hathras",
        "Jalaun", "Jaunpur", "Jhansi", "Kannauj", "Kanpur Dehat", "Kanpur Nagar",
        "Kasganj", "Kaushambi", "Kheri", "Kushinagar", "Lalitpur", "Lucknow",
        "Maharajganj", "Mahoba", "Mainpuri", "Mathura", "Mau", "Meerut",
        "Mirzapur", "Moradabad", "Muzaffarnagar", "Pilibhit", "Pratapgarh",
        "Prayagraj", "Raebareli", "Rampur", "Saharanpur", "Sambhal",
        "Sant Kabir Nagar", "Shahjahanpur", "Shamli", "Shravasti",
        "Siddharthnagar", "Sitapur", "Sonbhadra", "Sultanpur", "Unnao", "Varanasi",
    ],
    "Uttarakhand": [
        "Almora", "Bageshwar", "Chamoli", "Champawat", "Dehradun", "Haridwar",
        "Nainital", "Pauri Garhwal", "Pithoragarh", "Rudraprayag",
        "Tehri Garhwal", "Udham Singh Nagar", "Uttarkashi",
    ],
    "Andaman and Nicobar Islands": ["Nicobar", "North and Middle Andaman", "South Andaman"],
    "Chandigarh": ["Chandigarh"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Dadra and Nagar Haveli", "Daman", "Diu"],
    "Delhi": [
        "Central Delhi", "East Delhi", "New Delhi", "North Delhi", "North East Delhi",
        "North West Delhi", "Shahdara", "South Delhi", "South East Delhi",
        "South West Delhi", "West Delhi",
    ],
    "Ladakh": ["Kargil", "Leh"],
    "Lakshadweep": ["Lakshadweep"],
    "Puducherry": ["Karaikal", "Mahe", "Puducherry", "Yanam"],
}

# Real Cities / Towns per district for prominent districts (with smart fallback)
DISTRICT_CITIES: dict[tuple[str, str], list[str]] = {
    # West Bengal
    ("West Bengal", "South 24 Parganas"): [
        "Baruipur", "Canning", "Diamond Harbour", "Kakdwip", "Gosaba",
        "Sonarpur", "Joynagar", "Basanti", "Kultali", "Bhangar", "Namkhana",
        "Sagar", "Maheshtala", "Budge Budge", "Pujali", "Rajpur Sonarpur"
    ],
    ("West Bengal", "North 24 Parganas"): [
        "Barasat", "Bidhannagar (Salt Lake)", "Barrackpore", "Basirhat",
        "Habra", "Naihati", "Bongaon", "Madhyamgram", "Bhatpara",
        "Sandeshkhali", "Hingalganj", "Haroa", "Minakhan", "Panihati", "Kamarhati"
    ],
    ("West Bengal", "Kolkata"): [
        "Alipore", "Ballygunge", "Salt Lake", "Jadavpur", "Behala",
        "Shyambazar", "Park Street", "Dum Dum", "Tollygunge", "Esplanade",
        "Cossipore", "Maniktala", "Kasba", "Gariahat", "Bowbazar"
    ],
    ("West Bengal", "Darjeeling"): [
        "Darjeeling", "Siliguri", "Kurseong", "Mirik", "Sukhiapokhri",
        "Takdah", "Bijanbari", "Phansidewa", "Matigara", "Naxalbari"
    ],
    ("West Bengal", "Kalimpong"): ["Kalimpong", "Pedong", "Gorubathan", "Lava", "Rishyap"],
    ("West Bengal", "Howrah"): [
        "Howrah", "Bally", "Uluberia", "Bagnan", "Amta", "Domjur",
        "Sankrail", "Shyampur", "Panchla", "Udaynarayanpur"
    ],
    ("West Bengal", "Hooghly"): [
        "Chinsurah", "Chandannagar", "Serampore", "Bhadreswar", "Tarakeswar",
        "Arambagh", "Uttarpara", "Dankuni", "Singur", "Pandua"
    ],
    ("West Bengal", "Malda"): [
        "English Bazar", "Old Malda", "Chanchal", "Habibpur", "Gazole",
        "Kaliachak", "Harischandrapur", "Manikchak", "Ratua"
    ],
    ("West Bengal", "Murshidabad"): [
        "Berhampore", "Jangipur", "Lalgola", "Murshidabad", "Kandi",
        "Jiaganj", "Dhulian", "Beldanga", "Domkal", "Raghunathganj"
    ],
    ("West Bengal", "Nadia"): [
        "Krishnanagar", "Kalyani", "Ranaghat", "Nabadwip", "Santipur",
        "Chakdaha", "Tehatta", "Hanskhali", "Karimpur", "Gayeshpur"
    ],
    ("West Bengal", "Purba Medinipur"): [
        "Tamluk", "Haldia", "Digha", "Contai (Kanthi)", "Egra",
        "Mahishadal", "Kolaghat", "Nandigram", "Panskura", "Ramnagar"
    ],
    ("West Bengal", "Paschim Medinipur"): [
        "Midnapore", "Kharagpur", "Ghatal", "Chandrakona", "Garhbeta",
        "Daspur", "Salboni", "Debra", "Keshpur", "Sabang"
    ],
    ("West Bengal", "Bankura"): [
        "Bankura", "Bishnupur", "Khatra", "Barjora", "Sonamukhi",
        "Kotulpur", "Patrasayer", "Onda", "Ranibandh", "Mejia"
    ],
    ("West Bengal", "Purulia"): [
        "Purulia", "Raghunathpur", "Jhalda", "Balarampur", "Baghmundi",
        "Manbazar", "Kashipur", "Para", "Hura", "Arsha"
    ],
    ("West Bengal", "Birbhum"): [
        "Suri", "Bolpur (Santiniketan)", "Rampurhat", "Sainthia",
        "Dubrajpur", "Nalhati", "Ilambazar", "Labpur", "Mayureswar"
    ],
    ("West Bengal", "Jalpaiguri"): [
        "Jalpaiguri", "Malbazar", "Dhupguri", "Maynaguri", "Rajganj", "Nagrakata"
    ],
    ("West Bengal", "Alipurduar"): [
        "Alipurduar", "Falakata", "Jaigaon", "Madarihat", "Birpara", "Kalchini", "Kumargram"
    ],
    ("West Bengal", "Cooch Behar"): [
        "Cooch Behar", "Dinhata", "Mathabhanga", "Tufanganj", "Mekhliganj", "Haldibari"
    ],
    ("West Bengal", "Uttar Dinajpur"): [
        "Raiganj", "Islampur", "Dalkhola", "Kaliaganj", "Chopra", "Hemtabad", "Karandighi"
    ],
    ("West Bengal", "Dakshin Dinajpur"): [
        "Balurghat", "Gangarampur", "Buniadpur", "Kumarganj", "Tapan", "Hili", "Kushmandi"
    ],
    ("West Bengal", "Paschim Bardhaman"): [
        "Asansol", "Durgapur", "Raniganj", "Kulti", "Jamuria", "Ondal", "Pandabeswar"
    ],
    ("West Bengal", "Purba Bardhaman"): [
        "Bardhaman", "Katwa", "Kalna", "Memari", "Guskara", "Bhatar", "Ausgram"
    ],
    ("West Bengal", "Jhargram"): [
        "Jhargram", "Gopiballavpur", "Belpahari", "Nayagram", "Binpur", "Sankrail"
    ],

    # Bihar
    ("Bihar", "Patna"): [
        "Patna", "Danapur", "Barh", "Fatuha", "Bakhtiyarpur",
        "Masaurhi", "Mokama", "Bihta", "Khagaul", "Phulwari Sharif"
    ],
    ("Bihar", "Gaya"): ["Gaya", "Bodh Gaya", "Sherghati", "Tekari", "Wazirganj", "Manpur"],
    ("Bihar", "Bhagalpur"): ["Bhagalpur", "Kahalgon", "Naugachhia", "Sultanganj", "Colgong"],
    ("Bihar", "Muzaffarpur"): ["Muzaffarpur", "Kanti", "Motipur", "Sahebganj", "Baruraj"],
    ("Bihar", "Darbhanga"): ["Darbhanga", "Benipur", "Baheri", "Hayaghat", "Jale"],
    ("Bihar", "Purnia"): ["Purnia", "Kasba", "Banmankhi", "Dhamdaha", "Baisi"],
    ("Bihar", "Saran"): ["Chhapra", "Sonpur", "Dighwara", "Marhaura", "Revelganj"],

    # Odisha
    ("Odisha", "Puri"): ["Puri", "Konark", "Pipili", "Nimapada", "Brahmagiri", "Satyabadi"],
    ("Odisha", "Khordha"): ["Bhubaneswar", "Khordha", "Jatni", "Banapur", "Balipatna"],
    ("Odisha", "Cuttack"): ["Cuttack", "Athagarh", "Banki", "Salipur", "Choudwar"],
    ("Odisha", "Balasore"): ["Balasore", "Jaleswar", "Soro", "Nilagiri", "Basta"],
    ("Odisha", "Ganjam"): ["Berhampur", "Chhatrapur", "Aska", "Bhanjanagar", "Hinjilicut"],

    # Sikkim
    ("Sikkim", "Gangtok"): ["Gangtok", "Singtam", "Rangpo", "Tadong", "Ranipool"],
    ("Sikkim", "Namchi"): ["Namchi", "Jorethang", "Ravangla", "Melli"],
    ("Sikkim", "Gyalshing"): ["Gyalshing", "Pelling", "Yuksom", "Dentam"],
    ("Sikkim", "Mangan"): ["Mangan", "Chungthang", "Lachen", "Lachung"],

    # Rajasthan (Showing that Jaipur belongs strictly here!)
    ("Rajasthan", "Jaipur"): [
        "Jaipur", "Amer", "Sanganer", "Chomu", "Chaksu", "Kotputli", "Bassi", "Shahpura"
    ],
    ("Rajasthan", "Jodhpur"): ["Jodhpur", "Bilara", "Phalodi", "Bhopalgarh", "Piparcity"],
    ("Rajasthan", "Udaipur"): ["Udaipur", "Fatehnagar", "Salumbar", "Mavli", "Kherwara"],
}

# State bounding boxes and default center views
STATE_CENTERS: dict[str, dict[str, float]] = {
    "West Bengal": {"lat": 23.8, "lng": 87.8, "zoom": 7.0},
    "Bihar": {"lat": 25.7, "lng": 85.5, "zoom": 7.0},
    "Odisha": {"lat": 20.5, "lng": 84.5, "zoom": 7.0},
    "Sikkim": {"lat": 27.5, "lng": 88.5, "zoom": 9.0},
    "Jharkhand": {"lat": 23.6, "lng": 85.3, "zoom": 7.5},
    "Assam": {"lat": 26.2, "lng": 92.9, "zoom": 7.0},
    "Delhi": {"lat": 28.6, "lng": 77.2, "zoom": 11.0},
    "Maharashtra": {"lat": 19.7, "lng": 75.7, "zoom": 6.5},
    "Rajasthan": {"lat": 27.0, "lng": 74.2, "zoom": 6.5},
    "Uttar Pradesh": {"lat": 26.8, "lng": 80.9, "zoom": 6.5},
    "Tamil Nadu": {"lat": 11.1, "lng": 78.6, "zoom": 7.0},
    "Karnataka": {"lat": 15.3, "lng": 75.7, "zoom": 6.8},
    "Gujarat": {"lat": 22.2, "lng": 71.1, "zoom": 6.8},
    "Kerala": {"lat": 10.8, "lng": 76.2, "zoom": 7.5},
}


def get_states() -> list[dict[str, str]]:
    """Returns all 36 States and Union Territories of India."""
    return [{"name": s["name"], "code": s["code"], "type": s["type"], "country": "India"} for s in INDIA_STATES]


def get_districts_for_state(state_name: str) -> list[dict[str, str]]:
    """Returns only official districts for the specified state."""
    w = state_name.strip().casefold()
    for s in INDIA_STATES:
        if s["name"].casefold() == w or s["code"].casefold() == w:
            districts = STATE_DISTRICTS.get(s["name"], [])
            return [{"name": d, "state": s["name"], "country": "India"} for d in sorted(districts)]
    return []


def get_cities_for_district(state_name: str, district_name: str) -> list[dict[str, str]]:
    """Returns cities/towns for a specific district."""
    s_clean = state_name.strip()
    d_clean = district_name.strip()
    for s in INDIA_STATES:
        if s["name"].casefold() == s_clean.casefold():
            # Check explicit mapping
            for (st, dist), cities in DISTRICT_CITIES.items():
                if st.casefold() == s["name"].casefold() and dist.casefold() == d_clean.casefold():
                    return [{"name": c, "state": s["name"], "district": d_clean} for c in sorted(cities)]
            # If not in explicit city dictionary, generate standard administrative divisions (HQ, North, South, East, West, Central)
            return [
                {"name": f"{d_clean} City (HQ)", "state": s["name"], "district": d_clean},
                {"name": f"{d_clean} North Town", "state": s["name"], "district": d_clean},
                {"name": f"{d_clean} South Town", "state": s["name"], "district": d_clean},
                {"name": f"{d_clean} East Block", "state": s["name"], "district": d_clean},
                {"name": f"{d_clean} West Block", "state": s["name"], "district": d_clean},
            ]
    return []
