import plotly.graph_objects as go
import plotly.express as px
from config import COLORS
import pandas as pd

def create_sentiment_gauge(sentiment_score):
    """
    Create an animated gauge chart for sentiment score
    
    Args:
        sentiment_score: float between 0-1
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=sentiment_score * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Sentiment Score", 'font': {'size': 24, 'color': COLORS['text']}},
        delta={'reference': 50, 'increasing': {'color': COLORS['positive']}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': COLORS['text']},
            'bar': {'color': COLORS['accent']},
            'bgcolor': COLORS['secondary_bg'],
            'borderwidth': 2,
            'bordercolor': COLORS['text'],
            'steps': [
                {'range': [0, 40], 'color': COLORS['negative']},
                {'range': [40, 60], 'color': COLORS['neutral']},
                {'range': [60, 100], 'color': COLORS['positive']}
            ],
            'threshold': {
                'line': {'color': COLORS['text'], 'width': 4},
                'thickness': 0.75,
                'value': sentiment_score * 100
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor=COLORS['primary_bg'],
        plot_bgcolor=COLORS['primary_bg'],
        font={'color': COLORS['text'], 'family': 'Inter'},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_aspect_analysis_chart(aspects_data):
    """
    Create horizontal bar chart for aspect-based analysis
    
    Args:
        aspects_data: dict with aspect names as keys and sentiment scores as values
    """
    df = pd.DataFrame(list(aspects_data.items()), columns=['Aspect', 'Score'])
    df['Color'] = df['Score'].apply(lambda x: 
        COLORS['positive'] if x > 0.6 else 
        COLORS['negative'] if x < 0.4 else 
        COLORS['neutral']
    )
    
    fig = px.bar(
        df,
        x='Score',
        y='Aspect',
        orientation='h',
        color='Score',
        color_continuous_scale=[
            [0, COLORS['negative']],
            [0.5, COLORS['neutral']],
            [1, COLORS['positive']]
        ],
        title="Product Aspects Analysis"
    )
    
    fig.update_layout(
        paper_bgcolor=COLORS['primary_bg'],
        plot_bgcolor=COLORS['secondary_bg'],
        font={'color': COLORS['text'], 'family': 'Inter'},
        title_font_size=20,
        showlegend=False,
        height=400,
        xaxis=dict(range=[0, 1], title="Sentiment Score"),
        yaxis=dict(title=""),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_sentiment_distribution(positive_prob, neutral_prob, negative_prob):
    """Create donut chart for sentiment distribution"""
    labels = ['Positive', 'Neutral', 'Negative']
    values = [positive_prob, neutral_prob, negative_prob]
    colors = [COLORS['positive'], COLORS['neutral'], COLORS['negative']]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        marker_colors=colors,
        textinfo='label+percent',
        textfont_size=14
    )])
    
    fig.update_layout(
        title="Sentiment Distribution",
        title_font_size=20,
        paper_bgcolor=COLORS['primary_bg'],
        plot_bgcolor=COLORS['primary_bg'],
        font={'color': COLORS['text'], 'family': 'Inter'},
        height=350,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=20, r=20, t=50, b=50)
    )
    
    return fig
