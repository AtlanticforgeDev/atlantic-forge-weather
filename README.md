# Atlantic Forge Weather

Atlantic Forge Weather is a cloud-native Earth science and weather platform designed to integrate real-time and historical environmental data into a single interactive application.

## Project Goals

The platform will integrate data from authoritative scientific sources including:

- NOAA and National Weather Service weather data
- GOES satellite imagery
- NOAA/NDBC ocean buoy observations
- Tropical storms and hurricane tracking
- Ocean and atmospheric conditions
- ENSO / El Niño / La Niña monitoring
- USGS environmental and geological data
- Air-quality and natural-hazard data

## Architecture

Atlantic Forge Weather is being developed using:

- Python
- REST APIs
- Docker
- Kubernetes / K3s
- Kubernetes CronJobs
- Git and GitHub
- AWS Lightsail
- Traefik Ingress
- TLS / Let's Encrypt

The application will use scheduled data ingestion jobs to retrieve and process environmental observations while exposing the information through a web-based dashboard.

## Current Status

Early development.

Initial application structure and NOAA/NDBC data integration are under development.

## Roadmap

- Expand NOAA and NWS API integration
- Add NDBC buoy observations
- Integrate GOES satellite imagery
- Add ENSO monitoring
- Add tropical cyclone tracking
- Build interactive maps and dashboards
- Automate data collection with Kubernetes CronJobs
- Containerize and deploy application services
- Implement CI/CD deployment workflow

## Purpose

This project is being built as both an Earth science application and a hands-on cloud engineering platform for developing skills in APIs, containerization, Kubernetes, automation, observability, and DevOps.
