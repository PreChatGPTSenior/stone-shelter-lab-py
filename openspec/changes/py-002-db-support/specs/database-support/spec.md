## ADDED Requirements

### Requirement: Validated database configuration
The application SHALL validate database connection settings before creating a database engine and SHALL avoid exposing passwords in diagnostics.

#### Scenario: Valid connection settings
- **WHEN** complete valid database settings are loaded
- **THEN** the application can construct its connection configuration without logging credentials

#### Scenario: Invalid connection settings
- **WHEN** a required setting is absent or invalid
- **THEN** configuration fails with an actionable error that does not reveal secret values

### Requirement: Database resource lifecycle
The application SHALL manage its asynchronous engine within its runtime lifecycle and release engine resources during shutdown. Importing application modules or constructing the application SHALL NOT open database connections.

#### Scenario: Application construction
- **WHEN** application modules are imported and the application factory is called
- **THEN** no database network connection is opened as an import or construction side effect

#### Scenario: Authenticated connectivity
- **WHEN** a focused connection check runs with valid settings against the isolated PostgreSQL instance
- **THEN** an authenticated query succeeds using the configured target database

#### Scenario: Runtime shutdown
- **WHEN** the application runtime shuts down
- **THEN** its database engine releases its connection pool resources

### Requirement: Explicit transaction completion
A Unit of Work SHALL persist changes only after an explicit successful commit. Uncommitted work SHALL be rolled back on normal exit or exceptional exit, and its session SHALL be released. A failed commit SHALL NOT be reported as success.

#### Scenario: Successful commit
- **WHEN** an operation writes test data and successfully commits its Unit of Work
- **THEN** a separate transaction can read the persisted data

#### Scenario: Exit without commit
- **WHEN** an operation writes test data and exits without committing
- **THEN** a separate transaction cannot observe that uncommitted change

#### Scenario: Exception before commit
- **WHEN** an exception interrupts an operation before commit
- **THEN** the change is rolled back and the session is released

#### Scenario: Commit failure
- **WHEN** transaction commit fails
- **THEN** the failure is propagated to the caller and cleanup is attempted without reporting successful persistence

### Requirement: Session ownership
Each independent Unit of Work execution SHALL own a separate asynchronous session. Components participating in one Unit of Work SHALL share that execution's session and transaction; repositories SHALL NOT commit independently.

#### Scenario: Independent executions
- **WHEN** two independent Units of Work are created
- **THEN** they receive different session instances and one rollback does not roll back the other's committed work

#### Scenario: Shared transaction participants
- **WHEN** two persistence participants write within the same Unit of Work and that work is rolled back
- **THEN** neither participant's changes are persisted

### Requirement: Migration environment
The project SHALL provide an Alembic environment using validated database configuration and the shared SQLAlchemy metadata. This change SHALL NOT introduce business tables or apply migrations automatically at HTTP startup.

#### Scenario: Inspect database revision
- **WHEN** Alembic inspects the current revision of the isolated PostgreSQL database
- **THEN** it connects successfully without creating Stone or adoption tables

#### Scenario: Focused transaction tests
- **WHEN** commit and rollback guarantees are tested
- **THEN** tests use PostgreSQL and disposable isolated test data rather than SQLite or live application records
