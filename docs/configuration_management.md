# Configuration Management Module

## Overview

The **configuration_management** module provides centralized configuration settings for the CodeWiki web application. It manages application-wide settings including directory structures, queue configurations, cache policies, server parameters, and Git operations. This module is a critical component of the [web_application](web_application.md) module, ensuring consistent configuration across all web application components.

**Key Responsibilities:**
- Define and manage web application configuration settings
- Ensure required directory structures exist
- Provide path resolution utilities
- Configure cache, queue, and job management parameters
- Set server and Git operation defaults

---

## Architecture

### Component Overview

```mermaid
graph TB
    subgraph "Configuration Management Module"
        WAC[WebAppConfig]
        
        subgraph "Configuration Categories"
            DIR[Directory Settings]
            QUEUE[Queue Settings]
            CACHE[Cache Settings]
            JOB[Job Settings]
            SERVER[Server Settings]
            GIT[Git Settings]
        end
        
        subgraph "Utility Methods"
            ENSURE[ensure_directories]
            GETPATH[get_absolute_path]
        end
        
        WAC --> DIR
        WAC --> QUEUE
        WAC --> CACHE
        WAC --> JOB
        WAC --> SERVER
        WAC --> GIT
        WAC --> ENSURE
        WAC --> GETPATH
    end
    
    subgraph "Dependent Modules"
        WR[Web Routes]
        BG[Background Worker]
        CM[Cache Manager]
        GH[GitHub Processor]
    end
    
    WAC --> WR
    WAC --> BG
    WAC --> CM
    WAC --> GH
    
    style WAC fill:#4CAF50,stroke:#2E7D32,color:#fff
    style DIR fill:#90CAF9,stroke:#1976D2
    style QUEUE fill:#90CAF9,stroke:#1976D2
    style CACHE fill:#90CAF9,stroke:#1976D2
    style JOB fill:#90CAF9,stroke:#1976D2
    style SERVER fill:#90CAF9,stroke:#1976D2
    style GIT fill:#90CAF9,stroke:#1976D2
    style ENSURE fill:#FFE082,stroke:#F57C00
    style GETPATH fill:#FFE082,stroke:#F57C00
```

### Module Dependencies

```mermaid
graph LR
    subgraph "Configuration Management"
        WAC[WebAppConfig]
    end
    
    subgraph "Web Application Modules"
        WR[web_routes_api]
        BG[background_processing]
        CM[cache_management]
        GH[github_integration]
        DM[data_models]
    end
    
    subgraph "Shared Utilities"
        CFG[Config]
        FM[FileManager]
    end
    
    subgraph "Standard Library"
        OS[os]
        PATH[pathlib.Path]
    end
    
    WAC --> WR
    WAC --> BG
    WAC --> CM
    WAC --> GH
    WAC --> DM
    
    WAC -.similar to.-> CFG
    WAC -.uses pattern from.-> FM
    
    WAC --> OS
    WAC --> PATH
    
    style WAC fill:#4CAF50,stroke:#2E7D32,color:#fff
    style WR fill:#E1BEE7,stroke:#7B1FA2
    style BG fill:#E1BEE7,stroke:#7B1FA2
    style CM fill:#E1BEE7,stroke:#7B1FA2
    style GH fill:#E1BEE7,stroke:#7B1FA2
    style DM fill:#E1BEE7,stroke:#7B1FA2
    style CFG fill:#FFCCBC,stroke:#E64A19
    style FM fill:#FFCCBC,stroke:#E64A19
```

---

## Core Components

### WebAppConfig

The `WebAppConfig` class is the central configuration component that defines all web application settings as class-level constants.

#### Configuration Categories

##### 1. Directory Settings
```python
CACHE_DIR = "./output/cache"      # Cache storage location
TEMP_DIR = "./output/temp"        # Temporary file storage
OUTPUT_DIR = "./output"           # Base output directory
```

**Purpose:** Define the directory structure for web application file operations.

##### 2. Queue Settings
```python
QUEUE_SIZE = 100                  # Maximum queue capacity
```

**Purpose:** Configure the background job queue capacity for processing repository analysis requests.

##### 3. Cache Settings
```python
CACHE_EXPIRY_DAYS = 365          # Cache entry lifetime
```

**Purpose:** Define cache retention policies for generated documentation and analysis results.

##### 4. Job Cleanup Settings
```python
JOB_CLEANUP_HOURS = 24000        # Job retention period
RETRY_COOLDOWN_MINUTES = 3       # Retry delay for failed jobs
```

**Purpose:** Manage job lifecycle and retry behavior for background processing.

##### 5. Server Settings
```python
DEFAULT_HOST = "127.0.0.1"       # Default server host
DEFAULT_PORT = 8000              # Default server port
```

**Purpose:** Configure default web server binding parameters.

##### 6. Git Settings
```python
CLONE_TIMEOUT = 300              # Git clone timeout (seconds)
CLONE_DEPTH = 1                  # Shallow clone depth
```

**Purpose:** Configure Git repository cloning behavior for efficient repository processing.

#### Class Methods

##### ensure_directories()
```python
@classmethod
def ensure_directories(cls):
    """Ensure all required directories exist."""
```

**Purpose:** Create all required directories if they don't exist, ensuring the application can start successfully.

**Process Flow:**
```mermaid
flowchart TD
    START[Start] --> GETDIRS[Get Directory List]
    GETDIRS --> LOOP{For Each Directory}
    LOOP --> CREATE[Create Directory<br/>parents=True, exist_ok=True]
    CREATE --> LOOP
    LOOP --> END[End]
    
    style START fill:#4CAF50,stroke:#2E7D32,color:#fff
    style END fill:#4CAF50,stroke:#2E7D32,color:#fff
    style CREATE fill:#90CAF9,stroke:#1976D2
```

**Directories Created:**
- `CACHE_DIR`: For storing cached documentation
- `TEMP_DIR`: For temporary repository clones
- `OUTPUT_DIR`: Base directory for all outputs

##### get_absolute_path()
```python
@classmethod
def get_absolute_path(cls, path: str) -> str:
    """Get absolute path for a given relative path."""
```

**Purpose:** Convert relative paths to absolute paths for consistent file operations.

**Usage Example:**
```python
abs_cache_path = WebAppConfig.get_absolute_path(WebAppConfig.CACHE_DIR)
```

---

## Configuration Usage Patterns

### Initialization Pattern

```mermaid
sequenceDiagram
    participant App as Web Application
    participant WAC as WebAppConfig
    participant FS as File System
    participant Modules as Other Modules
    
    App->>WAC: ensure_directories()
    WAC->>FS: Create CACHE_DIR
    WAC->>FS: Create TEMP_DIR
    WAC->>FS: Create OUTPUT_DIR
    FS-->>WAC: Directories Ready
    WAC-->>App: Initialization Complete
    
    App->>Modules: Initialize with Config
    Modules->>WAC: Access Configuration Values
    WAC-->>Modules: Return Settings
    Modules-->>App: Modules Ready
```

### Configuration Access Pattern

```mermaid
flowchart LR
    subgraph "Module Components"
        WR[WebRoutes]
        BW[BackgroundWorker]
        CM[CacheManager]
        GP[GitHubProcessor]
    end
    
    subgraph "WebAppConfig"
        direction TB
        SERVER[Server Settings]
        QUEUE[Queue Settings]
        CACHE[Cache Settings]
        GIT[Git Settings]
        DIRS[Directory Settings]
    end
    
    WR --> SERVER
    BW --> QUEUE
    BW --> DIRS
    CM --> CACHE
    CM --> DIRS
    GP --> GIT
    GP --> DIRS
    
    style WR fill:#E1BEE7,stroke:#7B1FA2
    style BW fill:#E1BEE7,stroke:#7B1FA2
    style CM fill:#E1BEE7,stroke:#7B1FA2
    style GP fill:#E1BEE7,stroke:#7B1FA2
```

---

## Integration with Web Application

### Component Relationships

```mermaid
graph TB
    subgraph "Web Application Architecture"
        WAC[WebAppConfig]
        
        subgraph "Web Routes API"
            WR[WebRoutes]
            WR_SERVER[Uses: DEFAULT_HOST<br/>DEFAULT_PORT]
        end
        
        subgraph "Background Processing"
            BW[BackgroundWorker]
            BW_QUEUE[Uses: QUEUE_SIZE]
            BW_JOB[Uses: JOB_CLEANUP_HOURS<br/>RETRY_COOLDOWN_MINUTES]
            BW_TEMP[Uses: TEMP_DIR]
        end
        
        subgraph "Cache Management"
            CM[CacheManager]
            CM_DIR[Uses: CACHE_DIR]
            CM_EXP[Uses: CACHE_EXPIRY_DAYS]
        end
        
        subgraph "GitHub Integration"
            GP[GitHubProcessor]
            GP_GIT[Uses: CLONE_TIMEOUT<br/>CLONE_DEPTH]
            GP_TEMP[Uses: TEMP_DIR]
        end
    end
    
    WAC --> WR_SERVER
    WAC --> BW_QUEUE
    WAC --> BW_JOB
    WAC --> BW_TEMP
    WAC --> CM_DIR
    WAC --> CM_EXP
    WAC --> GP_GIT
    WAC --> GP_TEMP
    
    WR_SERVER --> WR
    BW_QUEUE --> BW
    BW_JOB --> BW
    BW_TEMP --> BW
    CM_DIR --> CM
    CM_EXP --> CM
    GP_GIT --> GP
    GP_TEMP --> GP
    
    style WAC fill:#4CAF50,stroke:#2E7D32,color:#fff
    style WR fill:#E1BEE7,stroke:#7B1FA2
    style BW fill:#E1BEE7,stroke:#7B1FA2
    style CM fill:#E1BEE7,stroke:#7B1FA2
    style GP fill:#E1BEE7,stroke:#7B1FA2
```

### Configuration Flow

```mermaid
flowchart TD
    START[Application Startup] --> INIT[WebAppConfig.ensure_directories]
    INIT --> CHECK{Directories Exist?}
    CHECK -->|No| CREATE[Create Directories]
    CHECK -->|Yes| SKIP[Skip Creation]
    CREATE --> READY[Configuration Ready]
    SKIP --> READY
    
    READY --> INIT_WR[Initialize WebRoutes]
    READY --> INIT_BW[Initialize BackgroundWorker]
    READY --> INIT_CM[Initialize CacheManager]
    READY --> INIT_GP[Initialize GitHubProcessor]
    
    INIT_WR --> APP_READY[Application Ready]
    INIT_BW --> APP_READY
    INIT_CM --> APP_READY
    INIT_GP --> APP_READY
    
    style START fill:#4CAF50,stroke:#2E7D32,color:#fff
    style READY fill:#4CAF50,stroke:#2E7D32,color:#fff
    style APP_READY fill:#4CAF50,stroke:#2E7D32,color:#fff
    style CREATE fill:#90CAF9,stroke:#1976D2
```

---

## Configuration vs. Shared Config

### Comparison with Shared Utilities Config

The CodeWiki system has two configuration classes serving different purposes:

```mermaid
graph TB
    subgraph "Configuration Hierarchy"
        subgraph "Shared Utilities"
            CFG[Config<br/>CLI & Core System]
            CFG_REPO[repo_path]
            CFG_OUTPUT[output_dir]
            CFG_DEPS[dependency_graph_dir]
            CFG_DOCS[docs_dir]
            CFG_LLM[LLM settings]
        end
        
        subgraph "Web Application"
            WAC[WebAppConfig<br/>Web Server]
            WAC_CACHE[CACHE_DIR]
            WAC_TEMP[TEMP_DIR]
            WAC_QUEUE[QUEUE_SIZE]
            WAC_SERVER[Server settings]
            WAC_GIT[Git settings]
        end
    end
    
    subgraph "Usage Context"
        CLI[CLI Interface]
        WEB[Web Application]
    end
    
    CFG --> CFG_REPO
    CFG --> CFG_OUTPUT
    CFG --> CFG_DEPS
    CFG --> CFG_DOCS
    CFG --> CFG_LLM
    
    WAC --> WAC_CACHE
    WAC --> WAC_TEMP
    WAC --> WAC_QUEUE
    WAC --> WAC_SERVER
    WAC --> WAC_GIT
    
    CFG --> CLI
    WAC --> WEB
    
    style CFG fill:#FFCCBC,stroke:#E64A19
    style WAC fill:#4CAF50,stroke:#2E7D32,color:#fff
    style CLI fill:#B3E5FC,stroke:#0277BD
    style WEB fill:#C5E1A5,stroke:#558B2F
```

**Key Differences:**

| Aspect | WebAppConfig | Config (Shared) |
|--------|-------------|-----------------|
| **Purpose** | Web application settings | CLI and core system settings |
| **Scope** | Web server, cache, queue | Repository analysis, LLM |
| **Initialization** | Class-level constants | Instance from args/CLI |
| **Directory Focus** | Cache, temp, output | Docs, dependency graphs |
| **Additional Settings** | Server, queue, Git | LLM models, max depth |

---

## Directory Structure Management

### Directory Hierarchy

```mermaid
graph TB
    ROOT[./output]
    
    ROOT --> CACHE[./output/cache]
    ROOT --> TEMP[./output/temp]
    
    CACHE --> CACHE_ENTRY1[Repository Hash 1]
    CACHE --> CACHE_ENTRY2[Repository Hash 2]
    
    TEMP --> TEMP_CLONE1[Temp Clone 1]
    TEMP --> TEMP_CLONE2[Temp Clone 2]
    
    CACHE_ENTRY1 --> DOCS1[docs/]
    CACHE_ENTRY1 --> META1[metadata.json]
    
    style ROOT fill:#4CAF50,stroke:#2E7D32,color:#fff
    style CACHE fill:#90CAF9,stroke:#1976D2
    style TEMP fill:#FFE082,stroke:#F57C00
```

### Directory Usage by Component

```mermaid
flowchart LR
    subgraph "Directories"
        CACHE[CACHE_DIR<br/>./output/cache]
        TEMP[TEMP_DIR<br/>./output/temp]
        OUTPUT[OUTPUT_DIR<br/>./output]
    end
    
    subgraph "Components"
        CM[CacheManager]
        GP[GitHubProcessor]
        BW[BackgroundWorker]
    end
    
    subgraph "Operations"
        STORE[Store Generated Docs]
        CLONE[Clone Repositories]
        PROCESS[Process Jobs]
    end
    
    CM --> STORE
    GP --> CLONE
    BW --> PROCESS
    
    STORE --> CACHE
    CLONE --> TEMP
    PROCESS --> TEMP
    PROCESS --> CACHE
    
    style CACHE fill:#90CAF9,stroke:#1976D2
    style TEMP fill:#FFE082,stroke:#F57C00
    style OUTPUT fill:#A5D6A7,stroke:#388E3C
```

---

## Configuration Best Practices

### 1. Initialization Sequence

```mermaid
sequenceDiagram
    participant Main as main.py
    participant WAC as WebAppConfig
    participant App as FastAPI App
    participant Modules as Application Modules
    
    Main->>WAC: ensure_directories()
    activate WAC
    WAC->>WAC: Create required directories
    WAC-->>Main: Success
    deactivate WAC
    
    Main->>App: Initialize FastAPI
    Main->>Modules: Initialize with WebAppConfig
    
    Modules->>WAC: Access configuration values
    WAC-->>Modules: Return settings
    
    Main->>App: Start server with DEFAULT_HOST:DEFAULT_PORT
```

### 2. Configuration Access Pattern

**Recommended:**
```python
# Direct class-level access
cache_dir = WebAppConfig.CACHE_DIR
queue_size = WebAppConfig.QUEUE_SIZE

# Ensure directories before use
WebAppConfig.ensure_directories()
```

**Not Recommended:**
```python
# Don't instantiate the config class
config = WebAppConfig()  # Unnecessary

# Don't hardcode values
cache_dir = "./output/cache"  # Use WebAppConfig.CACHE_DIR instead
```

### 3. Path Resolution

```python
# Use get_absolute_path for file operations
abs_path = WebAppConfig.get_absolute_path(WebAppConfig.CACHE_DIR)

# Combine with pathlib for advanced operations
from pathlib import Path
cache_path = Path(WebAppConfig.CACHE_DIR)
```

---

## Configuration Settings Reference

### Complete Settings Table

| Category | Setting | Default Value | Used By | Purpose |
|----------|---------|---------------|---------|---------|
| **Directories** | `CACHE_DIR` | `"./output/cache"` | [cache_management](cache_management.md) | Store cached documentation |
| | `TEMP_DIR` | `"./output/temp"` | [github_integration](github_integration.md), [background_processing](background_processing.md) | Temporary repository clones |
| | `OUTPUT_DIR` | `"./output"` | All modules | Base output directory |
| **Queue** | `QUEUE_SIZE` | `100` | [background_processing](background_processing.md) | Maximum concurrent jobs |
| **Cache** | `CACHE_EXPIRY_DAYS` | `365` | [cache_management](cache_management.md) | Cache retention period |
| **Jobs** | `JOB_CLEANUP_HOURS` | `24000` | [background_processing](background_processing.md) | Job history retention |
| | `RETRY_COOLDOWN_MINUTES` | `3` | [background_processing](background_processing.md) | Retry delay for failures |
| **Server** | `DEFAULT_HOST` | `"127.0.0.1"` | [web_routes_api](web_routes_api.md) | Server bind address |
| | `DEFAULT_PORT` | `8000` | [web_routes_api](web_routes_api.md) | Server bind port |
| **Git** | `CLONE_TIMEOUT` | `300` | [github_integration](github_integration.md) | Clone operation timeout |
| | `CLONE_DEPTH` | `1` | [github_integration](github_integration.md) | Shallow clone depth |

---

## Extension and Customization

### Adding New Configuration Settings

```mermaid
flowchart TD
    START[Need New Setting] --> IDENTIFY[Identify Category]
    IDENTIFY --> ADD[Add Class Constant]
    ADD --> DOC[Document Setting]
    DOC --> UPDATE[Update ensure_directories<br/>if directory-related]
    UPDATE --> TEST[Test Configuration]
    TEST --> DEPLOY[Deploy Changes]
    
    style START fill:#4CAF50,stroke:#2E7D32,color:#fff
    style DEPLOY fill:#4CAF50,stroke:#2E7D32,color:#fff
    style ADD fill:#90CAF9,stroke:#1976D2
    style UPDATE fill:#FFE082,stroke:#F57C00
```

### Example: Adding a New Directory Setting

```python
class WebAppConfig:
    # ... existing settings ...
    
    # New directory setting
    LOGS_DIR = "./output/logs"
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist."""
        directories = [
            cls.CACHE_DIR,
            cls.TEMP_DIR,
            cls.OUTPUT_DIR,
            cls.LOGS_DIR,  # Add new directory
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
```

---

## Error Handling and Validation

### Directory Creation Error Handling

```mermaid
flowchart TD
    START[ensure_directories] --> LOOP{For Each Directory}
    LOOP --> TRY[Try Create Directory]
    TRY --> SUCCESS{Success?}
    SUCCESS -->|Yes| NEXT[Next Directory]
    SUCCESS -->|No| ERROR[Path.mkdir handles<br/>exist_ok=True]
    ERROR --> NEXT
    NEXT --> LOOP
    LOOP --> END[All Directories Ready]
    
    style START fill:#4CAF50,stroke:#2E7D32,color:#fff
    style END fill:#4CAF50,stroke:#2E7D32,color:#fff
    style ERROR fill:#FFCDD2,stroke:#C62828
```

**Built-in Safety:**
- `parents=True`: Creates parent directories if needed
- `exist_ok=True`: No error if directory already exists
- Atomic operation: Each directory creation is independent

---

## Performance Considerations

### Configuration Access Performance

```mermaid
graph LR
    subgraph "Performance Characteristics"
        ACCESS[Class-level Access]
        MEMORY[Low Memory Footprint]
        INIT[One-time Initialization]
    end
    
    subgraph "Benefits"
        FAST[Constant Time Access]
        SHARED[Shared Across Modules]
        CACHE_FRIENDLY[CPU Cache Friendly]
    end
    
    ACCESS --> FAST
    MEMORY --> SHARED
    INIT --> CACHE_FRIENDLY
    
    style ACCESS fill:#4CAF50,stroke:#2E7D32,color:#fff
    style MEMORY fill:#4CAF50,stroke:#2E7D32,color:#fff
    style INIT fill:#4CAF50,stroke:#2E7D32,color:#fff
```

**Optimization Notes:**
- Class-level constants: No instantiation overhead
- Single directory creation: One-time startup cost
- No runtime configuration changes: Predictable behavior

---

## Testing Considerations

### Configuration Testing Strategy

```mermaid
flowchart TD
    subgraph "Test Categories"
        UNIT[Unit Tests]
        INTEGRATION[Integration Tests]
        E2E[End-to-End Tests]
    end
    
    subgraph "Test Scenarios"
        DIR_CREATE[Directory Creation]
        PATH_RESOLVE[Path Resolution]
        CONFIG_ACCESS[Configuration Access]
        MULTI_MODULE[Multi-Module Usage]
    end
    
    UNIT --> DIR_CREATE
    UNIT --> PATH_RESOLVE
    UNIT --> CONFIG_ACCESS
    
    INTEGRATION --> MULTI_MODULE
    
    E2E --> MULTI_MODULE
    
    style UNIT fill:#90CAF9,stroke:#1976D2
    style INTEGRATION fill:#A5D6A7,stroke:#388E3C
    style E2E fill:#FFE082,stroke:#F57C00
```

**Test Examples:**

```python
def test_ensure_directories():
    """Test directory creation."""
    WebAppConfig.ensure_directories()
    assert Path(WebAppConfig.CACHE_DIR).exists()
    assert Path(WebAppConfig.TEMP_DIR).exists()
    assert Path(WebAppConfig.OUTPUT_DIR).exists()

def test_get_absolute_path():
    """Test path resolution."""
    abs_path = WebAppConfig.get_absolute_path("./test")
    assert os.path.isabs(abs_path)

def test_configuration_values():
    """Test configuration constants."""
    assert WebAppConfig.QUEUE_SIZE == 100
    assert WebAppConfig.CACHE_EXPIRY_DAYS == 365
    assert WebAppConfig.DEFAULT_PORT == 8000
```

---

## Related Modules

### Direct Dependencies
- **[web_routes_api](web_routes_api.md)**: Uses server configuration settings
- **[background_processing](background_processing.md)**: Uses queue and job settings
- **[cache_management](cache_management.md)**: Uses cache directory and expiry settings
- **[github_integration](github_integration.md)**: Uses Git and temporary directory settings

### Related Configuration
- **[shared_utilities](shared_utilities.md)**: Contains `Config` class for CLI configuration
- **[cli_interface](cli_interface.md)**: Uses separate CLI configuration

### Parent Module
- **[web_application](web_application.md)**: Parent module containing all web components

---

## Summary

The **configuration_management** module provides a centralized, simple, and efficient configuration system for the CodeWiki web application. Key characteristics:

**Strengths:**
- ✅ Simple class-level constant design
- ✅ Clear separation of concerns by configuration category
- ✅ Built-in directory management utilities
- ✅ Zero-overhead configuration access
- ✅ Type-safe constant values

**Design Principles:**
- **Simplicity**: Class-level constants, no complex initialization
- **Reliability**: Built-in directory creation with error handling
- **Performance**: O(1) access time, minimal memory footprint
- **Maintainability**: Clear categorization and documentation

**Usage Pattern:**
```python
# Initialize once at startup
WebAppConfig.ensure_directories()

# Access anywhere in the application
cache_dir = WebAppConfig.CACHE_DIR
queue_size = WebAppConfig.QUEUE_SIZE
```

This module serves as the foundation for consistent configuration management across all web application components, ensuring reliable and predictable behavior.
