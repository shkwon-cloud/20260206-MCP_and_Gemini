# Product Requirement Document (PRD) - Team Introduction Website

## Project Overview
A premium, responsive web platform using React 19, TypeScript, and Tailwind CSS v4. The project emphasizes **Separation of Concerns (SoC)** and high-end aesthetics.

## Core Features
1. **Home (Greeting)**: A high-impact landing page.
    - Includes a **Browser Size Display** tracking real-time window dimensions (Width/Height) via a custom hook.
2. **Team Member List**: A responsive grid of profile cards.
    - Each card displays name, role, bio, and **Online Status**.
    - Includes an **Online Only Filter** toggle to filter members based on their real-time availability.
3. **About Page**: Semantic content showcasing the team's mission, values, and impact with premium typography.
4. **Responsive UI**: Fully adaptive design that ensures consistency and visibility across all breakpoints.

## Technical Architecture (SoC)
- **`src/types/`**: TypeScript interfaces and types.
- **`src/hooks/`**: Business logic, state management, and side effects.
- **`src/components/`**: Pure representational UI components.
- **`src/pages/`**: Orchestration layer assembling hooks and components.
- **Routing**: Nested routing with `Layout` and `Outlet`.
