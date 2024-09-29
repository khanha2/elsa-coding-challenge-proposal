## 1. System design

### 1.1. Architecture diagram

![Architecture Diagram](./images/architecture_diagram.png)

### 1.2. Component description

#### 1.2.1. Application services

##### 1.2.1.1. API

This service receives requests from users, including creating sessions, receiving participants' answers, and retrieving the scoreboard.

The number of API workers can be increased based on the growth in the number of users.

##### 1.2.1.2. Notificator

This service notifies participants and scoreboard viewers of new updates, including question results and scoreboard changes.

The number of Notificator workers can be increased based on the growth in the number of users.

##### 1.2.1.3. Worker

This service serves the following purposes:

- Evaluating participants' answers.
- Writing participants' scores to the database.
- Broadcasting results to the Notificator via Message Queue to notify users of updates.

The number of Worker service workers can be increased based on the growth in the number of users.

##### 1.2.1.4. Migrator

This component migrates the database to new migration versions before other application components are deployed. If any unapplied migration versions are detected, we can roll back the database to investigate.

#### 1.2.2. CI/CD Tools

##### 1.2.2.1. Build server

This component receives build requests from GitHub Actions to build Kubernetes images.

##### 1.2.2.2. Parameters management

This component provides parameters for building or deploying services.

##### 1.2.2.3. Container images repository

This component manages Kubernetes image versions for deploying services or rolling back service versions when needed.

##### 1.2.2.4. Argo CD

This component declares and controls service definitions, configurations, and environments. It ensures that deployment and lifecycle management are automated, auditable, and easy to understand.

#### 1.2.3. System monitor

##### 1.2.3.1. Sentry

This component notifies application exceptions immediately.

##### 1.2.3.2. ELK

This component helps developers monitor services via logs. It includes three tools:

- **Filebeat**: Collects logs from services.
- **Logstash**: Parses and extracts information from logs, storing it in the Log database.
- **Kibana**: A GUI for developers to access logs.

##### 1.2.3.3. Metrics monitoring

This component helps developers monitor systems via metrics. It includes:

- **Prometheus**: Collects metrics from all components, including Kubernetes containers, databases, message queues, Sentry, log databases, and load balancers.
- **Grafana**: A GUI for developers to access metrics.

#### 1.2.4. Traffic controller

##### 1.2.4.1. Cloudflare

This component serves for DNS management, web security, and secure connections via SSL/TLS.

##### 1.2.4.2. Load balancer

Since all application components can be scaled using the horizontal scaling method, the load balancer dynamically distributes traffic across API, Notificator workers.

#### 1.2.6. Message queue

This component controls requests from participants to write the results to the database in case the number of API workers is increased.

#### 1.2.7. Database

##### 1.2.7.1. Primary database

This database receives write transations from Worker service workers to store data.

##### 1.2.7.2. Replica database

This database serves the following purposes:

- Receives read transations from API service workers and responds with the queried data.
- Receives updated data from the primary database for reading.

The number of replica databases can be increased based on the growth in the number of users.

##### 1.2.7.3. Redis

Redis serves the following purposes:

- Centralized storage for temporary data, including web socket information and session information.
- Caches expected answers for quiz questions to reduce the number of read transactions to the database.

### 1.2. Data flows

#### 1.2.1. Creating a new session

```mermaid
sequenceDiagram
    autonumber
    User->>+API: request create a session
    API->>Redis: generate a session ID<br/>and store in Redis
    alt is participant
    API->>Message queue: Push session information to be stored in the database
    Message queue->>Worker: receive the session information.
    Worker->>Primary DB: store the session information
    end
    API->>-User: response the session information
    User->>+Notificator: open the web socket connection
    Notificator->>-User: return the web socket connection ID
    User->>+Notificator: push the session ID
    Notificator->>Redis: Create a pair of connection ID and the session ID<br/> and store it in Redis.
    Notificator->>-User: acknowlege the web socket connection.
```

#### 1.2.2. Receive anwsers from participants

```mermaid
sequenceDiagram
    autonumber
    _Participant->>+API: push the answer
    API->>+Redis: get the result from cache
    Redis->>-API: receive the result
    API->>API: evaluate the answer
    API->>Message queue: push the answer and<br />the evaluation result
    API->>_Participant: return the evaluation result
    Message queue->>Worker: receive the answer and<br />the evaluation result
    Worker->>Primary DB: store the awswer and<br />the evaluation result
    Primary DB->>Replica DB: synchronize updated data
    Worker->>Message queue: push the evaluation result to notify
    Message queue->>Notificator: receive the evaluation result
    Notificator->>Scoreboard viewer: notify the scoreboard is updated
```

#### 1.2.3. Update cache for result

To prevent Redis from running out of memory, we apply a time-to-live (TTL) for values. However, this approach requires querying the database to update cached values. The update method is described by the following flow:

```mermaid
sequenceDiagram
    autonumber
    API->>+Redis: get the result from cache
    Redis->>-API: receive the result
    alt is result does not exists in cache
    API->>+Replica DB: get the result from DB
    Replica DB->>-API: return the result
    API->>+Redis: update cache
    end
```

### 1.3. Technologies and tools

#### 1.3.1. Kubernetes

We use Kubernetes for the following purposes:

- Resource Management: control resources (CPU, RAM, Disk) that each container need.
- Horizontal scalling: Increase or decrease number of application containers based on the growth in the number of users.
- Load balancing: Distributes network traffic across multiple containers to ensure high availability and reliability of services.

#### 1.3.2. PostgreSQL

We use PostgresQL for the main database to store and query data.

The database is a bottleneck in the system, because we cannot scale it immediately when number of users changed. To solve this problem, we have 2 databases:

- The primary database: receive write transactions from Worker service containers. Number of transactions is controlled when using the message queue.
- The replica database: receive read transactions from API service containers. We can increase number of replica databases when number of users changed.

