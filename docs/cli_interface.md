# CLI Interface Module

## Overview

The CLI Interface module (`codewiki/cli`) provides the command-line interface layer for the CodeWiki system. It serves as the primary entry point for users interacting with the application through terminal commands, offering configuration management and visual progress tracking capabilities for long-running operations.

This module acts as a bridge between user commands and the underlying system components, orchestrating interactions with the dependency analysis engine, web frontend services, and core configuration systems.

---

## Table of Contents

- [Architecture](#architecture)
- [Core Components](#core-components)
- [Configuration Management](#configuration-management)
- [Progress Tracking](#progress-tracking)
- [Integration with Other Modules](#integration-with-other-modules)
- [Data Flow](#data-flow)
- [Usage Patterns](#usage-patterns)
- [Dependencies](#dependencies)

---

## Architecture

The CLI Interface module follows a layered architecture pattern, separating concerns between configuration management, user interaction, and progress visualization.

```mermaid
graph TB
    subgraph "CLI Interface Module"
        CLI[CLI Entry Point]
        Config[Configuration]
        Progress[ModuleProgressBar]
        
        CLI --> Config
        CLI --> Progress
    end
    
    subgraph "External Modules"
        CoreConfig[Core Config]
        DepAnalysis[Dependency Analysis]
        WebFE[Web Frontend]
        Utils[Utilities]
    end
    
    Config --> CoreConfig
    CLI --> DepAnalysis
    CLI --> WebFE
    Progress --> Utils
    
    User[User Commands] --> CLI
    CLI --> Output[Terminal Output]
    
    style CLI fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style Config fill:#50C878,stroke:#2E7D4E,color:#fff
    style Progress fill:#50C878,stroke:#2E7D4E,color:#fff
```

### Architectural Principles

1. **Separation of Concerns**: Configuration logic is isolated from progress tracking and command execution
2. **User-Centric Design**: Provides clear feedback and intuitive command structures
3. **Modularity**: Components can be used independently or composed together
4. **Extensibility**: Easy to add new commands and configuration options

---

## Core Components

### Component Hierarchy

```mermaid
classDiagram
    class Configuration {
        +load_config()
        +save_config()
        +validate()
        +get_setting(key)
        +set_setting(key, value)
        +merge_with_defaults()
    }
    
    class ModuleProgressBar {
        +start()
        +update(progress)
        +set_description(text)
        +finish()
        +reset()
        +get_current_progress()
    }
    
    class CLIInterface {
        -configuration: Configuration
        -progress_bar: ModuleProgressBar
        +execute_command()
        +handle_args()
    }
    
    CLIInterface --> Configuration
    CLIInterface --> ModuleProgressBar
    
    note for Configuration "Manages CLI configuration\nsettings and user preferences"
    note for ModuleProgressBar "Provides visual feedback\nfor long-running operations"
```

### Configuration (`codewiki.cli.models.config.Configuration`)

The Configuration component is responsible for managing all CLI-related settings, user preferences, and runtime parameters.

**Key Responsibilities:**
- Loading and parsing configuration files
- Validating configuration parameters
- Providing default values for missing settings
- Persisting user preferences
- Managing environment-specific configurations

**Configuration Scope:**
- CLI command defaults
- Output formatting preferences
- Logging levels and destinations
- Integration endpoints (web frontend, analysis engine)
- File system paths and working directories
- Performance tuning parameters

### ModuleProgressBar (`codewiki.cli.utils.progress.ModuleProgressBar`)

The ModuleProgressBar component provides visual feedback for operations that may take significant time to complete.

**Key Responsibilities:**
- Displaying progress indicators in the terminal
- Updating progress based on operation status
- Showing descriptive messages for current operations
- Managing multiple concurrent progress bars
- Graceful handling of terminal resize events

**Features:**
- Real-time progress updates
- Customizable progress bar styles
- Support for indeterminate progress (spinners)
- Module-specific progress tracking
- Clean terminal output management

---

## Configuration Management

### Configuration Flow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Config
    participant CoreConfig
    participant FileSystem
    
    User->>CLI: Execute command with options
    CLI->>Config: Initialize configuration
    Config->>FileSystem: Check for config file
    
    alt Config file exists
        FileSystem-->>Config: Return config data
        Config->>Config: Parse and validate
    else No config file
        Config->>Config: Use defaults
    end
    
    Config->>CoreConfig: Merge with core config
    CoreConfig-->>Config: Return merged config
    
    CLI->>Config: Get runtime settings
    Config-->>CLI: Return settings
    
    CLI->>CLI: Execute command logic
    
    opt Save preferences
        CLI->>Config: Update settings
        Config->>FileSystem: Persist configuration
    end
    
    CLI-->>User: Command output
```

### Configuration Hierarchy

The CLI configuration system follows a hierarchical approach:

1. **System Defaults**: Built-in default values
2. **Global Configuration**: System-wide settings from [core_config](core_config.md)
3. **User Configuration**: User-specific preferences
4. **Command-Line Arguments**: Runtime overrides with highest priority

```mermaid
graph LR
    A[System Defaults] --> B[Global Config]
    B --> C[User Config]
    C --> D[CLI Arguments]
    D --> E[Final Configuration]
    
    style E fill:#4A90E2,stroke:#2E5C8A,color:#fff
```

---

## Progress Tracking

### Progress Bar Architecture

```mermaid
stateDiagram-v2
    [*] --> Initialized: Create progress bar
    Initialized --> Running: start()
    Running --> Running: update(progress)
    Running --> Paused: pause()
    Paused --> Running: resume()
    Running --> Completed: finish()
    Completed --> [*]
    
    Running --> Error: Exception
    Error --> [*]
```

### Multi-Module Progress Tracking

When processing multiple modules (e.g., analyzing dependencies across modules), the progress bar system provides hierarchical tracking:

```mermaid
graph TD
    Main[Main Progress: Overall Operation]
    Main --> M1[Module 1 Progress]
    Main --> M2[Module 2 Progress]
    Main --> M3[Module 3 Progress]
    
    M1 --> T1[Task 1.1]
    M1 --> T2[Task 1.2]
    
    M2 --> T3[Task 2.1]
    M2 --> T4[Task 2.2]
    
    M3 --> T5[Task 3.1]
    M3 --> T6[Task 3.2]
    
    style Main fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style M1 fill:#50C878,stroke:#2E7D4E,color:#fff
    style M2 fill:#50C878,stroke:#2E7D4E,color:#fff
    style M3 fill:#50C878,stroke:#2E7D4E,color:#fff
```

---

## Integration with Other Modules

### Module Dependencies

```mermaid
graph TB
    CLI[CLI Interface]
    
    CLI -->|Configuration| CoreConfig[Core Config Module]
    CLI -->|File Operations| Utils[Utilities Module]
    CLI -->|Analysis Commands| DepAnalysis[Dependency Analysis Module]
    CLI -->|Web Commands| WebFE[Web Frontend Module]
    
    CoreConfig -->|Base Settings| CLI
    Utils -->|File Management| CLI
    DepAnalysis -->|Analysis Results| CLI
    WebFE -->|Service Status| CLI
    
    style CLI fill:#4A90E2,stroke:#2E5C8A,color:#fff
    
    click CoreConfig href "core_config.md" "Core Configuration Module"
    click Utils href "utilities.md" "Utilities Module"
    click DepAnalysis href "dependency_analysis.md" "Dependency Analysis Module"
    click WebFE href "web_frontend.md" "Web Frontend Module"
```

### Integration Points

#### With Core Config Module
- Inherits base configuration schema from [core_config](core_config.md)
- Extends configuration with CLI-specific settings
- Validates configuration against core constraints

#### With Utilities Module
- Uses FileManager from [utilities](utilities.md) for file operations
- Leverages utility functions for path resolution
- Integrates with logging utilities

#### With Dependency Analysis Module
- Triggers dependency analysis operations via [dependency_analysis](dependency_analysis.md)
- Receives Repository and Node data for display
- Processes NodeSelection results for output formatting

#### With Web Frontend Module
- Can start/stop web services from [web_frontend](web_frontend.md)
- Monitors BackgroundWorker job status
- Manages CacheManager operations
- Submits repositories for processing via GitHubRepoProcessor

---

## Data Flow

### Command Execution Flow

```mermaid
flowchart TD
    Start([User Input]) --> Parse[Parse Command & Arguments]
    Parse --> LoadConfig[Load Configuration]
    LoadConfig --> Validate[Validate Parameters]
    
    Validate -->|Invalid| Error[Display Error]
    Error --> End([Exit])
    
    Validate -->|Valid| InitProgress[Initialize Progress Bar]
    InitProgress --> Route{Command Type}
    
    Route -->|Analyze| AnalyzeCmd[Execute Analysis Command]
    Route -->|Web| WebCmd[Execute Web Command]
    Route -->|Config| ConfigCmd[Execute Config Command]
    
    AnalyzeCmd --> CallDepAnalysis[Call Dependency Analysis Module]
    CallDepAnalysis --> UpdateProgress1[Update Progress]
    UpdateProgress1 --> FormatResults1[Format Analysis Results]
    
    WebCmd --> CallWebFE[Call Web Frontend Module]
    CallWebFE --> UpdateProgress2[Update Progress]
    UpdateProgress2 --> FormatResults2[Format Web Response]
    
    ConfigCmd --> ModifyConfig[Modify Configuration]
    ModifyConfig --> SaveConfig[Save Configuration]
    SaveConfig --> FormatResults3[Format Config Output]
    
    FormatResults1 --> Display[Display Results]
    FormatResults2 --> Display
    FormatResults3 --> Display
    
    Display --> CompleteProgress[Complete Progress Bar]
    CompleteProgress --> End
    
    style Start fill:#90EE90,stroke:#2E7D4E,color:#000
    style End fill:#FFB6C1,stroke:#8B4C5C,color:#000
    style Route fill:#FFD700,stroke:#B8860B,color:#000
```

### Configuration Data Flow

```mermaid
flowchart LR
    subgraph Input Sources
        CLI_Args[CLI Arguments]
        Config_File[Config File]
        Env_Vars[Environment Variables]
        Defaults[System Defaults]
    end
    
    subgraph Processing
        Parser[Argument Parser]
        Loader[Config Loader]
        Merger[Config Merger]
        Validator[Validator]
    end
    
    subgraph Output
        Runtime_Config[Runtime Configuration]
        Persisted_Config[Persisted Configuration]
    end
    
    CLI_Args --> Parser
    Config_File --> Loader
    Env_Vars --> Loader
    Defaults --> Merger
    
    Parser --> Merger
    Loader --> Merger
    Merger --> Validator
    
    Validator --> Runtime_Config
    Validator --> Persisted_Config
    
    style Runtime_Config fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style Persisted_Config fill:#50C878,stroke:#2E7D4E,color:#fff
```

---

## Usage Patterns

### Common CLI Workflows

#### 1. Repository Analysis Workflow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Config
    participant Progress
    participant DepAnalysis
    
    User->>CLI: codewiki analyze <repo_path>
    CLI->>Config: Load configuration
    Config-->>CLI: Configuration loaded
    
    CLI->>Progress: Initialize progress bar
    Progress-->>User: Display: "Starting analysis..."
    
    CLI->>DepAnalysis: Analyze repository
    
    loop For each module
        DepAnalysis-->>Progress: Update progress (X%)
        Progress-->>User: Update display
    end
    
    DepAnalysis-->>CLI: Return Repository object
    CLI->>CLI: Format results
    
    CLI->>Progress: Complete progress bar
    Progress-->>User: Display: "Analysis complete"
    
    CLI-->>User: Display formatted results
```

#### 2. Web Service Management Workflow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Config
    participant WebFE
    participant BgWorker
    
    User->>CLI: codewiki web start
    CLI->>Config: Get web configuration
    Config-->>CLI: Web settings
    
    CLI->>WebFE: Start web service
    WebFE->>BgWorker: Initialize background worker
    BgWorker-->>WebFE: Worker started
    WebFE-->>CLI: Service started on port X
    
    CLI-->>User: Display: "Web service running at http://localhost:X"
    
    Note over User,BgWorker: Service running...
    
    User->>CLI: codewiki web status
    CLI->>WebFE: Get service status
    WebFE->>BgWorker: Get worker status
    BgWorker-->>WebFE: Job status
    WebFE-->>CLI: Service status
    CLI-->>User: Display status information
```

#### 3. Configuration Management Workflow

```mermaid
sequenceDiagram
    participant User
    participant CLI
    participant Config
    participant FileSystem
    
    User->>CLI: codewiki config set output.format json
    CLI->>Config: Parse setting path
    Config->>Config: Validate setting
    
    alt Valid setting
        Config->>Config: Update in-memory config
        Config->>FileSystem: Persist to file
        FileSystem-->>Config: Saved
        Config-->>CLI: Success
        CLI-->>User: Display: "Configuration updated"
    else Invalid setting
        Config-->>CLI: Validation error
        CLI-->>User: Display: "Error: Invalid setting"
    end
    
    User->>CLI: codewiki config get output.format
    CLI->>Config: Retrieve setting
    Config-->>CLI: Setting value
    CLI-->>User: Display: "output.format = json"
```

### Progress Bar Usage Patterns

```mermaid
flowchart TD
    Start[Start Operation] --> CheckDuration{Operation Duration Known?}
    
    CheckDuration -->|Yes| Determinate[Use Determinate Progress Bar]
    CheckDuration -->|No| Indeterminate[Use Indeterminate Progress Bar]
    
    Determinate --> SetTotal[Set Total Steps]
    SetTotal --> Loop1{More Steps?}
    Loop1 -->|Yes| UpdateDet[Update Progress]
    UpdateDet --> Loop1
    Loop1 -->|No| Complete1[Complete Progress]
    
    Indeterminate --> StartSpinner[Start Spinner]
    StartSpinner --> Loop2{Operation Complete?}
    Loop2 -->|No| UpdateDesc[Update Description]
    UpdateDesc --> Loop2
    Loop2 -->|Yes| Complete2[Stop Spinner]
    
    Complete1 --> End[End Operation]
    Complete2 --> End
    
    style Start fill:#90EE90,stroke:#2E7D4E,color:#000
    style End fill:#FFB6C1,stroke:#8B4C5C,color:#000
```

---

## Dependencies

### External Dependencies

The CLI Interface module relies on the following system modules:

```mermaid
graph LR
    CLI[CLI Interface Module]
    
    subgraph "Direct Dependencies"
        CoreConfig[Core Config Module]
        Utils[Utilities Module]
    end
    
    subgraph "Functional Dependencies"
        DepAnalysis[Dependency Analysis Module]
        WebFE[Web Frontend Module]
    end
    
    CLI --> CoreConfig
    CLI --> Utils
    CLI -.->|Commands| DepAnalysis
    CLI -.->|Commands| WebFE
    
    CoreConfig --> Config[Config Class]
    Utils --> FileManager[FileManager Class]
    
    DepAnalysis --> Repository[Repository Class]
    DepAnalysis --> Node[Node Class]
    DepAnalysis --> NodeSelection[NodeSelection Class]
    
    WebFE --> BgWorker[BackgroundWorker]
    WebFE --> CacheManager[CacheManager]
    WebFE --> GitHubProcessor[GitHubRepoProcessor]
    WebFE --> WebConfig[WebAppConfig]
    
    style CLI fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style CoreConfig fill:#50C878,stroke:#2E7D4E,color:#fff
    style Utils fill:#50C878,stroke:#2E7D4E,color:#fff
```

### Dependency Details

| Module | Components Used | Purpose |
|--------|----------------|---------|
| [core_config](core_config.md) | `Config` | Base configuration management and validation |
| [utilities](utilities.md) | `FileManager` | File system operations and path management |
| [dependency_analysis](dependency_analysis.md) | `Repository`, `Node`, `NodeSelection` | Repository analysis and dependency graph generation |
| [web_frontend](web_frontend.md) | `BackgroundWorker`, `CacheManager`, `GitHubRepoProcessor`, `WebAppConfig` | Web service management and repository processing |

### Component Interaction Map

```mermaid
graph TB
    subgraph "CLI Interface Components"
        Config[Configuration]
        Progress[ModuleProgressBar]
    end
    
    subgraph "Core Config Module"
        CoreConfig[Config]
    end
    
    subgraph "Utilities Module"
        FileManager[FileManager]
    end
    
    subgraph "Dependency Analysis Module"
        Repository[Repository]
        Node[Node]
        NodeSelection[NodeSelection]
    end
    
    subgraph "Web Frontend Module"
        BgWorker[BackgroundWorker]
        CacheManager[CacheManager]
        GitHubProcessor[GitHubRepoProcessor]
        WebAppConfig[WebAppConfig]
        JobStatus[JobStatus]
    end
    
    Config -->|Extends| CoreConfig
    Config -->|Uses| FileManager
    
    Progress -->|Tracks| Repository
    Progress -->|Monitors| BgWorker
    Progress -->|Displays| JobStatus
    
    Config -->|Configures| WebAppConfig
    Config -->|Configures| GitHubProcessor
    
    style Config fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style Progress fill:#4A90E2,stroke:#2E5C8A,color:#fff
```

---

## Command Structure

### Typical Command Patterns

The CLI Interface module likely supports the following command patterns:

```
codewiki <command> [subcommand] [options] [arguments]
```

#### Analysis Commands
```bash
# Analyze a repository
codewiki analyze <repo_path> [--output <format>] [--depth <level>]

# Analyze specific modules
codewiki analyze <repo_path> --modules <module1,module2>

# Generate dependency graph
codewiki analyze <repo_path> --graph [--format <dot|json|svg>]
```

#### Web Service Commands
```bash
# Start web service
codewiki web start [--port <port>] [--host <host>]

# Stop web service
codewiki web stop

# Check service status
codewiki web status

# Process repository via web interface
codewiki web process <github_url>
```

#### Configuration Commands
```bash
# View all configuration
codewiki config list

# Get specific setting
codewiki config get <key>

# Set configuration value
codewiki config set <key> <value>

# Reset to defaults
codewiki config reset [--all]
```

#### Utility Commands
```bash
# Display version information
codewiki version

# Show help
codewiki help [command]

# Validate configuration
codewiki validate
```

---

## Error Handling

### Error Handling Flow

```mermaid
flowchart TD
    Start[Command Execution] --> Try{Try Execute}
    
    Try -->|Success| Complete[Complete Successfully]
    Try -->|Error| Catch[Catch Exception]
    
    Catch --> ErrorType{Error Type}
    
    ErrorType -->|Config Error| ConfigHandler[Configuration Error Handler]
    ErrorType -->|Validation Error| ValidationHandler[Validation Error Handler]
    ErrorType -->|Runtime Error| RuntimeHandler[Runtime Error Handler]
    ErrorType -->|Unknown Error| UnknownHandler[Unknown Error Handler]
    
    ConfigHandler --> LogError1[Log Error Details]
    ValidationHandler --> LogError2[Log Error Details]
    RuntimeHandler --> LogError3[Log Error Details]
    UnknownHandler --> LogError4[Log Error Details]
    
    LogError1 --> DisplayUser1[Display User-Friendly Message]
    LogError2 --> DisplayUser2[Display User-Friendly Message]
    LogError3 --> DisplayUser3[Display User-Friendly Message]
    LogError4 --> DisplayUser4[Display User-Friendly Message]
    
    DisplayUser1 --> Cleanup[Cleanup Resources]
    DisplayUser2 --> Cleanup
    DisplayUser3 --> Cleanup
    DisplayUser4 --> Cleanup
    
    Cleanup --> Exit[Exit with Error Code]
    Complete --> ExitSuccess[Exit with Success Code]
    
    style Start fill:#90EE90,stroke:#2E7D4E,color:#000
    style Exit fill:#FFB6C1,stroke:#8B4C5C,color:#000
    style ExitSuccess fill:#90EE90,stroke:#2E7D4E,color:#000
```

---

## Performance Considerations

### Progress Bar Performance

The ModuleProgressBar is designed to minimize performance impact:

1. **Throttled Updates**: Progress updates are throttled to avoid excessive terminal I/O
2. **Async Updates**: Progress updates don't block main operation execution
3. **Efficient Rendering**: Only changed portions of the display are redrawn
4. **Resource Cleanup**: Proper cleanup of terminal resources on completion

### Configuration Caching

```mermaid
sequenceDiagram
    participant CLI
    participant ConfigCache
    participant FileSystem
    
    CLI->>ConfigCache: Request configuration
    
    alt Cache hit
        ConfigCache-->>CLI: Return cached config
    else Cache miss
        ConfigCache->>FileSystem: Load config file
        FileSystem-->>ConfigCache: Config data
        ConfigCache->>ConfigCache: Parse and cache
        ConfigCache-->>CLI: Return config
    end
    
    Note over ConfigCache: Cache invalidated on file change
```

---

## Best Practices

### Configuration Management
1. **Use hierarchical configuration**: Override defaults progressively
2. **Validate early**: Validate configuration before executing commands
3. **Provide sensible defaults**: Ensure the CLI works out-of-the-box
4. **Document settings**: Include help text for all configuration options

### Progress Tracking
1. **Always provide feedback**: Use progress bars for operations > 1 second
2. **Use appropriate indicators**: Determinate for known duration, indeterminate otherwise
3. **Update descriptions**: Keep users informed of current operation
4. **Handle interruptions**: Gracefully handle Ctrl+C and cleanup properly

### Error Handling
1. **User-friendly messages**: Translate technical errors to actionable messages
2. **Provide context**: Include relevant details (file paths, settings, etc.)
3. **Suggest solutions**: When possible, suggest how to fix the error
4. **Log details**: Log full error details for debugging while showing summary to user

---

## Future Enhancements

Potential areas for future development:

1. **Interactive Mode**: REPL-style interactive command interface
2. **Command Aliases**: User-defined command shortcuts
3. **Plugin System**: Support for third-party command extensions
4. **Shell Completion**: Auto-completion for bash/zsh/fish
5. **Configuration Profiles**: Multiple named configuration profiles
6. **Advanced Progress**: Nested progress bars for complex operations
7. **Output Templating**: Customizable output formats using templates
8. **Command History**: Track and replay previous commands

---

## Related Documentation

- [Core Config Module](core_config.md) - Base configuration system
- [Utilities Module](utilities.md) - File management and utilities
- [Dependency Analysis Module](dependency_analysis.md) - Repository analysis engine
- [Web Frontend Module](web_frontend.md) - Web interface and services

---

## Summary

The CLI Interface module serves as the primary user interaction layer for the CodeWiki system, providing:

- **Configuration Management**: Flexible, hierarchical configuration system via the `Configuration` component
- **Progress Tracking**: Visual feedback for long-running operations via the `ModuleProgressBar` component
- **Command Orchestration**: Coordination between analysis, web services, and configuration management
- **User Experience**: Intuitive command structure with helpful error messages and feedback

The module integrates seamlessly with other system components, leveraging the [core_config](core_config.md) for base configuration, [utilities](utilities.md) for file operations, [dependency_analysis](dependency_analysis.md) for repository analysis, and [web_frontend](web_frontend.md) for web service management.
