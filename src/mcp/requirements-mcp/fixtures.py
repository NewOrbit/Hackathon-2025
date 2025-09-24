"""Static fixtures mirroring the mock clients used inside the agent."""

SECURITY_FIXTURES = {
    "default": {
        "prohibited": [
            "Explosives",
            "Flammable liquids",
            "Firearms",
        ],
        "restricted": [
            "Liquids over 100ml",
            "Lithium batteries over 100Wh",
            "Sharp objects",
        ],
        "notes": [
            "Follow standard TSA/EU aviation security rules.",
            "Liquids must fit in a 1L transparent bag.",
        ],
    }
}


VISA_FIXTURES = {
    "pl-ph": {
        "visa_requirement": "Visa-free for up to 30 days",
        "max_stay_days": 30,
        "notes": "Passport must be valid for at least 6 months and return ticket required.",
    },
    "default": {
        "visa_requirement": "Check with destination embassy",
        "max_stay_days": 14,
        "notes": "Carry passport valid for 6 months and proof of funds.",
    },
}


BAGGAGE_FIXTURES = {
    "default": {
        "economy": {
            "checked_allowance": "1 bag up to 23kg",
            "carry_on": "1 bag up to 7kg",
            "personal_item": "Small backpack or handbag",
        },
        "business": {
            "checked_allowance": "2 bags up to 32kg each",
            "carry_on": "2 bags up to 7kg each",
            "personal_item": "Laptop bag or briefcase",
        },
    },
    "lot": {
        "economy": {
            "checked_allowance": "1 bag up to 23kg (LOT standard)",
            "carry_on": "1 carry-on up to 8kg (55x40x23cm)",
            "personal_item": "Handbag, laptop bag, or small backpack",
        },
        "business": {
            "checked_allowance": "2 bags up to 32kg each",
            "carry_on": "2 carry-on bags up to 9kg each",
            "personal_item": "Laptop bag or garment bag",
        },
        "default": {
            "checked_allowance": "1 bag up to 23kg",
            "carry_on": "1 carry-on up to 8kg",
            "personal_item": "Handbag or laptop bag",
        },
    },
}

