# 🛒 Microservices e-commerce – Projet EPSIC

Ce projet démontre l’architecture de microservices à l’aide de deux services REST :
- **Catalogue produit** (Spring Boot + PostgreSQL)
- **Gestion de commandes** (Flask + SQLite)

L'infrastructure utilise :
- 📦 Docker Compose pour le déploiement multi-conteneur
- 🚪 Traefik comme API Gateway
- 🐰 RabbitMQ comme middleware de messagerie (Work Queues)
- 🗃️ PostgreSQL comme base de données du catalogue

---

## 📁 Structure du projet

ecommerce_374/
├── catalogue/ # Service Spring Boot
├── orders/ # Service Flask
├── docker-compose.yml # Déploiement multi-conteneur
├── README.md # Guide de démarrage

yaml
Copier
Modifier

---

## ⚙️ Technologies utilisées

| Composant       | Techno                    |
|----------------|---------------------------|
| API Catalogue   | Spring Boot + PostgreSQL |
| API Commandes   | Flask + SQLite           |
| API Gateway     | Traefik                  |
| Message Broker  | RabbitMQ (Work Queue)    |
| Orchestration   | Docker Compose           |

---

## 🚀 Lancer le projet

### 1. Pré-requis

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Java 17 (si build local du .jar)

---

### 2. Générer le `.jar` pour Spring Boot

Dans le dossier `catalogue/`, exécute :

```bash
mvn clean package
```
Un fichier .jar sera généré dans target/. Il sera utilisé par le Dockerfile.

3. Lancer les conteneurs
À la racine du projet (ecommerce_374/), exécute :

```bash
docker-compose up --build
```
Cela démarre :

Spring Boot sur /api/products

Flask sur /api/orders

RabbitMQ sur localhost:15672

Traefik Dashboard sur localhost:8080

4. Accès aux services
Composant	URL
API Produits	http://localhost/api/products
API Commandes	http://localhost/api/orders
RabbitMQ UI	http://localhost:15672 (guest / guest)
Traefik UI	http://localhost:8080

🧪 Exemple de requêtes
➕ Ajouter un produit
```bash
curl -X POST http://localhost/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "T-shirt", "description": "100% coton", "price": 20.0}'
```
🧾 Passer une commande
```bash
curl -X POST http://localhost/api/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 3}'
```
🔁 Communication entre services
Le service Flask appelle l’API Spring Boot pour vérifier le prix du produit.

Le service Spring Boot envoie un message dans RabbitMQ après chaque création de produit.

Le service Flask consomme ce message via une Work Queue.

🛠️ Débogage
📦 docker ps → Voir les conteneurs actifs

📜 docker logs <nom_du_service> → Afficher les logs d’un service

🧹 docker-compose down → Arrêter et supprimer tous les conteneurs

📘 Pattern de messagerie utilisé
Work Queues (modèle producteur → file → consommateur)

Cela permet :

un découplage entre microservices

une mise en file fiable des événements

une scalabilité facile (plusieurs workers Flask possibles)

🧹 Nettoyer le projet
bash
Copier
Modifier
docker-compose down -v --remove-orphans
📬 Auteur
Projet développé dans le cadre de l’EPSIC – Module 321 – VGZ 6
Auteur : Jérémy Gachet

yaml
Copier
Modifier

---





---
# 🚀 Déploiement avec Docker Swarm
---

## Étapes pour déployer :
1. Initialiser Swarm (sur Play With Docker ou localement) :
```bash
docker swarm init
```

2. Déployer la stack :
```bash
docker stack deploy -c docker-compose.yml ecommerce
```

3. Vérifier les services :
```bash
docker service ls
```

4. Vérifier les réplicas :
```bash
docker service ps ecommerce_catalogue
```

5. (Optionnel) Ajouter le visualizer :
```yaml
  visualizer:
    image: dockersamples/visualizer:latest
    ports:
      - "8081:8080"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
    deploy:
      placement:
        constraints: [node.role == manager]
    networks:
      - backend
```
Accès : `http://localhost:8081` pour voir l’état du cluster.

---
