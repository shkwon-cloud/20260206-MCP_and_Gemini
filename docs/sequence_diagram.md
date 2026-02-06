```mermaid
sequenceDiagram
    participant User
    participant Page as TeamPage (Assembly)
    participant Hook as useTeam (Logic)
    participant UI as TeamCard (Pure UI)

    User->>Page: Toggle "Online Only"
    Page->>Hook: toggleFilter()
    Hook->>Hook: Update state & filter members
    Hook-->>Page: Return filteredMembers
    Page->>UI: Render with filtered data
    UI-->>User: Display updated Grid