"""
Hardcoded restaurant data for London and Paris.
"""

from models import Restaurant, MenuItem, Ingredient

# London Restaurants
LONDON_RESTAURANTS = [
    Restaurant(
        id="london_1",
        name="The Ivy",
        description="Classic British cuisine with modern twists in an elegant setting",
        cuisine_type="British",
        location="London",
        address="1-5 West Street, London WC2H 9NQ",
        phone="+44 20 7836 4751",
        email="reservations@the-ivy.co.uk",
        rating=4.5,
        price_range="$$$$",
        opening_hours={
            "Monday": "12:00-23:00",
            "Tuesday": "12:00-23:00",
            "Wednesday": "12:00-23:00",
            "Thursday": "12:00-23:00",
            "Friday": "12:00-23:00",
            "Saturday": "12:00-23:00",
            "Sunday": "12:00-22:00"
        },
        menu=[
            MenuItem(
                id="london_1_1",
                name="Beef Wellington",
                description="Premium beef fillet wrapped in puff pastry with mushroom duxelles",
                price=45.00,
                currency="GBP",
                category="main",
                ingredients=[
                    Ingredient("beef fillet", "200g", 250, 45, 0, 15, 0, ["beef"]),
                    Ingredient("puff pastry", "100g", 350, 5, 35, 20, 1, ["gluten", "dairy"]),
                    Ingredient("mushrooms", "50g", 15, 2, 3, 0, 1),
                    Ingredient("prosciutto", "30g", 80, 6, 0, 6, 0, ["pork"])
                ],
                total_calories=695,
                total_protein=58,
                total_carbs=38,
                total_fat=41,
                total_fiber=2,
                allergens=["beef", "gluten", "dairy", "pork"],
                dietary_tags=[],
                preparation_time=45,
                spice_level=1
            ),
            MenuItem(
                id="london_1_2",
                name="Fish and Chips",
                description="Traditional British fish and chips with mushy peas",
                price=18.50,
                currency="GBP",
                category="main",
                ingredients=[
                    Ingredient("cod fillet", "180g", 200, 40, 0, 2, 0, ["fish"]),
                    Ingredient("potatoes", "200g", 160, 4, 35, 0, 3),
                    Ingredient("flour", "50g", 180, 5, 35, 1, 2, ["gluten"]),
                    Ingredient("peas", "80g", 60, 4, 10, 0, 4)
                ],
                total_calories=600,
                total_protein=53,
                total_carbs=80,
                total_fat=3,
                total_fiber=9,
                allergens=["fish", "gluten"],
                dietary_tags=[],
                preparation_time=25,
                spice_level=1
            )
        ],
        capacity=120,
        booking_advance_days=30,
        special_features=["outdoor seating", "private dining", "wine cellar"],
        coordinates={"lat": 51.5118, "lng": -0.1260}
    ),
    Restaurant(
        id="london_2",
        name="Dishoom",
        description="Bombay-style cafe serving authentic Indian street food",
        cuisine_type="Indian",
        location="London",
        address="12 Upper St Martin's Ln, London WC2H 9FB",
        phone="+44 20 7420 9320",
        email="reservations@dishoom.com",
        rating=4.3,
        price_range="$$",
        opening_hours={
            "Monday": "08:00-23:00",
            "Tuesday": "08:00-23:00",
            "Wednesday": "08:00-23:00",
            "Thursday": "08:00-23:00",
            "Friday": "08:00-23:00",
            "Saturday": "08:00-23:00",
            "Sunday": "09:00-22:00"
        },
        menu=[
            MenuItem(
                id="london_2_1",
                name="Black Daal",
                description="Slow-cooked black lentils with butter and cream",
                price=12.50,
                currency="GBP",
                category="main",
                ingredients=[
                    Ingredient("black lentils", "150g", 200, 15, 35, 1, 8),
                    Ingredient("butter", "20g", 150, 0, 0, 16, 0, ["dairy"]),
                    Ingredient("cream", "30ml", 100, 1, 1, 10, 0, ["dairy"]),
                    Ingredient("onions", "50g", 20, 1, 4, 0, 1),
                    Ingredient("garlic", "10g", 15, 1, 3, 0, 0)
                ],
                total_calories=485,
                total_protein=18,
                total_carbs=43,
                total_fat=27,
                total_fiber=9,
                allergens=["dairy"],
                dietary_tags=["vegetarian", "gluten-free"],
                preparation_time=20,
                spice_level=3
            )
        ],
        capacity=80,
        booking_advance_days=14,
        special_features=["live music", "outdoor seating", "takeaway"],
        coordinates={"lat": 51.5118, "lng": -0.1260}
    )
]

# Paris Restaurants
PARIS_RESTAURANTS = [
    Restaurant(
        id="paris_1",
        name="L'Atelier de Joël Robuchon",
        description="Michelin-starred French cuisine with innovative presentations",
        cuisine_type="French",
        location="Paris",
        address="5 Rue de Montalembert, 75007 Paris",
        phone="+33 1 42 22 56 56",
        email="reservations@joelrobuchon.com",
        rating=4.7,
        price_range="$$$$",
        opening_hours={
            "Monday": "19:00-22:30",
            "Tuesday": "19:00-22:30",
            "Wednesday": "19:00-22:30",
            "Thursday": "19:00-22:30",
            "Friday": "19:00-22:30",
            "Saturday": "19:00-22:30",
            "Sunday": "Closed"
        },
        menu=[
            MenuItem(
                id="paris_1_1",
                name="Truffle Risotto",
                description="Creamy risotto with black truffle and parmesan",
                price=65.00,
                currency="EUR",
                category="main",
                ingredients=[
                    Ingredient("arborio rice", "120g", 420, 8, 90, 1, 2, ["gluten"]),
                    Ingredient("black truffle", "15g", 50, 2, 5, 2, 1),
                    Ingredient("parmesan", "40g", 160, 14, 0, 11, 0, ["dairy"]),
                    Ingredient("butter", "30g", 220, 0, 0, 24, 0, ["dairy"]),
                    Ingredient("white wine", "50ml", 35, 0, 1, 0, 0)
                ],
                total_calories=885,
                total_protein=24,
                total_carbs=96,
                total_fat=38,
                total_fiber=3,
                allergens=["gluten", "dairy"],
                dietary_tags=["vegetarian"],
                preparation_time=35,
                spice_level=1
            )
        ],
        capacity=60,
        booking_advance_days=60,
        special_features=["michelin star", "wine pairing", "private chef"],
        coordinates={"lat": 48.8566, "lng": 2.3522}
    ),
    Restaurant(
        id="paris_2",
        name="Le Comptoir du Relais",
        description="Traditional French bistro with classic dishes and local atmosphere",
        cuisine_type="French",
        location="Paris",
        address="9 Carrefour de l'Odéon, 75006 Paris",
        phone="+33 1 44 27 07 97",
        email="contact@comptoirdurelais.com",
        rating=4.2,
        price_range="$$$",
        opening_hours={
            "Monday": "12:00-14:30, 19:00-22:30",
            "Tuesday": "12:00-14:30, 19:00-22:30",
            "Wednesday": "12:00-14:30, 19:00-22:30",
            "Thursday": "12:00-14:30, 19:00-22:30",
            "Friday": "12:00-14:30, 19:00-22:30",
            "Saturday": "12:00-14:30, 19:00-22:30",
            "Sunday": "Closed"
        },
        menu=[
            MenuItem(
                id="paris_2_1",
                name="Coq au Vin",
                description="Classic French chicken braised in red wine with mushrooms",
                price=28.00,
                currency="EUR",
                category="main",
                ingredients=[
                    Ingredient("chicken thigh", "200g", 300, 35, 0, 18, 0, ["chicken"]),
                    Ingredient("red wine", "100ml", 85, 0, 2, 0, 0),
                    Ingredient("mushrooms", "80g", 20, 3, 4, 0, 2),
                    Ingredient("bacon", "40g", 180, 8, 0, 14, 0, ["pork"]),
                    Ingredient("onions", "60g", 25, 1, 6, 0, 1)
                ],
                total_calories=610,
                total_protein=47,
                total_carbs=12,
                total_fat=32,
                total_fiber=3,
                allergens=["chicken", "pork"],
                dietary_tags=["gluten-free"],
                preparation_time=50,
                spice_level=2
            )
        ],
        capacity=45,
        booking_advance_days=21,
        special_features=["outdoor seating", "wine bar", "traditional atmosphere"],
        coordinates={"lat": 48.8522, "lng": 2.3372}
    )
]

# Rome Restaurants
ROME_RESTAURANTS = [
    Restaurant(
        id="rome_1",
        name="Roscioli",
        description="Historic Roman trattoria serving traditional Roman cuisine and exceptional wine selection",
        cuisine_type="Italian",
        location="Rome",
        address="Via dei Giubbonari, 21, 00186 Roma RM",
        phone="+39 06 687 5287",
        email="info@roscioli.com",
        rating=4.6,
        price_range="$$$",
        opening_hours={
            "Monday": "12:00-15:00, 19:00-23:00",
            "Tuesday": "12:00-15:00, 19:00-23:00",
            "Wednesday": "12:00-15:00, 19:00-23:00",
            "Thursday": "12:00-15:00, 19:00-23:00",
            "Friday": "12:00-15:00, 19:00-23:00",
            "Saturday": "12:00-15:00, 19:00-23:00",
            "Sunday": "Closed"
        },
        menu=[
            MenuItem(
                id="rome_1_1",
                name="Cacio e Pepe",
                description="Classic Roman pasta with pecorino cheese and black pepper",
                price=16.00,
                currency="EUR",
                category="main",
                ingredients=[
                    Ingredient("spaghetti", "120g", 420, 15, 85, 2, 3, ["gluten"]),
                    Ingredient("pecorino romano", "60g", 240, 18, 0, 18, 0, ["dairy"]),
                    Ingredient("black pepper", "5g", 15, 1, 3, 0, 1),
                    Ingredient("pasta water", "50ml", 0, 0, 0, 0, 0),
                    Ingredient("olive oil", "10ml", 90, 0, 0, 10, 0)
                ],
                total_calories=765,
                total_protein=34,
                total_carbs=88,
                total_fat=30,
                total_fiber=4,
                allergens=["gluten", "dairy"],
                dietary_tags=["vegetarian"],
                preparation_time=15,
                spice_level=2
            ),
            MenuItem(
                id="rome_1_2",
                name="Saltimbocca alla Romana",
                description="Veal cutlets with prosciutto and sage in white wine sauce",
                price=28.00,
                currency="EUR",
                category="main",
                ingredients=[
                    Ingredient("veal cutlets", "200g", 300, 40, 0, 12, 0, ["beef"]),
                    Ingredient("prosciutto", "40g", 120, 8, 0, 10, 0, ["pork"]),
                    Ingredient("sage", "5g", 5, 0, 1, 0, 0),
                    Ingredient("white wine", "50ml", 35, 0, 1, 0, 0),
                    Ingredient("butter", "20g", 150, 0, 0, 16, 0, ["dairy"]),
                    Ingredient("flour", "20g", 70, 2, 15, 0, 1, ["gluten"])
                ],
                total_calories=680,
                total_protein=50,
                total_carbs=17,
                total_fat=38,
                total_fiber=1,
                allergens=["beef", "pork", "dairy", "gluten"],
                dietary_tags=[],
                preparation_time=25,
                spice_level=1
            ),
            MenuItem(
                id="rome_1_3",
                name="Tiramisu",
                description="Classic Italian dessert with coffee-soaked ladyfingers and mascarpone",
                price=8.50,
                currency="EUR",
                category="dessert",
                ingredients=[
                    Ingredient("ladyfingers", "80g", 280, 8, 50, 4, 2, ["gluten", "eggs"]),
                    Ingredient("mascarpone", "100g", 400, 6, 4, 40, 0, ["dairy"]),
                    Ingredient("espresso", "60ml", 2, 0, 0, 0, 0),
                    Ingredient("eggs", "2 large", 140, 12, 1, 10, 0, ["eggs"]),
                    Ingredient("sugar", "40g", 160, 0, 40, 0, 0),
                    Ingredient("cocoa powder", "10g", 20, 2, 4, 1, 2)
                ],
                total_calories=1002,
                total_protein=28,
                total_carbs=99,
                total_fat=55,
                total_fiber=4,
                allergens=["gluten", "eggs", "dairy"],
                dietary_tags=["vegetarian"],
                preparation_time=20,
                spice_level=1
            )
        ],
        capacity=60,
        booking_advance_days=21,
        special_features=["wine cellar", "traditional atmosphere", "historic location"],
        coordinates={"lat": 41.9028, "lng": 12.4964}
    ),
    Restaurant(
        id="rome_2",
        name="Armando al Pantheon",
        description="Family-run trattoria near the Pantheon serving authentic Roman specialties",
        cuisine_type="Italian",
        location="Rome",
        address="Salita dei Crescenzi, 31, 00186 Roma RM",
        phone="+39 06 6880 3034",
        email="info@armandoalpantheon.it",
        rating=4.4,
        price_range="$$",
        opening_hours={
            "Monday": "12:30-14:30, 19:30-22:30",
            "Tuesday": "12:30-14:30, 19:30-22:30",
            "Wednesday": "12:30-14:30, 19:30-22:30",
            "Thursday": "12:30-14:30, 19:30-22:30",
            "Friday": "12:30-14:30, 19:30-22:30",
            "Saturday": "12:30-14:30, 19:30-22:30",
            "Sunday": "Closed"
        },
        menu=[
            MenuItem(
                id="rome_2_1",
                name="Carbonara",
                description="Traditional Roman pasta with eggs, pecorino, guanciale, and black pepper",
                price=14.00,
                currency="EUR",
                category="main",
                ingredients=[
                    Ingredient("spaghetti", "120g", 420, 15, 85, 2, 3, ["gluten"]),
                    Ingredient("guanciale", "60g", 300, 8, 0, 30, 0, ["pork"]),
                    Ingredient("eggs", "2 large", 140, 12, 1, 10, 0, ["eggs"]),
                    Ingredient("pecorino romano", "40g", 160, 12, 0, 12, 0, ["dairy"]),
                    Ingredient("black pepper", "3g", 8, 0, 2, 0, 0)
                ],
                total_calories=1028,
                total_protein=35,
                total_carbs=88,
                total_fat=52,
                total_fiber=3,
                allergens=["gluten", "pork", "eggs", "dairy"],
                dietary_tags=[],
                preparation_time=12,
                spice_level=2
            ),
            MenuItem(
                id="rome_2_2",
                name="Amatriciana",
                description="Classic Roman pasta with tomato sauce, guanciale, and pecorino",
                price=13.00,
                currency="EUR",
                category="main",
                ingredients=[
                    Ingredient("bucatini", "120g", 420, 15, 85, 2, 3, ["gluten"]),
                    Ingredient("guanciale", "50g", 250, 7, 0, 25, 0, ["pork"]),
                    Ingredient("tomato sauce", "100g", 20, 1, 4, 0, 1),
                    Ingredient("pecorino romano", "30g", 120, 9, 0, 9, 0, ["dairy"]),
                    Ingredient("onion", "30g", 12, 0, 3, 0, 0),
                    Ingredient("red pepper flakes", "2g", 6, 0, 1, 0, 0)
                ],
                total_calories=828,
                total_protein=32,
                total_carbs=94,
                total_fat=36,
                total_fiber=4,
                allergens=["gluten", "pork", "dairy"],
                dietary_tags=[],
                preparation_time=18,
                spice_level=3
            ),
            MenuItem(
                id="rome_2_3",
                name="Suppli al Telefono",
                description="Roman rice balls with mozzarella and tomato sauce, breaded and fried",
                price=6.00,
                currency="EUR",
                category="appetizer",
                ingredients=[
                    Ingredient("arborio rice", "80g", 280, 6, 60, 0, 1),
                    Ingredient("mozzarella", "40g", 120, 8, 1, 9, 0, ["dairy"]),
                    Ingredient("tomato sauce", "30g", 6, 0, 1, 0, 0),
                    Ingredient("eggs", "1 large", 70, 6, 0, 5, 0, ["eggs"]),
                    Ingredient("breadcrumbs", "30g", 120, 4, 22, 2, 2, ["gluten"]),
                    Ingredient("olive oil", "20ml", 180, 0, 0, 20, 0)
                ],
                total_calories=776,
                total_protein=24,
                total_carbs=84,
                total_fat=36,
                total_fiber=3,
                allergens=["dairy", "eggs", "gluten"],
                dietary_tags=["vegetarian"],
                preparation_time=30,
                spice_level=1
            )
        ],
        capacity=40,
        booking_advance_days=14,
        special_features=["family-run", "near Pantheon", "traditional recipes"],
        coordinates={"lat": 41.8986, "lng": 12.4769}
    )
]
