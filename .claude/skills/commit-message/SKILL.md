---
name: commit-message
description: Use when the user asks to commit, write a commit message, or stage and commit changes. Analyzes staged git changes and generates a Conventional Commits message (feat/fix/chore/refactor/docs/test/style/perf/ci/build).
---

# Commit Message

Generate a Conventional Commits message from the current staged changes.

## Process

1. **Read the staged diff:**

```bash
git diff --cached --stat
git diff --cached
```

If nothing is staged, report that and stop — do not commit.

2. **Read recent commit history** for style consistency:

```bash
git log --oneline -10
```

3. **Classify the change** into exactly one type:

| Type | When |
|------|------|
| `feat` | New user-facing functionality |
| `fix` | Bug fix |
| `refactor` | Code restructuring, no behavior change |
| `chore` | Dependencies, config, build tooling, housekeeping |
| `docs` | Documentation only |
| `test` | Adding or updating tests only |
| `style` | Formatting, whitespace, linting — no logic change |
| `perf` | Performance improvement, no behavior change |
| `ci` | CI/CD pipeline changes |
| `build` | Build system or external dependency changes |

If the diff spans multiple types, use the most significant one. If changes are truly unrelated, suggest splitting into separate commits.

4. **Determine scope** (optional). Scope is a noun in parentheses describing the area: `feat(auth):`, `fix(parser):`. Use scope when the repo has clear modules or domains. Omit for small repos or cross-cutting changes.

5. **Check for breaking changes.** If the diff removes or renames public API, changes function signatures consumers depend on, or alters behavior in a backwards-incompatible way, append `!` after the type/scope: `feat!:` or `feat(api)!:`.

6. **Write the message** using this format:

```
<type>[optional scope][!]: <subject>

[optional body]

[optional footer(s)]
```

**Subject line rules:**
- Imperative mood ("add", "fix", "remove" — not "added", "fixes", "removed")
- Lowercase first letter after the colon
- No period at the end
- Max 72 characters total (type + scope + subject)
- Describe WHAT changed and WHY if not obvious from the what

**Body** (add when the subject alone is insufficient):
- Separated from subject by a blank line
- Explain motivation or context the diff doesn't show
- Wrap at 72 characters

**Footer:**
- `BREAKING CHANGE: <description>` for breaking changes (in addition to `!`)
- `Co-Authored-By:` lines as required by the environment

7. **Present the message** to the user for approval before committing. Do not commit without confirmation unless the user has explicitly asked you to commit directly.

## Examples

Single-line:
```
feat(auth): add OAuth2 login flow
```

With body:
```
fix(parser): handle nested brackets in expressions

The recursive descent parser failed on inputs like `a[b[c]]` because
the bracket counter reset on each recursive call. Track depth in the
parent scope instead.
```

Breaking change:
```
feat(api)!: require authentication for /users endpoint

BREAKING CHANGE: GET /users now returns 401 without a valid token.
Previously this endpoint was public.
```

Chore:
```
chore: upgrade typescript to 5.5
```

## Common Mistakes

- Using past tense ("added feature") instead of imperative ("add feature")
- Writing vague subjects ("fix bug", "update code", "misc changes")
- Stuffing multiple unrelated changes into one commit — suggest splitting
- Using `feat` for internal refactors that don't add user-facing behavior
- Capitalizing the first word after the colon
