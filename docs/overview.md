# AI Agent Repository Overview

## Purpose

The **ai-agent** repository implements an AI-powered coding assistant system that enables autonomous code analysis, modification, and execution within a secure, sandboxed environment. The system leverages Google's Gemini AI model to provide intelligent code assistance through both command-line and web-based interfaces, with comprehensive dependency analysis capabilities for understanding code structure and relationships.

The repository serves as a complete framework for building AI coding agents that can:
- Analyze code repositories and generate dependency graphs
- Read, write, and execute code files within defined boundaries
- Provide interactive code exploration through web and CLI interfaces
- Process GitHub repositories for automated documentation and analysis
- Manage background jobs for long-running analysis tasks
- Cache analysis results for improved performance

---

## End-to-End Architecture

### High-Level System Architecture

```mermaid
graph TB
    subgraph "User Interfaces"
        CLI[CLI Interface]
        WebUI[Web Browser]
    end
    
    subgraph "Application Layer"
        CLIModule[CLI Interface Module]
        WebFE[Web Frontend Module]
        MainApp[Main Application]
    end
    
    subgraph "Core Processing"
        DepAnalysis[Dependency Analysis Module]
        BgWorker[Background Worker]
        GitHubProc[GitHub Processor]
    end
    
    subgraph "Infrastructure"
        Config[Core Config Module]
        Utils[Utilities Module]
        Cache[Cache Manager]
    end
    
    subgraph "External Services"
        Gemini[Google Gemini AI]
        GitHub[GitHub API]
        FileSystem[File System]
    end
    
    CLI --> CLIModule
    WebUI --> WebFE
    
    CLIModule --> DepAnalysis
    CLIModule --> Config
    CLIModule --> Utils
    
    WebFE --> BgWorker
    WebFE --> GitHubProc
    WebFE --> Cache
    
    BgWorker --> DepAnalysis
    GitHubProc --> DepAnalysis
    GitHubProc --> GitHub
    
    MainApp --> Gemini
    MainApp --> Utils
    MainApp --> Config
    
    DepAnalysis --> FileSystem
    Utils --> FileSystem
    Cache --> FileSystem
    
    style CLIModule fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style WebFE fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style DepAnalysis fill:#50C878,stroke:#2E7D4E,color:#fff
    style Config fill:#F39C12,stroke:#C87F0A,color:#fff
    style Utils fill:#F39C12,stroke:#C87F0A,color:#fff
```

### Component Interaction Flow

```mermaid
sequenceDiagram
    participant User
    participant Interface as CLI/Web Interface
    participant Config as Core Config
    participant Analysis as Dependency Analysis
    participant Utils as Utilities
    participant AI as Gemini AI
    participant FS as File System
    
    User->>Interface: Submit Request
    Interface->>Config: Load Configuration
    Config-->>Interface: Settings (WORKING_DIR, MAX_CHARS, MAX_ITERS)
    
    Interface->>Analysis: Analyze Repository
    Analysis->>Utils: Read Source Files
    Utils->>Config: Validate Paths
    Config-->>Utils: Security Boundaries
    Utils->>FS: Perform File Operations
    FS-->>Utils: File Content
    Utils-->>Analysis: Parsed Data
    
    Analysis->>Analysis: Build Dependency Graph
    Analysis->>Analysis: Compute Metrics
    Analysis-->>Interface: Repository Object
    
    alt AI Agent Mode
        Interface->>AI: Generate Content
        AI-->>Interface: Function Calls
        Interface->>Utils: Execute Functions
        Utils->>FS: File Operations
        FS-->>Utils: Results
        Utils-->>Interface: Function Results
        Interface->>AI: Function Results
        AI-->>Interface: Next Action
    end
    
    Interface-->>User: Display Results
```

### Data Flow Architecture

```mermaid
flowchart TD
    Start([User Request]) --> InputType{Request Type}
    
    InputType -->|CLI Command| CLIFlow[CLI Processing]
    InputType -->|Web Request| WebFlow[Web Processing]
    InputType -->|AI Agent| AIFlow[AI Agent Loop]
    
    CLIFlow --> LoadConfig[Load Configuration]
    WebFlow --> LoadConfig
    AIFlow --> LoadConfig
    
    LoadConfig --> ValidateInput[Validate Input]
    ValidateInput --> CheckCache{Cache Available?}
    
    CheckCache -->|Yes, Hit| ReturnCached[Return Cached Result]
    CheckCache -->|No/Miss| ProcessRepo[Process Repository]
    
    ProcessRepo --> ScanFiles[Scan Source Files]
    ScanFiles --> ParseCode[Parse Code]
    ParseCode --> BuildGraph[Build Dependency Graph]
    BuildGraph --> ComputeMetrics[Compute Metrics]
    ComputeMetrics --> CreateRepo[Create Repository Object]
    
    CreateRepo --> StoreCache[Store in Cache]
    StoreCache --> FormatOutput[Format Output]
    
    ReturnCached --> FormatOutput
    FormatOutput --> End([Return Results])
    
    style LoadConfig fill:#F39C12,stroke:#C87F0A,color:#fff
    style ProcessRepo fill:#50C878,stroke:#2E7D4E,color:#fff
    style CheckCache fill:#4A90E2,stroke:#2E5C8A,color:#fff
```

### Module Dependency Graph

```mermaid
graph TB
    subgraph "Presentation Layer"
        CLI[CLI Interface Module]
        WebRoutes[Web Routes]
    end
    
    subgraph "Business Logic Layer"
        DepAnalyzer[Dependency Analysis Module]
        BgWorker[Background Worker]
        GitHubProc[GitHub Processor]
    end
    
    subgraph "Data Layer"
        CacheManager[Cache Manager]
        Models[Data Models]
    end
    
    subgraph "Infrastructure Layer"
        CoreConfig[Core Config Module]
        Utils[Utilities Module]
    end
    
    CLI --> DepAnalyzer
    CLI --> CoreConfig
    CLI --> Utils
    
    WebRoutes --> BgWorker
    WebRoutes --> GitHubProc
    WebRoutes --> CacheManager
    
    BgWorker --> DepAnalyzer
    GitHubProc --> DepAnalyzer
    GitHubProc --> Utils
    
    CacheManager --> Utils
    
    DepAnalyzer --> CoreConfig
    DepAnalyzer --> Utils
    
    BgWorker --> Models
    CacheManager --> Models
    
    style CLI fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style WebRoutes fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style DepAnalyzer fill:#50C878,stroke:#2E7D4E,color:#fff
    style CoreConfig fill:#F39C12,stroke:#C87F0A,color:#fff
    style Utils fill:#F39C12,stroke:#C87F0A,color:#fff
```

---

## Core Modules Documentation

The ai-agent repository is organized into five core modules, each serving a specific purpose in the system architecture:

### 1. [CLI Interface Module](cli_interface.md)
**Location:** `codewiki/cli`

Provides the command-line interface for interacting with the CodeWiki system, enabling users to analyze repositories, manage configuration, and track progress through terminal commands.

**Key Components:**
- `Configuration` - CLI configuration management
- `ModuleProgressBar` - Visual progress tracking for terminal

**Primary Use Cases:**
- Command-line repository analysis
- Configuration management via CLI
- Progress monitoring for long-running operations
- Integration with CI/CD pipelines

---

### 2. [Dependency Analysis Module](dependency_analysis.md)
**Location:** `codewiki/src/be/dependency_analyzer`

The core analytical engine that processes source code repositories to extract structural information, build dependency graphs, and compute code metrics.

**Key Components:**
- `Repository` - Complete repository structure representation
- `Node` - Individual code component (class, function, module)
- `NodeSelection` - Filtered subset of nodes for focused analysis

**Primary Use Cases:**
- Code dependency graph generation
- Circular dependency detection
- Code structure analysis
- Dependency metrics computation
- Multi-language code parsing

---

### 3. [Web Frontend Module](web_frontend.md)
**Location:** `codewiki/src/fe`

Provides the web-based user interface and API layer, enabling browser-based interaction with the code analysis system through RESTful endpoints and asynchronous job processing.

**Key Components:**
- `WebRoutes` - HTTP routing and API endpoints
- `BackgroundWorker` - Asynchronous job processing
- `CacheManager` - Result caching and optimization
- `GitHubRepoProcessor` - GitHub integration
- `WebAppConfig` - Web application configuration
- `JobStatus` - Job tracking and progress
- `CacheEntry` - Cache entry management
- `RepositorySubmission` - Repository submission handling

**Primary Use Cases:**
- Web-based code exploration
- GitHub repository analysis
- Asynchronous job processing
- Result caching and retrieval
- API-based integrations

---

### 4. [Core Config Module](core_config.md)
**Location:** `codewiki/src/config.py`

Central configuration hub that defines runtime parameters, security boundaries, and operational constraints for the entire system.

**Key Components:**
- `Config` - Configuration management class

**Configuration Parameters:**
- `MAX_CHARS` - Maximum file read size (default: 10,000 characters)
- `WORKING_DIR` - Sandboxed working directory (default: "./calculator")
- `MAX_ITERS` - Maximum AI agent iterations (default: 20)

**Primary Use Cases:**
- Security boundary enforcement
- Resource limit management
- Environment-specific configuration
- System-wide parameter control

---

### 5. [Utilities Module](utilities.md)
**Location:** `codewiki/src/utils.py`

Provides secure, sandboxed file system operations that enable the AI agent to interact with code files while maintaining strict security boundaries.

**Key Components:**
- `FileManager` - File system operations manager

**Core Functions:**
- `get_files_info` - Directory listing with file metadata
- `get_file_content` - Secure file reading with size limits
- `write_file` - File writing with directory creation
- `run_python_file` - Python script execution with timeout

**Primary Use Cases:**
- Secure file system access
- Code file reading and writing
- Python script execution
- Directory exploration
- Path validation and sandboxing

---

## System Integration

### Configuration Flow

```mermaid
graph LR
    EnvVars[Environment Variables] --> CoreConfig[Core Config]
    ConfigFiles[Config Files] --> CoreConfig
    Defaults[System Defaults] --> CoreConfig
    
    CoreConfig --> CLIConfig[CLI Configuration]
    CoreConfig --> WebConfig[Web App Config]
    CoreConfig --> AnalysisConfig[Analysis Config]
    
    CLIConfig --> CLIModule[CLI Interface]
    WebConfig --> WebFE[Web Frontend]
    AnalysisConfig --> DepAnalysis[Dependency Analysis]
    
    style CoreConfig fill:#F39C12,stroke:#C87F0A,color:#fff
```

### Security Architecture

```mermaid
graph TB
    subgraph "Security Layers"
        Input[User Input] --> PathValidation[Path Validation]
        PathValidation --> SandboxCheck{Within WORKING_DIR?}
        
        SandboxCheck -->|No| Reject[Reject Access]
        SandboxCheck -->|Yes| ResourceCheck[Resource Limits]
        
        ResourceCheck --> SizeCheck{Size < MAX_CHARS?}
        ResourceCheck --> TimeCheck{Time < Timeout?}
        ResourceCheck --> IterCheck{Iterations < MAX_ITERS?}
        
        SizeCheck -->|Yes| Execute[Execute Operation]
        TimeCheck -->|Yes| Execute
        IterCheck -->|Yes| Execute
        
        SizeCheck -->|No| Truncate[Truncate/Limit]
        TimeCheck -->|No| Timeout[Timeout Error]
        IterCheck -->|No| MaxIters[Max Iterations Error]
        
        Execute --> Result[Return Result]
        Truncate --> Result
    end
    
    style SandboxCheck fill:#FFB74D,stroke:#F57C00,color:#fff
    style Reject fill:#E74C3C,stroke:#C0392B,color:#fff
    style Execute fill:#50C878,stroke:#2E7D4E,color:#fff
```

---

## Getting Started

### Quick Start Guide

1. **Installation**
   ```bash
   git clone <repository-url>
   cd ai-agent
   pip install -r requirements.txt
   ```

2. **Configuration**
   ```python
   # Edit codewiki/src/config.py
   MAX_CHARS = 10000
   WORKING_DIR = "./your-project"
   MAX_ITERS = 20
   ```

3. **CLI Usage**
   ```bash
   # Analyze a repository
   python -m codewiki.cli analyze ./path/to/repo
   
   # View configuration
   python -m codewiki.cli config list
   ```

4. **Web Interface**
   ```bash
   # Start web server
   python -m codewiki.src.fe.app
   
   # Access at http://localhost:5000
   ```

### Module Navigation

- **For CLI users**: Start with [CLI Interface Module](cli_interface.md)
- **For web developers**: Start with [Web Frontend Module](web_frontend.md)
- **For code analysis**: Start with [Dependency Analysis Module](dependency_analysis.md)
- **For configuration**: Start with [Core Config Module](core_config.md)
- **For file operations**: Start with [Utilities Module](utilities.md)

---

## Key Features

### 🔍 Code Analysis
- Multi-language dependency analysis
- Circular dependency detection
- Code metrics computation
- Dependency graph visualization

### 🌐 Web Interface
- RESTful API endpoints
- Asynchronous job processing
- GitHub repository integration
- Intelligent result caching

### 🖥️ CLI Interface
- Command-line repository analysis
- Configuration management
- Progress tracking
- Batch processing support

### 🔒 Security
- Sandboxed file operations
- Path traversal prevention
- Resource consumption limits
- Execution timeouts

### ⚡ Performance
- Multi-tier caching
- Parallel processing
- Incremental analysis
- Background job queuing

---

## Architecture Highlights

### Modular Design
Each module has clear responsibilities and well-defined interfaces, enabling independent development and testing.

### Security-First Approach
All file operations are validated against security boundaries, preventing unauthorized access and resource exhaustion.

### Scalable Architecture
Stateless API design and background job processing enable horizontal scaling for production deployments.

### AI Integration
Seamless integration with Google Gemini AI for intelligent code assistance and automated decision-making.

### Extensible Framework
Plugin-friendly architecture allows easy addition of new languages, analysis types, and integration points.

---

## Documentation Structure

Each core module includes comprehensive documentation covering:
- **Architecture**: Component design and interaction patterns
- **Core Components**: Detailed component specifications
- **Integration Points**: How modules interact with each other
- **Data Flow**: Request/response patterns and data transformations
- **Usage Examples**: Practical code examples and workflows
- **Best Practices**: Guidelines for effective usage
- **Security Considerations**: Security features and recommendations

---

## Contributing

For detailed information about each module's implementation, please refer to the individual module documentation linked above. Each document provides in-depth coverage of architecture, components, and usage patterns specific to that module.