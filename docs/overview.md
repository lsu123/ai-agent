# AI-Agent Repository Overview

## Purpose

The **ai-agent** repository (also known as **CodeWiki**) is an intelligent documentation generation system that automatically analyzes code repositories and produces comprehensive, structured documentation using Large Language Models (LLMs). The system provides both command-line and web-based interfaces for transforming complex codebases into navigable, well-organized documentation with minimal manual effort.

### Core Capabilities

- **Automated Code Analysis**: Analyzes repository structure, dependencies, and relationships between code components
- **Intelligent Documentation Generation**: Leverages LLMs to generate human-readable documentation from source code
- **Multi-Interface Support**: Provides both CLI and web application interfaces for different use cases
- **Smart Caching**: Implements intelligent caching to avoid redundant documentation generation
- **GitHub Integration**: Seamlessly processes repositories from GitHub with commit-specific support
- **Asynchronous Processing**: Background job processing for non-blocking documentation generation

---

## End-to-End Architecture

### High-Level System Architecture

```mermaid
graph TB
    subgraph "User Interfaces"
        CLI[CLI Interface]
        WEB[Web Application]
    end
    
    subgraph "Core Processing"
        DA[Dependency Analysis Core]
        DG[Documentation Generator]
        MC[Module Clusterer]
    end
    
    subgraph "Infrastructure"
        SU[Shared Utilities]
        CM[Cache Manager]
        BW[Background Worker]
        GH[GitHub Processor]
    end
    
    subgraph "External Services"
        LLM[LLM API<br/>OpenAI/Anthropic/Local]
        GITHUB[GitHub Repositories]
    end
    
    subgraph "Storage"
        FS[File System]
        CACHE[Documentation Cache]
    end
    
    CLI -->|submits| DA
    WEB -->|submits| BW
    BW -->|processes| DA
    
    DA -->|analyzes| GITHUB
    DA -->|uses| SU
    DA -->|generates| DG
    
    DG -->|clusters| MC
    DG -->|calls| LLM
    DG -->|stores| FS
    
    BW -->|clones| GH
    BW -->|caches| CM
    CM -->|stores| CACHE
    
    GH -->|fetches| GITHUB
    
    style CLI fill:#4A90E2,color:#fff
    style WEB fill:#4A90E2,color:#fff
    style DA fill:#E27D60,color:#fff
    style DG fill:#E27D60,color:#fff
    style SU fill:#85DCB0,color:#fff
    style LLM fill:#9C27B0,color:#fff
```

### Data Flow Architecture

```mermaid
flowchart LR
    subgraph "Input Layer"
        USER[User Input]
        REPO[Repository URL/Path]
    end
    
    subgraph "Interface Layer"
        CLI_IF[CLI Interface]
        WEB_IF[Web Routes]
    end
    
    subgraph "Processing Layer"
        VALIDATE[Validation]
        CACHE_CHECK[Cache Check]
        CLONE[Repository Clone]
        ANALYZE[Dependency Analysis]
        CLUSTER[Module Clustering]
        GENERATE[Doc Generation]
    end
    
    subgraph "Storage Layer"
        CACHE_STORE[Cache Storage]
        FILE_STORE[File Storage]
    end
    
    subgraph "Output Layer"
        DOCS[Documentation]
        STATUS[Job Status]
    end
    
    USER --> REPO
    REPO --> CLI_IF
    REPO --> WEB_IF
    
    CLI_IF --> VALIDATE
    WEB_IF --> VALIDATE
    
    VALIDATE --> CACHE_CHECK
    CACHE_CHECK -->|Hit| DOCS
    CACHE_CHECK -->|Miss| CLONE
    
    CLONE --> ANALYZE
    ANALYZE --> CLUSTER
    CLUSTER --> GENERATE
    
    GENERATE --> CACHE_STORE
    GENERATE --> FILE_STORE
    GENERATE --> DOCS
    
    WEB_IF --> STATUS
    
    style USER fill:#FFE5B4
    style DOCS fill:#90EE90
    style CACHE_CHECK fill:#FFD700
```

### Component Interaction Sequence

```mermaid
sequenceDiagram
    participant User
    participant Interface as CLI/Web Interface
    participant Config as Configuration
    participant Cache as Cache Manager
    participant GitHub as GitHub Processor
    participant Analyzer as Dependency Analyzer
    participant Generator as Doc Generator
    participant LLM as LLM Service
    participant Storage as File Storage
    
    User->>Interface: Submit repository
    Interface->>Config: Load configuration
    Config-->>Interface: Config ready
    
    Interface->>Cache: Check cache
    alt Cache Hit
        Cache-->>Interface: Return cached docs
        Interface-->>User: Display documentation
    else Cache Miss
        Interface->>GitHub: Clone repository
        GitHub-->>Interface: Repository ready
        
        Interface->>Analyzer: Analyze dependencies
        Analyzer->>Analyzer: Build dependency graph
        Analyzer->>Analyzer: Extract components
        Analyzer-->>Interface: Analysis complete
        
        Interface->>Generator: Generate documentation
        Generator->>LLM: Request doc generation
        LLM-->>Generator: Generated content
        Generator->>Storage: Save documentation
        Generator->>Cache: Update cache
        Generator-->>Interface: Docs ready
        
        Interface-->>User: Display documentation
    end
```

---

## Core Modules

The ai-agent repository is organized into four primary modules, each serving a distinct purpose in the documentation generation pipeline:

### 1. [CLI Interface Module](cli_interface.md)

**Purpose**: Provides command-line interface for documentation generation with configuration management and progress tracking.

**Key Components**:
- `Configuration`: Persistent user settings management
- `ProgressTracker`: Multi-stage progress tracking with ETA
- `ModuleProgressBar`: Per-module progress visualization

**Primary Responsibilities**:
- User configuration storage (`~/.codewiki/config.json`)
- Command-line argument parsing and validation
- Real-time progress feedback during generation
- Integration with backend configuration system

**Usage Context**: Ideal for developers who prefer terminal-based workflows, CI/CD integration, and scripted documentation generation.

---

### 2. [Dependency Analysis Core Module](dependency_analysis_core.md)

**Purpose**: Analyzes code repositories to extract structure, dependencies, and relationships between components.

**Key Components**:
- `Node`: Represents code components (functions, classes, methods)
- `CallRelationship`: Models caller-callee relationships
- `Repository`: Repository metadata container
- `AnalysisResult`: Complete analysis output package
- `NodeSelection`: Selective export configuration

**Primary Responsibilities**:
- Code structure representation as dependency graphs
- Relationship tracking between components
- Source code and metadata extraction
- Analysis result packaging and serialization

**Usage Context**: Core data foundation used by all other modules for representing analyzed code structure.

---

### 3. [Web Application Module](web_application.md)

**Purpose**: Provides web-based interface for repository submission, job tracking, and documentation viewing.

**Key Components**:
- `WebRoutes`: FastAPI route handlers
- `BackgroundWorker`: Asynchronous job processing
- `CacheManager`: Documentation caching system
- `GitHubRepoProcessor`: GitHub integration
- `WebAppConfig`: Web application configuration

**Sub-modules**:
- [Configuration Management](configuration_management.md): Web app settings
- [Web Routes & API](web_routes_api.md): HTTP endpoints
- [Background Processing](background_processing.md): Job queue management
- [Cache Management](cache_management.md): Intelligent caching
- [GitHub Integration](github_integration.md): Repository operations
- [Data Models](data_models.md): Request/response models

**Primary Responsibilities**:
- Web-based repository submission
- Background job processing and tracking
- Cache management and retrieval
- GitHub repository cloning and processing
- Documentation serving and viewing

**Usage Context**: Ideal for teams, web-based workflows, and users who prefer graphical interfaces.

---

### 4. [Shared Utilities Module](shared_utilities.md)

**Purpose**: Provides foundational infrastructure for configuration and file operations shared across all modules.

**Key Components**:
- `Config`: Unified configuration management
- `FileManager`: Standardized file I/O operations

**Primary Responsibilities**:
- Context-aware configuration (CLI vs. Web)
- LLM API configuration management
- Directory structure management
- JSON and text file operations
- Environment variable handling

**Usage Context**: Foundation module used by all other modules for configuration and file operations.

---

## Module Dependency Graph

```mermaid
graph TD
    subgraph "User-Facing Modules"
        CLI[CLI Interface Module]
        WEB[Web Application Module]
    end
    
    subgraph "Core Processing Modules"
        DAC[Dependency Analysis Core]
    end
    
    subgraph "Infrastructure Modules"
        SU[Shared Utilities Module]
    end
    
    CLI -->|uses config| SU
    CLI -->|uses models| DAC
    CLI -->|triggers analysis| DAC
    
    WEB -->|uses config| SU
    WEB -->|uses models| DAC
    WEB -->|triggers analysis| DAC
    WEB -->|uses file ops| SU
    
    DAC -->|uses config| SU
    DAC -->|uses file ops| SU
    
    style CLI fill:#4A90E2,color:#fff
    style WEB fill:#4A90E2,color:#fff
    style DAC fill:#E27D60,color:#fff
    style SU fill:#85DCB0,color:#fff
```

---

## System Workflows

### CLI Documentation Generation Workflow

```mermaid
flowchart TD
    START([User runs CLI command]) --> INIT[Load CLI Configuration]
    INIT --> VALIDATE[Validate settings]
    VALIDATE --> CREATE_CONFIG[Create Backend Config]
    CREATE_CONFIG --> START_PROGRESS[Initialize Progress Tracker]
    
    START_PROGRESS --> STAGE1[Stage 1: Dependency Analysis]
    STAGE1 --> STAGE2[Stage 2: Module Clustering]
    STAGE2 --> STAGE3[Stage 3: Doc Generation]
    STAGE3 --> STAGE4[Stage 4: HTML Generation]
    STAGE4 --> STAGE5[Stage 5: Finalization]
    
    STAGE5 --> SAVE[Save Documentation]
    SAVE --> END([Documentation Complete])
    
    style START fill:#4CAF50,color:#fff
    style END fill:#4CAF50,color:#fff
    style STAGE3 fill:#FF9800,color:#fff
```

### Web Application Workflow

```mermaid
flowchart TD
    START([User submits repository]) --> VALIDATE[Validate GitHub URL]
    VALIDATE --> CACHE_CHECK{Check Cache}
    
    CACHE_CHECK -->|Hit| SERVE[Serve Cached Docs]
    CACHE_CHECK -->|Miss| QUEUE[Add to Job Queue]
    
    QUEUE --> WORKER[Background Worker Picks Up]
    WORKER --> CLONE[Clone Repository]
    CLONE --> ANALYZE[Analyze Dependencies]
    ANALYZE --> GENERATE[Generate Documentation]
    GENERATE --> CACHE_STORE[Store in Cache]
    CACHE_STORE --> UPDATE_STATUS[Update Job Status]
    UPDATE_STATUS --> SERVE
    
    SERVE --> END([Display Documentation])
    
    style START fill:#4CAF50,color:#fff
    style END fill:#4CAF50,color:#fff
    style CACHE_CHECK fill:#FFD700
    style WORKER fill:#FF9800,color:#fff
```

---

## Key Features

### 1. Dual Interface Support
- **CLI**: Terminal-based workflow with progress tracking
- **Web**: Browser-based interface with job tracking

### 2. Intelligent Caching
- SHA-256 hash-based cache indexing
- Configurable expiration (default: 365 days)
- Automatic cache validation and cleanup

### 3. Asynchronous Processing
- Non-blocking background job execution
- Queue-based job management
- Real-time status updates

### 4. LLM Integration
- Support for multiple LLM providers (OpenAI, Anthropic, local)
- Configurable models for different tasks
- Fallback model support

### 5. GitHub Integration
- URL validation and normalization
- Commit-specific documentation
- Shallow cloning for efficiency

### 6. Comprehensive Analysis
- Dependency graph construction
- Module clustering
- Relationship tracking
- Metadata extraction

---

## Configuration Management

### CLI Configuration
- Stored in `~/.codewiki/config.json`
- Persistent user preferences
- API key management via keyring

### Web Application Configuration
- Environment variable based
- Runtime configuration injection
- Separate cache and temp directories

### Shared Configuration
- Unified `Config` class
- Context-aware settings
- LLM endpoint configuration

---

## Technology Stack

### Core Technologies
- **Python 3.12+**: Primary programming language
- **FastAPI**: Web framework for REST API
- **Pydantic**: Data validation and serialization
- **Click**: CLI framework

### External Services
- **LLM APIs**: OpenAI, Anthropic, or local LLM endpoints
- **GitHub**: Repository hosting and access

### Storage
- **File System**: Documentation and cache storage
- **JSON**: Configuration and data serialization

---

## Getting Started

### CLI Usage
```bash
# Initialize configuration
codewiki init

# Generate documentation
codewiki generate /path/to/repo --verbose

# Update configuration
codewiki config set main_model gpt-4-turbo
```

### Web Application Usage
```bash
# Start web server
python -m codewiki.web

# Access at http://localhost:8000
# Submit repository URL via web form
```

---

## Module Reference Summary

| Module | Primary Purpose | Key Components | Documentation |
|--------|----------------|----------------|---------------|
| **CLI Interface** | Command-line interface | Configuration, ProgressTracker | [cli_interface.md](cli_interface.md) |
| **Dependency Analysis Core** | Code analysis and modeling | Node, Repository, AnalysisResult | [dependency_analysis_core.md](dependency_analysis_core.md) |
| **Web Application** | Web-based interface | WebRoutes, BackgroundWorker, CacheManager | [web_application.md](web_application.md) |
| **Shared Utilities** | Common infrastructure | Config, FileManager | [shared_utilities.md](shared_utilities.md) |

---

## System Characteristics

### Strengths
✅ **Automated Documentation**: Minimal manual effort required  
✅ **Multi-Interface**: CLI and web options for different workflows  
✅ **Intelligent Caching**: Avoids redundant processing  
✅ **Asynchronous Processing**: Non-blocking operations  
✅ **Flexible LLM Support**: Multiple provider options  
✅ **Comprehensive Analysis**: Deep code understanding  

### Use Cases
- **Open Source Projects**: Generate documentation for public repositories
- **Enterprise Codebases**: Document internal code for team knowledge sharing
- **Code Reviews**: Understand unfamiliar codebases quickly
- **Onboarding**: Help new developers understand project structure
- **Documentation Maintenance**: Keep docs in sync with code changes

---

## Conclusion

The **ai-agent** (CodeWiki) repository provides a sophisticated, production-ready system for automated code documentation generation. Its modular architecture, dual-interface support, and intelligent processing make it suitable for both individual developers and enterprise teams seeking to maintain high-quality, up-to-date documentation with minimal manual effort.

For detailed information about specific modules, please refer to the individual module documentation linked throughout this overview.