# Quickstart Guide: Docusaurus Configuration for Physical AI & Humanoid Robotics

## Prerequisites

Before configuring the Docusaurus site for the Physical AI & Humanoid Robotics book, ensure you have:

1. **Node.js**: Version 18.x or higher
2. **npm**: Latest version (comes with Node.js)
3. **Git**: Version control system
4. **Basic knowledge**: JavaScript and Markdown

## Installation Steps

### 1. Install Docusaurus CLI

```bash
npm install -g @docusaurus/cli
```

### 2. Create a New Docusaurus Site

```bash
npx create-docusaurus@latest my-website classic
cd my-website
```

### 3. Install Dependencies

```bash
npm install
```

## Configuration Steps

### 1. Update Site Configuration

Replace the content of `docusaurus.config.js` with the following configuration:

```javascript
// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A comprehensive guide to robotics and AI integration',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-organization.github.io', // TODO: Update with actual GitHub Pages URL
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub Pages, this is usually '/<project-name>/'
  baseUrl: '/physical-ai-book/', // TODO: Update with actual project name

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'your-organization', // Usually your GitHub org/user name.
  projectName: 'physical-ai-book', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/your-organization/your-repo/tree/main/',
        },
        blog: false, // Optional: disable the blog plugin
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Physical AI & Humanoid Robotics Logo',
          src: 'img/logo.svg', // You can add a logo in static/img/
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'module1Sidebar',
            position: 'left',
            label: 'Module 1: ROS 2',
          },
          {
            href: 'https://github.com/your-organization/your-repo',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Modules',
            items: [
              {
                label: 'Module 1: ROS 2',
                to: '/docs/module1',
              },
              {
                label: 'Module 2: Digital Twin',
                to: '/docs/module2',
              },
              {
                label: 'Module 3: Advanced Topics',
                to: '/docs/module3',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'ROS Documentation',
                href: 'https://docs.ros.org/',
              },
              {
                label: 'Spec-Kit Documentation',
                href: 'https://specify.ai/docs',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/your-organization/your-repo',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Book Project. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'yaml'],
      },
    }),
};

export default config;
```

### 2. Create Sidebar Configuration

Create a `sidebars.js` file with the following content:

```javascript
// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  module1Sidebar: [
    'module1/index',
    {
      type: 'category',
      label: 'Chapter 1: ROS 2 Core',
      items: [
        'module1/chapter-1-ros2-core/index',
        'module1/chapter-1-ros2-core/nodes-topics-services',
        'module1/chapter-1-ros2-core/publisher-subscriber-patterns',
        'module1/chapter-1-ros2-core/hands-on-tutorial',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2: AI-ROS Bridge',
      items: [
        'module1/chapter-2-ai-ros-bridge/index',
        'module1/chapter-2-ai-ros-bridge/rclpy-integration',
        'module1/chapter-2-ai-ros-bridge/message-interfaces',
        'module1/chapter-2-ai-ros-bridge/ai-agent-tutorial',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 3: URDF Interpretation',
      items: [
        'module1/chapter-3-urdf-kinematics/index',
        'module1/chapter-3-urdf-kinematics/urdf-overview',
        'module1/chapter-3-urdf-kinematics/kinematic-structure',
        'module1/chapter-3-urdf-kinematics/interpretation-guide',
      ],
    },
  ],
};

module.exports = sidebars;
```

### 3. Create Custom CSS (Optional)

Create a `src/css/custom.css` file to add custom styling:

```css
/**
 * Copyright (c) 2017-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

/* You can override the default Docusaurus styling with this file. */

:root {
  --ifm-color-primary: #25c2a0;
  --ifm-color-primary-dark: #21af90;
  --ifm-color-primary-darker: #1fa588;
  --ifm-color-primary-darkest: #1a8870;
  --ifm-color-primary-light: #29d5b0;
  --ifm-color-primary-lighter: #32d8b4;
  --ifm-color-primary-lightest: #4fddbf;
  --ifm-code-font-size: 95%;
}

.docusaurus-highlight-code-line {
  background-color: rgba(0, 0, 0, 0.1);
  display: block;
  margin: 0 calc(-1 * var(--ifm-pre-padding));
  padding: 0 var(--ifm-pre-padding);
}

html[data-theme='dark'] .docusaurus-highlight-code-line {
  background-color: rgba(0, 0, 0, 0.3);
}
```

## Running the Development Server

1. Navigate to your project directory
2. Start the development server:

```bash
npm start
```

This will start a local server at `http://localhost:3000` where you can view your configured site.

## Building for Production

To build the site for deployment:

```bash
npm run build
```

This creates a `build/` directory with the static files for deployment.

## Deploying to GitHub Pages

1. Update the `organizationName` and `projectName` in `docusaurus.config.js` with your GitHub username and repository name
2. Run the deployment command:

```bash
npm run deploy
```

This will build the site and push it to the `gh-pages` branch of your repository, making it accessible at `https://<your-username>.github.io/<repository-name>/`.

## Next Steps

1. Add your module content to the `docs/` directory following the sidebar structure
2. Customize the site with your own logo and styling
3. Add additional modules as needed
4. Test the site locally before deploying