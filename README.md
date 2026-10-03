# Feedback Analyzer

Feedback Analyzer est une application d'analyse de sentiment. L'utilisateur saisit un avis dans une interface web, et l'application indique s'il est positif, négatif ou neutre, avec un score entre -1 et +1.

Le projet comprend :

- une **API REST Flask** qui analyse le texte avec la bibliothèque VADER (testée avec pytest),
- une **interface Streamlit** qui appelle cette API,
- une **chaîne DevOps complète** : Docker, Docker Compose avec Nginx, CI GitHub Actions, déploiement sur Render et déploiement sur Kubernetes (Minikube).

VADER fonctionne pour l'anglais. Un texte en français sera le plus souvent classé neutre.

## Structure

```
app/                  API Flask
tests/                tests pytest
ui/                   interface Streamlit (avec son Dockerfile)
docker/nginx.conf     configuration Nginx
k8s/                  manifests Kubernetes
.github/workflows/    pipeline CI
Dockerfile            image de l'API
docker-compose.yml    API + UI + Nginx
```

## API

| Méthode | Route      | Description                      |
|---------|------------|----------------------------------|
| GET     | `/health`  | Vérifie que l'API fonctionne     |
| POST    | `/analyze` | Analyse le sentiment d'un texte  |

Exemple de requête et de réponse :

```bash
curl -X POST http://localhost/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

```json
{"text": "I love this product!", "sentiment": "positive", "score": 0.6696}
```

## Lancer le projet

### Avec Docker Compose

```bash
docker compose up --build
```

Ouvrir <http://localhost> pour l'interface. L'API est accessible via <http://localhost/health> et <http://localhost/analyze>.

Arrêter : `docker compose down`.

### En local, sans Docker

Lancer l'API :

```bash
pip install -r requirements.txt
python -m pytest
python app.py
```

Dans un autre terminal, lancer l'interface :

```bash
cd ui
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Ouvrir <http://localhost:8501>.

### Avec Kubernetes (Minikube)

```bash
minikube start

docker build -t feedback-analyzer:latest .
docker build -t feedback-ui:latest ./ui
minikube image load feedback-analyzer:latest
minikube image load feedback-ui:latest

kubectl apply -f k8s/
kubectl get pods
kubectl port-forward svc/feedback-ui-service 8501:80
```

Ouvrir <http://localhost:8501>.

## CI/CD

À chaque push sur `main`, GitHub Actions installe les dépendances, lance les tests pytest et construit les images Docker de l'API et de l'interface. L'API est ensuite déployée automatiquement sur Render.