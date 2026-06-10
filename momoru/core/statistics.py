from momoru.core.scanner import BuzzerScanner

class TrustEvaluator:
    def __init__(self, scanner: BuzzerScanner):
        self.scanner = scanner

    def generate_metrics(self) -> dict:
        similarity = self.scanner.calculate_similarity()
        
        # Grading Intelligence scoring algorithm
        confidence_score = 0
        if similarity > 0.85:
            confidence_score = 100
        elif similarity > 0.70:
            confidence_score = 75
        elif similarity > 0.40:
            confidence_score = 40
            
        # Add risk calculation parameters
        status = "ORGANIC"
        if confidence_score >= 75:
            status = "SUSPECTED_BUZZER_COORDINATED"
        elif confidence_score >= 40:
            status = "AMBIGUOUS"

        return {
            "username": self.scanner.target_user,
            "similarity_index": round(similarity, 4),
            "confidence_score": confidence_score,
            "status": status,
            "total_scanned_comments": len(self.scanner.comments)
        }