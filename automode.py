import j2l.pytactx.agent as pytactx
import random

agent = None

etat = "Ronde"
voisinCibleInfos = {}

def rechercheMin(dictionnaire):
  """
  Renvoie la valeur min et sa clé associée dans le dictionnaire spécifié en paramètre
  :param dictionnaire: dictionnaire de clé et valeurs entieres
  :type dictionnaire: dict de key Any, value int or float
  :return: tuple comprenant la clé, la valeur minimale
  """
  minValue = None
  minKey = None
  for key, value in dictionnaire.items():
    if (minValue == None or value < minValue):
      minValue = value
      minKey = key
  return (minKey, minValue)

def actualiserEnnemi():
  global voisinCibleInfos
  possibilites = {}
  for voisinId, voisinInfos in agent.voisins.items():
    agentInfo = {"x":agent.x, "y":agent.y}
    possibilites[voisinId] = eval(agentInfo, voisinInfos)
  # Si des ennemis sont dans le dico possibilités ...
  if (len(possibilites) > 0):
    # Trouver celui qui à le score minimum
    voisinCibleId, voisinCibleCout = rechercheMin(possibilites)
    # Puis se déplacer à sa position en la récupérant dans le dico agent voisin
    voisinCibleInfos = agent.voisins[voisinCibleId]
  

def eval(agentRef, voisin):
  """
  Renvoie un nombre representaant le cout pour notre agent de referent pour aller abattre le voisin spécifié. Cout faible pour voisin interressant à aller abattre.
    type agentRef: dict avec clé str comme attributs d'agent "x", "y" ... 
    type voisin: dict avec clé str comme attributs d'agent "x", "y" ... 
  """
  dx = (agentRef["x"]-voisin["x"])**2
  dy = (agentRef["y"]-voisin["y"])**2
  #rajouter ce que vous voulez pour prendre en compte d'autre critères que la distance comme heuristique
  return dx+dy

def veiller():
  """
  L'agent effectue une ronde dans une zone ou il est actuellement present
  """
  agent.changerCouleur(0, 0, 255)
  global etat
  #Si on repere un ennemi dans la zone, on passe à l'état Eval
  if len(agent.voisins):
    etat = "Eval"
  else:
    agent.deplacer(random.randint(-1,1), random.randint(-1,1),)

def evaluer():
  """
  L'agent est en surveillance dans la zone
  """
  agent.changerCouleur(0, 255, 0)
  global voisinCibleInfos
  global etat
  # Evalue toutes les possibilités : pour chaque agent ennemi dont l'id est mis en clé, on associe en valeur son coût calculé par l'heuristique eval
  possibilites = {}
  for voisinId, voisinInfos in agent.voisins.items():
    agentInfo = {"x":agent.x, "y":agent.y}
    possibilites[voisinId] = eval(agentInfo, voisinInfos)
  # Si des ennemis sont dans le dico possibilités ...
  if (len(possibilites) > 0):
    # Trouver celui qui à le score minimum
    voisinCibleId, voisinCibleCout = rechercheMin(possibilites)
    # Puis se déplacer à sa position en la récupérant dans le dico agent voisin
    voisinCibleInfos = agent.voisins[voisinCibleId]
    
    etat = "Poursuite"
  else:
    etat = "Ronde"
  #Si ennemi dans notre champs de vision, on passe à l'etat poursuite
  if False:
    etat = "Poursuite"
  #Si ennemi present quitte la zone, repasser a l'etat veiller
  

def poursuivre():
  global voisinCibleInfos
  """
  L'agent à un chemin defini en fonction du mouvement de l'ennemi
  """
  agent.changerCouleur(255, 0, 0)
  agent.tirer(True)
  global etat
  #Si ennemi present quitte notre champ de vision, repasser a l'etat Eval
  if agent.voisins == {}:
    etat = "Eval"
  else:
    agent.deplacerVers(voisinCibleInfos["x"], voisinCibleInfos["y"])


def actualiserEtat():
  actualiserEnnemi()
  #Si la variable etat = ronde, on appelle veiller
  if etat == "Ronde":
    veiller()
  elif etat == "Eval":
    evaluer()
  elif etat == "Poursuite":
    poursuivre()
    
  agent.orienter((agent.orientation+1)%4)
  agent.actualiser()