"""Country safety assessment service for travel warnings."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class SafetyLevel(str, Enum):
    """Travel safety risk levels based on government travel advisories."""
    SAFE = "safe"
    LOW_RISK = "low_risk"
    MODERATE_RISK = "moderate_risk"
    HIGH_RISK = "high_risk"
    EXTREME_RISK = "extreme_risk"
    TRAVEL_BANNED = "travel_banned"


@dataclass
class SafetyWarning:
    """Travel safety warning information."""
    country: str
    level: SafetyLevel
    message: str
    advisory_date: str
    source: str
    recommendations: List[str]
    emergency_contacts: Optional[Dict[str, str]] = None


class CountrySafetyService:
    """Service to assess travel safety for countries."""

    def __init__(self):
        # In a real implementation, this would connect to government APIs like:
        # - US State Department Travel Advisories
        # - UK Foreign Office Travel Advice
        # - Canadian Travel Advisories
        # - Australian DFAT Smart Traveller
        self._safety_data = self._load_safety_data()

    def _load_safety_data(self) -> Dict[str, SafetyWarning]:
        """Load country safety data. In production, this would fetch from APIs."""
        return {
            # High-risk countries (based on common travel advisories)
            "afghanistan": SafetyWarning(
                country="Afghanistan",
                level=SafetyLevel.EXTREME_RISK,
                message="Do not travel due to armed conflict, civil unrest, crime, terrorism, and kidnapping.",
                advisory_date="2024-09-01",
                source="Multiple Government Advisories",
                recommendations=[
                    "Do not travel to Afghanistan",
                    "If already there, leave immediately via commercial flights",
                    "Register with your embassy if departure is not possible"
                ],
                emergency_contacts={"embassy": "+93-700-108-001", "emergency": "119"}
            ),
            "syria": SafetyWarning(
                country="Syria",
                level=SafetyLevel.EXTREME_RISK,
                message="Do not travel due to terrorism, civil unrest, kidnapping, armed conflict.",
                advisory_date="2024-09-01",
                source="Multiple Government Advisories",
                recommendations=[
                    "Do not travel to Syria",
                    "High risk of detention and kidnapping",
                    "Limited consular services available"
                ]
            ),
            "yemen": SafetyWarning(
                country="Yemen",
                level=SafetyLevel.EXTREME_RISK,
                message="Do not travel due to armed conflict, civil unrest, kidnapping, and terrorism.",
                advisory_date="2024-09-01",
                source="Multiple Government Advisories",
                recommendations=[
                    "Do not travel to Yemen",
                    "Extremely limited consular services",
                    "High risk of arbitrary detention"
                ]
            ),
            "somalia": SafetyWarning(
                country="Somalia",
                level=SafetyLevel.EXTREME_RISK,
                message="Do not travel due to terrorism, kidnapping, and armed conflict.",
                advisory_date="2024-09-01",
                source="Multiple Government Advisories",
                recommendations=[
                    "Do not travel to Somalia",
                    "High terrorism threat",
                    "Limited emergency services"
                ]
            ),
            "iraq": SafetyWarning(
                country="Iraq",
                level=SafetyLevel.HIGH_RISK,
                message="Reconsider travel due to terrorism, kidnapping, armed conflict, and civil unrest.",
                advisory_date="2024-09-01",
                source="Multiple Government Advisories",
                recommendations=[
                    "Reconsider travel to Iraq",
                    "Avoid Kurdistan Region if possible",
                    "Register with your embassy",
                    "Maintain high situational awareness"
                ],
                emergency_contacts={"embassy": "+964-770-443-2030", "emergency": "104"}
            ),
            "libya": SafetyWarning(
                country="Libya",
                level=SafetyLevel.HIGH_RISK,
                message="Do not travel due to crime, terrorism, civil unrest, kidnapping, and armed conflict.",
                advisory_date="2024-09-01",
                source="Multiple Government Advisories",
                recommendations=[
                    "Do not travel to Libya",
                    "Unpredictable security situation",
                    "Limited consular services"
                ]
            ),
            "iran": SafetyWarning(
                country="Iran",
                level=SafetyLevel.HIGH_RISK,
                message="Reconsider travel due to arbitrary enforcement of local laws, terrorism, civil unrest, and kidnapping.",
                advisory_date="2024-09-01",
                source="Multiple Government Advisories",
                recommendations=[
                    "Reconsider travel to Iran",
                    "Risk of arbitrary detention",
                    "Limited consular access for dual nationals"
                ]
            ),
            "north korea": SafetyWarning(
                country="North Korea",
                level=SafetyLevel.TRAVEL_BANNED,
                message="Do not travel due to arbitrary enforcement of local laws and risk of arrest and long-term detention.",
                advisory_date="2024-09-01",
                source="Multiple Government Advisories",
                recommendations=[
                    "Do not travel to North Korea",
                    "US citizens are prohibited from travel",
                    "Extreme risk of arbitrary detention"
                ]
            ),
            "myanmar": SafetyWarning(
                country="Myanmar",
                level=SafetyLevel.HIGH_RISK,
                message="Do not travel due to civil unrest, armed conflict, and arbitrary enforcement of local laws.",
                advisory_date="2024-09-01",
                source="Multiple Government Advisories",
                recommendations=[
                    "Do not travel to Myanmar",
                    "Ongoing civil conflict",
                    "Limited communication and banking services"
                ]
            ),
            "venezuela": SafetyWarning(
                country="Venezuela",
                level=SafetyLevel.HIGH_RISK,
                message="Reconsider travel due to crime, civil unrest, kidnapping, and arbitrary detention.",
                advisory_date="2024-09-01",
                source="Multiple Government Advisories",
                recommendations=[
                    "Reconsider travel to Venezuela",
                    "High crime rates including kidnapping",
                    "Limited consular services"
                ]
            ),
            # Moderate risk examples
            "russia": SafetyWarning(
                country="Russia",
                level=SafetyLevel.MODERATE_RISK,
                message="Exercise increased caution due to terrorism, harassment, and arbitrary enforcement of local laws.",
                advisory_date="2024-09-01",
                source="Multiple Government Advisories",
                recommendations=[
                    "Exercise increased caution",
                    "Avoid political activities and demonstrations",
                    "Register with your embassy"
                ]
            ),
            "china": SafetyWarning(
                country="China",
                level=SafetyLevel.MODERATE_RISK,
                message="Exercise increased caution due to arbitrary enforcement of local laws and COVID-19 restrictions.",
                advisory_date="2024-09-01",
                source="Multiple Government Advisories",
                recommendations=[
                    "Exercise increased caution",
                    "Be aware of local laws and penalties",
                    "Avoid political activities"
                ]
            ),
            # Add some safer countries for context
            "canada": SafetyWarning(
                country="Canada",
                level=SafetyLevel.SAFE,
                message="Exercise normal precautions.",
                advisory_date="2024-09-01",
                source="Travel Advisory",
                recommendations=["Exercise normal travel precautions"]
            ),
            "japan": SafetyWarning(
                country="Japan",
                level=SafetyLevel.SAFE,
                message="Exercise normal precautions.",
                advisory_date="2024-09-01",
                source="Travel Advisory",
                recommendations=["Exercise normal travel precautions"]
            ),
            "australia": SafetyWarning(
                country="Australia",
                level=SafetyLevel.SAFE,
                message="Exercise normal precautions.",
                advisory_date="2024-09-01",
                source="Travel Advisory",
                recommendations=["Exercise normal travel precautions"]
            ),
        }

    def get_safety_warning(self, country: str) -> Optional[SafetyWarning]:
        """Get safety warning for a country."""
        country_key = country.lower().strip()
        return self._safety_data.get(country_key)

    def is_dangerous_destination(self, country: str) -> bool:
        """Check if a destination is considered dangerous for travel."""
        warning = self.get_safety_warning(country)
        if not warning:
            return False

        dangerous_levels = {
            SafetyLevel.HIGH_RISK,
            SafetyLevel.EXTREME_RISK,
            SafetyLevel.TRAVEL_BANNED
        }
        return warning.level in dangerous_levels

    def get_all_dangerous_countries(self) -> List[SafetyWarning]:
        """Get all countries with high risk or above."""
        dangerous_levels = {
            SafetyLevel.HIGH_RISK,
            SafetyLevel.EXTREME_RISK,
            SafetyLevel.TRAVEL_BANNED
        }
        return [
            warning for warning in self._safety_data.values()
            if warning.level in dangerous_levels
        ]

    def format_warning_message(self, warning: SafetyWarning) -> str:
        """Format a safety warning for display."""
        level_emojis = {
            SafetyLevel.SAFE: "✅",
            SafetyLevel.LOW_RISK: "🟡",
            SafetyLevel.MODERATE_RISK: "🟠",
            SafetyLevel.HIGH_RISK: "🔴",
            SafetyLevel.EXTREME_RISK: "⛔",
            SafetyLevel.TRAVEL_BANNED: "🚫"
        }

        emoji = level_emojis.get(warning.level, "⚠️")

        message = f"\n{emoji} **TRAVEL SAFETY WARNING** {emoji}\n"
        message += f"Country: {warning.country}\n"
        message += f"Risk Level: {warning.level.value.upper()}\n"
        message += f"Advisory: {warning.message}\n"

        if warning.recommendations:
            message += "\nRecommendations:\n"
            for rec in warning.recommendations:
                message += f"• {rec}\n"

        if warning.emergency_contacts:
            message += "\nEmergency Contacts:\n"
            for contact_type, number in warning.emergency_contacts.items():
                message += f"• {contact_type.title()}: {number}\n"

        message += f"\nAdvisory Date: {warning.advisory_date}\n"
        message += f"Source: {warning.source}\n"

        return message


def extract_country_from_destination(destination: str) -> Optional[str]:
    """Extract country name from destination string."""
    # Simple mapping for common destinations
    # In production, this would use a more sophisticated approach
    country_mapping = {
        # Cities to countries
        "kabul": "afghanistan",
        "damascus": "syria",
        "aleppo": "syria",
        "sanaa": "yemen",
        "baghdad": "iraq",
        "basra": "iraq",
        "erbil": "iraq",
        "tripoli": "libya",
        "benghazi": "libya",
        "tehran": "iran",
        "isfahan": "iran",
        "pyongyang": "north korea",
        "yangon": "myanmar",
        "mandalay": "myanmar",
        "caracas": "venezuela",
        "moscow": "russia",
        "st. petersburg": "russia",
        "saint petersburg": "russia",
        "beijing": "china",
        "shanghai": "china",
        "hong kong": "china",
        "toronto": "canada",
        "vancouver": "canada",
        "montreal": "canada",
        "tokyo": "japan",
        "osaka": "japan",
        "kyoto": "japan",
        "sydney": "australia",
        "melbourne": "australia",
        "perth": "australia",
        "paris": "france",
        "london": "england",
        "berlin": "germany",
        "rome": "italy",
        "madrid": "spain",
        "amsterdam": "netherlands",
        "stockholm": "sweden",
        "oslo": "norway",
        "copenhagen": "denmark",
        "helsinki": "finland",
    }

    dest_lower = destination.lower().strip()

    # Check if it's directly a country we monitor
    if dest_lower in ["afghanistan", "syria", "yemen", "somalia", "iraq", "libya",
                     "iran", "north korea", "myanmar", "venezuela", "russia", "china",
                     "canada", "japan", "australia", "france", "england", "germany",
                     "italy", "spain", "netherlands", "sweden", "norway", "denmark", "finland"]:
        return dest_lower

    # Check city mapping
    return country_mapping.get(dest_lower)
