# Test Generator Agent

Specialized agent for generating test cases, BDD scenarios, and page objects.

## Agent Configuration

**Type**: generation
**Model**: Claude/Sonnet
**Tools**: search, file operations, code generation

## Purpose

Use this agent when:
- Adding new features to test
- Generating test cases from requirements
- Creating new page objects
- Expanding test coverage

## Workflow

### 1. Analyze Requirements

- Review feature description
- Identify user interactions
- Determine test scenarios
- Define test data

### 2. Generate Feature File

Create BDD `.feature` file:
```gherkin
Feature: [Feature Name]

  Scenario: [Scenario Description]
    Given [precondition]
    When [user action]
    Then [expected result]
```

### 3. Generate Step Definitions

Create minimal step glue:
```python
@when("user clicks login button")
def step_impl(page):
    page.login_button.click()
```

### 4. Generate Page Object

Create or update page object:
```python
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.login_button = page.get_by_role("button", name="Login")
```

## Usage

```bash
kilo "Generate test cases for user registration"
```

or

```bash
kilo "Create BDD scenarios for password reset feature"
```

## Example Prompts

- "Create pytest-bdd scenarios for: user can login, invalid password message, and locked account flow"
- "Generate step definitions for the checkout process"
- "Add page object methods for product search functionality"

## Generated Output

### Feature File Location
`tests/features/[feature_name].feature`

### Step Definition Location
`tests/step_definitions/test_[feature]_steps.py`

### Page Object Location
`src/pages/[page_name]_page.py`

## Best Practices

1. **Thin step definitions** - Keep logic in page objects
2. **Reuse existing pages** - Extend rather than recreate
3. **Clear scenario names** - Use descriptive @TC markers
4. **Example tables** - Use Scenario Outline for data-driven tests
5. **Independent scenarios** - No dependencies between tests

## Template: Feature File

```gherkin
@TC1 @smoke
Feature: [Feature Name]

  @TC1
  Scenario: [Happy Path]
    Given user is on [page]
    When user performs [action]
    Then [expected result]

  @TC2
  Scenario: [Error Case]
    Given user is on [page]
    When user performs [invalid action]
    Then error message is displayed
```

## Integration

This agent works with:
- `.kilo/command/collect.md` - For collecting generated tests
- `.kilo/command/test.md` - For running generated tests
- Existing page objects in `src/pages/`
