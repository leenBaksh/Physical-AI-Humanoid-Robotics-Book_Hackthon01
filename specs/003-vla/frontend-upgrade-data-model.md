# Data Model: Docusaurus Frontend Upgrade

## Entities

### 1. Documentation Module
- **Name**: Module identifier (e.g., "Module 1: ROS 2 Fundamentals")
- **Description**: High-level grouping of related content
- **Fields**:
  - id: string (unique identifier)
  - title: string (display title)
  - description: string (brief overview)
  - chapters: array of Chapter entities
  - order: integer (sequence in curriculum)
  - prerequisites: array of Module IDs
- **Relationships**: Contains multiple Chapters

### 2. Documentation Chapter
- **Name**: Chapter identifier (e.g., "Chapter 1: Voice-to-Action with Whisper")
- **Description**: Detailed section within a module
- **Fields**:
  - id: string (unique identifier)
  - title: string (display title)
  - content: string (main content in markdown)
  - module_id: string (parent module)
  - order: integer (sequence within module)
  - learning_objectives: array of strings
  - prerequisites: array of Chapter IDs
- **Relationships**: Belongs to one Module, contains multiple Content Sections

### 3. Content Section
- **Name**: Section within a chapter
- **Description**: Individual content block with specific focus
- **Fields**:
  - id: string (unique identifier)
  - title: string (section heading)
  - content: string (content in markdown)
  - chapter_id: string (parent chapter)
  - order: integer (sequence within chapter)
  - type: enum ("text", "code", "diagram", "exercise", "example")
- **Relationships**: Belongs to one Chapter

### 4. UI Component
- **Name**: Frontend UI element
- **Description**: Reusable interface component for documentation site
- **Fields**:
  - id: string (unique identifier)
  - name: string (component name)
  - type: enum ("sidebar", "navbar", "content", "search", "footer")
  - properties: object (configuration options)
  - styling: object (CSS/SCSS definitions)
  - responsive_behavior: object (mobile/tablet/desktop behavior)
- **Relationships**: Used by multiple Pages

### 5. Theme Configuration
- **Name**: Theme settings and options
- **Description**: Configuration for visual appearance and behavior
- **Fields**:
  - id: string (unique identifier)
  - name: string (theme name)
  - colors: object (color palette)
  - typography: object (font settings)
  - layout: object (spacing and structure)
  - dark_mode: boolean (support for dark theme)
  - accessibility: object (accessibility settings)
- **Relationships**: Applied to all Pages

### 6. Asset
- **Name**: Static resource
- **Description**: Images, videos, documents, or other static files
- **Fields**:
  - id: string (unique identifier)
  - filename: string (original file name)
  - path: string (relative path from assets folder)
  - type: enum ("image", "video", "document", "other")
  - optimized: boolean (whether optimized for web)
  - alt_text: string (accessibility description for images)
  - size: integer (file size in bytes)
- **Relationships**: Referenced by multiple Content Sections

### 7. Navigation Item
- **Name**: Navigation element
- **Description**: Item in sidebar or other navigation structure
- **Fields**:
  - id: string (unique identifier)
  - title: string (display text)
  - path: string (URL path)
  - parent_id: string (parent navigation item, if any)
  - order: integer (position in navigation)
  - icon: string (icon identifier, optional)
  - collapsed: boolean (initial collapsed state for groups)
- **Relationships**: Forms hierarchical structure

## State Transitions

### Documentation Module State Transitions
- draft → review → approved → published
- published → archived (for deprecated modules)

### Content Section State Transitions
- created → draft → review → approved → published
- published → updated → review → approved → published (new version)

## Validation Rules

### Module Validation
- Title must be 3-100 characters
- Must have at least one chapter
- Order must be a positive integer
- ID must be unique across all modules

### Chapter Validation
- Title must be 3-100 characters
- Must belong to a valid module
- Order must be a positive integer within module
- Content must be valid markdown

### Content Section Validation
- Title must be 1-100 characters
- Must belong to a valid chapter
- Type must be one of the defined enum values
- Content length must be appropriate for type

### UI Component Validation
- Name must follow component naming conventions
- Properties must match expected schema for component type
- Styling must use approved CSS patterns
- Must be responsive across all device sizes

### Asset Validation
- File type must be in approved list
- File size must be under specified limits
- Alt text required for images
- Path must be properly formatted

## Relationships

### Hierarchical Relationships
- Module (1) → (Many) Chapter
- Chapter (1) → (Many) Content Section
- Navigation Item (1) → (Many) Child Navigation Items

### Reference Relationships
- Content Section (Many) → (Many) Assets (via content references)
- UI Component (Many) → (Many) Pages (via usage)

### Dependency Relationships
- Module (Many) → (Many) Prerequisite Modules
- Chapter (Many) → (Many) Prerequisite Chapters