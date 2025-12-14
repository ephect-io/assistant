# Lora-php-ephect: Fine-tuning LLMs for PHP Code Generation

Ce projet permet de générer un dataset à partir de sources Ephect, puis d'entraîner un modèle de langage (LLM) pour la génération de code PHP à l'aide de la méthode LoRA (Low-Rank Adaptation) et de la bibliothèque PEFT.

## Fonctionnalités principales
- Génération automatique d'un dataset d'instructions et de code PHP à partir de sources Ephect
- Préparation et tokenisation des données pour l'entraînement
- Fine-tuning d'un modèle LLM (par défaut DeepSeek Coder 6.7B) avec LoRA
- Utilisation de HuggingFace Transformers, Datasets, PEFT, Accelerate
- Configuration flexible via YAML (LoRA, Accelerate)

## Structure
- `lora-php-ephect/scripts/generate_dataset.py` : Génère le dataset d'entraînement à partir des sources Ephect
- `lora-php-ephect/scripts/run_all.sh` : Pipeline complet (génération dataset + entraînement)
- `lora-php-ephect/train.py` : Script principal d'entraînement LoRA
- `lora-php-ephect/requirements.txt` : Dépendances Python
- `lora-php-ephect/config/lora.yaml` : Paramètres LoRA
- `lora-php-ephect/accelerate.yaml` : Paramètres Accelerate
- `data/train.jsonl` : Dataset généré
- `outputs/` : Modèles et checkpoints entraînés

## Installation
1. Installez les dépendances Python :
   ```bash
   pip install -r lora-php-ephect/requirements.txt
   ```
2. Installez le framework Ephect :
 
   ```bash
   git clone https://github.com/ephect-io/framework.git ephect-framework
   ```

3. Placez le dossier `framework` à la racine du projet ou ajustez les chemins dans `generate_dataset.py` si nécessaire.

4. Vérifiez/éditez les fichiers de configuration YAML selon vos besoins.

## Utilisation
Lancez le pipeline complet (génération + entraînement) :
```bash
bash lora-php-ephect/scripts/run_all.sh
```

## Prérequis
- Python 3.10+
- GPU recommandé (CUDA)
- Accès internet pour télécharger les modèles HuggingFace

## Auteurs
- David Blanchard
- Projet basé sur Ephect Framework
