import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.image_analysis import ImageAnalyzer
from src.interpretation_engine import ArtworkInterpreter
from src.report_generator import ReportGenerator
from src.pdf_generator import generate_pdf_report
import io

def create_emotion_radar_chart(interpretation):
    # Extract emotional scores (this is a simplified example - you'll need to 
    # modify based on your actual interpretation structure)
    emotions = {
        'Joy': 0.7,
        'Calm': 0.5,
        'Energy': 0.8,
        'Tension': 0.3,
        'Expression': 0.6
    }
    
    fig = go.Figure(data=go.Scatterpolar(
        r=list(emotions.values()),
        theta=list(emotions.keys()),
        fill='toself'
    ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=False,
        title="Emotional Expression Profile"
    )
    return fig

def create_color_distribution_chart(color_stats):
    colors = ['Red', 'Green', 'Blue']
    means = [color_stats['r']['mean'], color_stats['g']['mean'], color_stats['b']['mean']]
    
    fig = go.Figure(data=[
        go.Bar(name='Color Intensity', x=colors, y=means,
               marker_color=['red', 'green', 'blue'])
    ])
    
    fig.update_layout(
        title="Color Distribution",
        yaxis_title="Intensity",
        showlegend=False
    )
    return fig

def extract_key_points(interpretation):
    # This is a placeholder - you'll need to modify based on your actual interpretation
    return {
        "Emotional State": [
            "Predominantly positive emotional expression",
            "Signs of creative energy and vitality",
            "Balanced emotional regulation"
        ],
        "Cognitive Patterns": [
            "Structured thinking approach",
            "Good problem-solving indicators",
            "Creative flexibility present"
        ],
        "Behavioral Insights": [
            "Active engagement with the process",
            "Balanced energy levels",
            "Positive social indicators"
        ]
    }

def main():
    st.title("Art Therapy Analysis Tool")
    st.write("Upload your artwork for analysis and interpretation")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Create tabs
        upload_tab, analysis_tab, interpretation_tab, report_tab = st.tabs([
            "Uploaded Image", 
            "Technical Analysis", 
            "Interpretation", 
            "Final Report"
        ])
        
        # Tab 1: Uploaded Image
        with upload_tab:
            st.subheader("Your Artwork")
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Artwork", use_column_width=True)
        
        with st.spinner("Analyzing artwork..."):
            # Perform analysis
            analyzer = ImageAnalyzer(image)
            color_stats = analyzer.analyze_colors()
            texture_stats = analyzer.analyze_texture()
            composition_stats = analyzer.analyze_composition()
            
            # Generate interpretation
            interpreter = ArtworkInterpreter()
            interpretation = interpreter.interpret_features(
                color_stats, texture_stats, composition_stats
            )
            
            # Generate final report
            report_gen = ReportGenerator()
            report = report_gen.generate_report(interpretation)
            
            # Tab 2: Technical Analysis
            with analysis_tab:
                st.subheader("Technical Analysis Results")
                
                # Color Analysis
                st.write("🎨 Color Analysis")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Red Channel Mean", f"{color_stats['r']['mean']:.2f}")
                with col2:
                    st.metric("Green Channel Mean", f"{color_stats['g']['mean']:.2f}")
                with col3:
                    st.metric("Blue Channel Mean", f"{color_stats['b']['mean']:.2f}")
                
                # Texture Analysis
                st.write("🔍 Texture Analysis")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Contrast", f"{texture_stats['contrast']:.2f}")
                with col2:
                    st.metric("Homogeneity", f"{texture_stats['homogeneity']:.2f}")
                with col3:
                    st.metric("Energy", f"{texture_stats['energy']:.2f}")
                
                # Composition Analysis
                st.write("📐 Composition Analysis")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Edge Density", f"{composition_stats['edge_density']:.2f}")
                with col2:
                    st.metric("Symmetry Score", f"{composition_stats['symmetry_score']:.2f}")
                
                with st.expander("View Raw Data"):
                    st.json({
                        "color_analysis": color_stats,
                        "texture_analysis": texture_stats,
                        "composition_analysis": composition_stats
                    })
            
            # Tab 3: Interpretation
            with interpretation_tab:
                st.subheader("Artwork Interpretation")
                
                # Create two columns for the charts
                col1, col2 = st.columns(2)
                
                with col1:
                    # Emotion Radar Chart
                    emotion_chart = create_emotion_radar_chart(interpretation)
                    st.plotly_chart(emotion_chart, use_container_width=True)
                
                with col2:
                    # Color Distribution Chart
                    color_chart = create_color_distribution_chart(color_stats)
                    st.plotly_chart(color_chart, use_container_width=True)
                
                # Key Points Section
                st.subheader("🎯 Key Insights")
                key_points = extract_key_points(interpretation)
                
                # Display key points in columns
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("💭 Emotional State")
                    for point in key_points["Emotional State"]:
                        st.write(f"• {point}")
                        
                with col2:
                    st.write("🧠 Cognitive Patterns")
                    for point in key_points["Cognitive Patterns"]:
                        st.write(f"• {point}")
                        
                with col3:
                    st.write("🔄 Behavioral Insights")
                    for point in key_points["Behavioral Insights"]:
                        st.write(f"• {point}")
                
                # Progress Indicators
                st.subheader("📊 Analysis Metrics")
                metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                
                with metrics_col1:
                    st.metric(
                        label="Expression Level",
                        value="High",
                        delta="Positive"
                    )
                
                with metrics_col2:
                    st.metric(
                        label="Emotional Balance",
                        value="Moderate",
                        delta="Stable"
                    )
                
                with metrics_col3:
                    st.metric(
                        label="Creative Energy",
                        value="High",
                        delta="↗️"
                    )
                
                # Detailed interpretation in expander
                with st.expander("📝 See Detailed Interpretation"):
                    st.write(interpretation)
                    
                    st.info("""
                    This detailed interpretation provides in-depth analysis of your artwork. 
                    Remember that art interpretation is subjective and should be used as a 
                    tool for self-reflection and discussion with mental health professionals.
                    """)
                
                # Additional context and resources
                with st.expander("🔍 Understanding Your Results"):
                    st.write("""
                    ### How to Use These Insights
                    - Use these insights as starting points for self-reflection
                    - Consider discussing patterns with a mental health professional
                    - Remember that art interpretation is subjective
                    - Focus on patterns rather than individual elements
                    
                    ### Key Terms
                    - **Expression Level**: Overall emotional communication in the artwork
                    - **Emotional Balance**: Distribution of emotional elements
                    - **Creative Energy**: Level of engagement and vitality in creation
                    """)
            
            # Tab 4: Final Report
            with report_tab:
                st.subheader("Comprehensive Report")
                st.write("📊 Detailed Analysis Report")
                st.write(report)
                
                # Generate and offer PDF download
                pdf = generate_pdf_report(interpretation, report)
                pdf_output = io.BytesIO()
                pdf.output(pdf_output)
                pdf_bytes = pdf_output.getvalue()
                
                st.download_button(
                    label="📥 Download Detailed Report (PDF)",
                    data=pdf_bytes,
                    file_name="art_therapy_analysis.pdf",
                    mime="application/pdf",
                    help="Download a comprehensive PDF report of your artwork analysis"
                )
                
                st.warning(
                    "⚠️ Note: This analysis is meant for self-reflection and should not be "
                    "considered as professional psychological advice. Please consult with "
                    "a qualified art therapist for professional interpretation."
                )

if __name__ == "__main__":
    main() 