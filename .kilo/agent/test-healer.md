---
name: "test-healer"
description: "Use this agent when tests fail due to selector changes, stale selectors, flaky tests, or UI changes that break existing tests. Examples: fixing failing selectors in login page, healing flaky tests with proper waits, implementing locator fallback strategies for product cards, or resolving timing issues in test execution."
---

# Test Healer Agent

Specialized agent for fixing failing tests and self-healing selectors.

## Agent Configuration

**Type**: debugging/healing
**Model**: Claude/Sonnet
**Tools**: search, file operations, code analysis

## Purpose

Use this agent when:
- Tests fail due to selector changes
- Selectors become stale
- Flaky tests occur
- UI changes break existing tests

## Workflow

### 1. Analyze Failure

Examine:
- Error message and type
- Failed selector
- Page structure
- Timing issues

### 2. Identify Root Cause

Common causes:
- Selector too specific (breaks on change)
- Dynamic elements
- Timing/waiting issues
- Element moved or renamed

### 3. Propose Solution

**Selector Fix Strategies**:
- Use semantic selectors (`get_by_role`, `get_by_label`)
- Add fallback locators
- Use partial attribute matching
- Implement retry logic

**Timing Fixes**:
- Use explicit waits
- Add wait for element state
- Implement retry mechanisms

### 4. Implement Fix

Update page objects only:
- Never change step definitions
- Keep locators in `src/pages/`
- Add descriptive comments

## Fix Patterns

### Before (Fragile)
```python
# DON'T: Use fragile selectors
self.page.locator("#product-123").click()
self.page.locator("div.card:nth-child(2)").click()
```

### After (Robust)
```python
# DO: Use semantic selectors with fallback
self.page.get_by_role("button", name="Add to Cart").click()
# OR
self.page.locator(".product-card").filter(has_text="Product Name").click()
```

## Best Practices

1. **Never modify step definitions** — Only change page objects
2. **Use semantic selectors** — Prefer `get_by_role`, `get_by_label`
3. **Add fallback locators** — Multiple strategies for resilience
4. **Centralize waits** — Use page object wait methods
5. **Test fixes locally** — Verify before committing

## Integration

This agent works with:
- `.kilo/command/debug.md` — For debugging issues
- `.kilo/command/test.md` — For running fixed tests
- Page objects in `src/pages/`

## Reference

- **Unified AGENTS.md**: See [AGENTS.md](../AGENTS.md) for all platform guidelines
- **CLAUDE.md**: See [CLAUDE.md](../CLAUDE.md) for Claude-specific commands
- **KILO.md**: See [KILO.md](../KILO.md) for Kilo-specific commands

