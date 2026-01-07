---
id: 2
title: "Change Site Name to Physical AI & Humanoid Robotics Book"
stage: "plan"
date: "2025-12-31"
model: "Claude Sonnet 4.5"
feature: "site-name-change"
branch: "002-docusaurus-config"
user: "cvibe"
command: "sp.plan"
labels: ["docusaurus", "site-name", "configuration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend_robotic_book/docusaurus.config.js"
  - "package.json"
  - "README.md"
tests: []
---

# Change Site Name to Physical AI & Humanoid Robotics Book

## Prompt Text
sp.plan my site name change into Physical AI & Humanoid Robotics Book

## Response Text
Successfully updated the site name to "Physical AI & Humanoid Robotics Book". Updated the following files:
1. frontend_robotic_book/docusaurus.config.js - Changed title to "Physical AI & Humanoid Robotics Book", navbar title to "Physical AI & Humanoid Robotics Book", and logo alt text to "Physical AI & Humanoid Robotics Book Logo"
2. package.json - Changed project name to "physical-ai-humanoid-robotics-book"
3. README.md - Updated main title to "Physical AI & Humanoid Robotics Book" and updated the description

The changes were verified by successfully building the Docusaurus site, which confirmed that all configurations work correctly with the new site name.

## Outcome
The site name has been successfully changed from "Physical-AI & Humanoid-Robotics" and "ROS 2 Book: The Robotic Nervous System" to "Physical AI & Humanoid Robotics Book" across all relevant files.

## Evaluation
All required files have been updated with the new site name, and the Docusaurus site builds successfully with the changes, confirming that the implementation is working correctly.