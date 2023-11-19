# Log Ingestor and Query Interface

## Overview

This project is a log ingestor system with a query interface. It efficiently handles vast volumes of log data and offers a simple interface for querying this data using full-text search or specific field filters. The system comprises a log ingestor that accepts logs over HTTP and a web-based query interface.

## Table of Contents

- [How to Run](#how-to-run)
- [System Design](#system-design)
- [Features](#features)
- [Identified Issues](#identified-issues)

## How to Run

### Prerequisites

- Python 3.x
- MongoDB
- Redis (for Celery)
- Additional Python packages listed in `requirements.txt`

### Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/log-ingestor.git
    cd log-ingestor
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables:**

    Create a `.env` file with the following:

    ```env
    MONGO_URI=mongodb://localhost:27017/your_database
    DB_NAME=your_collection
    FLASK_DEBUG=True
    ```

    Update `MONGO_URI` and `DB_NAME` with your MongoDB details.

4. **Run the application:**

    ```bash
    python app.py
    ```

    The application will run on `http://localhost:3000` by default.

## System Design

The system consists of two main components:

- **Log Ingestor:**
  - Accepts logs over HTTP.
  - Validates log data against a JSON schema.
  - Processes logs asynchronously using Celery.
  - Inserts validated logs into MongoDB.

- **Query Interface:**
  - Web-based interface accessible at `http://localhost:3000`.
  - Allows users to search logs based on various parameters.
  - Implements advanced features such as date range search and regular expression support.

## Features

- Log ingestion over HTTP
- Full-text search and specific field filters
- Scalable architecture
- MongoDB integration
- Asynchronous log processing with Celery
- User-friendly query interface
- Advanced Features (Bonus):
  - Search within specific date ranges
  - Utilize regular expressions for search
  - Allow combining multiple filters
  - Provide real-time log ingestion and searching capabilities
  - Implement role-based access to the query interface

## Identified Issues

- **Issue 1:**

  Description of the issue and steps to reproduce.

- **Issue 2:**

  Description of the issue and steps to reproduce.

Feel free to explore and contribute to the project. If you encounter any issues or have suggestions for improvements, please create an issue on the repository.

