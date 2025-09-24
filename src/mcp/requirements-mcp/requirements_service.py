"""Mocked travel requirements data used by the MCP server."""

from __future__ import annotations

from typing import Dict, Any, Optional
from dataclasses import dataclass

from fixtures import SECURITY_FIXTURES, VISA_FIXTURES, BAGGAGE_FIXTURES


@dataclass
class RequirementsRouter:
    security_fixtures: Dict[str, Dict[str, Any]]
    visa_fixtures: Dict[str, Dict[str, Any]]
    baggage_fixtures: Dict[str, Dict[str, Any]]

    def get_security_rules(
        self,
        airport_code: Optional[str],
        country_code: Optional[str],
        airline: Optional[str],
        cabin_class: Optional[str],
    ) -> Dict[str, Any]:
        key_candidates = [
            airport_code.lower() if airport_code else None,
            airline.lower() if airline else None,
            country_code.lower() if country_code else None,
            "default",
        ]
        for candidate in key_candidates:
            if candidate and candidate in self.security_fixtures:
                return self.security_fixtures[candidate]
        return self.security_fixtures["default"]

    def get_visa_requirements(
        self,
        nationality: str,
        destination_country: str,
        stay_length_days: int,
    ) -> Dict[str, Any]:
        key = f"{nationality.lower()}-{destination_country.lower()}"
        info = self.visa_fixtures.get(key, self.visa_fixtures["default"])
        info = info.copy()
        info["stay_length_days"] = stay_length_days
        return info

    def check_baggage_allowance(self, airline: str, cabin_class: str) -> Dict[str, Any]:
        airline_key = (airline or "").lower()
        cabin_key = (cabin_class or "").lower() or "default"

        airline_data = self.baggage_fixtures.get(airline_key, self.baggage_fixtures["default"])
        result = airline_data.get(cabin_key)
        if result is None:
            if "default" in airline_data:
                return airline_data["default"]
            return self.baggage_fixtures["default"].get(cabin_key, self.baggage_fixtures["default"]["economy"])
        return result

    def format_requirements_resource(self, nationality: str, destination: str) -> str:
        visa = self.get_visa_requirements(nationality, destination, stay_length_days=7)
        security = self.get_security_rules(None, destination, None, None)
        prohibited = ", ".join(security.get("prohibited", []))
        restricted = ", ".join(security.get("restricted", []))
        return "\n".join(
            [
                f"Requirements summary for travellers from {nationality} to {destination}:",
                "",
                "Visa / entry:",
                f"- Requirement: {visa['visa_requirement']}",
                f"- Max stay: {visa['max_stay_days']} days",
                f"- Notes: {visa['notes']}",
                "",
                "Security reminders:",
                f"- Prohibited: {prohibited or 'None listed'}",
                f"- Restricted: {restricted or 'None listed'}",
            ]
        )

    def get_required_documents_prompt(self, nationality: str, destination: str) -> str:
        return (
            f"Provide a checklist for a traveller from {nationality} visiting {destination}, "
            "including visa paperwork, identification, health documents, and airline baggage considerations."
        )


requirements_router = RequirementsRouter(
    SECURITY_FIXTURES,
    VISA_FIXTURES,
    BAGGAGE_FIXTURES,
)

