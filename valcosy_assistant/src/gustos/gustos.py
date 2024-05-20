import spacy
from spacy.matcher import Matcher
import os

nlp = spacy.load("es_core_news_lg")

matcher = Matcher(nlp.vocab)
matcher.add("LIKE_VERB_NOUN", [[{"LOWER": "me gusta"}, {"POS": "NOUN"}]])
matcher.add("LIKE_ADJ_NOUN", [[{"POS": "ADJ"}, {"POS": "NOUN"}]])
matcher.add("LIKE_SENTIMENT_VERB_NOUN", [[{"LOWER": "estar"}, {"LOWER": "muy"}, {"POS": "NOUN"}]])
"""
matcher.add("PASSIONATE_PHRASE", [
    [{"LOWER": "apasionado"}, {"POS": "ADP"}, {"POS": "DET"}, {"POS": "NOUN"}, {"POS": "CCONJ"}, {"POS": "DET"}, {"POS": "NOUN"}],
    [{"LOWER": "de", "OP": "!"}]  # Negative lookahead for "de"
])
# Worse rules again
"""
matcher.add("LIKE_VERB_GASTRONOMY", [[
    # Negative lookahead for liking verb (won't be matched)
    {"LOWER": {"IN": ["gusta", "encanta", "fascina"]}, "OP": "!"},
    # Optional verb
    {"OP": "?"}, {"POS": "VERB", "OP": "?"},
    # Food/Gastronomy term
    {"LOWER": {"IN": ["comida", "gastronomía"]}},
    # Optional location/type
    {"OP": "?"}, {"LOWER": {"IN": ["local", "nueva", "internacional"]}, "OP": "?"}
]])



matcher.add("CULTURAL_INTEREST", [[{"LOWER": "fascina"}, {"POS": "DET"}, {"POS": "NOUN"}, {"POS": "CCONJ"}, {"POS": "DET"}, {"POS": "NOUN"}, {"POS": "CCONJ"}, {"POS": "DET"}, {"POS": "NOUN"}],[{"LOWER": "historia"}, {"LOWER": "tradiciones"}, {"LOWER": "sitios"}, {"LOWER": "culturales"}]])

your_conversation_data_url = "https://raw.githubusercontent.com/jovillarrealm/mouse_size/master/Sitios%20tur%C3%ADsticos%20culturales.txt"
def fetch(url):
  file_data = "downloaded_file.txt"
  # Check if the file already exists
  if os.path.isfile("downloaded_file.txt"):
    print("File 'downloaded_file.txt' already exists. Skipping download.")
  else:
    import requests
    response = requests.get(url)
    
    if response.status_code == 200:
      # Write the content to a file
      with open(file_data, "wb") as f:
        f.write(response.content)
      print("File downloaded successfully!")
    else:
      print(f"Error downloading file: {response.status_code}")
  with open(file_data, "r") as f:
    out = f.read()
  return out

def run_preferences():
    your_conversation_data = fetch(your_conversation_data_url)
    print(type(your_conversation_data))
    doc = nlp(your_conversation_data)
    matches = matcher(doc)
    for match_id, start, end in matches:
        matched_span = doc[start:end]
        print(f"Gusto encontrado: {matched_span.text}")