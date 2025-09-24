"""
Trivia MCP configuration and in-memory database.
"""

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

    "eiffel_tower": {
        "secrets": [
            "The tower's height changes by 6 inches due to thermal expansion in summer",
            "There's a secret apartment at the top that Gustave Eiffel used for experiments",
            "The tower has its own post office with a unique postal code",
            "Local legend: if you whisper your wish at the base, it will come true within a year",
        ],
        "celebrity_sightings": [
            "Tom Hanks was spotted here filming a secret romantic scene in 2018",
            "Emma Stone once got lost in the tower's secret maintenance tunnels",
            "Brad Pitt has been seen here every Valentine's Day for the past 10 years",
        ],
        "insider_tips": [
            "Best photo time: 30 minutes before sunset for the golden hour glow",
            "Skip the elevator - the stairs offer better views and fewer crowds",
            "There's a secret champagne bar on the second level that locals know about",
            "Visit on Bastille Day for the spectacular fireworks display",
        ],
    },
    "taj_mahal": {
        "secrets": [
            "The marble changes color throughout the day - pink at dawn, white at noon, golden at sunset",
            "There's a secret underground chamber that's never been opened",
            "The four minarets are slightly tilted outward to protect the main structure",
            "Local legend: if you make a wish while touching the cenotaph, it will come true",
        ],
        "celebrity_sightings": [
            "Princess Diana was photographed here in 1992, creating an iconic image",
            "Oprah Winfrey once spent 6 hours here just sitting and meditating",
            "Bill Clinton was so moved he wrote a poem about it in the guest book",
        ],
        "insider_tips": [
            "Best time to visit: sunrise for the most magical lighting",
            "The full moon nights offer the most romantic experience",
            "There's a secret garden behind the main structure that few tourists find",
            "Wear comfortable shoes - the marble floors can be slippery",
        ],
    },
    "colosseum": {
        "secrets": [
            "The underground chambers were flooded for mock naval battles",
            "There's a secret tunnel system that connected to the emperor's palace",
            "The arena floor was covered with sand to absorb blood during gladiator fights",
            "Local legend: the ghosts of gladiators can be heard at midnight",
        ],
        "celebrity_sightings": [
            "Russell Crowe was spotted here researching for Gladiator in 1999",
            "Angelina Jolie once got lost in the underground chambers",
            "Leonardo DiCaprio has a secret collection of ancient Roman artifacts from here",
        ],
        "insider_tips": [
            "Best time to visit: early morning to avoid the crowds and heat",
            "The underground tour is worth the extra cost - it's incredible",
            "There's a secret viewpoint from the top tier that offers the best photos",
            "Visit during the evening for the dramatic lighting effects",
        ],
    },
    "machu_picchu": {
        "secrets": [
            "The site was built without mortar - the stones fit together perfectly",
            "There's a secret underground chamber that's never been fully explored",
            "The Intihuatana stone is said to have mystical powers",
            "Local legend: the spirits of the Incan emperors still walk the terraces",
        ],
        "celebrity_sightings": [
            "Oprah Winfrey hiked the Inca Trail and was so moved she cried at the top",
            "Leonardo DiCaprio once spent 3 days here just meditating",
            "Emma Stone was spotted here during a spiritual retreat in 2019",
        ],
        "insider_tips": [
            "Best time to visit: sunrise for the most spectacular views",
            "The 4-day Inca Trail is worth it for the full experience",
            "There's a secret viewpoint that only locals know about",
            "Bring layers - the temperature changes dramatically throughout the day",
        ],
    },
    "louvre_museum": {
        "secrets": [
            "The museum has over 35,000 works of art but only displays about 3,500",
            "There's a secret underground storage facility that's never been photographed",
            "The Mona Lisa has its own climate-controlled room with bulletproof glass",
            "Local legend: the museum's cats have been there since the 18th century",
        ],
        "celebrity_sightings": [
            "Beyoncé was spotted here filming a secret music video in 2018",
            "Tom Hanks once got lost in the Egyptian antiquities section for 2 hours",
            "Emma Stone has been seen here every Tuesday for the past year",
        ],
        "insider_tips": [
            "Best time to visit: Wednesday and Friday evenings when it's less crowded",
            "There's a secret entrance that locals use to avoid the main queue",
            "The museum has a secret rooftop garden with amazing city views",
            "Ask about the 'Louvre Ghost' - the staff will tell you the legend",
        ],
    },
    "great_wall_china": {
        "secrets": [
            "The wall is not visible from space with the naked eye, contrary to popular belief",
            "There's a secret section that's never been restored and is off-limits to tourists",
            "The wall was built by over 1 million workers, many of whom are buried within it",
            "Local legend: the wall was built with rice flour mortar that's stronger than modern concrete",
        ],
        "celebrity_sightings": [
            "Tom Cruise was spotted here filming Mission Impossible in 2018",
            "Oprah Winfrey once walked 10 miles along the wall in one day",
            "Leonardo DiCaprio has a secret collection of ancient Chinese artifacts from here",
        ],
        "insider_tips": [
            "Best time to visit: early morning to avoid the crowds and heat",
            "The Mutianyu section is less crowded than Badaling",
            "There's a secret section that locals know about with amazing views",
            "Bring plenty of water - there are no facilities along most sections",
        ],
    },
    "santorini": {
        "secrets": [
            "The island was formed by a massive volcanic eruption 3,600 years ago",
            "There's a secret underground city that's never been fully explored",
            "The famous blue domes are actually white - the blue is just the sky reflection",
            "Local legend: the island's cats have been there since ancient times",
        ],
        "celebrity_sightings": [
            "Tom Hanks was spotted here filming a secret romantic scene in 2019",
            "Emma Stone once got lost in the island's secret underground tunnels",
            "Brad Pitt has been seen here every summer for the past 5 years",
        ],
        "insider_tips": [
            "Best time to visit: sunset from Oia for the most spectacular views",
            "There's a secret beach that only locals know about",
            "The island's wine is incredible - ask for the local varieties",
            "Visit during the off-season for a more authentic experience",
        ],
    },
    "angkor_wat": {
        "secrets": [
            "The temple was built to face west, which is unusual for Hindu temples",
            "There's a secret underground chamber that's never been opened",
            "The temple's alignment with the sun creates a spectacular light show at sunrise",
            "Local legend: the temple's guardian spirits still protect the site",
        ],
        "celebrity_sightings": [
            "Angelina Jolie was spotted here filming Tomb Raider in 2000",
            "Tom Hanks once spent 3 days here just exploring the ruins",
            "Emma Stone was seen here during a spiritual retreat in 2018",
        ],
        "insider_tips": [
            "Best time to visit: sunrise for the most magical lighting",
            "The 3-day pass is worth it for the full experience",
            "There's a secret viewpoint that only locals know about",
            "Bring a guide - the history is incredible and complex",
        ],
    },
    "petra": {
        "secrets": [
            "The city was carved directly into the rock face over 2,000 years ago",
            "There's a secret underground water system that's still functional",
            "The Treasury's facade was carved from top to bottom, not bottom to top",
            "Local legend: the city's guardian spirits still protect the site",
        ],
        "celebrity_sightings": [
            "Tom Hanks was spotted here filming a secret adventure scene in 2019",
            "Emma Stone once got lost in the city's secret underground chambers",
            "Brad Pitt has been seen here every spring for the past 3 years",
        ],
        "insider_tips": [
            "Best time to visit: early morning to avoid the crowds and heat",
            "The 2-day pass is worth it for the full experience",
            "There's a secret viewpoint that only locals know about",
            "Bring comfortable shoes - there's a lot of walking involved",
        ],
    },
    "statue_liberty": {
        "secrets": [
            "The statue's torch was closed to visitors after a 1916 explosion",
            "There's a secret staircase inside the statue that's never been opened to the public",
            "The statue's crown has 25 windows representing the 25 gemstones found on Earth",
            "Local legend: the statue's torch has never been extinguished since 1886",
        ],
        "celebrity_sightings": [
            "Tom Hanks was spotted here filming a secret patriotic scene in 2018",
            "Emma Stone once got lost in the statue's secret underground chambers",
            "Brad Pitt has been seen here every July 4th for the past 10 years",
        ],
        "insider_tips": [
            "Best time to visit: early morning to avoid the crowds",
            "The crown access is limited and requires advance booking",
            "There's a secret viewpoint from the pedestal that offers amazing views",
            "Visit during the evening for the dramatic lighting effects",
        ],
    },
    "sagrada_familia": {
        "secrets": [
            "The church has been under construction for over 140 years and is still not finished",
            "There's a secret underground chamber that's never been opened",
            "The church's design incorporates elements from nature, including trees and flowers",
            "Local legend: the church's guardian spirits still protect the site",
        ],
        "celebrity_sightings": [
            "Tom Hanks was spotted here filming a secret architectural scene in 2019",
            "Emma Stone once got lost in the church's secret underground chambers",
            "Brad Pitt has been seen here every summer for the past 5 years",
        ],
        "insider_tips": [
            "Best time to visit: early morning to avoid the crowds",
            "The tower access is worth the extra cost for the amazing views",
            "There's a secret viewpoint that only locals know about",
            "Visit during the evening for the dramatic lighting effects",
        ],
    },
    "kinkaku_ji": {
        "secrets": [
            "The temple was burned down in 1950 and rebuilt in 1955",
            "There's a secret underground chamber that's never been opened",
            "The temple's gold leaf is replaced every 20 years",
            "Local legend: the temple's guardian spirits still protect the site",
        ],
        "celebrity_sightings": [
            "Tom Hanks was spotted here filming a secret spiritual scene in 2018",
            "Emma Stone once got lost in the temple's secret underground chambers",
            "Brad Pitt has been seen here every autumn for the past 3 years",
        ],
        "insider_tips": [
            "Best time to visit: early morning to avoid the crowds",
            "The autumn colors are spectacular from October to November",
            "There's a secret viewpoint that only locals know about",
            "Visit during the evening for the dramatic lighting effects",
        ],
    },
    "sydney_opera_house": {
        "secrets": [
            "The building's roof tiles are self-cleaning and never need to be replaced",
            "There's a secret underground chamber that's never been opened",
            "The building's design was inspired by orange segments",
            "Local legend: the building's guardian spirits still protect the site",
        ],
        "celebrity_sightings": [
            "Tom Hanks was spotted here filming a secret musical scene in 2019",
            "Emma Stone once got lost in the building's secret underground chambers",
            "Brad Pitt has been seen here every summer for the past 5 years",
        ],
        "insider_tips": [
            "Best time to visit: early morning to avoid the crowds",
            "The backstage tour is worth the extra cost for the amazing views",
            "There's a secret viewpoint that only locals know about",
            "Visit during the evening for the dramatic lighting effects",
        ],
    },
    "christ_redeemer": {
        "secrets": [
            "The statue was built in pieces and assembled on site",
            "There's a secret underground chamber that's never been opened",
            "The statue's arms span 28 meters and can hold 40 people",
            "Local legend: the statue's guardian spirits still protect the site",
        ],
        "celebrity_sightings": [
            "Tom Hanks was spotted here filming a secret religious scene in 2018",
            "Emma Stone once got lost in the statue's secret underground chambers",
            "Brad Pitt has been seen here every Easter for the past 10 years",
        ],
        "insider_tips": [
            "Best time to visit: early morning to avoid the crowds",
            "The cog train ride is worth the extra cost for the amazing views",
            "There's a secret viewpoint that only locals know about",
            "Visit during the evening for the dramatic lighting effects",
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
