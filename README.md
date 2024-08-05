# Problèmes d'Optimisation en Python

Ce dépôt contient des implémentations de trois problèmes d'optimisation : le bin-packing 1D, le vertex cover résolu avec une approche branch and bound, et un problème d'ordonnancement en programmation par contraintes. Tout le code est écrit en Python et un environnement virtuel est utilisé pour gérer les dépendances.

## Table des Matières

- [Description des Problèmes](#description-des-problèmes)
  - [Bin-Packing 1D](#bin-packing-1d)
  - [Vertex Cover avec Branch and Bound](#vertex-cover-avec-branch-and-bound)
  - [Problème d'Ordonnancement en Programmation par Contraintes](#problème-dordonnancement-en-programmation-par-contraintes)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Contribuer](#contribuer)
- [Licence](#licence)

## Description des Problèmes

### Bin-Packing 1D

Le problème de bin-packing consiste à affecter des objets de tailles différentes dans un nombre minimal de conteneurs de capacité fixe.

### Vertex Cover avec Branch and Bound

Le problème de vertex cover consiste à trouver le plus petit ensemble de sommets dans un graphe tel que chaque arête du graphe est incidente à au moins un sommet de cet ensemble. La solution est trouvée en utilisant une approche de branch and bound.

### Problème d'Ordonnancement en Programmation par Contraintes

Ce problème consiste à attribuer des tâches à des ressources de manière à respecter certaines contraintes (temps, ordre, etc.). La solution utilise la programmation par contraintes pour trouver un ordonnancement optimal.

## Installation

Pour installer et exécuter ce projet, suivez les étapes ci-dessous :

1. Clonez le dépôt :
    ```sh
    git clone https://github.com/votre-nom-utilisateur/votre-repo.git
    cd votre-repo
    ```

2. Créez un environnement virtuel :
    ```sh
    python -m venv env
    ```

3. Activez l'environnement virtuel :
    - Sous Windows :
      ```sh
      .\env\Scripts\activate
      ```
    - Sous macOS et Linux :
      ```sh
      source env/bin/activate
      ```

4. Installez les dépendances :
    ```sh
    pip install -r requirements.txt
    ```

## Utilisation

Chaque problème peut être exécuté séparément. Voici comment les utiliser :

### Bin-Packing 1D

Pour exécuter le script de bin-packing 1D :
```sh
python ./BP/front.py
```
