flowchart LR
    A[Input: User Preferences] --> B[Set Targets and Weights]
    B --> C[Loop Through Each Song in CSV]
    C --> D[Compute Mood Match]
    C --> E[Compute Genre Match]
    C --> F[Compute Energy Match]
    D --> G[Weighted Total Score]
    E --> G
    F --> G
    G --> H[Store Song + Score]
    H --> I[Sort All Songs by Score Descending]
    I --> J[Output: Top K Recommendations]