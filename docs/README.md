## System design

### Architecture diagram

![Architecture Diagram](./images/architecture_diagram.png)

### Component description

#### Application components

##### API

This component receives requests from users, including creating sessions, receiving participants' answers, and retrieving the scoreboard.

##### Notificator

This component notifies participants and scoreboard viewers of new updates, including question results and scoreboard changes.

##### Worker

This component serves the following purposes:

- Evaluating participants' answers.
- Writing participants' scores to the database.
- Broadcasting results to the Notificator via Message Queue to notify users of updates.

##### Migrator

This component migrates the database to new migration versions before other application components are deployed. If any unapplied migration versions are detected, we can roll back the database to investigate.

### Data flows



### Technologies and tools
