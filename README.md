# 🛒 Microservices e-commerce – Projet EPSIC

Ce projet démontre l’architecture de microservices à l’aide de deux services REST :
- **Catalogue produit** (Spring Boot + PostgreSQL)
- **Gestion de commandes** (Flask + SQLite)

L'infrastructure utilise :
- 📦 Docker Swarm pour le déploiement multi-conteneur
- 🚪 Traefik comme API Gateway
- 🐰 RabbitMQ comme middleware de messagerie (Work Queues)
- 🗃️ PostgreSQL comme base de données du catalogue

---

## 📁 Structure du projet

```
ecommerce_374/
├── src/                    # Service Spring Boot (catalogue)
│   ├── Dockerfile
│   └── ... (code + pom.xml)
├── front/                  # Service Flask (commandes)
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
├── target/                 # Fichier .jar généré par Maven
├── docker-compose.yml      # Déploiement Docker Swarm
├── README.md
```

---

## ⚙️ Technologies utilisées

| Composant       | Techno                    |
|----------------|---------------------------|
| API Catalogue   | Spring Boot + PostgreSQL |
| API Commandes   | Flask + SQLite           |
| API Gateway     | Traefik                  |
| Message Broker  | RabbitMQ (Work Queue)    |
| Orchestration   | Docker Swarm             |

---

## 🚀 Lancer le projet

### 1. Pré-requis

- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Java 17 (pour compiler le projet Spring)
- Maven (`mvn -v` doit fonctionner)

---

### 2. Générer le fichier `.jar` Spring Boot

Dans le dossier racine du projet :

```bash
mvn clean package
```

Un fichier `.jar` sera généré dans `target/`. Il est utilisé par le Dockerfile du service `catalogue`.

---

### 3. Construire les images Docker

```bash
# Image Spring Boot
docker build -t ecommerce_catalogue -f src/Dockerfile .

# Image Flask
docker build -t ecommerce_orders ./front
```

---

### 4. Initialiser Docker Swarm

```bash
docker swarm init
```

---

### 5. Déployer la stack avec Docker Swarm

```bash
docker stack deploy -c docker-compose.yml ecommerce
```

---

## 🔗 Accès aux services

| Composant       | URL                                     |
|----------------|------------------------------------------|
| API Produits    | http://localhost/api/products           |
| API Commandes   | http://localhost/api/orders             |
| RabbitMQ UI     | http://localhost:15672 (guest / guest)  |
| Traefik UI      | http://localhost:8080                   |

---

## 🧪 Exemple de requêtes

### ➕ Ajouter un produit

```bash
curl -X POST http://localhost/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "T-shirt", "description": "100% coton", "price": 20.0}'
```

### 🧾 Passer une commande

```bash
curl -X POST http://localhost/api/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 3}'
```

---

## 🔁 Communication entre services

- Le service Flask appelle l’API Spring Boot pour récupérer le produit.
- Le service Spring Boot publie un message RabbitMQ après la création du produit.
- Le service Flask consomme ce message dans un **worker asynchrone**.

---

## 🛠️ Débogage

| Action                      | Commande                                     |
|----------------------------|----------------------------------------------|
| Voir les services Swarm    | `docker service ls`                          |
| Voir les conteneurs actifs | `docker ps`                                  |
| Logs d’un service          | `docker service logs ecommerce_orders`       |
| Voir les réplicas          | `docker service ps ecommerce_catalogue`      |

---

## 📘 Pattern de messagerie utilisé

Le système utilise le pattern **Work Queues** de RabbitMQ :

- 📤 Producteur = service Spring Boot
- 📥 Consommateur = worker du service Flask
- ✅ Avantages : découplage, scalabilité, fiabilité des messages

---

## 🧹 Nettoyer le projet

```bash
docker stack rm ecommerce
docker system prune -f
```

---

## 🔭 (Optionnel) Visualiser le cluster Swarm

Ajoute ce service dans `docker-compose.yml` :

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

Accès : [http://localhost:8081](http://localhost:8081)

---

## 👨‍💻 Auteurs

- Jérémy Gachet  
- Nahel Kivuila  
- Paco Galasso
