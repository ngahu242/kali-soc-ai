from ai.brain import ask_ai

def metasploit_help(service):
    prompt = f"""
Act as Metasploit Assistant.

Target service:
{service}

Provide:

1. Likely exploit modules
2. Recon steps
3. Payload suggestions
4. Safe testing workflow
5. Post exploitation checks
"""
    return ask_ai(prompt)