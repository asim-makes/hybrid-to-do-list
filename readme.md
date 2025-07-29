Project Goal: To build a robust and versatile backend API (using FastAPI) for a personal productivity application that offers a seamless experience for both offline (local, temporary) and online (account-based, synced) task management, including Pomodoro focus sessions.

Key Features (Backend Focus):

    Flexible Task Creation:

        "Immediate Notes": Client-side only (not stored on backend).

        "Later Notes" (Guest Mode): Temporarily stored on the backend for 24 hours without an account.

        "Account-Based Tasks": Permanently stored with user accounts, offering full features.

    Comprehensive Task Management:

        Nested tasks.

        Advanced search, filtering, and sorting.

        Recurring tasks.

        Task attachments (references to cloud storage).

    User Authentication & Authorization:

        Secure user registration, login (JWT + Refresh Tokens).

        Password reset functionality.

    Pomodoro Focus Session Tracking:

        API endpoints to start, pause, stop, and complete Pomodoro sessions.

        Real-time updates of active sessions across devices via WebSockets.

    Data Sync Across Devices:

        Real-time task synchronization for logged-in users (via WebSockets).

    Basic Analytics & Reporting:

        API endpoints to query task completion stats over time.

    Optional Email Notifications (Later Phase):

        Email notifications for task reminders (e.g., "task due soon").

Project Breakdown: Your Actionable Roadmap

Here's a breakdown of the core components and the order you might tackle them:

Phase 1: Foundation (User Management & Basic Task CRUD)

    Project Setup (FastAPI & Database):

        Initialize a new FastAPI project.

        Choose your ORM: SQLModel (highly recommended for FastAPI) or SQLAlchemy.

        Set up PostgreSQL database.

        Configure database connection (using environment variables for credentials).

        Implement basic main.py and database.py structure.

        Tools: uvicorn, FastAPI, SQLModel, psycopg2-binary (or asyncpg), python-dotenv.

    User Authentication & Authorization (Essential):

        User Model: Define the User model (id, username, email, hashed_password, is_active, is_verified).

        Password Hashing: Integrate passlib[bcrypt] for secure password hashing.

        User Registration: Create an endpoint (/register) to create new users.

        User Login: Create an endpoint (/token or /login) to authenticate users and issue JWT access tokens.

        JWT Generation & Validation: Implement JWT token creation, encoding, and decoding using python-jose.

        Dependency Injection for Authentication: Use FastAPI's Depends to inject the current authenticated user into your route functions.

        Refresh Tokens (Optional but Recommended): Implement a refresh token mechanism to issue new access tokens without re-logging in.

        Challenge: This is a critical security component. Take your time to understand JWT, hashing, and FastAPI's security features.

    Basic Task Management (CRUD for Logged-In Users):

        Task Model: Define the Task model (id, title, description, status, due_date, priority, user_id (foreign key to User)).

        CRUD Endpoints: Implement endpoints for:

            POST /tasks: Create a new task (associated with the authenticated user).

            GET /tasks: Retrieve all tasks for the authenticated user.

            GET /tasks/{task_id}: Retrieve a specific task.

            PUT /tasks/{task_id}: Update a task.

            DELETE /tasks/{task_id}: Delete a task.

        Authorization: Ensure users can only access/modify their own tasks.

        Tools: Pydantic for request/response models.

Phase 2: Introducing Offline/Guest & Advanced Task Features

    Temporary Guest Mode ("Later Notes" without Account):

        Guest Task Model: Create a separate GuestTask model (id, title, description, status, created_at, guest_uuid).

        Guest UUID Generation: On the client side (or a dedicated backend endpoint), generate a UUID for guest users.

        Guest Task Endpoints: Implement basic CRUD (POST, GET, PUT, DELETE) for guest tasks, using the guest_uuid for access.

        Background Task for Cleanup:

            Use FastAPI's BackgroundTasks for simple, short-running cleanup, or introduce Celery + Redis/RabbitMQ for robust, scheduled deletion of tasks older than 24 hours. (Celery is a bigger setup but teaches a lot).

        Challenge: Managing temporary data and ensuring reliable deletion.

    Nested Tasks:

        Modify Task Model: Add a parent_id (optional foreign key to Task.id) to your Task model.

        API Logic: Adjust your GET /tasks endpoint to handle returning tasks with their nested children (you might need to fetch them recursively or structure your query carefully).

        Challenge: Efficiently querying and representing hierarchical data. Ensuring proper deletion behavior (e.g., deleting parent deletes children, or re-parenting children).

    Advanced Search, Filtering, and Sorting:

        Query Parameters: Design your GET /tasks endpoint to accept query parameters like status, priority, due_date_start, due_date_end, search_term, sort_by, order.

        Database Queries: Implement the logic in your ORM to build dynamic queries based on these parameters.

        Pagination: Implement skip and limit (or page and page_size) parameters for pagination.

        Challenge: Writing flexible and efficient database queries.

    Recurring Tasks:

        Modify Task Model: Add fields like recurrence_pattern (e.g., daily, weekly, monthly, custom_json), recurrence_start_date, recurrence_end_date (optional).

        Background Task for Generation: Use Celery Beat (if using Celery) or a custom scheduled script to periodically check for recurring tasks and generate new instances based on their pattern.

        Challenge: Defining a flexible recurrence pattern. Implementing the logic to correctly generate future task instances.

Phase 3: Real-time & Attachments

    Pomodoro Focus Session Tracking:

        Pomodoro Session Model: id, user_id, task_id (optional foreign key), start_time, end_time (optional), duration, status (active, paused, completed).

        API Endpoints:

            POST /pomodoro/start: Start a session (check for existing active session).

            POST /pomodoro/pause, POST /pomodoro/resume, POST /pomodoro/stop, POST /pomodoro/complete: Manage session state.

        Challenge: Managing the state of a timer and ensuring only one active per user.

    Real-time Data Sync (WebSockets):

        WebSocket Endpoint: Create a /ws endpoint in FastAPI.

        Connection Management: Keep track of active WebSocket connections for each user.

        Broadcast Changes: When a user creates/updates/deletes a task (via REST API) or changes Pomodoro status, broadcast the change via WebSocket to all other connected clients of that same user.

        Challenge: Understanding WebSocket lifecycle, managing connections, and implementing a robust broadcast mechanism (potentially using Redis Pub/Sub for scalability).

    Task Attachments:

        Attachment Model: id, task_id, filename, file_url, file_type, upload_date.

        File Storage Integration: Integrate with a cloud storage service like AWS S3 or MinIO (a local S3-compatible server for dev).

        Upload Endpoint: Create an endpoint (POST /attachments/upload) that receives a file, uploads it to S3, and saves the URL/metadata to the database.

        Challenge: Handling file uploads securely and efficiently, integrating with a cloud storage API.

Phase 4: Analytics & Future Enhancements

    Basic Analytics & Reporting API:

        Reporting Endpoints: Create GET endpoints like:

            /reports/tasks_completed_by_day

            /reports/total_pomodoros_completed

            /reports/most_frequent_tags

        Aggregation Queries: Use SQL aggregation functions to generate these reports.

        Challenge: Writing performant aggregation queries.

    Password Reset (Enhancement):

        Request Reset: Endpoint to request a password reset (generates a unique token, stores it with expiry in DB, emails to user).

        Reset Password: Endpoint to receive the token and new password, hash new password, invalidate token.

        Challenge: Securely generating, storing, and validating one-time tokens.

    Optional Email Notifications (Later Phase):

        Email Sending Integration: Use a service like SendGrid, Mailgun, or smtplib.

        Background Task for Sending: Ensure email sending is done in a background task (Celery).

        Notification Triggers: Add logic to trigger emails (e.g., when a task is overdue, or a Pomodoro finishes).
