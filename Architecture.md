# Architecture for Numerojobs Platform

This document describes the high-level architecture for Numerojobs—a job search platform that leverages AI and numerological analysis to match job seekers with recruiters. The goal is to create a scalable, maintainable, and modular system that can easily accommodate new features as the product evolves.

---

## 1. Overview

The system is divided into two primary parts:
- **Backend API**: Built with FastAPI (Python) to handle authentication, business logic, data processing (resume parsing, numerology calculations, compatibility algorithms), and external integrations.
- **Frontend Application**: Developed in NextJS to render a dynamic, responsive user interface that communicates with the backend APIs.

This **decoupled architecture** ensures clear separation of concerns, improves scalability, and simplifies maintenance.

---

## 2. Technology Stack

- **Backend & Auth/Storage**: 
  - **Framework**: FastAPI (Python)
  - **Integrated Services via Supabase**:
    - **Authentication & Authorization**: Leverage Supabase's built-in authentication using JWT and social login integrations (e.g., LinkedIn, Google).
    - **Database**: Use Supabase's managed PostgreSQL for core data storage. This offers scalability and an easier migration path.
    - **Storage**: Utilize Supabase Storage to securely handle file uploads (resumes, assets).
  - **Data Processing & Task Queue**:
    - Python libraries for numerology, AI recommendations, and resume parsing.
    - For asynchronous tasks (e.g., resume parsing), consider using Celery with RabbitMQ/Redis as the system scales. Initially, Supabase Edge Functions could be an alternative.

- **Frontend**:
  - **Framework**: NextJS (React-based)
  - **Rendering Strategy**: Combination of server-side rendering (SSR) and static site generation (SSG) for performance and SEO
  - **Communication**: RESTful API integration with the FastAPI backend via secure HTTP endpoints
  - **State Management**: React Context or libraries like Redux if needed for complex state requirements

- **DevOps & Infrastructure**:
  - **Containerization**: Docker for environment consistency and ease of deployment
  - **Orchestration**: Kubernetes (or similar) for managing container clusters as the system scales, though initially many backend operations are managed by Supabase.
  - **CI/CD**: Pipelines for continuous integration and deployment
  - **Monitoring & Logging**: Combine Supabase's built-in monitoring with standard observability tools as needed

---

## 3. Architectural Components

### 3.1. API Backend (FastAPI)

- **Authentication & Authorization**: 
  - All user registration and login actions (job seekers and recruiters) are handled by FastAPI.
  - JWT tokens are issued after successful authentication.
  - Social authentication endpoints (e.g., LinkedIn, Google) are also managed in the API.

- **Business Logic Layer**:
  - **User Profile Management**: Creating and updating user profiles, resume parsing and extraction.
  - **Numerology & Compatibility Calculation**: Services to compute Life Path Number, Expression Number, etc.
  - **Job Matching & Recommendations**: Endpoints to fetch recommended jobs or candidates based on compatibility, skills, and goals.

- **Integration Layer**:
  - **External Services**: Interfaces to payment gateways, SMS and Email providers for notifications.  
  - **Cloud Storage**: Integration with S3 (or similar) for storing and retrieving resumes and assets.

- **Asynchronous Processing**:
  - A task queue (e.g., Celery) offloads intensive computations (resume parsing, numerology analysis) asynchronously, ensuring a responsive API.

---

### 3.2. Frontend Application (NextJS)

- **User Interface**:
  - **Responsive Design**: Clean UI for job seekers and recruiters, including dashboards, job posting forms, and profile management.
  - **Routing & Navigation**: Dynamic routing for different user types (job seekers vs. recruiters) and blog/landing pages.

- **Data Fetching**:
  - The NextJS frontend makes RESTful API calls to the FastAPI backend for dynamic data.
  - Use SWR or React Query for efficient data fetching and caching on the client side.

- **Authentication Integration**:
  - The frontend handles user login, storing JWT tokens in secure HTTP-only cookies, while relying on backend endpoints for token validation and renewals.
  - Server-side rendered pages can utilize these tokens for secure, authenticated requests.

---

### 3.3. Communication & Security

- **API Gateway / Reverse Proxy**:
  - Use an API gateway (like NGINX or Traefik) to route requests to the correct backend services and provide load balancing, SSL termination, and rate limiting.

- **Security Best Practices**:
  - Implement HTTPS for all external communications.
  - Use secure headers and proper CORS configurations.
  - Encrypt sensitive data at rest and in transit.
  - Monitor for anomalies and enforce rate limiting.

---

### 3.4. Data Storage & Management

- **Relational Database**:
  - Use PostgreSQL (or similar) to store structured data such as user profiles, job posts, and compatibility scores.
  
- **NoSQL/Additional Stores**:
  - Consider a NoSQL database for session storage or logging unstructured data if required.

- **Persistent File Storage**: 
  - Store resumes and other file uploads in a cloud storage solution, accessible via secure URLs.

- **Storage & File Handling with Supabase**:  
  - **Integrated with Supabase Storage**: This approach simplifies file management by offering direct and secure file uploads and retrievals, while still allowing for future migration to another storage provider if needed.

---

### 3.5. Deployment, Scaling, and Maintenance

- **Containerization & Orchestration**:
  - Package both the FastAPI and NextJS applications in Docker containers.
  - Deploy using Kubernetes to enable horizontal scaling based on load.

- **CI/CD Pipelines**:
  - Automated testing and deployment pipelines ensure quick iterations and maintainability as new features are added.

- **Microservices/Modularization**:
  - Although initially a monolithic API service might be sufficient, design the codebase with clear modules (authentication, resume processing, numerology, job matching) that can later be split into microservices if needed.

- **Monitoring & Logging**:
  - Integrate comprehensive monitoring (Prometheus/Grafana) and logging (ELK) to observe system health, performance, and potential issues.

---

## 4. Decision Rationale: Python vs. NextJS for Key Functions

- **Authentication & Authorization with Supabase**:  
  - **Backend (FastAPI + Supabase)**: Using Supabase simplifies managing user credentials and role-based access via secure JWT tokens, reducing complexity within FastAPI.
  - **Frontend (NextJS)**: Consumes Supabase authentication endpoints and handles JWT tokens securely (e.g., via HTTP-only cookies).

- **Business Logic & Data Processing**:  
  - **Backend (FastAPI)**: All logic related to numerology, resume parsing, AI-based recommendations, and database interactions should reside in Python where the performance and security can be controlled.

- **Storage & File Handling**:  
  - **Backend (FastAPI)**: Manages file uploads and integrates with cloud storage solutions ensuring that all files are processed on a secure server before being stored.

This clear separation not only shields the frontend from unnecessary complexity but also makes it easier to update and extend the business logic without impacting the user experience.

---

## 5. Conclusion

This architecture leverages the strengths of both FastAPI and NextJS by clearly delineating responsibilities between the backend and frontend. The decoupled nature, emphasis on asynchronous processing, containerized deployment, and robust monitoring ensures that the platform is scalable, maintainable, and ready to incorporate new features as demand grows.

This document serves as the blueprint for the development, deployment, and future enhancements of the Numerojobs platform. 