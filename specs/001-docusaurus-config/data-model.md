# Data Model: Docusaurus Configuration for Physical AI & Humanoid Robotics

## Docusaurus Configuration Structure

### SiteConfig
- **title**: String (e.g., "Physical AI & Humanoid Robotics")
- **tagline**: String (e.g., "A comprehensive guide to robotics and AI integration")
- **favicon**: String (path to favicon file)
- **url**: String (base URL for the site)
- **baseUrl**: String (base path for the site)
- **organizationName**: String (GitHub organization name for deployment)
- **projectName**: String (GitHub project name for deployment)
- **onBrokenLinks**: String (how to handle broken links: "throw", "warn", "ignore")
- **onBrokenMarkdownLinks**: String (how to handle broken markdown links)
- **i18n**: Object (internationalization settings)

### NavbarConfig
- **title**: String (displayed title in navbar)
- **logo**: Object (logo configuration with alt and src)
- **items**: Array of NavbarItem objects
- **hideOnScroll**: Boolean (whether to hide navbar on scroll)

### NavbarItem
- **type**: String ("doc", "docsVersion", "link", "localeDropdown", "search", "theme", "custom")
- **position**: String ("left", "right") for positioning in navbar
- **label**: String (displayed text for the item)
- **to**: String (URL path for internal links)
- **href**: String (URL for external links)
- **docId**: String (document ID for doc type items)

### FooterConfig
- **style**: String ("dark", "light") for footer theme
- **links**: Array of FooterLink objects
- **copyright**: String (copyright text displayed in footer)

### FooterLink
- **title**: String (section title in footer)
- **items**: Array of FooterLinkItem objects

### FooterLinkItem
- **label**: String (displayed text for the link)
- **to**: String (URL path for the link)

### PrismConfig
- **theme**: Object (prism theme for light mode)
- **darkTheme**: Object (prism theme for dark mode)
- **additionalLanguages**: Array of String (additional syntax highlighting languages)

## Book Structure

### Module
- **name**: String (e.g., "Module 1: ROS 2")
- **description**: String (overview of module content)
- **chapters**: Array of Chapter objects
- **sidebarId**: String (ID of the sidebar for this module)

### Chapter
- **title**: String (e.g., "ROS 2 Core – Nodes, Topics, & Services")
- **description**: String (overview of chapter content)
- **sections**: Array of Section objects
- **files**: Array of String (file paths for chapter content)

### Section
- **title**: String (e.g., "Publisher-Subscriber Patterns")
- **content**: String (path to content file)
- **prerequisites**: Array of String (what reader should know)
- **learning_objectives**: Array of String (what reader will learn)

## Content Files

### MarkdownFile
- **path**: String (relative path from docs/ directory)
- **frontmatter**: Object (YAML frontmatter with metadata)
- **content**: String (markdown content)
- **sidebar_position**: Number (position in sidebar navigation)

### Frontmatter
- **title**: String (page title)
- **sidebar_label**: String (label to display in sidebar)
- **sidebar_position**: Number (position in sidebar)
- **description**: String (page description for SEO)

## Deployment Configuration

### GitHubPagesConfig
- **organizationName**: String (GitHub organization/user name)
- **projectName**: String (Repository name for GitHub Pages)
- **deployment_branch**: String (Branch for deployment, typically gh-pages)
- **build_script**: String (Script to run during build)
- **output_dir**: String (Directory containing built site)