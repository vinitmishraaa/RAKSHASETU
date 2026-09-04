"""Prototype district catalog for RakshaSetu's eastern response region.

The names are used for demo filtering and synthetic district-level coverage.
Coordinates and incident metrics are generated separately and are explicitly
prototype data until verified GIS boundaries/centroids are connected.
"""

TARGET_REGIONS = [
    "West Bengal",
    "Bihar",
    "Odisha",
    "Jharkhand",
    "Sikkim",
    "Nepal",
]

DISTRICTS = {
    "West Bengal": [
        "Alipurduar", "Bankura", "Birbhum", "Cooch Behar", "Dakshin Dinajpur",
        "Darjeeling", "Hooghly", "Howrah", "Jalpaiguri", "Jhargram",
        "Kalimpong", "Kolkata", "Maldah", "Murshidabad", "Nadia",
        "North 24 Parganas", "South 24 Parganas", "Paschim Bardhaman",
        "Paschim Medinipur", "Purba Bardhaman", "Purba Medinipur",
        "Uttar Dinajpur", "Kolkata",
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
        "Nabarangpur", "Nayagarh", "Nuapada", "Puri", "Rayagada",
        "Sambalpur", "Subarnapur", "Sundargarh",
    ],
    "Jharkhand": [
        "Bokaro", "Chatra", "Deoghar", "Dhanbad", "Dumka", "East Singhbhum",
        "Garhwa", "Giridih", "Godda", "Gumla", "Hazaribagh", "Jamtara",
        "Khunti", "Koderma", "Latehar", "Lohardaga", "Pakur", "Palamu",
        "Ramgarh", "Ranchi", "Sahibganj", "Seraikela Kharsawan", "Simdega",
        "West Singhbhum",
    ],
    "Sikkim": [
        "Gangtok", "Gyalshing", "Mangan", "Namchi", "Pakyong", "Soreng",
    ],
    "Nepal": [
        "Achham", "Arghakhanchi", "Baglung", "Baitadi", "Bajhang", "Bajura",
        "Banke", "Bara", "Bardiya", "Bhaktapur", "Bhojpur", "Chitwan",
        "Dadeldhura", "Dailekh", "Dang", "Darchula", "Dhading", "Dhankuta",
        "Dhanusha", "Dolakha", "Dolpa", "Doti", "Eastern Rukum", "Gorkha",
        "Gulmi", "Humla", "Ilam", "Jajarkot", "Jhapa", "Jumla", "Kailali",
        "Kalikot", "Kanchanpur", "Kapilvastu", "Kaski", "Kathmandu", "Kavrepalanchok",
        "Khotang", "Lalitpur", "Lamjung", "Mahottari", "Makwanpur", "Manang",
        "Morang", "Mugu", "Mustang", "Myagdi", "Nawalpur", "Nuwakot", "Okhaldhunga",
        "Palpa", "Panchthar", "Parasi", "Parbat", "Parsa", "Pyuthan", "Ramechhap",
        "Rasuwa", "Rautahat", "Rolpa", "Rupandehi", "Salyan", "Sankhuwasabha",
        "Saptari", "Sarlahi", "Sindhuli", "Sindhupalchok", "Siraha", "Solukhumbu",
        "Sunsari", "Surkhet", "Syangja", "Tanahun", "Taplejung", "Tehrathum",
        "Udayapur", "Western Rukum",
    ],
}

# Approximate bounding boxes used only to place synthetic prototype markers.
REGION_BOUNDS = {
    "West Bengal": (21.5, 27.2, 85.8, 89.9),
    "Bihar": (24.0, 27.6, 83.3, 88.3),
    "Odisha": (17.7, 22.6, 81.3, 87.5),
    "Jharkhand": (21.9, 25.3, 83.3, 87.9),
    "Sikkim": (27.0, 28.2, 88.0, 88.9),
    "Nepal": (26.3, 30.5, 80.0, 88.2),
}


def get_districts(region: str | None = None):
    if region:
        return DISTRICTS.get(region, [])
    return [district for districts in DISTRICTS.values() for district in districts]
