import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.image_analysis import ImageAnalyzer

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

def main():
    st.title("Art Therapy Analysis Tool")
    st.write("Upload your artwork for analysis and interpretation")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Create tabs
        upload_tab, analysis_tab = st.tabs([
            "Uploaded Image", 
            "Technical Analysis"
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

if __name__ == "__main__":
    main() 