# Quickstart Guide: Docusaurus Frontend Upgrade

## Overview
This guide provides a quick path to upgrade the frontend_robotic_book Docusaurus project with modern UI and improved content structure. Follow these steps to get the upgraded site running quickly.

## Prerequisites
- Node.js (v18 or higher)
- npm or yarn package manager
- Git for version control
- Basic knowledge of React and Docusaurus

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
cd D:\Physical-AI---Humanoid-Robotics\frontend_robotic_book
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Update Docusaurus to Latest Version
```bash
npm update @docusaurus/core @docusaurus/preset-classic
```

### 4. Verify Current Setup
```bash
npm run start
```

## Upgrade Process

### 1. Apply Theme Customization
1. Update `docusaurus.config.js` with new theme settings
2. Add custom CSS in `src/css/custom.css`
3. Configure dark mode support

### 2. Update Content Structure
1. Organize content into modular structure:
   ```
   docs/
   ├── module1/
   │   ├── chapter1/
   │   │   ├── index.md
   │   │   └── content.md
   │   └── ...
   ├── module2/
   └── ...
   ```

### 3. Enhance Navigation
1. Update `sidebars.js` with hierarchical structure
2. Implement collapsible sections
3. Add search functionality

### 4. Optimize Assets
1. Move images to `static/img/` or use Docusaurus assets
2. Optimize images for web delivery
3. Implement lazy loading where appropriate

## Configuration Options

### Theme Configuration
```javascript
// docusaurus.config.js
module.exports = {
  themeConfig: {
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Robotics Logo',
        src: '/img/logo.svg',
      },
      items: [
        // Navigation items
      ],
    },
    footer: {
      style: 'dark',
      links: [/* footer links */],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics`,
    },
    prism: {
      theme: require('prism-react-renderer/themes/github'),
      darkTheme: require('prism-react-renderer/themes/dracula'),
    },
  },
};
```

### Custom Styling
```scss
// src/css/custom.css
:root {
  --ifm-color-primary: #25c2a0;
  --ifm-color-primary-dark: rgb(33, 175, 144);
  --ifm-color-primary-darker: rgb(31, 165, 136);
  --ifm-color-primary-darkest: rgb(26, 136, 112);
  --ifm-color-primary-light: rgb(70, 203, 174);
  --ifm-color-primary-lighter: rgb(102, 212, 189);
  --ifm-color-primary-lightest: rgb(146, 224, 208);
  --ifm-code-font-size: 95%;
}

/* Responsive design improvements */
@media (max-width: 996px) {
  .hero__title {
    font-size: 2rem;
  }
}
```

## Testing the Upgrade

### 1. Local Development Server
```bash
npm run start
```

### 2. Production Build Test
```bash
npm run build
npm run serve
```

### 3. Validation Checks
- [ ] All pages load without errors
- [ ] Navigation works correctly
- [ ] Responsive design on mobile/tablet/desktop
- [ ] Search functionality works
- [ ] Code blocks display properly
- [ ] Images load correctly
- [ ] Internal links work
- [ ] Dark mode toggle works

## Deployment

### GitHub Pages Deployment
```bash
GIT_USER=<Your GitHub username> npm run deploy
```

### Environment Variables
```bash
# For deployment
USE_SSH=false
GH_TOKEN=<your-github-token>
```

## Troubleshooting

### Common Issues
1. **Build errors**: Run `npm run clear` to clear cache
2. **Missing styles**: Verify CSS files are properly imported
3. **Navigation issues**: Check sidebar configuration
4. **Image loading**: Verify asset paths are correct

### Performance Tips
- Use optimized images (WebP format when possible)
- Implement code splitting for large pages
- Enable gzip compression
- Use CDN for static assets

## Next Steps
1. Review content organization
2. Add interactive elements where appropriate
3. Implement analytics
4. Set up continuous integration
5. Create content authoring guidelines