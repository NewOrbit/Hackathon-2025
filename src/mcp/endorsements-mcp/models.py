"""
Endorsements data models - Data classes for endorsement objects.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class Endorsement:
    name: str
    comment: str
    timestamp: datetime
    
    def __str__(self) -> str:
        return f"{self.timestamp.isoformat()}|{self.name}|{self.comment}"
    
    @classmethod
    def from_string(cls, line: str) -> 'Endorsement':
        """Parse an endorsement from a string line"""
        parts = line.strip().split('|', 2)
        if len(parts) >= 2:
            timestamp_str = parts[0]
            name = parts[1]
            comment = parts[2] if len(parts) > 2 else ""
            
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
            except ValueError:
                timestamp = datetime.now()
            
            return cls(name=name, comment=comment, timestamp=timestamp)
        else:
            # Fallback for malformed lines
            return cls(name=line.strip(), comment="", timestamp=datetime.now())


@dataclass
class EndorsementStats:
    total_count: int
    recent_count: int  # Last 30 days
    latest_endorsement: Optional[Endorsement] = None
    
    def to_dict(self):
        return {
            "total_count": self.total_count,
            "recent_count": self.recent_count,
            "latest_endorsement": {
                "name": self.latest_endorsement.name,
                "comment": self.latest_endorsement.comment,
                "timestamp": self.latest_endorsement.timestamp.isoformat()
            } if self.latest_endorsement else None
        }