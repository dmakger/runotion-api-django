# Database ER Diagram

Source: Django models in `user`, `core`, `project`, and `task` apps.

```mermaid
erDiagramж
    AUTH_USER {
        int id PK
        string username
        string password
        string email
        bool is_active
        bool is_staff
        datetime date_joined
    }

    USER_DEPARTMENT {
        int id PK
        string name
    }

    USER_USERPROFILE {
        int id PK
        int user_id FK
        string name
        int department_id FK
        string image
    }

    USER_REGISTRATIONREQUEST {
        int id PK
        string mts_login
        string username
        string password
        string full_name
        text comment
        string status
        int created_user_id FK
        datetime created_at
        datetime updated_at
    }

    CORE_IMPORTANCELEVEL {
        int id PK
        string name
        int value
    }

    CORE_COLOR {
        int id PK
        string name
        string value
    }

    PROJECT_PROJECT {
        int id PK
        int admin_id FK
        string name
        string code
        datetime created_at
        string image
    }

    PROJECT_ROLEPROJECT {
        int id PK
        string name
        int level_id FK
    }

    PROJECT_USERTOPROJECT {
        int id PK
        int user_id FK
        int project_id FK
        int role_id FK
        datetime created_at
    }

    PROJECT_SECTIONPROJECT {
        int id PK
        int project_id FK
        string name
        int position
        int color_id FK
        bool is_final
        datetime created_at
    }

    PROJECT_ACTIONPROJECT {
        int id PK
        string name
    }

    PROJECT_HISTORYPROJECT {
        int id PK
        int user_id FK
        int project_id FK
        int action_id FK
        int victim_id FK
        datetime created_at
    }

    TASK_TASKCATEGORY {
        int id PK
        int project_id FK
        string name
        string color
        datetime created_at
    }

    TASK_TASK {
        int id PK
        int director_id FK
        int project_id FK
        string name
        text description
        string code
        datetime created_at
        datetime deadline
        datetime completed_at
        int category_id FK
    }

    TASK_TASKTOSECTION {
        int id PK
        int task_id FK
        int section_project_id FK
        datetime created_at
        int position
    }

    TASK_USERLEVELTASK {
        int id PK
        string name
        int level_id FK
    }

    TASK_USERTOTASK {
        int id PK
        int user_id FK
        int task_id FK
        int level_id FK
        datetime created_at
    }

    TASK_COMMENTTASK {
        int id PK
        int user_id FK
        text text
        datetime created_at
    }

    TASK_TASKATTACHMENT {
        int id PK
        int task_id FK
        int user_id FK
        string file
        string name
        int size
        string content_type
        datetime created_at
    }

    TASK_COMMENTTASKATTACHMENT {
        int id PK
        int comment_id FK
        string file
        string name
        int size
        string content_type
        datetime created_at
    }

    TASK_NOTIFICATION {
        int id PK
        int user_id FK
        int actor_id FK
        int project_id FK
        int task_id FK
        string type
        string title
        text text
        bool is_read
        datetime created_at
    }

    TASK_CHECKLISTTASK {
        int id PK
        int user_id FK
        string name
        int position
        datetime completed_at
        datetime created_at
    }

    TASK_SUBTASKCHECKLIST {
        int id PK
        int checklist_id FK
        string name
        int position
        datetime completed_at
        datetime created_at
    }

    AUTH_USER ||--|| USER_USERPROFILE : has_profile
    AUTH_USER ||--o{ USER_REGISTRATIONREQUEST : created_user
    USER_DEPARTMENT ||--o{ USER_USERPROFILE : contains

    USER_USERPROFILE ||--o{ PROJECT_PROJECT : administers
    USER_USERPROFILE ||--o{ PROJECT_USERTOPROJECT : member
    PROJECT_PROJECT ||--o{ PROJECT_USERTOPROJECT : has_members
    PROJECT_ROLEPROJECT ||--o{ PROJECT_USERTOPROJECT : assigns_role
    CORE_IMPORTANCELEVEL ||--|| PROJECT_ROLEPROJECT : role_level

    PROJECT_PROJECT ||--o{ PROJECT_SECTIONPROJECT : has_sections
    CORE_COLOR ||--o{ PROJECT_SECTIONPROJECT : section_color
    USER_USERPROFILE ||--o{ PROJECT_HISTORYPROJECT : actor
    USER_USERPROFILE ||--o{ PROJECT_HISTORYPROJECT : victim
    PROJECT_PROJECT ||--o{ PROJECT_HISTORYPROJECT : history
    PROJECT_ACTIONPROJECT ||--o{ PROJECT_HISTORYPROJECT : action

    PROJECT_PROJECT ||--o{ TASK_TASKCATEGORY : has_categories
    TASK_TASKCATEGORY ||--o{ TASK_TASK : categorizes
    USER_USERPROFILE ||--o{ TASK_TASK : directs
    PROJECT_PROJECT ||--o{ TASK_TASK : has_tasks

    TASK_TASK ||--o{ TASK_TASKTOSECTION : placement
    PROJECT_SECTIONPROJECT ||--o{ TASK_TASKTOSECTION : contains_tasks

    CORE_IMPORTANCELEVEL ||--o{ TASK_USERLEVELTASK : task_level
    USER_USERPROFILE ||--o{ TASK_USERTOTASK : participant
    TASK_TASK ||--o{ TASK_USERTOTASK : assignees
    TASK_USERLEVELTASK ||--o{ TASK_USERTOTASK : assignment_level

    TASK_USERTOTASK ||--o{ TASK_COMMENTTASK : writes
    TASK_TASK ||--o{ TASK_TASKATTACHMENT : has_files
    USER_USERPROFILE ||--o{ TASK_TASKATTACHMENT : uploaded_by
    TASK_COMMENTTASK ||--o{ TASK_COMMENTTASKATTACHMENT : has_files

    USER_USERPROFILE ||--o{ TASK_NOTIFICATION : receives
    USER_USERPROFILE ||--o{ TASK_NOTIFICATION : triggers
    PROJECT_PROJECT ||--o{ TASK_NOTIFICATION : about_project
    TASK_TASK ||--o{ TASK_NOTIFICATION : about_task

    TASK_USERTOTASK ||--o{ TASK_CHECKLISTTASK : owns_checklists
    TASK_CHECKLISTTASK ||--o{ TASK_SUBTASKCHECKLIST : has_subtasks
```

## Notes

- Django creates `id` primary keys automatically for these models.
- `AUTH_USER` is Django's built-in `auth.User` table used by `UserProfile` and `RegistrationRequest`.
- `PROJECT_USERTOPROJECT` and `TASK_USERTOTASK` are join tables that store roles/levels for users.
- `TASK_TASKTOSECTION` stores kanban placement and order of tasks inside project sections.
- `TaskCategory` has a unique constraint on `(project, name)`.
