from difflib import SequenceMatcher

def intable(s: str) -> bool:
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def match_score(item: str, against: str) -> float:    
    matcher = SequenceMatcher(None)
    
    score = 0
    
    matcher.set_seqs(item, against)
    
    if " " in item:
        wordScore = 0
        
        words = item.split(" ")
        
        againstLower = against.lower()
        
        for word in words:
            if word.lower() in againstLower:
                wordScore += 1
                
        score += wordScore / len(words) * 0.6
    else:
        score = matcher.ratio()
        
    return score