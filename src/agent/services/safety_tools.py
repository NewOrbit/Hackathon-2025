"""LangChain tools for travel safety warnings."""

from __future__ import annotations

from typing import Optional, Type

from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from .safety_service import CountrySafetyService, extract_country_from_destination


class SafetyCheckInput(BaseModel):
    """Input for safety check tool."""
    destination: str = Field(description="The destination country or city to check for travel safety warnings")


class TravelSafetyTool(BaseTool):
    """Tool for checking travel safety warnings for destinations."""

    name: str = "check_travel_safety"
    description: str = """Check for travel safety warnings and risk levels for a destination country.
    Use this tool whenever a user mentions a destination to ensure they are aware of any safety risks.
    This is critical for responsible travel advice and should be checked BEFORE providing other recommendations."""
    args_schema: Type[BaseModel] = SafetyCheckInput

    def __init__(self):
        super().__init__()
        # Store safety service as a private attribute to avoid Pydantic issues
        self._safety_service = CountrySafetyService()

    def _run(self, destination: str) -> str:
        """Check safety warnings for a destination."""
        country = extract_country_from_destination(destination)
        if not country:
            return f"No specific safety information available for '{destination}'. Please check official government travel advisories for the most current information."

        warning = self._safety_service.get_safety_warning(country)
        if not warning:
            return f"'{destination.title()}' appears to be a safe destination with no special travel advisories. Always check current conditions before travel."

        # Return warnings for moderate risk and above
        from .safety_service import SafetyLevel
        if warning.level in {SafetyLevel.MODERATE_RISK, SafetyLevel.HIGH_RISK,
                           SafetyLevel.EXTREME_RISK, SafetyLevel.TRAVEL_BANNED}:
            return self._safety_service.format_warning_message(warning)

        return f"'{destination.title()}' is considered a safe destination with normal travel precautions recommended."


def create_safety_tool() -> TravelSafetyTool:
    """Factory function to create the travel safety tool."""
    return TravelSafetyTool()
