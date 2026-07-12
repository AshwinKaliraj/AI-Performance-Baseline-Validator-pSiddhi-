latest_analysis = {
    "gemini": "",
    "groq": ""
}

def update(gemini, groq):
    latest_analysis["gemini"] = gemini
    latest_analysis["groq"] = groq

def get():
    return latest_analysis