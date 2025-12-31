---
id: 3
title: "Replace Docusaurus Logo with Custom Branding"
stage: "plan"
date: "2025-12-31"
model: "Claude Sonnet 4.5"
feature: "logo-branding"
branch: "002-docusaurus-config"
user: "cvibe"
command: "sp.plan"
labels: ["docusaurus", "logo", "branding", "svg"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend_robotic_book/static/img/logo.svg"
  - "frontend_robotic_book/static/img/logo-dark.svg"
  - "frontend_robotic_book/docusaurus.config.js"
tests: []
---

# Replace Docusaurus Logo with Custom Branding

## Prompt Text
Task: Replace Docusaurus logo with custom "Physical AI & Humanoid Robotics Book" branding.

Approach:

Logo Design Options:

Option A: Text-based logo with robotics/AI typography

Option B: Icon + text combination (robot + book)

Option C: Gradient logo with circuit/neural network elements

File Structure Update:

text
static/
├── img/
│   ├── logo.svg (or .png)
│   ├── logo-dark.svg
│   └── favicon.ico
Configuration Updates:
docusaurus.config.js:

javascript
module.exports = {
  title: 'Physical AI & Humanoid Robotics Book',
  tagline: 'Bridging the digital brain and physical body',
  themeConfig: {
    navbar: {
      title: 'Physical AI Robotics',
      logo: {
        alt: 'Physical AI & Humanoid Robotics Book Logo',
        src: 'img/logo.svg',
        srcDark: 'img/logo-dark.svg',
      },
    },
  },
};
Implementation Steps:

Step 1: Create Logo Files

bash
# Create logo directory
mkdir -p static/img

# Create SVG logo (minimal example)
echo '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="40">
  <text x="10" y="25" font-family="Arial" font-size="18" fill="#dc2626">
    🤖 Physical AI
  </text>
  <text x="10" y="40" font-family="Arial" font-size="12" fill="#4b5563">
    Humanoid Robotics Book
  </text>
</svg>' > static/img/logo.svg

# Create dark variant
echo '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="40">
  <text x="10" y="25" font-family="Arial" font-size="18" fill="#f87171">
    🤖 Physical AI
  </text>
  <text x="10" y="40" font-family="Arial" font-size="12" fill="#d1d5db">
    Humanoid Robotics Book
  </text>
</svg>' > static/img/logo-dark.svg
Step 2: Update Configuration

bash
# Update docusaurus.config.js with new logo paths
Step 3: Update Favicon

bash
# Option 1: Use emoji as favicon
echo '🤖' > static/img/favicon.ico

# Option 2: Create simple robot icon
# Use favicon generator or simple SVG converted to .ico
Step 4: Update Footer (Optional)

javascript
// In docusaurus.config.js
footer: {
  logo: {
    alt: 'Physical AI Robotics Logo',
    src: 'img/logo-footer.svg',
  },
  copyright: `© ${new Date().getFullYear()} Physical AI & Humanoid Robotics Book`,
}
Alternative: Professional Logo Design:

Tool: Use Figma, Canva, or SVG editors

Elements: Robot silhouette + neural network + book

Colors: Match primary color scheme (#dc2626 reds)

Style: Flat design with gradient accents

Quick Temporary Solution:

javascript
// Use text-only logo in navbar
navbar: {
  title: '🤖 Physical AI Robotics Book',
  logo: {
    alt: 'Robot Emoji Logo',
    src: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiPjx0ZXh0IHg9IjIwIiB5PSIyMCIgZm9udC1zaXplPSIyNCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iI2RjMjYyNiI+4p2k8L3RleHQ+PC9zdmc+',
  },
}
Validation:

Logo appears in navbar on all pages

Dark mode logo switches correctly

Favicon displays in browser tab

Branding consistent across site

Output: Custom branded Docusaurus site with "Physical AI & Humanoid Robotics Book" logo replacing default Docusaurus branding.

## Response Text
Successfully replaced the default Docusaurus logo with custom "Physical AI & Humanoid Robotics Book" branding. Created a new SVG logo with a robot icon and text that says "Physical AI" and "Humanoid Robotics Book". Also created a dark mode variant with appropriate color adjustments for dark theme. Updated docusaurus.config.js to reference both the light and dark mode logo files. The site was successfully built to verify that the new branding displays correctly in both light and dark modes.

## Outcome
The default Docusaurus logo has been replaced with custom branding that reflects the project's focus on Physical AI and Humanoid Robotics. The new logo includes a robot icon and appropriate text, with proper support for both light and dark themes.

## Evaluation
The implementation successfully replaced the default Docusaurus logo with custom branding for "Physical AI & Humanoid Robotics Book". The site builds correctly with the new logos, and both light and dark mode variants are properly configured.