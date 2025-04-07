from typing import Dict, Any, List

class AiProgramTool:
    """
    Tool for accessing information about Duke's AI MEng program
    """
    
    def __init__(self):
        # This data would ideally come from a database or API
        # For demonstration purposes, we'll hardcode some information
        self.program_info = {
            "general": {
                "name": "AI Master of Engineering Program",
                "department": "Pratt School of Engineering",
                "website": "https://ai.meng.duke.edu/",
                "duration": "30 credits, typically completed in two or three semesters",
                "description": "The Duke AI MEng program prepares students to develop and deploy advanced AI solutions, focusing on practical implementation and ethical considerations."
            },
            "curriculum": {
                "core_courses": [
                    "Introduction to AI",
                    "Machine Learning",
                    "Deep Learning",
                    "Natural Language Processing",
                    "Computer Vision"
                ],
                "electives": [
                    "Reinforcement Learning",
                    "AI Ethics",
                    "Robotics",
                    "Data Engineering",
                    "AI Project Management"
                ],
                "capstone": "Industry-partnered capstone project"
            },
            "faculty": [
                {
                    "name": "Dr. Ricardo Henao",
                    "specialty": "Machine Learning",
                    "email": "ricardo.henao@duke.edu"
                },
                {
                    "name": "Dr. Cynthia Rudin",
                    "specialty": "Interpretable AI",
                    "email": "cynthia.rudin@duke.edu"
                },
                {
                    "name": "Dr. Lawrence Carin",
                    "specialty": "Deep Learning",
                    "email": "lawrence.carin@duke.edu"
                }
            ],
            "admissions": {
                "deadlines": "Rolling admissions with priority deadline of January 15",
                "requirements": [
                    "Bachelor's degree in CS, ECE, or related field",
                    "Programming experience (Python preferred)",
                    "Basic knowledge of statistics and linear algebra",
                    "GRE scores (optional)",
                    "TOEFL/IELTS for international students"
                ],
                "application_url": "https://gradschool.duke.edu/admissions/apply"
            },
            "career": {
                "outcomes": [
                    "Machine Learning Engineer",
                    "AI Researcher",
                    "Data Scientist",
                    "AI Product Manager",
                    "Computer Vision Engineer"
                ],
                "average_salary": "$120,000 - $150,000",
                "top_employers": [
                    "Google",
                    "Microsoft",
                    "Amazon",
                    "Meta",
                    "IBM",
                    "Local startups"
                ]
            },
            "faq": {
                "What background do I need?": "A technical background in computer science, electrical engineering, mathematics, or a related field is recommended. Strong programming skills are essential.",
                "Can I study part-time?": "Yes, we offer part-time options for professionals looking to enhance their skills while working.",
                "Are scholarships available?": "Limited merit-based scholarships are available to exceptional candidates.",
                "How is the program different from a CS Master's?": "Our program focuses specifically on practical AI implementation with industry-relevant projects, rather than general computer science theory."
            }
        }
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """
        Return the tool definition for Vertex AI
        """
        return {
            "name": "ai_program_tool",
            "description": "Tool for accessing information about Duke's AI MEng program",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The category of information to retrieve (e.g., 'general', 'curriculum', 'faculty', 'admissions', 'career', 'faq')"
                    },
                    "specific_info": {
                        "type": "string",
                        "description": "Optional specific information to retrieve within a category"
                    }
                },
                "required": ["category"]
            }
        }
    
    def execute(self, category: str, specific_info: str = None) -> Dict[str, Any]:
        """
        Execute a query for AI program information
        
        Args:
            category: The category of information to retrieve
            specific_info: Optional specific information to retrieve
            
        Returns:
            The requested information
        """
        if category not in self.program_info:
            return {
                "status": "error",
                "error": f"Category '{category}' not found. Available categories: {', '.join(self.program_info.keys())}"
            }
        
        category_data = self.program_info[category]
        
        if specific_info:
            if isinstance(category_data, dict) and specific_info in category_data:
                return {
                    "status": "success",
                    "category": category,
                    "specific_info": specific_info,
                    "data": category_data[specific_info]
                }
            else:
                # Search within the category data for relevant information
                if isinstance(category_data, dict):
                    for key, value in category_data.items():
                        if specific_info.lower() in key.lower():
                            return {
                                "status": "success",
                                "category": category,
                                "specific_info": key,
                                "data": value
                            }
                
                return {
                    "status": "error",
                    "error": f"Specific information '{specific_info}' not found in category '{category}'"
                }
        
        return {
            "status": "success",
            "category": category,
            "data": category_data
        }
