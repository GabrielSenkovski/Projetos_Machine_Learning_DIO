# app/schemas.py
from pydantic import BaseModel
from typing import List

class Threat(BaseModel):
    threat_description: str
    mitigation_suggestion: str

class StrideAnalysis(BaseModel):
    spoofing: List[Threat]
    tampering: List[Threat]
    repudiation: List[Threat]
    information_disclosure: List[Threat]
    denial_of_service: List[Threat]
    elevation_of_privilege: List[Threat]

class AnalysisResponse(BaseModel):
    analysis: StrideAnalysis