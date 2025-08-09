#!/usr/bin/env python3
"""
EWU Course Catalog Scraper - CSCD Course Prerequisites Analysis

Educational Purpose:
Demonstrates web scraping techniques, HTML parsing, and graph construction
for academic course dependencies. Students learn practical data extraction
and academic planning tools development.

Features:
- BeautifulSoup HTML parsing for structured data extraction
- Prerequisite relationship mapping for course planning
- JSON output compatible with D3.js visualization
- Educational scaffolding for computer science curriculum analysis
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Dict, List, Set, Optional
import sys
from pathlib import Path


class CSCDCourseScraper:
    """
    Scrapes Eastern Washington University CSCD course catalog
    and extracts course prerequisites for knowledge graph construction.

    Educational Notes:
    - Demonstrates web scraping best practices
    - Shows HTML parsing and data cleaning techniques
    - Implements prerequisite graph construction
    - Provides structured data for visualization
    """

    def __init__(self):
        self.base_url = "https://catalog.ewu.edu/course-listings/cscd/"
        self.courses = {}
        self.prerequisites = []

    def scrape_catalog(self) -> Dict:
        """
        Scrape the EWU CSCD course catalog and extract course information.

        Returns:
            Dict containing courses and their prerequisites
        """
        print("🔍 Scraping EWU CSCD Course Catalog...")

        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Find course blocks (this will need to be adjusted based on actual HTML structure)
            course_blocks = soup.find_all("div", class_="courseblock")

            if not course_blocks:
                # Fallback: look for common course listing patterns
                course_blocks = soup.find_all(
                    ["div", "section"], string=re.compile(r"CSCD\s+\d+")
                )

            print(f"📚 Found {len(course_blocks)} course blocks")

            for block in course_blocks:
                course_info = self._parse_course_block(block)
                if course_info:
                    self.courses[course_info["code"]] = course_info

            # If no structured blocks found, use text-based extraction
            if not self.courses:
                self._extract_from_text(soup.get_text())

            print(f"✅ Extracted {len(self.courses)} courses")
            return self._build_graph_data()

        except requests.RequestException as e:
            print(f"❌ Error fetching catalog: {e}")
            return self._create_fallback_data()

    def _parse_course_block(self, block) -> Optional[Dict]:
        """Parse individual course block for course information."""
        try:
            # Look for course code pattern like "CSCD 210"
            title_elem = block.find(["h3", "h4", "strong", "b"])
            if not title_elem:
                return None

            title_text = title_elem.get_text().strip()
            course_match = re.search(r"CSCD\s+(\d+)", title_text)

            if not course_match:
                return None

            course_number = course_match.group(1)
            course_code = f"CSCD{course_number}"

            # Extract course title
            title_parts = title_text.split(" - ", 1)
            course_title = (
                title_parts[1]
                if len(title_parts) > 1
                else f"Computer Science Course {course_number}"
            )

            # Look for prerequisites
            prerequisites = self._extract_prerequisites(block.get_text())

            # Extract credits
            credits_match = re.search(
                r"(\d+)\s+credit", block.get_text(), re.IGNORECASE
            )
            credits = int(credits_match.group(1)) if credits_match else 3

            return {
                "code": course_code,
                "number": course_number,
                "title": course_title,
                "credits": credits,
                "prerequisites": prerequisites,
                "description": self._extract_description(block),
            }

        except Exception as e:
            print(f"⚠️ Error parsing course block: {e}")
            return None

    def _extract_prerequisites(self, text: str) -> List[str]:
        """Extract prerequisite course codes from course text."""
        prerequisites = []

        # Common prerequisite patterns
        prereq_patterns = [
            r"Prerequisite[s]?:?\s*([^.]+)",
            r"Prereq[s]?:?\s*([^.]+)",
            r"Prerequisites include[s]?:?\s*([^.]+)",
        ]

        for pattern in prereq_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                prereq_text = match.group(1)
                # Find CSCD course codes in prerequisite text
                cscd_codes = re.findall(r"CSCD\s*(\d+)", prereq_text, re.IGNORECASE)
                prerequisites.extend([f"CSCD{code}" for code in cscd_codes])

        return list(set(prerequisites))  # Remove duplicates

    def _extract_description(self, block) -> str:
        """Extract course description from course block."""
        text = block.get_text()

        # Try to find description after title and before prerequisites
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        description_lines = []
        found_title = False

        for line in lines:
            if re.search(r"CSCD\s+\d+", line):
                found_title = True
                continue

            if found_title and not re.search(
                r"prerequisite|credit|prereq", line, re.IGNORECASE
            ):
                if len(line) > 20:  # Likely a description
                    description_lines.append(line)

            if re.search(r"prerequisite|prereq", line, re.IGNORECASE):
                break

        return " ".join(description_lines[:3])  # First few sentences

    def _extract_from_text(self, text: str):
        """Fallback method to extract courses from raw text."""
        print("📝 Using text-based extraction fallback...")

        # Find all CSCD course references
        course_matches = re.finditer(
            r"CSCD\s+(\d+)([^.]*?)(?=CSCD\s+\d+|$)", text, re.IGNORECASE | re.DOTALL
        )

        for match in course_matches:
            course_number = match.group(1)
            course_text = match.group(2)
            course_code = f"CSCD{course_number}"

            # Extract title from first line
            first_line = course_text.split("\n")[0].strip()
            title_match = re.search(r"[-–]\s*(.+?)(?:\d+\s+credit|$)", first_line)
            title = (
                title_match.group(1).strip()
                if title_match
                else f"Computer Science Course {course_number}"
            )

            prerequisites = self._extract_prerequisites(course_text)

            self.courses[course_code] = {
                "code": course_code,
                "number": course_number,
                "title": title,
                "credits": 3,  # Default
                "prerequisites": prerequisites,
                "description": course_text[:200].replace("\n", " ").strip(),
            }

    def _build_graph_data(self) -> Dict:
        """Build D3.js compatible graph data structure."""
        nodes = []
        links = []

        for course_code, course_info in self.courses.items():
            # Create node for course
            nodes.append(
                {
                    "id": course_code,
                    "name": f"{course_code}: {course_info['title']}",
                    "type": "course",
                    "level": self._determine_level(course_info["number"]),
                    "credits": course_info["credits"],
                    "description": course_info["description"],
                    "group": f"CSCD_{course_info['number'][0]}xx",  # Group by hundreds
                    "size": 20 + course_info["credits"] * 5,
                }
            )

            # Create links for prerequisites
            for prereq in course_info["prerequisites"]:
                if prereq in self.courses:
                    links.append(
                        {
                            "source": prereq,
                            "target": course_code,
                            "type": "prerequisite",
                            "strength": 1.0,
                        }
                    )

        return {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "total_courses": len(nodes),
                "total_prerequisites": len(links),
                "source": "EWU CSCD Catalog",
                "scraped_at": "2025-08-09",
            },
        }

    def _determine_level(self, course_number: str) -> str:
        """Determine academic level based on course number."""
        number = int(course_number)
        if number < 200:
            return "introductory"
        elif number < 300:
            return "intermediate"
        elif number < 400:
            return "advanced"
        else:
            return "senior"

    def _create_fallback_data(self) -> Dict:
        """Create fallback data with known CSCD courses if scraping fails."""
        print("📋 Creating fallback course data...")

        fallback_courses = {
            "CSCD210": {
                "title": "Programming Principles I",
                "prerequisites": [],
                "level": "introductory",
                "credits": 4,
            },
            "CSCD211": {
                "title": "Programming Principles II",
                "prerequisites": ["CSCD210"],
                "level": "introductory",
                "credits": 4,
            },
            "CSCD300": {
                "title": "Data Structures",
                "prerequisites": ["CSCD211"],
                "level": "intermediate",
                "credits": 4,
            },
            "CSCD301": {
                "title": "Algorithm Analysis",
                "prerequisites": ["CSCD300"],
                "level": "intermediate",
                "credits": 4,
            },
            "CSCD320": {
                "title": "Algorithms",
                "prerequisites": ["CSCD301"],
                "level": "advanced",
                "credits": 4,
            },
        }

        nodes = []
        links = []

        for code, info in fallback_courses.items():
            nodes.append(
                {
                    "id": code,
                    "name": f"{code}: {info['title']}",
                    "type": "course",
                    "level": info["level"],
                    "credits": info["credits"],
                    "group": f"CSCD_{code[4]}xx",
                    "size": 20 + info["credits"] * 5,
                }
            )

            for prereq in info["prerequisites"]:
                links.append(
                    {
                        "source": prereq,
                        "target": code,
                        "type": "prerequisite",
                        "strength": 1.0,
                    }
                )

        return {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "total_courses": len(nodes),
                "total_prerequisites": len(links),
                "source": "Fallback CSCD Data",
                "note": "Live scraping failed, using known course structure",
            },
        }


def main():
    """Main execution function."""
    print("🎓 EWU CSCD Course Catalog Scraper")
    print("=" * 50)

    scraper = CSCDCourseScraper()
    course_data = scraper.scrape_catalog()

    # Create config directory structure if it doesn't exist
    config_dir = Path("./config")
    config_dir.mkdir(exist_ok=True)

    cscd_dir = config_dir / "programming-principles-I-II"
    cscd_dir.mkdir(exist_ok=True)

    # Save course data
    output_file = cscd_dir / "cscd_courses.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(course_data, f, indent=2, ensure_ascii=False)

    print(f"💾 Saved course data to: {output_file}")
    print(f"📊 Summary: {course_data['metadata']}")

    # Also create a public version for the web interface
    public_file = Path("./public/cscd-courses.json")
    with open(public_file, "w", encoding="utf-8") as f:
        json.dump(course_data, f, indent=2, ensure_ascii=False)

    print(f"🌐 Saved public course data to: {public_file}")
    print("✅ CSCD course extraction complete!")


if __name__ == "__main__":
    main()
