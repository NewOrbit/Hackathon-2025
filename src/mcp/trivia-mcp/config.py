"""
Trivia MCP configuration and in-memory database.
"""

# these are initial onces, we should update to more complete ones later
SECRET_DATABASE = {
    "space_needle": {
        "secrets": [
            "The elevator operator is actually a retired Broadway star who will sing show tunes if you ask nicely",
            "Local legend says if you spot the hidden gum wall from the top, your startup will get funded",
            "Thursday nights: the staff has secret karaoke sessions after closing",
            "The architect's ghost allegedly haunts the observation deck on foggy nights",
        ],
        "celebrity_sightings": [
            "Bill Gates was seen here arguing with a vending machine in 2019",
            "Taylor Swift allegedly wrote a secret song about the view",
            "Jeff Bezos once got stuck in the elevator for 20 minutes and started a meditation group",
        ],
        "insider_tips": [
            "Best photo spot: third floor bathroom mirror (don't ask why)",
            "Secret menu item: ask for the 'Space Needle-tini' - it's not on the menu",
            "Go at 3:17 PM for the best golden hour photos - the staff calls it 'magic minute'",
            "The gift shop has a secret back room with vintage Seattle memorabilia",
        ],
    },
    "pike_place": {
        "secrets": [
            "The original Starbucks has a secret menu item: 'The 1971 Special'",
            "The fish throwers have an ongoing feud with the flower vendors",
            "There's a hidden speakeasy behind the cheese shop that only locals know about",
            "The market has a secret underground tunnel system from the 1920s",
        ],
        "celebrity_sightings": [
            "Tom Hanks was spotted buying flowers for his wife here in 2018",
            "Oprah Winfrey once tried to throw a fish and failed spectacularly",
            "Bill Murray has been seen here every Thursday for the past 5 years",
        ],
        "insider_tips": [
            "Best time to visit: Tuesday mornings when it's less crowded",
            "Ask for the 'Pike Place Special' at any food stall - it's a secret combo",
            "The flower vendors give free samples to people who can name 3 types of tulips",
            "There's a secret rooftop garden with the best city views",
        ],
    },
    "golden_gate_bridge": {
        "secrets": [
            "The bridge's color is called 'International Orange' and was chosen to make it visible in fog",
            "There's a secret maintenance tunnel that runs the length of the bridge",
            "The bridge has its own weather station that predicts fog 2 hours in advance",
            "Local legend: if you walk across during a full moon, you'll see a ghost ship",
        ],
        "celebrity_sightings": [
            "Robin Williams was spotted here filming a secret project in 2013",
            "Steve Jobs used to walk across the bridge every morning for inspiration",
            "Maya Angelou wrote poetry about the bridge's fog patterns",
        ],
        "insider_tips": [
            "Best photo time: sunrise from the Marin Headlands side",
            "The bridge has a secret pedestrian path that's only open on Sundays",
            "Ask the maintenance crew about the 'Golden Gate Ghost' - they'll tell you the story",
            "There's a hidden viewpoint that only locals know about",
        ],
    },
    "central_park": {
        "secrets": [
            "There's a secret underground lake that only appears during heavy rain",
            "The park has its own microclimate that's 3 degrees cooler than the city",
            "There's a hidden garden that's only accessible through a secret entrance",
            "The park's squirrels have been trained to perform for tourists (unofficially)",
        ],
        "celebrity_sightings": [
            "Taylor Swift was spotted here writing songs in 2019",
            "Robert De Niro walks his dog here every morning at 6 AM",
            "Lady Gaga once had a secret concert in the park's hidden amphitheater",
        ],
        "insider_tips": [
            "Best time to visit: 6 AM when the park is empty and magical",
            "There's a secret food truck that only appears on Tuesdays",
            "The park has a hidden speakeasy in the old boathouse",
            "Ask the carriage drivers about the 'Central Park Ghost' - they know the legend",
        ],
    },
    "times_square": {
        "secrets": [
            "The ball drop on New Year's Eve is actually controlled by a secret underground bunker",
            "There's a hidden speakeasy behind one of the billboards",
            "The street performers have a secret hierarchy and territory system",
            "Times Square has its own microclimate due to all the electronic billboards",
        ],
        "celebrity_sightings": [
            "Ryan Reynolds was spotted here filming a secret Deadpool scene",
            "Jennifer Lawrence once got lost here and asked a tourist for directions",
            "Leonardo DiCaprio has a secret apartment above one of the theaters",
        ],
        "insider_tips": [
            "Best time to visit: 3 AM when it's actually peaceful",
            "There's a secret rooftop bar with the best views of the square",
            "The street vendors have a secret menu - just ask for 'the usual'",
            "Avoid the middle of the square - the real action is on the side streets",
        ],
    },
}

# Tip categories for organized retrieval
TIP_CATEGORIES = {
    "photo": "Photography tips and best spots",
    "food": "Secret menu items and hidden restaurants",
    "timing": "Best times to visit and avoid crowds",
    "access": "Secret entrances and hidden areas",
    "local": "Local customs and insider knowledge",
}

# Secret types
SECRET_TYPES = ["secrets", "celebrity_sightings", "insider_tips"]
