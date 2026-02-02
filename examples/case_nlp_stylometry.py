#!/usr/bin/env python3
"""
Example: NLP Stylometry (Discrete Sets).

Comparing large vocabulary sets of different authors to find unique vs shared terms.
Demonstrates performance on larger sets.
"""

from eule import euler

def tokenize(text):
    """Simple tokenizer."""
    # Lowercase, remove punctuation, split
    import re
    text = text.lower()
    tokens = re.findall(r'\b[a-z]{3,}\b', text) # Words > 3 chars
    return set(tokens)

def main():
    print("📜 NLP Text Analysis (Stylometry)")
    print("===================================\n")
    
    # 1. Simulate Texts (In a real app, these would be load from files)
    # Using generic placeholders for simplicity
    
    text_shakespeare = """
    To be, or not to be, that is the question:
    Whether 'tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune,
    Or to take arms against a sea of troubles
    """
    
    text_modern_marketing = """
    To be the best in the market, usually you have to take outrageous risks.
    We suffer from low fortune unless we optimize our mind for success.
    Arrows of metrics point up.
    """
    
    text_tech_docs = """
    The function takes an array of arrows.
    If the network suffers from high latency, we optimized the sea of data.
    To be boolean or not to be logical, that is the question.
    """

    # 2. Extract Vocabularies
    vocab_sh = tokenize(text_shakespeare)
    vocab_mk = tokenize(text_modern_marketing)
    vocab_tc = tokenize(text_tech_docs)
    
    print(f"Vocabulary Sizes:")
    print(f"  Shakespeare : {len(vocab_sh)}")
    print(f"  Marketing   : {len(vocab_mk)}")
    print(f"  Tech Docs   : {len(vocab_tc)}")
    
    sets = {
        'Shake': vocab_sh,
        'Markt': vocab_mk,
        'Tech': vocab_tc
    }
    
    # 3. Compute Venn Regions
    print("\n🔍 Analyzing Linguistic Overlap...")
    diagram = euler(sets)
    
    # 4. Results
    print("\n📊 Word Distribution:")
    for keys, words in sorted(diagram.items(), key=lambda x: -len(x[1])):
        if not words: continue
        
        # Limit output
        word_list = list(words)
        sample = ", ".join(word_list[:5])
        more = "..." if len(word_list) > 5 else ""
        
        label = " & ".join(sorted(list(keys)))
        print(f"  [{label}]: {len(words)} words")
        print(f"    Sample: {sample}{more}")

    # Specific Query: "Shakespearean Core"
    core = diagram.get(('Shake', 'Markt', 'Tech'), set())
    if core:
        print(f"\n🧠 Universal Core (All 3): {core}")
    else:
        print("\n🧠 No universal words found ( > 3 chars).")

if __name__ == "__main__":
    main()
