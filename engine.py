# --- CELL #2: THE ENGINE ---
#NO def polyglot_nexus_engine(technical_topic: str):
    # System prompt defines the unique cultural logic for your 6 languages
    #NO system_prompt = """
    #NO You are the Polyglot-Nexus Semantic Logic Adapter. 
    # NO Explain the topic below for 5 cultures using these specific 'Pragmatic
# Rules':

#NO    1. GERMAN: Direct, formal 'Sie', technical rigor, no fluff.
#NO    2. FRENCH: Analytical structure, high linguistic register (Soutenu).
#NO    3. ITALIAN: Relational, focus on the 'art' and history of the logic.
#NO    4. SPANISH: High-energy, collaborative, focus on community impact.
#NO    5. ARABIC: High-context, respectful, use traditional honorifics.

#NO    Format the output with bold headers for each language.
#NO    """

    # Calling Llama 3.3 70B for high-intelligence multilingual reasoning
#NO    completion = client.chat.completions.create(
#NO        model="llama-3.3-70b-versatile",
#NO        messages=[
#NO            {"role": "system", "content": system_prompt},
#NO            {"role": "user", "content": f"Concept: {technical_topic}"}
#NO        ],
#NO        temperature=0.6,
#NO        max_tokens=2500
#NO    )
    
#NO    return completion.choices[0].message.content


# New "Stabilized" version to avoid hallucination due to the fact that non latin
# language tokanization neiborhood proximity

# --- CELL #2: THE ENGINE (STABILIZED) ---
import os
from groq import Groq
def polyglot_nexus_engine(technical_topic: str):
    system_prompt = """
    You are the Polyglot-Nexus Semantic Logic Adapter. 
    Explain the topic for 5 cultures. 
    
    STRICT SCRIPT RULES:
    1. GERMAN: Formal 'Sie'.
    2. FRENCH: Academic 'Soutenu'.
    3. ITALIAN: Relational/Artistic.
    4. SPANISH: Community-focused.
    5. ARABIC: Use ONLY Modern Standard Arabic script (العربية). 
       Do not use any other non-Latin scripts like Chinese or Cyrillic.
       Use respectful honorifics.

    6. Maltese: Use ONLY Maltese script. Do not use any other scripts like 
       Chinese or Cyrillic or Arabic.

    Format: Use clear Markdown headers.
    """

    # Lowering temperature to 0.4 makes the model more 'stable' and less likely
    # to swap scripts
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Concept: {technical_topic}"}
        ],
        temperature=0.4 
    )
    
    return completion.choices[0].message.content
