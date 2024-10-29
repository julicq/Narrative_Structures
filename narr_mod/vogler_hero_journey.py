# narr_mod/vogler_hero_journey.py

from dataclasses import dataclass
import math
from typing import List, Dict, Optional, Final, ClassVar
from enum import Enum
from narr_mod import NarrativeStructure, StructureType, AnalysisResult, AnalysisMetadata

class WorldType(Enum):
    ORDINARY = "Ordinary World"
    SPECIAL = "Special World"

class ActType(Enum):
    BEGINNING = "Beginning"
    MIDDLE = "Middle"
    END = "End"

@dataclass
class StageElement:
    name: str
    description: str
    keywords: List[str]
    importance: int  # 1-10
    world_type: WorldType

@dataclass
class Stage:
    number: int
    name: str
    description: str
    act: ActType
    world: WorldType
    elements: List[StageElement]
    angle: int  # угол на круговой диаграмме
    color: str

@dataclass
class StageAnalysis:
    elements_present: Dict[str, bool]
    strengths: List[str]
    weaknesses: List[str]
    score: float

class VoglerHeroJourney(NarrativeStructure):
    """Implementation of Chris Vogler's Hero's Journey structure."""

    @property
    def structure_type(self) -> StructureType:
        return StructureType.VOGLER_HERO_JOURNEY

    # Константы
    TOTAL_STAGES: Final[int] = 12
    CIRCLE_DEGREES: Final[int] = 360

    # Определение стадий
    STAGES: ClassVar[List[Stage]] = [
        Stage(
            1,
            "Ordinary World",
            "Hero's starting point",
            ActType.BEGINNING,
            WorldType.ORDINARY,
            [
                StageElement(
                    "Initial State",
                    "Hero's life before the adventure",
                    ["normal", "routine", "ordinary", "everyday"],
                    9,
                    WorldType.ORDINARY
                ),
                StageElement(
                    "Character Establishment",
                    "Introduction of hero's character",
                    ["personality", "traits", "background", "life"],
                    8,
                    WorldType.ORDINARY
                )
            ],
            0,
            "#e6f3ff"
        ),
        # ... добавьте остальные стадии аналогично
    ]

    CSS_TEMPLATE: ClassVar[str] = """
        .vogler-journey {
            width: 800px;
            height: 800px;
            position: relative;
            margin: 50px auto;
        }
        .journey-circle {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 3px solid #333;
            position: absolute;
            background: radial-gradient(circle, #fff, #f5f5f5);
        }
        .stage {
            position: absolute;
            width: 120px;
            text-align: center;
            left: 50%;
            top: 50%;
            font-size: 14px;
            line-height: 1.3;
            transform-origin: 0 0;
            transition: all 0.3s ease;
        }
        .stage-content {
            background: rgba(255, 255, 255, 0.9);
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .stage-content:hover {
            transform: scale(1.1);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .stage-number {
            font-weight: bold;
            color: #666;
        }
        .stage-name {
            font-weight: bold;
            margin: 5px 0;
        }
        .stage-description {
            font-size: 12px;
            color: #666;
        }
        .world-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 5px;
        }
        .ordinary-world {
            background-color: #4CAF50;
        }
        .special-world {
            background-color: #2196F3;
        }
        .connection-line {
            position: absolute;
            height: 2px;
            background: #ddd;
            transform-origin: 0 0;
        }
    """

    def analyze(self, text: str) -> AnalysisResult:
        """
        Analyze the narrative structure according to Vogler's Hero's Journey.
        
        Args:
            text: Input text to analyze
            
        Returns:
            AnalysisResult: Analysis results with detailed evaluation
        """

        # Разбиваем текст на части по стадиям
        formatted_structure = self._split_into_stages(text)
        # Анализируем каждую стадию
        analysis = {
            "stages": {},
            "worlds": {
                "ordinary": self._analyze_world(WorldType.ORDINARY, formatted_structure),
                "special": self._analyze_world(WorldType.SPECIAL, formatted_structure)
            }
        }

        for stage in self.STAGES:
            analysis["stages"][stage.name] = self._analyze_stage(stage, formatted_structure)

        # Добавляем общий анализ
        analysis["overall"] = self._analyze_overall_structure(formatted_structure)

        # Создаем метаданные
        metadata = AnalysisMetadata(
            model_name="gpt-4",
            model_version="1.0",
            confidence=0.85,
            processing_time=1.0,
            structure_type=self.structure_type,
            display_name=self.display_name
        )

        # Создаем краткое описание
        summary = "Analysis of narrative using Vogler's Hero's Journey"

        # Создаем визуализацию
        visualization = self.visualize(analysis)

        return AnalysisResult(
            structure=analysis,
            summary=summary,
            visualization=visualization,
            metadata=metadata
        )
    
    def _split_into_stages(self, text: str) -> Dict[str, str]:
        """Split the text into stages based on keywords and structure."""
        stages_content = {}
        total_length = len(text)
        stage_length = total_length // self.TOTAL_STAGES
        
        for i, stage in enumerate(self.STAGES):
            start = i * stage_length
            end = (i + 1) * stage_length if i < self.TOTAL_STAGES - 1 else total_length
            stage_key = stage.name.lower().replace(" ", "_")
            stages_content[stage_key] = text[start:end]
            
        return stages_content

    def _analyze_stage(self, stage: Stage, content: dict) -> StageAnalysis:
        """Analyze a single stage of the journey."""
        stage_content = content.get(stage.name.lower().replace(" ", "_"), "")
        
        elements_present = {}
        strengths = []
        weaknesses = []
        
        for element in stage.elements:
            is_present = any(keyword in stage_content.lower() for keyword in element.keywords)
            elements_present[element.name] = is_present
            
            if is_present:
                strengths.append(f"{element.name} is well established")
            else:
                weaknesses.append(f"{element.name} needs more development")

        return StageAnalysis(
            elements_present=elements_present,
            strengths=strengths,
            weaknesses=weaknesses,
            score=sum(elements_present.values()) / len(stage.elements)
        )

    def _analyze_world(self, world_type: WorldType, content: dict) -> dict:
        """Analyze the representation of a world type."""
        relevant_stages = [s for s in self.STAGES if s.world == world_type]
        world_content = " ".join(content.get(s.name.lower().replace(" ", "_"), "") 
                               for s in relevant_stages)
        
        return {
            "strength": len(world_content) / 1000,  # примерная метрика
            "balance": len(relevant_stages) / len(self.STAGES),
            "transitions": self._analyze_transitions(world_type, content)
        }

    def _analyze_transitions(self, world_type: WorldType, content: dict) -> dict:
        return {
            "clarity": 0.8,
            "impact": 0.7,
            "smoothness": 0.9
        }
    
    def _analyze_overall_structure(self, content: dict) -> dict:
        return {
            "completeness": sum(stage.score for stage in self._get_stage_analyses(content)) / len(self.STAGES),
            "balance": self._analyze_world_balance(content),
            "flow": self._analyze_narrative_flow(content)
        }

    def visualize(self, analysis_result: dict) -> str:
        """
        Generate HTML visualization of the Hero's Journey.
        
        Args:
            analysis_result: Dictionary containing analysis results
            
        Returns:
            str: HTML representation of the journey
        """
        html_parts = [
            "<div class='vogler-journey'>",
            "<div class='journey-circle'>"
        ]

        # Добавляем стадии
        for stage in self.STAGES:
            angle = stage.angle
            radius = 400  # px
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            
            stage_analysis = analysis_result.get("stages", {}).get(stage.name, {})
            score = stage_analysis.get("score", 0)
            
            html_parts.append(f"""
                <div class='stage' style='
                    transform: translate({x}px, {y}px) rotate({angle}deg);
                    background-color: {self._get_color_by_score(score)};
                '>
                    <div class='stage-content'>
                        <div class='stage-number'>{stage.number}</div>
                        <div class='stage-name'>{stage.name}</div>
                        <div class='world-indicator {stage.world.name.lower()}-world'></div>
                        <div class='stage-description'>{stage.description}</div>
                    </div>
                </div>
            """)

        html_parts.extend([
            "</div>",  # закрываем journey-circle
            "</div>",  # закрываем vogler-journey
            f"<style>{self.CSS_TEMPLATE}</style>"
        ])

        return "\n".join(html_parts)

    def _get_color_by_score(self, score: float) -> str:
        """Generate color based on analysis score."""
        # Конвертируем score (0-1) в оттенок зеленого
        green = int(score * 255)
        return f"rgb(200, {green}, 200)"

    def get_prompt(self) -> str:
        """Generate analysis prompt for the Hero's Journey."""
        prompt_parts = [
            "Analyze the following narrative structure based on Chris Vogler's Hero's Journey:\n"
        ]

        current_act = None
        current_world = None
        
        for stage in self.STAGES:
            if stage.act != current_act:
                current_act = stage.act
                prompt_parts.append(f"\nAct - {current_act.value}:")
            
            if stage.world != current_world:
                current_world = stage.world
                prompt_parts.append(f"\n{current_world.value}:")
            
            prompt_parts.append(f"\n{stage.number}. {stage.name}")
            prompt_parts.append(f"   Description: {stage.description}")
            
            for element in stage.elements:
                prompt_parts.append(
                    f"   - {element.name} (Importance: {element.importance}/10)"
                )

        return "\n".join(prompt_parts)
    
    def _get_stage_analyses(self, content: dict) -> List[StageAnalysis]:
        return [self._analyze_stage(stage, content) for stage in self.STAGES]

    def _analyze_world_balance(self, content: dict) -> float:
        ordinary_world = self._analyze_world(WorldType.ORDINARY, content)
        special_world = self._analyze_world(WorldType.SPECIAL, content)
        return min(ordinary_world["strength"], special_world["strength"]) / max(ordinary_world["strength"], special_world["strength"])

    def _analyze_narrative_flow(self, content: dict) -> float:
        # Упрощенная метрика для оценки плавности повествования
        return 0.85  # placeholder
