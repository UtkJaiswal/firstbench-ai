from typing import List, Dict
from pydantic import BaseModel, condecimal

class Metric(BaseModel):
    metric: str
    relevance_score: int

class GenreMetrics(BaseModel):
    genre: str
    dynamic_metric: List[Metric]

class FirstPromptClass(BaseModel):
    dynamic_metrics: List[GenreMetrics]


class MetricScore(BaseModel):
    metric_name: str     
    score: condecimal(gt=0.0, le=10.0)  

class GrpScore(BaseModel):
    dynamic_metrics_score: List[MetricScore]
    static_metrics_score: List[MetricScore]

class SecondPromptClass(BaseModel):
    scores: GrpScore  
    deductions: List[str]


class ThirdPromptClass(BaseModel):
    feedback: Dict[str, str]                
    suggestions: Dict[str, str]             


if __name__ == "__main__":
    arg_class = FirstPromptClass(
        genre="Argumentative",
        dynamic_matrix=["Accuracy of Facts", "Use of Data"]
    )
    
    evaluation = SecondPromptClass(
        dynamic_metrics={
            "Accuracy of Facts": MetricScore(score=8.0, reason_for_deduction="Some outdated data used"),
            "Use of Data": MetricScore(score=9.0, reason_for_deduction="Good data, but lacked variety")
        },
        static_metrics={
            "Clarity & Structure": MetricScore(score=7.0, reason_for_deduction="Conclusion was weak"),
            "Logical Coherence": MetricScore(score=9.0, reason_for_deduction="Mostly coherent, with minor logical gaps")
        }
    )
    
    feedback = ThirdPromptClass(
        feedback={
            "Accuracy of Facts": "Improve by using more up-to-date sources.",
            "Clarity & Structure": "Strengthen your conclusion to improve clarity."
        },
        suggestions={
            "Use of Data": "Consider adding more data from varied sources.",
            "Logical Coherence": "Try tightening the logical flow between your main points."
        }
    )
    
    print(arg_class)
    print(evaluation)
    print(feedback)
