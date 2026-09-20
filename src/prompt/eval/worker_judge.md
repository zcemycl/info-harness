"""Judge prompt for FDA axis-worker eval answers."""

You score an FDA label search *worker* answer.

Scale 1–5:
- 5: Correct tools for the brief, faithful to tool results, clear and complete
- 4: Mostly correct; minor gaps or verbosity
- 3: Partially useful; missing key facts or weak tool choice
- 2: Largely wrong or hallucinated beyond tools
- 1: Empty, error, or irrelevant

Also score optional subscores (1–5): faithfulness, completeness, tool_use.

Return structured JudgeScore fields only. Be strict about unsupported claims.
