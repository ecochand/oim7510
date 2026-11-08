
```mermaid
erDiagram
    SHOWS ||--o{ SHOW_PEOPLE : has
    PEOPLE ||--o{ SHOW_PEOPLE : participates
    SHOWS ||--o{ SHOW_GENRES : has
    GENRES ||--o{ SHOW_GENRES : categorizes

    SHOWS {
        int show_id PK
        string title
        int release_year
        string show_type
        int episodes
        float rating
        int votes
    }

    PEOPLE {
        int person_id PK
        string name
        int birth_year
    }

    SHOW_PEOPLE {
        int show_id PK,FK
        int person_id PK,FK
        string role PK
    }

    GENRES {
        int genre_id PK
        string genre_name
    }

    SHOW_GENRES {
        int show_id PK,FK
        int genre_id PK,FK
    }
```
#Assumptions
Each TV show has a unique Show ID, and each person has a unique Person ID, even if names or titles are the same.

A person can work on multiple TV shows, and each show can have multiple actors and writers.

A person can have more than one role in the same show, such as being both an actor and a writer.

A TV show can belong to multiple genres, and each genre can be associated with multiple shows.

Some shows may not have a rating or votes yet, so these fields can be left empty (NULL).

Each person's information is stored only once in the People table, regardless of how many shows they have worked on.