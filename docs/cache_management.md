# Cache Management Module

## Overview

The **cache_management** module is a critical component of the CodeWiki web application that manages the caching of generated documentation results. It provides efficient storage, retrieval, and lifecycle management of documentation artifacts to minimize redundant processing and improve response times for frequently accessed repositories.

This module implements a hash-based caching system with automatic expiration, persistence, and cleanup capabilities, ensuring optimal resource utilization while maintaining data freshness.

---

## Table of Contents

- [Architecture](#architecture)
- [Core Components](#core-components)
- [Cache Management System](#cache-management-system)
- [Data Flow](#data-flow)
- [Cache Lifecycle](#cache-lifecycle)
- [Integration Points](#integration-points)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Performance Considerations](#performance-considerations)
- [Error Handling](#error-handling)

---

## Architecture

### System Context

```mermaid
graph TB
    subgraph "Web Application Layer"
        WR[Web Routes]
        BW[Background Worker]
        GP[GitHub Processor]
    end
    
    subgraph "Cache Management Module"
        CM[CacheManager]
        CI[Cache Index]
        CE[Cache Entries]
    end
    
    subgraph "Storage Layer"
        FS[File System]
        IDX[cache_index.json]
        DOCS[Documentation Files]
    end
    
    subgraph "Configuration"
        WAC[WebAppConfig]
        FM[FileManager]
    end
    
    WR -->|Check Cache| CM
    BW -->|Store Results| CM
    GP -->|Retrieve Cached| CM
    
    CM -->|Read/Write| CI
    CM -->|Manage| CE
    CM -->|Uses| WAC
    CM -->|File Operations| FM
    
    CI -->|Persist| IDX
    CE -->|Reference| DOCS
    
    IDX -.->|Stored in| FS
    DOCS -.->|Stored in| FS
    
    style CM fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style CI fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
    style CE fill:#2196F3,stroke:#1565C0,stroke-width:2px,color:#fff
```

### Module Dependencies

```mermaid
graph LR
    subgraph "cache_management"
        CM[CacheManager]
    end
    
    subgraph "data_models"
        CE[CacheEntry]
    end
    
    subgraph "configuration_management"
        WAC[WebAppConfig]
    end
    
    subgraph "shared_utilities"
        FM[FileManager]
    end
    
    subgraph "External Libraries"
        PL[pathlib.Path]
        HL[hashlib]
        DT[datetime]
    end
    
    CM -->|Uses Model| CE
    CM -->|Reads Config| WAC
    CM -->|File I/O| FM
    CM -->|Path Operations| PL
    CM -->|Hash Generation| HL
    CM -->|Time Management| DT
    
    style CM fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    
    click CE "data_models.md"
    click WAC "configuration_management.md"
    click FM "shared_utilities.md"
```

---

## Core Components

### CacheManager

The `CacheManager` class is the central component responsible for all cache operations.

**Key Responsibilities:**
- **Cache Storage**: Persist documentation results with metadata
- **Cache Retrieval**: Quickly locate and return cached documentation
- **Expiration Management**: Automatically invalidate stale cache entries
- **Index Persistence**: Maintain a searchable index of all cached items
- **Hash Generation**: Create unique identifiers for repository URLs
- **Cleanup Operations**: Remove expired entries to free resources

**Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| `cache_dir` | `Path` | Directory where cache files are stored |
| `cache_expiry_days` | `int` | Number of days before cache entries expire |
| `cache_index` | `Dict[str, CacheEntry]` | In-memory index of all cache entries |

**Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `cache_dir: str`, `cache_expiry_days: int` | - | Initialize cache manager with configuration |
| `load_cache_index` | - | `None` | Load cache index from persistent storage |
| `save_cache_index` | - | `None` | Save cache index to persistent storage |
| `get_repo_hash` | `repo_url: str` | `str` | Generate unique hash for repository URL |
| `get_cached_docs` | `repo_url: str` | `Optional[str]` | Retrieve cached documentation path |
| `add_to_cache` | `repo_url: str`, `docs_path: str` | `None` | Add new documentation to cache |
| `remove_from_cache` | `repo_url: str` | `None` | Remove documentation from cache |
| `cleanup_expired_cache` | - | `None` | Remove all expired cache entries |

---

## Cache Management System

### Hash-Based Indexing

The cache system uses SHA-256 hashing to create unique, deterministic identifiers for repository URLs:

```mermaid
graph LR
    A[Repository URL] -->|SHA-256| B[Full Hash]
    B -->|Truncate to 16 chars| C[Repo Hash]
    C -->|Index Key| D[Cache Entry]
    
    style C fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
```

**Hash Generation Process:**
1. Repository URL is encoded to bytes
2. SHA-256 hash is computed
3. Hash is truncated to first 16 hexadecimal characters
4. Result is used as cache index key

**Benefits:**
- **Deterministic**: Same URL always produces same hash
- **Collision-Resistant**: SHA-256 provides strong uniqueness guarantees
- **Compact**: 16-character keys are efficient for storage and lookup
- **URL-Safe**: Hash contains only hexadecimal characters

### Cache Index Structure

```mermaid
erDiagram
    CACHE_INDEX ||--o{ CACHE_ENTRY : contains
    
    CACHE_INDEX {
        string index_file_path
        dict entries
    }
    
    CACHE_ENTRY {
        string repo_url
        string repo_url_hash
        string docs_path
        datetime created_at
        datetime last_accessed
    }
```

The cache index is a JSON file (`cache_index.json`) that maps repository hashes to cache entry metadata:

```json
{
  "a1b2c3d4e5f6g7h8": {
    "repo_url": "https://github.com/user/repo",
    "repo_url_hash": "a1b2c3d4e5f6g7h8",
    "docs_path": "./output/cache/a1b2c3d4e5f6g7h8/docs",
    "created_at": "2024-01-15T10:30:00",
    "last_accessed": "2024-01-20T14:45:00"
  }
}
```

---

## Data Flow

### Cache Write Operation

```mermaid
sequenceDiagram
    participant BW as Background Worker
    participant CM as CacheManager
    participant CE as CacheEntry
    participant FS as File System
    
    BW->>CM: add_to_cache(repo_url, docs_path)
    CM->>CM: get_repo_hash(repo_url)
    CM->>CE: Create CacheEntry
    Note over CE: repo_url, hash, docs_path<br/>created_at, last_accessed
    CM->>CM: cache_index[hash] = entry
    CM->>CM: save_cache_index()
    CM->>FS: Write cache_index.json
    FS-->>CM: Success
    CM-->>BW: Cache updated
```

### Cache Read Operation

```mermaid
sequenceDiagram
    participant WR as Web Routes
    participant CM as CacheManager
    participant CE as CacheEntry
    participant FS as File System
    
    WR->>CM: get_cached_docs(repo_url)
    CM->>CM: get_repo_hash(repo_url)
    CM->>CM: Lookup in cache_index
    
    alt Cache Hit
        CM->>CE: Get entry
        CM->>CM: Check expiration
        
        alt Not Expired
            CM->>CE: Update last_accessed
            CM->>FS: Save cache_index.json
            CM-->>WR: Return docs_path
        else Expired
            CM->>CM: remove_from_cache(repo_url)
            CM-->>WR: Return None
        end
    else Cache Miss
        CM-->>WR: Return None
    end
```

### Cache Cleanup Operation

```mermaid
sequenceDiagram
    participant SYS as System/Scheduler
    participant CM as CacheManager
    participant CI as Cache Index
    participant FS as File System
    
    SYS->>CM: cleanup_expired_cache()
    CM->>CM: Calculate cutoff date
    Note over CM: now - cache_expiry_days
    
    loop For each entry
        CM->>CI: Check created_at
        alt Expired
            CM->>CM: Add to expired_entries list
        end
    end
    
    loop For each expired entry
        CM->>CI: Delete from cache_index
    end
    
    alt Has expired entries
        CM->>FS: Save updated cache_index.json
        FS-->>CM: Success
    end
    
    CM-->>SYS: Cleanup complete
```

---

## Cache Lifecycle

### Entry States and Transitions

```mermaid
stateDiagram-v2
    [*] --> Creating: add_to_cache()
    Creating --> Active: Entry created
    Active --> Accessed: get_cached_docs()
    Accessed --> Active: Update last_accessed
    Active --> Expired: Time > expiry_days
    Expired --> Removed: cleanup_expired_cache()
    Active --> Removed: remove_from_cache()
    Removed --> [*]
    
    note right of Active
        Valid cache entry
        Available for retrieval
    end note
    
    note right of Expired
        Created_at exceeds
        cache_expiry_days
    end note
```

### Cache Entry Lifecycle Timeline

```mermaid
gantt
    title Cache Entry Lifecycle (365 days expiry)
    dateFormat YYYY-MM-DD
    section Cache Entry
    Created           :milestone, m1, 2024-01-01, 0d
    Active Period     :active, a1, 2024-01-01, 365d
    Accessed (Day 30) :milestone, m2, 2024-01-30, 0d
    Accessed (Day 180):milestone, m3, 2024-06-29, 0d
    Expiration Date   :milestone, m4, 2024-12-31, 0d
    Expired State     :crit, e1, 2024-12-31, 7d
    Cleanup/Removal   :milestone, m5, 2025-01-07, 0d
```

---

## Integration Points

### Integration with Web Application Components

```mermaid
graph TB
    subgraph "Request Flow"
        REQ[HTTP Request]
        WR[Web Routes]
    end
    
    subgraph "Cache Management"
        CM[CacheManager]
        CHK{Cache Hit?}
    end
    
    subgraph "Processing Pipeline"
        BW[Background Worker]
        GP[GitHub Processor]
        DG[Doc Generator]
    end
    
    subgraph "Response"
        CACHED[Cached Docs]
        FRESH[Fresh Docs]
    end
    
    REQ --> WR
    WR --> CM
    CM --> CHK
    
    CHK -->|Yes| CACHED
    CHK -->|No| BW
    
    BW --> GP
    GP --> DG
    DG --> CM
    CM --> FRESH
    
    CACHED --> WR
    FRESH --> WR
    
    style CM fill:#4CAF50,stroke:#2E7D32,stroke-width:3px,color:#fff
    style CHK fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    
    click WR "web_routes_api.md"
    click BW "background_processing.md"
    click GP "github_integration.md"
```

### Component Interaction Flow

```mermaid
sequenceDiagram
    participant User
    participant WebRoutes
    participant CacheManager
    participant BackgroundWorker
    participant GitHubProcessor
    
    User->>WebRoutes: Request docs for repo
    WebRoutes->>CacheManager: get_cached_docs(repo_url)
    
    alt Cache Hit (Valid)
        CacheManager-->>WebRoutes: docs_path
        WebRoutes-->>User: Serve cached docs
    else Cache Miss
        CacheManager-->>WebRoutes: None
        WebRoutes->>BackgroundWorker: Queue job
        BackgroundWorker->>GitHubProcessor: Process repo
        GitHubProcessor->>GitHubProcessor: Generate docs
        GitHubProcessor->>CacheManager: add_to_cache(repo_url, docs_path)
        CacheManager-->>GitHubProcessor: Cached
        GitHubProcessor-->>BackgroundWorker: Complete
        BackgroundWorker-->>User: Docs ready (via polling/webhook)
    end
```

---

## Configuration

### Configuration Parameters

The cache management module relies on configuration from [WebAppConfig](configuration_management.md):

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| `CACHE_DIR` | `"./output/cache"` | Directory for storing cache files |
| `CACHE_EXPIRY_DAYS` | `365` | Number of days before cache expires |

### Directory Structure

```
output/
├── cache/
│   ├── cache_index.json          # Cache metadata index
│   ├── a1b2c3d4e5f6g7h8/         # Cached repo (hash-based)
│   │   └── docs/                  # Generated documentation
│   ├── 9z8y7x6w5v4u3t2s/
│   │   └── docs/
│   └── ...
├── temp/                          # Temporary processing files
└── ...
```

### Initialization

```python
# Default initialization (uses WebAppConfig)
cache_manager = CacheManager()

# Custom configuration
cache_manager = CacheManager(
    cache_dir="./custom/cache",
    cache_expiry_days=180
)
```

---

## Usage Examples

### Basic Cache Operations

#### Adding Documentation to Cache

```python
from codewiki.src.fe.cache_manager import CacheManager

# Initialize cache manager
cache_manager = CacheManager()

# Add generated documentation to cache
repo_url = "https://github.com/user/awesome-project"
docs_path = "./output/cache/a1b2c3d4e5f6g7h8/docs"

cache_manager.add_to_cache(repo_url, docs_path)
print(f"Documentation cached for {repo_url}")
```

#### Retrieving Cached Documentation

```python
# Check if documentation is cached
repo_url = "https://github.com/user/awesome-project"
cached_path = cache_manager.get_cached_docs(repo_url)

if cached_path:
    print(f"Cache hit! Documentation at: {cached_path}")
    # Serve documentation from cached_path
else:
    print("Cache miss. Need to generate documentation.")
    # Trigger documentation generation
```

#### Manual Cache Removal

```python
# Remove specific repository from cache
repo_url = "https://github.com/user/old-project"
cache_manager.remove_from_cache(repo_url)
print(f"Cache cleared for {repo_url}")
```

#### Cleanup Expired Entries

```python
# Remove all expired cache entries
cache_manager.cleanup_expired_cache()
print("Expired cache entries removed")
```

### Advanced Usage Patterns

#### Cache-First Request Handler

```python
from codewiki.src.fe.cache_manager import CacheManager
from codewiki.src.fe.background_worker import BackgroundWorker

def handle_documentation_request(repo_url: str):
    """Handle documentation request with cache-first strategy."""
    cache_manager = CacheManager()
    
    # Try cache first
    cached_docs = cache_manager.get_cached_docs(repo_url)
    
    if cached_docs:
        return {
            "status": "ready",
            "source": "cache",
            "docs_path": cached_docs
        }
    
    # Cache miss - queue for processing
    background_worker = BackgroundWorker()
    job_id = background_worker.submit_job(repo_url)
    
    return {
        "status": "processing",
        "source": "fresh",
        "job_id": job_id
    }
```

#### Scheduled Cache Maintenance

```python
import schedule
import time

def scheduled_cache_cleanup():
    """Perform scheduled cache cleanup."""
    cache_manager = CacheManager()
    
    print("Starting cache cleanup...")
    initial_count = len(cache_manager.cache_index)
    
    cache_manager.cleanup_expired_cache()
    
    final_count = len(cache_manager.cache_index)
    removed = initial_count - final_count
    
    print(f"Cleanup complete. Removed {removed} expired entries.")
    print(f"Active cache entries: {final_count}")

# Schedule cleanup daily at 2 AM
schedule.every().day.at("02:00").do(scheduled_cache_cleanup)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(60)
```

#### Cache Statistics

```python
from datetime import datetime, timedelta

def get_cache_statistics(cache_manager: CacheManager):
    """Generate cache usage statistics."""
    total_entries = len(cache_manager.cache_index)
    
    now = datetime.now()
    cutoff = now - timedelta(days=cache_manager.cache_expiry_days)
    
    active_entries = 0
    expired_entries = 0
    recently_accessed = 0
    
    for entry in cache_manager.cache_index.values():
        if entry.created_at >= cutoff:
            active_entries += 1
        else:
            expired_entries += 1
        
        if entry.last_accessed >= now - timedelta(days=7):
            recently_accessed += 1
    
    return {
        "total_entries": total_entries,
        "active_entries": active_entries,
        "expired_entries": expired_entries,
        "recently_accessed_7d": recently_accessed,
        "cache_hit_potential": f"{(active_entries/total_entries*100):.1f}%" if total_entries > 0 else "0%"
    }

# Usage
cache_manager = CacheManager()
stats = get_cache_statistics(cache_manager)
print(f"Cache Statistics: {stats}")
```

---

## Performance Considerations

### Optimization Strategies

```mermaid
graph LR
    subgraph Optimizations["Performance Optimizations"]
        A[In-Memory Index]
        B[Hash-Based Lookup]
        C[Lazy Loading]
        D[Batch Operations]
    end
    
    subgraph Benefits["Benefits"]
        A1[O1 Lookup Time]
        B1[Fast Key Generation]
        C1[Reduced I/O]
        D1[Efficient Cleanup]
    end
    
    A --> A1
    B --> B1
    C --> C1
    D --> D1
    
    style A fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style B fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style C fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style D fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
```

### Performance Characteristics

| Operation | Time Complexity | Space Complexity | Notes |
|-----------|----------------|------------------|-------|
| `get_cached_docs()` | O(1) | O(1) | Hash-based dictionary lookup |
| `add_to_cache()` | O(1) + I/O | O(1) | Dictionary insert + file write |
| `remove_from_cache()` | O(1) + I/O | O(1) | Dictionary delete + file write |
| `cleanup_expired_cache()` | O(n) + I/O | O(n) | Iterate all entries + file write |
| `load_cache_index()` | O(n) + I/O | O(n) | Load and parse JSON file |
| `get_repo_hash()` | O(m) | O(1) | m = length of repo URL |

### Memory Management

**In-Memory Index:**
- Cache index is loaded into memory on initialization
- Provides fast O(1) lookups without disk I/O
- Memory usage scales linearly with number of cached repositories
- Estimated: ~500 bytes per cache entry

**Disk Persistence:**
- Index is persisted to `cache_index.json` after modifications
- Documentation files remain on disk
- Only metadata is kept in memory

### Scalability Considerations

```mermaid
graph LR
    subgraph "Small Scale (< 100 repos)"
        S1[In-Memory Index]
        S2[Single JSON File]
        S3[Simple Cleanup]
    end
    
    subgraph "Medium Scale (100-1000 repos)"
        M1[In-Memory Index]
        M2[Partitioned Storage]
        M3[Scheduled Cleanup]
    end
    
    subgraph "Large Scale (> 1000 repos)"
        L1[Database Index]
        L2[Distributed Storage]
        L3[Background Cleanup]
    end
    
    S1 --> M1
    S2 --> M2
    S3 --> M3
    
    M1 -.->|Consider| L1
    M2 -.->|Consider| L2
    M3 -.->|Consider| L3
    
    style S1 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style M1 fill:#FF9800,stroke:#E65100,stroke-width:2px,color:#fff
    style L1 fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
```

**Recommendations:**
- **< 100 repositories**: Current implementation is optimal
- **100-1000 repositories**: Consider partitioning cache index by hash prefix
- **> 1000 repositories**: Consider migrating to database-backed cache (Redis, SQLite)

---

## Error Handling

### Error Scenarios and Recovery

```mermaid
graph TB
    subgraph "Error Types"
        E1[Index Load Failure]
        E2[Index Save Failure]
        E3[Corrupted Index]
        E4[Missing Cache Files]
    end
    
    subgraph "Recovery Strategies"
        R1[Initialize Empty Index]
        R2[Log Error, Continue]
        R3[Rebuild from Disk]
        R4[Remove Invalid Entries]
    end
    
    E1 --> R1
    E2 --> R2
    E3 --> R3
    E4 --> R4
    
    style E1 fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style E2 fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style E3 fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    style E4 fill:#F44336,stroke:#C62828,stroke-width:2px,color:#fff
    
    style R1 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style R2 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style R3 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
    style R4 fill:#4CAF50,stroke:#2E7D32,stroke-width:2px,color:#fff
```

### Error Handling Implementation

#### Index Load Errors

```python
def load_cache_index(self):
    """Load cache index from disk."""
    index_file = self.cache_dir / "cache_index.json"
    if index_file.exists():
        try:
            data = file_manager.load_json(index_file)
            for key, value in data.items():
                self.cache_index[key] = CacheEntry(...)
        except Exception as e:
            # Graceful degradation: start with empty index
            print(f"Error loading cache index: {e}")
            self.cache_index = {}
```

**Recovery Strategy:**
- Log error for debugging
- Initialize with empty cache index
- System continues to function (cache misses until rebuilt)

#### Index Save Errors

```python
def save_cache_index(self):
    """Save cache index to disk."""
    index_file = self.cache_dir / "cache_index.json"
    try:
        data = {...}
        file_manager.save_json(data, index_file)
    except Exception as e:
        # Log error but don't crash
        print(f"Error saving cache index: {e}")
```

**Recovery Strategy:**
- Log error for monitoring
- In-memory index remains intact
- Next successful save will persist changes

### Defensive Programming Patterns

```python
def get_cached_docs(self, repo_url: str) -> Optional[str]:
    """Get cached documentation path if available."""
    try:
        repo_hash = self.get_repo_hash(repo_url)
        
        if repo_hash in self.cache_index:
            entry = self.cache_index[repo_hash]
            
            # Verify cache file still exists
            if not Path(entry.docs_path).exists():
                self.remove_from_cache(repo_url)
                return None
            
            # Check expiration
            if datetime.now() - entry.created_at < timedelta(days=self.cache_expiry_days):
                entry.last_accessed = datetime.now()
                self.save_cache_index()
                return entry.docs_path
            else:
                self.remove_from_cache(repo_url)
        
        return None
    except Exception as e:
        print(f"Error retrieving cached docs: {e}")
        return None  # Fail gracefully
```

---

## Related Documentation

- **[configuration_management](configuration_management.md)**: WebAppConfig settings and directory management
- **[data_models](data_models.md)**: CacheEntry model structure and validation
- **[web_routes_api](web_routes_api.md)**: HTTP endpoints that utilize cache
- **[background_processing](background_processing.md)**: Job processing and cache population
- **[github_integration](github_integration.md)**: Repository processing and documentation generation
- **[shared_utilities](shared_utilities.md)**: FileManager for JSON persistence

---

## Summary

The **cache_management** module provides a robust, efficient caching layer for the CodeWiki web application. Key features include:

✅ **Hash-based indexing** for fast O(1) lookups  
✅ **Automatic expiration** with configurable TTL  
✅ **Persistent storage** with JSON-based index  
✅ **Graceful error handling** with degradation strategies  
✅ **Memory-efficient** in-memory index design  
✅ **Cleanup utilities** for resource management  
✅ **Integration-ready** with web application components  

The module balances performance, reliability, and simplicity, making it suitable for small to medium-scale deployments while providing clear paths for scaling to larger workloads.
