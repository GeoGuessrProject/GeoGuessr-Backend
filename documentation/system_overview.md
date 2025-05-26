# GeoGuessr Microservices System Overview

Dette projekt er en GeoGuessr-lignende platform udviklet i Python (FastAPI) og Svelte.

## Tech Stack
- **Backend**: Python (FastAPI) med microservice-arkitektur
- **Frontend**: Svelte (Vite) - integrerer med Google Maps API til billeder og kortdata
- **Kommunikation**: REST API + RabbitMQ
- **Databaser**: 
  - MySQL til brugerdata (auth_service)
  - MongoDB til spildata (game_service)
- **Containerisering**: Docker og Docker Compose

## Services

| Service              | Beskrivelse                                                  |
|----------------------|--------------------------------------------------------------|
| `auth_service`       | Håndterer login, register og JWT-token. Gemmer brugere i MySQL |
| `game_service`       | Håndterer spildata (runde, point, historik) via MongoDB        |
| `score_service`      | Håndterer point og leaderboard                                |
| `notification_service` | Sender notifikationer og e-mails til brugere                |
| `rabbitmq`           | Message broker til kommunikation mellem services             |

## RabbitMQ
RabbitMQ bruges som en message broker, så services kan kommunikere decentralt. Eksempler:
- Når en bruger logger ind, sender `auth_service` en besked til `game_service` for at opdatere login-tid.
- Events som `"user_registered"` eller `"user_logged_in"` håndteres via queue `auth_events`.

