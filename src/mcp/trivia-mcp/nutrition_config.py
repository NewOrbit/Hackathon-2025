"""
Nutrition Trivia MCP configuration and in-memory database.
"""

# Nutrition-focused trivia database
NUTRITION_TRIVIA_DATABASE = {
    "protein": {
        "nutrition_secrets": [
            "Your body can only absorb 25-35g of protein per meal - the rest gets stored as fat!",
            "Plant proteins are incomplete - you need to combine grains with legumes for complete amino acids",
            "Whey protein is absorbed 30% faster than casein, making it perfect for post-workout",
            "Ancient bodybuilders used to eat 20+ eggs daily - modern science says 3-4 is optimal",
        ],
        "celebrity_nutrition": [
            "Dwayne 'The Rock' Johnson eats 6-7 meals daily, consuming 5,000+ calories",
            "Arnold Schwarzenegger's secret: he never skipped breakfast, even during competitions",
            "Serena Williams follows a plant-based diet but still dominates tennis",
            "Chris Hemsworth's Thor diet: 4,000 calories daily with 40% protein",
        ],
        "nutrition_tips": [
            "Eat protein within 30 minutes post-workout for maximum muscle synthesis",
            "Combine rice and beans for a complete protein - it's cheaper than meat!",
            "Greek yogurt has 2x the protein of regular yogurt",
            "Your body burns 20-30% of protein calories just digesting it (thermic effect)",
        ],
    },
    "carbs": {
        "nutrition_secrets": [
            "Your brain uses 120g of glucose daily - that's why you feel foggy on low-carb diets",
            "Resistant starch in cold potatoes acts like fiber and feeds good gut bacteria",
            "White rice has a higher glycemic index than table sugar (GI 73 vs 65)",
            "Ancient humans ate 100+ different plant foods - modern diets average just 12",
        ],
        "celebrity_nutrition": [
            "Tom Brady avoids nightshades (tomatoes, peppers) - claims they cause inflammation",
            "LeBron James eats 5-6 meals daily, with carbs strategically timed around workouts",
            "Venus Williams switched to raw vegan diet to manage her autoimmune condition",
            "Conor McGregor's secret: sweet potatoes before fights for sustained energy",
        ],
        "nutrition_tips": [
            "Eat carbs 2-3 hours before workouts for optimal performance",
            "Brown rice has 3x more fiber than white rice",
            "Oats contain beta-glucan fiber that lowers cholesterol naturally",
            "Your muscles can store 400-500g of glycogen - that's 1,600-2,000 calories!",
        ],
    },
    "fats": {
        "nutrition_secrets": [
            "Your brain is 60% fat - that's why low-fat diets can cause depression",
            "Coconut oil is 90% saturated fat but contains MCTs that boost metabolism",
            "Omega-3s from fish reduce inflammation better than supplements",
            "Avocados have more potassium than bananas and 20+ vitamins/minerals",
        ],
        "celebrity_nutrition": [
            "Gwyneth Paltrow's GOOP diet: bulletproof coffee with grass-fed butter daily",
            "Mark Wahlberg eats 6 meals with healthy fats to maintain his physique",
            "Jennifer Aniston's secret: she never skips her morning avocado toast",
            "Hugh Jackman's Wolverine diet: 40% healthy fats for hormone production",
        ],
        "nutrition_tips": [
            "Eat fats with vegetables to absorb fat-soluble vitamins (A, D, E, K)",
            "Olive oil loses nutrients when heated above 375°F - use for dressings",
            "Nuts and seeds are nature's multivitamins - eat a handful daily",
            "Your body needs fat to make hormones - low-fat diets can cause hormonal issues",
        ],
    },
    "vitamins": {
        "nutrition_secrets": [
            "Vitamin D deficiency affects 1 billion people worldwide - it's the 'sunshine vitamin'",
            "Vitamin C from food is absorbed 2x better than supplements",
            "B12 deficiency can cause permanent nerve damage - vegans must supplement",
            "Vitamin K2 directs calcium to bones instead of arteries - found in fermented foods",
        ],
        "celebrity_nutrition": [
            "Oprah takes 50+ supplements daily and credits them for her energy",
            "Gwyneth Paltrow's vitamin routine costs $200+ monthly",
            "Tom Brady avoids nightshades but loads up on vitamin C from citrus",
            "Jennifer Lopez's secret: she gets vitamin D from 15 minutes of daily sun",
        ],
        "nutrition_tips": [
            "Take vitamin D with fat for better absorption",
            "Vitamin C enhances iron absorption from plant foods",
            "B vitamins work together - take a B-complex, not individual B vitamins",
            "Your skin makes vitamin D from sunlight - but sunscreen blocks it completely",
        ],
    },
    "minerals": {
        "nutrition_secrets": [
            "Magnesium deficiency affects 68% of Americans - it's needed for 300+ enzyme reactions",
            "Zinc deficiency can cause loss of taste and smell - it's in oysters and pumpkin seeds",
            "Iron from meat is absorbed 3x better than from plants",
            "Calcium needs vitamin D and K2 to reach bones - not just calcium alone",
        ],
        "celebrity_nutrition": [
            "Cameron Diaz takes magnesium before bed for better sleep",
            "Ryan Reynolds drinks bone broth daily for collagen and minerals",
            "Gisele Bündchen's secret: she eats seaweed for iodine and trace minerals",
            "Matthew McConaughey credits zinc for his immune system during filming",
        ],
        "nutrition_tips": [
            "Take iron with vitamin C for better absorption",
            "Magnesium helps with sleep, muscle cramps, and anxiety",
            "Zinc is crucial for immune function - oysters have the most",
            "Sea salt contains 60+ trace minerals that table salt lacks",
        ],
    },
    "hydration": {
        "nutrition_secrets": [
            "You lose 2-3 liters of water daily through breathing, sweating, and urination",
            "Dehydration reduces cognitive performance by 20% - even mild dehydration matters",
            "Coconut water has natural electrolytes - better than sports drinks",
            "Your thirst mechanism weakens with age - older adults need to drink more",
        ],
        "celebrity_nutrition": [
            "Beyoncé drinks 1 gallon of water daily and credits it for her glowing skin",
            "Ryan Reynolds starts each day with 32oz of water before coffee",
            "Jennifer Aniston's secret: she adds lemon to water for vitamin C",
            "Dwayne Johnson drinks 1.5 gallons daily during intense training",
        ],
        "nutrition_tips": [
            "Drink water 30 minutes before meals to avoid diluting stomach acid",
            "Add a pinch of sea salt to water for better hydration",
            "Your urine should be pale yellow - dark yellow means dehydration",
            "Cold water is absorbed faster than room temperature water",
        ],
    },
    "gut_health": {
        "nutrition_secrets": [
            "Your gut has 100 trillion bacteria - 10x more than human cells in your body",
            "Fiber feeds good bacteria - they produce short-chain fatty acids that reduce inflammation",
            "Probiotics can survive stomach acid if taken with food",
            "Your gut microbiome affects your mood, weight, and immune system",
        ],
        "celebrity_nutrition": [
            "Gwyneth Paltrow takes probiotics daily and credits them for her energy",
            "Tom Brady avoids gluten and dairy to reduce gut inflammation",
            "Jennifer Lopez's secret: she eats fermented foods for gut health",
            "Hugh Jackman drinks kombucha daily for probiotics",
        ],
        "nutrition_tips": [
            "Eat 30+ different plant foods weekly for diverse gut bacteria",
            "Fermented foods like kimchi and sauerkraut are natural probiotics",
            "Prebiotics (fiber) feed probiotics - eat both together",
            "Your gut takes 2-4 weeks to adapt to dietary changes",
        ],
    },
    "metabolism": {
        "nutrition_secrets": [
            "Your metabolism slows 2-3% per decade after age 30 - but you can reverse it",
            "Muscle burns 6 calories per pound at rest - fat burns only 2 calories",
            "Eating protein increases metabolism for 3-4 hours (thermic effect)",
            "Cold exposure can boost metabolism by 15% through brown fat activation",
        ],
        "celebrity_nutrition": [
            "Chris Hemsworth takes ice baths daily to boost metabolism",
            "Jennifer Lopez's secret: she does intermittent fasting to reset metabolism",
            "Dwayne Johnson eats every 2-3 hours to keep metabolism high",
            "Ryan Reynolds credits cold showers for his energy and metabolism",
        ],
        "nutrition_tips": [
            "Eat protein with every meal to maintain muscle mass",
            "Strength training increases metabolism for 24-48 hours post-workout",
            "Green tea can boost metabolism by 4-5% for 2-3 hours",
            "Your metabolism is highest in the morning - eat your biggest meal then",
        ],
    },
    "weight_loss": {
        "nutrition_secrets": [
            "You need a 3,500 calorie deficit to lose 1 pound of fat",
            "Crash diets slow metabolism permanently - sustainable weight loss is 1-2 lbs/week",
            "Sleep deprivation increases hunger hormones by 30%",
            "Stress increases cortisol, which promotes belly fat storage",
        ],
        "celebrity_nutrition": [
            "Jennifer Aniston lost 30 lbs by cutting out processed foods completely",
            "Chris Pratt's transformation: he ate 6 small meals daily with protein",
            "Rebel Wilson's secret: she focused on building muscle, not just losing weight",
            "Adele's weight loss: she followed a Mediterranean diet with portion control",
        ],
        "nutrition_tips": [
            "Eat protein first to reduce blood sugar spikes and hunger",
            "Drink water before meals to reduce calorie intake by 20%",
            "Chew food 20+ times to increase satiety hormones",
            "Your body burns more calories digesting protein than carbs or fat",
        ],
    },
    "performance": {
        "nutrition_secrets": [
            "Carb loading works best when you taper training 3 days before competition",
            "Caffeine can improve performance by 3-5% - but tolerance builds quickly",
            "Beet juice increases nitric oxide, improving endurance by 2-3%",
            "Your body can store 2,000 calories of glycogen - enough for 2 hours of intense exercise",
        ],
        "celebrity_nutrition": [
            "Serena Williams eats bananas during matches for quick energy",
            "LeBron James drinks beet juice daily for performance",
            "Tom Brady's secret: he avoids inflammatory foods before games",
            "Conor McGregor loads carbs 3 days before fights for maximum energy",
        ],
        "nutrition_tips": [
            "Eat carbs 2-3 hours before training for sustained energy",
            "Protein within 30 minutes post-workout maximizes muscle building",
            "Hydration affects performance more than most people realize",
            "Your body needs 1g protein per pound of bodyweight for muscle building",
        ],
    },
}

NUTRITION_TIP_CATEGORIES = {
    "macros": "Macronutrient tips and secrets",
    "vitamins": "Vitamin and mineral insights",
    "hydration": "Water and electrolyte balance",
    "gut_health": "Digestive health and microbiome",
    "performance": "Sports nutrition and energy",
    "weight_management": "Weight loss and gain strategies",
    "celebrity": "Celebrity nutrition secrets",
    "science": "Scientific nutrition facts",
}

NUTRITION_SECRET_TYPES = ["nutrition_secrets", "celebrity_nutrition", "nutrition_tips"]
