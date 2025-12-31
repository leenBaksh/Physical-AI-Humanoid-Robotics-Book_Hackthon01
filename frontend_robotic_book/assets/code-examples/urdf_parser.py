#!/usr/bin/env python3
"""
URDF Parser and Analysis Tool

This script provides utilities for parsing and analyzing URDF files
to understand robot kinematic structure.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Optional


class URDFParser:
    """
    A class to parse and analyze URDF files for robot kinematic structure.
    """

    def __init__(self, urdf_path: str):
        """
        Initialize the URDF parser with a URDF file path.

        Args:
            urdf_path: Path to the URDF file to parse
        """
        self.urdf_path = urdf_path
        self.tree = ET.parse(urdf_path)
        self.root = self.tree.getroot()
        self.robot_name = self.root.get('name')

        # Extract all links and joints
        self.links = {link.get('name'): link for link in self.root.findall('link')}
        self.joints = {joint.get('name'): joint for joint in self.root.findall('joint')}

        # Build parent-child relationships
        self.parent_map = {}
        self.child_map = {}
        self._build_kinematic_tree()

    def _build_kinematic_tree(self):
        """
        Build parent-child relationships for kinematic analysis.
        """
        for joint_name, joint in self.joints.items():
            parent_link = joint.find('parent').get('link')
            child_link = joint.find('child').get('link')

            self.parent_map[child_link] = {
                'parent': parent_link,
                'joint_name': joint_name,
                'joint_type': joint.get('type')
            }

            if parent_link not in self.child_map:
                self.child_map[parent_link] = []
            self.child_map[parent_link].append({
                'child': child_link,
                'joint_name': joint_name,
                'joint_type': joint.get('type')
            })

    def find_base_link(self) -> str:
        """
        Find the base link of the robot (the link with no parent).

        Returns:
            Name of the base link
        """
        all_child_links = set(self.parent_map.keys())
        all_parent_links = set(self.child_map.keys())

        # Base link is a parent that has no parent itself
        for link in all_parent_links:
            if link not in all_child_links:
                return link

        # If no such link exists, return the first parent (fallback)
        if all_parent_links:
            return list(all_parent_links)[0]

        raise ValueError("Could not determine base link")

    def get_kinematic_chain(self, end_effector: str) -> List[Dict]:
        """
        Get the kinematic chain from base to end effector.

        Args:
            end_effector: Name of the end effector link

        Returns:
            List of dictionaries representing the chain (base to end_effector)
        """
        chain = []
        current = end_effector

        while current in self.parent_map:
            parent_info = self.parent_map[current]
            chain.append({
                'link': current,
                'parent': parent_info['parent'],
                'joint_name': parent_info['joint_name'],
                'joint_type': parent_info['joint_type']
            })
            current = parent_info['parent']

        # Add base link
        chain.append({
            'link': current,
            'parent': None,
            'joint_name': None,
            'joint_type': None
        })

        # Reverse to get base to end effector order
        return list(reversed(chain))

    def calculate_dof(self) -> int:
        """
        Calculate the total degrees of freedom of the robot.

        Returns:
            Total degrees of freedom
        """
        dof = 0
        for joint in self.joints.values():
            joint_type = joint.get('type')
            if joint_type in ['revolute', 'prismatic']:
                dof += 1
            elif joint_type == 'continuous':
                dof += 1  # Continuous is like revolute but unlimited
            elif joint_type == 'spherical':
                dof += 3
            elif joint_type == 'planar':
                dof += 3
            # Fixed joints add 0 DOF

        return dof

    def find_end_effectors(self) -> List[str]:
        """
        Find all end effector links (links with no children).

        Returns:
            List of end effector link names
        """
        all_parent_links = set(self.child_map.keys())
        all_child_links = set(self.parent_map.keys())

        # End effectors are child links that are not parents
        end_effectors = []
        for link in all_child_links:
            if link not in all_parent_links:
                end_effectors.append(link)

        return end_effectors

    def get_joint_info(self, joint_name: str) -> Dict:
        """
        Get detailed information about a specific joint.

        Args:
            joint_name: Name of the joint

        Returns:
            Dictionary with joint information
        """
        joint = self.joints.get(joint_name)
        if joint is None:
            return {}

        info = {
            'name': joint_name,
            'type': joint.get('type'),
            'parent_link': joint.find('parent').get('link'),
            'child_link': joint.find('child').get('link'),
        }

        # Add origin if present
        origin = joint.find('origin')
        if origin is not None:
            info['origin_xyz'] = origin.get('xyz')
            info['origin_rpy'] = origin.get('rpy')

        # Add axis if present (for revolute/prismatic joints)
        axis = joint.find('axis')
        if axis is not None:
            info['axis'] = axis.get('xyz')

        # Add limits if present
        limit = joint.find('limit')
        if limit is not None:
            info['limit'] = {
                'lower': limit.get('lower'),
                'upper': limit.get('upper'),
                'effort': limit.get('effort'),
                'velocity': limit.get('velocity')
            }

        return info

    def print_robot_summary(self):
        """
        Print a summary of the robot structure.
        """
        print(f"Robot: {self.robot_name}")
        print(f"Total links: {len(self.links)}")
        print(f"Total joints: {len(self.joints)}")
        print(f"Total DOF: {self.calculate_dof()}")

        base_link = self.find_base_link()
        print(f"Base link: {base_link}")

        end_effectors = self.find_end_effectors()
        print(f"End effectors: {end_effectors}")

        print("\nKinematic chains:")
        for ee in end_effectors:
            chain = self.get_kinematic_chain(ee)
            chain_names = [step['link'] for step in chain]
            print(f"  {base_link} -> ... -> {ee} : {' -> '.join(chain_names)}")


def main():
    """
    Main function to demonstrate URDF parsing.
    """
    import sys
    import os

    if len(sys.argv) != 2:
        print("Usage: python urdf_parser.py <path_to_urdf_file>")
        sys.exit(1)

    urdf_path = sys.argv[1]

    if not os.path.exists(urdf_path):
        print(f"Error: URDF file '{urdf_path}' does not exist")
        sys.exit(1)

    try:
        parser = URDFParser(urdf_path)
        parser.print_robot_summary()

        print("\nDetailed joint information:")
        for joint_name in parser.joints.keys():
            info = parser.get_joint_info(joint_name)
            print(f"  Joint '{info['name']}' ({info['type']}): {info['parent_link']} -> {info['child_link']}")

    except Exception as e:
        print(f"Error parsing URDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()