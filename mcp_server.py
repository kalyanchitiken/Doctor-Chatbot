from mcp.server.fastmcp import FastMCP
from dataset_loader import search_by_symptoms

mcp = FastMCP("DoctorTools")


@mcp.tool()
def check_emergency(symptoms: str) -> str:
    emergency_keywords = [
        "chest pain", "breathing problem", "shortness of breath",
        "unconscious", "seizure", "bleeding"
    ]

    found = [kw for kw in emergency_keywords if kw in symptoms.lower()]

    if found:
        return f"🚨 EMERGENCY: {', '.join(found)} detected. Call 108 immediately."

    return "No emergency detected."


@mcp.tool()
def search_diseases(symptoms: str) -> str:
    return search_by_symptoms(symptoms)


if __name__ == "__main__":
    mcp.run(transport="stdio")