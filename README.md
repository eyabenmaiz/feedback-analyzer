# Feedback analyzer

## Déploiement

L'API est déployée sur Render (PaaS) et accessible publiquement :
https://feedback-analyzer-8vic.onrender.com

Le déploiement est automatique (CD) : chaque push sur `main` déclenche
GitHub Actions (tests + build Docker), et si les checks passent, Render
redéploie automatiquement la nouvelle version.
