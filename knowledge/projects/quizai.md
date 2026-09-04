---
id: project-quizai
title: QuizAI - AI-Powered Adaptive Quiz Platform by Abhishek Yadav
entity: Abhishek Yadav
category: projects
project_name: QuizAI
project_type: Full-Stack Web Application (WebApp)
domain: Artificial Intelligence, EdTech & Adaptive Learning
tech_stack:
  - Next.js
  - Node.js
  - MongoDB
  - Firebase Authentication
  - Groq API
cloud_deployment:
  frontend: Vercel
  backend: Render
tags:
  - project
  - ai
  - llm
  - groq-api
  - nextjs
  - nodejs
  - mongodb
  - firebase-auth
  - edtech
  - adaptive-learning
summary: QuizAI is a full-stack adaptive learning quiz platform developed by Abhishek Yadav using Next.js, Node.js, MongoDB, Firebase Authentication, and Groq API, dynamically generating personalized, non-repeating questions based on user performance.
---

# Project: QuizAI - AI-Powered Adaptive Quiz Platform

## Executive Summary
- **Project Name**: QuizAI
- **Developer / Creator**: Abhishek Yadav
- **Application Type**: Full-Stack Web Application (WebApp)
- **Primary Tech Stack**: Next.js, Node.js, MongoDB, Firebase Authentication, Groq API
- **Deployment**: Vercel (Frontend / Web Application), Render (Backend Services)
- **Domain**: Artificial Intelligence in Education (EdTech), Personalized Assessment & Adaptive Learning

---

## Technical Architecture & Implementation

### 1. Dynamic AI Question Generation (Groq API)
- Utilizes the high-speed **Groq API** to generate customized quiz questions dynamically on the fly.
- Leverages LLM inference to tailor question difficulty, topic depth, and format according to real-time user performance metrics.

### 2. Adaptive Learning Algorithm & History Tracking
- Dynamically selects subsequent questions based on the learner's previous answer accuracy and performance trajectory.
- Implements an intelligent historical tracking system that records attempted questions, ensuring previously attempted questions are **never repeated**.
- Provides comprehensive progress tracking, analytics, and performance reporting.

### 3. Authentication & Security
- Integrated **Firebase Authentication** to provide secure, robust user onboarding, identity management, and credential protection.
- Maintains protected session states and isolated user history profiles.

### 4. Database Architecture & Storage
- Leverages **MongoDB** for flexible, scalable NoSQL document storage.
- Stores user performance records, quiz history, question bank metadata, and tracking states with high query efficiency.

### 5. Cloud Infrastructure & Scalable Deployment
- Multi-cloud deployment architecture:
  - **Vercel**: Deployed frontend application ensuring global edge caching, fast time-to-first-byte (TTFB), and responsive UI.
  - **Render**: Deployed backend microservices and Node.js APIs ensuring reliable continuous execution and scalability.

---

## Technology Stack Breakdown

| Layer / Component | Technology | Purpose & Responsibility |
| :--- | :--- | :--- |
| **Frontend Framework** | Next.js (React) | Dynamic UI rendering, client state management, interactive quiz flows |
| **Backend Runtime** | Node.js | Server-side logic, API endpoints, and orchestration with Groq API |
| **Artificial Intelligence** | Groq API | High-speed LLM inference for real-time dynamic quiz question generation |
| **Database** | MongoDB | Persistent document storage for user scores, question metadata, and logs |
| **Authentication** | Firebase Authentication | Secure user sign-up, sign-in, and session management |
| **Cloud Deployment** | Vercel & Render | Dual cloud deployment for scalable, high-availability web delivery |

---

## Target RAG Retrieval Queries
This document provides answers to queries such as:
- What is QuizAI?
- What AI technology or API powers QuizAI?
- How does QuizAI adapt questions to the user?
- Does QuizAI repeat questions that have already been attempted?
- What tech stack is QuizAI built on?
- Where is QuizAI hosted or deployed?
- Does Abhishek Yadav have experience using Groq API or LLMs?
- How is user authentication handled in QuizAI?
