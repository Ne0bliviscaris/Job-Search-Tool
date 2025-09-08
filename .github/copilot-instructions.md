---
applyTo: '**'
---

[Must]
- Always write code in English, but communicate with user in Polish.
- Only add type hints for function parameters and return types; do not add type hints for local variables unless explicitly instructed.
- Always write short docstrings explaining inputs, outputs, and side effects.  
- Always keep existing inline comments.  
- Never add new inline comments.  
- Never output placeholders like "# ...existing code...".
- Always keep functions short and single-responsibility.  
- Always follow team naming conventions.  
- Always specify full file paths for multi-file changes.  
- Always provide 1–2 sentence explanations of changes.  
- Always return only changed blocks, not entire files.  
- Always import only what is needed.  
- Always return the function in its correct position, not in isolation.
- Always remove or mark obsolete functions and unused code when introducing new logic.
- Always clean up constructors and variables made redundant by refactoring.
- Always point out obsolete functions that can be removed and include their removal in the code changes.
- Always suggest minimal refactoring to improve code clarity and maintainability.
- Never break line after opening docstring and before closing docstring.
- Always generate code with correct Python indentation relative to the class or enclosing block.


[Naming Conventions]
- Use clear, descriptive variable names.  
- Prefix abstract classes with `Abstract`.  
- Prefix enum classes with `Enum`.  

[Prefer]
- Prefer simple logic over complex logic. Extract intermediate variables for readability.  
- Prefer small helper functions instead of deep nesting.  
- Prefer minimal implementations first, refine iteratively.  
- Prefer specific exception handling over broad `except`.  

[Avoid]
- Avoid placeholders in code.  
- Avoid pseudocode or unused fragments.  
- Avoid unrelated or redundant changes.  
- Avoid `if __name__ == "__main__":` unless the module is meant as a script.  
- Avoid handling multiple types unless explicitly required.  
- Avoid `isinstance` checks unless explicitly required.  

[Process]
- First analyze requirements and context; ask if unclear.  
- Then explain the purpose of code changes briefly.  
- Finally, show the modified code.  

[Error Messages]
- Provide short, clear summaries.  

[Code changes]
- Do not change existing behavior unless explicitly instructed.
- If new code replaces existing logic, remove obsolete lines or methods instead of leaving dead code.  
- When introducing new code, clean up related existing code to avoid duplication or unused code.
- Treat removal of dead code as part of the relevant modification.