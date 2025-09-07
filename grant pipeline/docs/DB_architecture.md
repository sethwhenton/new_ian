```mermaid
erDiagram
    OBJECT_TYPE {
        int id PK
        timestamp created_at
        timestamp updated_at
        varchar name
        varchar description
    }

    INPUT {
        int id PK
        timestamp created_at
        timestamp updated_at
        varchar image_path
        varchar description
    }

    OUTPUT {
        int id PK
        timestamp created_at
        timestamp updated_at
        int predicted_count
        int corrected_count
        float pred_confidence
        varchar object_type_fk FK
        varchar input_fk FK
    }

    OBJECT_TYPE ||--o{ OUTPUT : has
    INPUT ||--o{ OUTPUT : produces
