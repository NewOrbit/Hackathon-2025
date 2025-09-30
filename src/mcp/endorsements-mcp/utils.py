"""
Utility functions for the Endorsements MCP server.
"""

import os
from pathlib import Path
from typing import List
from datetime import datetime, timedelta

from models import Endorsement, EndorsementStats
from config import ENDORSEMENTS_FILE


def ensure_endorsements_file_exists():
    """Ensure the endorsements file exists"""
    ENDORSEMENTS_FILE.touch(exist_ok=True)


def load_endorsements() -> List[Endorsement]:
    """Load all endorsements from the file"""
    ensure_endorsements_file_exists()
    
    endorsements = []
    try:
        with open(ENDORSEMENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        endorsement = Endorsement.from_string(line)
                        endorsements.append(endorsement)
                    except Exception as e:
                        print(f"Warning: Could not parse endorsement line: {line.strip()} - {e}")
    except FileNotFoundError:
        pass  # File doesn't exist yet, return empty list
    
    return endorsements


def save_endorsements(endorsements: List[Endorsement]):
    """Save all endorsements to the file"""
    with open(ENDORSEMENTS_FILE, 'w', encoding='utf-8') as f:
        for endorsement in endorsements:
            f.write(str(endorsement) + '\n')


def add_endorsement_to_file(name: str, comment: str = "") -> bool:
    """Add a new endorsement to the file"""
    if not name or not name.strip():
        return False
    
    endorsements = load_endorsements()
    
    # Check if this person has already endorsed (prevent duplicates)
    for existing in endorsements:
        if existing.name.lower().strip() == name.lower().strip():
            return False  # Already exists
    
    new_endorsement = Endorsement(
        name=name.strip(),
        comment=comment.strip(),
        timestamp=datetime.now()
    )
    
    endorsements.append(new_endorsement)
    save_endorsements(endorsements)
    return True


def remove_endorsement_from_file(name: str) -> bool:
    """Remove an endorsement by name"""
    if not name or not name.strip():
        return False
    
    endorsements = load_endorsements()
    original_count = len(endorsements)
    
    # Filter out the endorsement with matching name (case-insensitive)
    endorsements = [e for e in endorsements if e.name.lower().strip() != name.lower().strip()]
    
    if len(endorsements) < original_count:
        save_endorsements(endorsements)
        return True
    return False


def get_endorsement_statistics() -> EndorsementStats:
    """Get statistics about endorsements"""
    endorsements = load_endorsements()
    
    total_count = len(endorsements)
    
    # Count recent endorsements (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_count = sum(1 for e in endorsements if e.timestamp >= thirty_days_ago)
    
    # Get latest endorsement
    latest_endorsement = None
    if endorsements:
        latest_endorsement = max(endorsements, key=lambda e: e.timestamp)
    
    return EndorsementStats(
        total_count=total_count,
        recent_count=recent_count,
        latest_endorsement=latest_endorsement
    )


def format_endorsements_for_display(endorsements: List[Endorsement]) -> str:
    """Format endorsements for display"""
    if not endorsements:
        return "No endorsements yet. Be the first to endorse this travel agent!"
    
    formatted = []
    formatted.append(f"🌟 Travel Agent Endorsements ({len(endorsements)} total)")
    formatted.append("=" * 50)
    
    # Sort by most recent first
    sorted_endorsements = sorted(endorsements, key=lambda e: e.timestamp, reverse=True)
    
    for endorsement in sorted_endorsements:
        date_str = endorsement.timestamp.strftime("%Y-%m-%d %H:%M")
        formatted.append(f"👤 {endorsement.name} ({date_str})")
        if endorsement.comment:
            formatted.append(f"   💬 \"{endorsement.comment}\"")
        formatted.append("")
    
    return "\n".join(formatted)