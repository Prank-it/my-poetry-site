import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('firebase_key.json')  # Use your Firebase key
firebase_admin.initialize_app(cred)
db = firestore.client()

# Sample Poems Data
sample_poems = [
    {
        "title": "Eternal Whispers",
        "category": "love",
        "content": "Your smile, a light in my darkest days,\nA poem etched in tender phrase.",
        "thumbnail": "https://source.unsplash.com/400x300/?love"
    },
    {
        "title": "Midnight Rain",
        "category": "sad",
        "content": "Raindrops cry on the windowpane,\nLike memories I can’t contain.",
        "thumbnail": "https://source.unsplash.com/400x300/?sad"
    },
    {
        "title": "Whispers of Wind",
        "category": "nature",
        "content": "Leaves converse in gentle tones,\nAs forest breathes through mossy stones.",
        "thumbnail": "https://source.unsplash.com/400x300/?forest"
    },
    {
        "title": "Moonlit Silence",
        "category": "haiku",
        "content": "Still night, windless air—\nA single owl breaks silence,\nStars blink unaware.",
        "thumbnail": "https://source.unsplash.com/400x300/?moon"
    },
    {
        "title": "Golden Hour Hearts",
        "category": "love",
        "content": "Your hand in mine, sun painting gold,\nTogether, stories brave and bold.",
        "thumbnail": "https://source.unsplash.com/400x300/?romance"
    },
]

# Push to Firestore
for poem in sample_poems:
    db.collection('poems').add(poem)

print("✅ Sample poems added to Firestore.")
