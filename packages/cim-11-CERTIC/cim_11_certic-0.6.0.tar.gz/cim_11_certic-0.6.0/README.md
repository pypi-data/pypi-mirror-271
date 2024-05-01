# CIM-11

## Classification Internationale des Maladies, Onzième Révision

Package fournissant en français une liste de maladies associées à leurs codes internationaux, 
tels que diffusés par l'OMS (Organisation Mondiale de la Santé), ainsi qu'une recherche 
plein-texte sur les labels de ces maladies.

Pour plus de renseignements, voir la page officielle de la CIM-11: https://icd.who.int/fr

## Avertissements

- Ce package n'est pas affilié à l'OMS, merci de ne pas les contacter pour un quelconque support à son sujet
- Ce package est destiné à fournir une solution simple, rapide et surtout hors-ligne au codage des maladies
- Il ne se soustrait pas aux outils fournis par l'OMS et en particulier son API
- Dans sa dernière version, les données de ce package sont figées au 12 mars 2024

## Installation

    pip install cim-11-CERTIC

## Utilisation

    from cim_11 import root_concepts, label_search

    # Parcours de l'arbre:

    for item in root_concepts():
        print(f"-- {item.icode + ' ' if item.icode else ''}{item.label}")
        for child in item.children:
            print(f"-- {child.icode + ' ' if child.icode else ''}{child.label}")
            for sub in child.children:
                print(f"---- {sub.icode + ' ' if sub.icode else ''}{sub.label}")
    
    # Recherche full-text sur label:

    for item in label_search("tumeur foie métastase"):
        print(f"{item.icode} {item.label}")
    
    # Résultats de la recherche:
    
    # 2D80 Métastase de tumeur maligne, dans le foie ou les voies biliaires intrahépatiques
    # 2D80 Métastase de tumeur maligne, dans le foie ou les voies biliaires intrahépatiques
    # 2D80 Métastase de tumeur maligne, dans le foie ou les voies biliaires intrahépatiques
    # 2D80.0 Métastase de tumeur maligne, dans le foie

