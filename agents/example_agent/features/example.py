
import logging
from typing import Dict, Any, List

class ExampleFeature:
    """Example feature class"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.logger = logging.getLogger("example_feature")
        self.config = config or {}
    
    async def process_data(self, data: Any) -> Dict[str, Any]:
        """Process some data"""
        self.logger.info("🔄 Processing data...")
        
        # Example processing logic
        result = {
            "status": "processed",
            "input_type": type(data).__name__,
            "processed_at": "now",
            "data": data
        }
        
        return result
    
    async def analyze_patterns(self, data_list: List[Any]) -> Dict[str, Any]:
        """Analyze patterns in data"""
        self.logger.info("📊 Analyzing patterns...")
        
        analysis = {
            "total_items": len(data_list),
            "unique_types": len(set(type(item).__name__ for item in data_list)),
            "patterns_found": []
        }
        
        # Example pattern detection
        if len(data_list) > 10:
            analysis["patterns_found"].append("large_dataset")
        
        return analysis
    
    def validate_input(self, data: Any) -> bool:
        """Validate input data"""
        # Example validation logic
        if data is None:
            return False
        
        if isinstance(data, (str, int, float, dict, list)):
            return True
        
        return False