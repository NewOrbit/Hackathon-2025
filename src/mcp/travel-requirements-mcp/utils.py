"""Travel Requirements MCP Server utilities"""

from typing import Dict, Any

def format_restriction_summary(restrictions: Dict[str, Any]) -> str:
    """Format security restrictions into a readable summary"""
    summary = f"Security restrictions for {restrictions['departure_country']} → {restrictions['arrival_country']}:\n\n"
    
    for item, restriction in restrictions.get('restrictions', {}).items():
        status = restriction['status'].upper()
        carry_on = "✅" if restriction['carry_on_allowed'] else "❌"
        checked = "✅" if restriction['checked_allowed'] else "❌"
        
        summary += f"• {item}: {status}\n"
        summary += f"  Carry-on: {carry_on} | Checked: {checked}\n"
        
        if restriction.get('special_instructions'):
            summary += f"  Note: {restriction['special_instructions']}\n"
        summary += "\n"
    
    return summary

def format_baggage_summary(baggage: Dict[str, Any]) -> str:
    """Format baggage rules into a readable summary"""
    summary = f"Baggage rules for {baggage['airline']} ({baggage['cabin_class']}):\n\n"
    
    carry_on = baggage['carry_on']
    summary += f"✈️ Carry-on: {carry_on['weight_limit_kg']}kg, {carry_on['dimensions_cm']}\n"
    
    checked = baggage['checked']
    summary += f"🧳 Checked: {checked['weight_limit_kg']}kg, {checked['dimensions_cm']}\n"
    summary += f"   Excess fee: ${checked['excess_fee_per_kg']}/kg\n\n"
    
    if baggage.get('prohibited_items'):
        summary += "🚫 Prohibited items:\n"
        for item in baggage['prohibited_items'][:5]:  # Show first 5
            summary += f"   • {item}\n"
    
    return summary