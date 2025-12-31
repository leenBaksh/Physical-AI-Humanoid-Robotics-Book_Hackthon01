---
id: 4
title: "Implement Responsive Hero Banner with Fluid Background"
stage: "plan"
date: "2025-12-31"
model: "Claude Sonnet 4.5"
feature: "responsive-hero-banner"
branch: "002-docusaurus-config"
user: "cvibe"
command: "sp.plan"
labels: ["docusaurus", "responsive", "css", "hero-banner", "fluid-typography"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend_robotic_book/src/pages/index.module.css"
  - "frontend_robotic_book/src/pages/index.js"
tests: []
---

# Implement Responsive Hero Banner with Fluid Background

## Prompt Text
Task: Implement responsive hero banner with fluid background, text sizing, and color scaling across 7 screen tiers.

Breakpoints & Scaling Strategy:

XXL (1600px+): Premium space, cinematic experience

XL (1200-1599px): Desktop optimization

LG (992-1199px): Tablet landscape

MD (768-991px): Tablet portrait

SM (576-767px): Mobile landscape

XS (480-575px): Mobile portrait

XXS (<479px): Small mobile

Implementation Plan:

1. Fluid Typography System

css
:root {
  --fluid-min: 320px;
  --fluid-max: 1600px;
  --fluid-range: calc(var(--fluid-max) - var(--fluid-min));
}

.heroBanner h1 {
  font-size: clamp(
    2.2rem,  /* XXS: 320px */
    4vw + 1rem,  /* Fluid scaling */
    6rem    /* XXL: 1600px+ */
  );
}
2. Color Theme Per Breakpoint

XXL: Deep space gradient (purples/blues)

XL: Ocean depth gradient (blues/teals)

LG: Royal gradient (purples/violets)

MD: Deep sea gradient (navy/teal)

SM: Forest gradient (greens)

XS: Magenta gradient (purples/pinks)

XXS: Crimson gradient (reds/pinks)

3. Responsive Animation System

css
/* Slower animations on larger screens */
@media (min-width: 1200px) {
  .heroBanner { animation-duration: 20s; }
}
@media (max-width: 479px) {
  .heroBanner { animation-duration: 45s; }
}
4. Touch-First Mobile Optimization

Minimum touch targets: 44×44px

Increased spacing on small screens

Stacked buttons on mobile

Reduced animations for performance

5. Accessibility Layers

Reduced motion support

High contrast mode

Print styles

Dark mode adjustments

Implementation Steps:

Base Styles: Set fluid typography foundation with clamp()

XXL Tier: Cinematic experience with maximum spacing

XL Tier: Optimized for desktop viewing

LG Tier: Tablet landscape with adjusted gradients

MD Tier: Tablet portrait with simplified animations

SM Tier: Mobile landscape with stacked layout

XS Tier: Mobile portrait with compact design

XXS Tier: Small mobile with minimal animations

Accessibility: Add prefers-reduced-motion, print, high-contrast

Validation:

Each tier maintains visual hierarchy

Color

## Response Text
Successfully implemented a responsive hero banner with fluid background, text sizing, and color scaling across 7 screen tiers. The implementation includes:

1. CSS custom properties for fluid scaling with clamp() functions for responsive typography
2. Specific gradients for each of the 7 screen tiers:
   - XXL (1600px+): Deep space gradient (purples/blues)
   - XL (1200-1599px): Ocean depth gradient (blues/teals)
   - LG (992-1199px): Royal gradient (purples/violets)
   - MD (768-991px): Deep sea gradient (navy/teal)
   - SM (576-767px): Forest gradient (greens)
   - XS (480-575px): Magenta gradient (purples/pinks)
   - XXS (<479px): Crimson gradient (reds/pinks)
3. Responsive animation system with slower animations on larger screens
4. Touch-optimized styles for mobile devices with minimum 44x44px touch targets
5. Accessibility features including reduced motion, high contrast mode, print styles, and dark mode adjustments

The site was successfully built to verify all changes work correctly.

## Outcome
The hero banner now has responsive design with fluid typography, color scaling across 7 screen tiers, optimized animations, touch-friendly mobile styling, and full accessibility support.

## Evaluation
The implementation successfully meets all requirements with responsive design across all 7 screen tiers, fluid typography, gradient color scaling, responsive animations, touch optimization, and accessibility features.