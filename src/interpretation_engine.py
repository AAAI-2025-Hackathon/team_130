from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME
from src.prompts import ART_INTERPRETER_SYSTEM_PROMPT, get_analysis_prompt

class ArtworkInterpreter:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
    
    def interpret_features(self, color_stats, texture_stats, composition_stats):
        prompt = get_analysis_prompt(color_stats, texture_stats, composition_stats)
        
        completion = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": ART_INTERPRETER_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        return completion.choices[0].message.content
    
    def _get_system_prompt(self):
        return """You are an expert art therapist with deep knowledge of color psychology, 
        art therapy principles, and emotional interpretation of artwork. Your role is to analyze 
        artwork features and provide meaningful psychological and emotional interpretations.
        
        Consider these established art therapy principles:
        - Colors can reflect emotional states and psychological conditions
        - Texture patterns may indicate stress levels and emotional regulation
        - Composition elements can reveal cognitive organization and emotional balance
        - Line quality can indicate energy levels and emotional stability
        
        Provide thoughtful, nuanced interpretations while maintaining professional boundaries 
        and acknowledging the subjective nature of art analysis."""

    def _create_analysis_prompt(self, color_stats, texture_stats, composition_stats):
        return f"""Please analyze the following artwork features and provide an interpretation 
        of the potential emotional and psychological aspects they might reveal. 
        
        Color Analysis:
        - Red Channel: mean={color_stats['r']['mean']:.2f}, std={color_stats['r']['std']:.2f}
        - Green Channel: mean={color_stats['g']['mean']:.2f}, std={color_stats['g']['std']:.2f}
        - Blue Channel: mean={color_stats['b']['mean']:.2f}, std={color_stats['b']['std']:.2f}
        
        Texture Analysis:
        - Contrast: {texture_stats['contrast']:.2f}
        - Homogeneity: {texture_stats['homogeneity']:.2f}
        - Energy: {texture_stats['energy']:.2f}
        
        Composition Analysis:
        - Edge Density: {composition_stats['edge_density']:.2f}
        - Symmetry Score: {composition_stats['symmetry_score']:.2f}
        
        Please provide:
        1. Color Interpretation: What might the color usage suggest about emotional state?
        2. Texture Analysis: What could the texture patterns reveal about emotional expression?
        3. Composition Insights: What might the structural elements suggest about cognitive/emotional organization?
        4. Overall Interpretation: Synthesize the above elements into a cohesive analysis
        
        Format the response in clear sections and maintain a professional, thoughtful tone.""" 