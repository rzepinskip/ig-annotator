import requests
import json
from igannotator.rulesexecutor.ig_element import IGElement

API_URL = "http://api.slowosiec.clarin-pl.eu:80/plwordnet-api/"
ACTOR_DOMAINS = ['os', 'grp']

def nounClassifier(word):
    """Classifies noun as actor o object

    Parameters
    ----------
    word : str
        Lematized noun to be classified (case-insensitive).
    """
    
    word = word.lower()
    response_raw = requests.get(f'{API_URL}senses/search?lemma={word}&&&partOfSpeech=noun&&&&&&')
    response = json.loads(response_raw.content)
    response = [item for item in response['content'] if item['lemma']['word'].lower() == word]
    if len(response) == 0:
        return None
    if any(item['domain']['name'][item['domain']['name'].rfind('_')+1 : ] in ACTOR_DOMAINS for item in response): 
        return IGElement.ACTOR
    else:
        return IGElement.OBJECT