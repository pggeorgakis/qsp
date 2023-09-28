import matplotlib.pyplot as plt
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go
import pandas as pd
import streamlit as st


def plot_mesh_pass(data):
    plt.figure(figsize=(18, 6))
    real_line, = plt.plot(data.index, data['325 Mesh Pass'], label='325 Mesh Pass', c='gray', linestyle='--')
    real_line.set_dashes([4, 4])
    plt.plot(data.index, data['325 Mesh Pass Optimized'], label='325 Mesh Pass Optimized', c='teal', linewidth=2)
    plt.xlabel('Datetime')
    plt.ylabel('325 Mesh Pass (%)')
    plt.grid()
    plt.legend()
    plt.show()
    

def plot_strength(data):
    plt.figure(figsize=(18, 6))
    real_line, = plt.plot(data.index, data['1 Day'], label='Compressive Strength 1D', c='gray', linestyle='--')
    real_line.set_dashes([4, 4])
    plt.plot(data.index, data['1 Day Strength Pred.'], label='Compressive Strength 1D Pred.', c='teal', linewidth=2)
    plt.xlabel('Datetime')
    plt.ylabel('Compressive Strength (PSI)')
    plt.grid()
    plt.legend()
    plt.show()
    
    
def plot_mesh_pass_plotly(data):
    fig = px.line(data, x=data.index, y=['325 Mesh Pass', '325 Mesh Pass Optimized'], 
                  labels={'index': 'Datetime', 'value': '325 Mesh Pass (%)'},
                  title='325 Mesh Pass')
    fig.update_traces(line=dict(dash='dash'), selector=dict(name='325 Mesh Pass'))
    fig.update_xaxes(title_text='Datetime')
    fig.update_yaxes(title_text='325 Mesh Pass (%)')
    fig.update_layout(width=1500,
                      height=300,
                      showlegend=True)
    return fig

def plot_strength_plotly(data):
    fig = px.line(data, x='Datetime', y=['1 Day', '1 Day Strength Pred.'], labels={'Datetime': 'Datetime', 'value': 'Compressive Strength (PSI)'})
    fig.update_traces(line=dict(dash='dash'), selector=dict(name='1 Day'))
    # Change line colors
    fig.update_traces(line=dict(color='gray'), selector=dict(name='1 Day'))
    fig.update_traces(line=dict(color='red'), selector=dict(name='1 Day Strength Pred.'))
    
    # Add the title to the figure
    fig.update_layout(
        title="Compressive Strength 1D",
        xaxis_title="Datetime",
        yaxis_title="Compressive Strength (PSI)",
        width=1500,
        height=300,
        showlegend=True)
    return fig


@st.cache_data
def combined_plot(data_filtered):
    data_filtered['Datetime'] = pd.to_datetime(data_filtered['Datetime'])
    # Create a subplot with shared x-axis
    fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

    # Add "Compressive Strength" traces to the second subplot
    fig.add_trace(go.Scatter(x=data_filtered['Datetime'], 
                             y=data_filtered['1 Day'],
                            mode='markers', 
                            name='1 Day Strength',
                            line=dict(width=1, color='red'),
                            marker=dict(symbol='circle-open', size=8, color='black', line=dict(width=1.5))), 
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=data_filtered['Datetime'], 
                             y=data_filtered['1 Day Strength Pred.'],
                             mode='lines+markers', 
                             name='1 Day Strength Pred.',
                             line=dict(width=1, color='red'),
                             marker=dict(symbol='circle', size=8, color='red', line=dict(width=0))),
                  row=1, col=1)
    
            # Add "325 Mesh Pass" traces to the first subplot
    fig.add_trace(go.Scatter(x=data_filtered['Datetime'], 
                             y=data_filtered['325 Mesh Pass'],
                             name='325 Mesh Pass', 
                             mode='markers',
                             line=dict(width=1, color='red'),
                             marker=dict(symbol='circle-open', size=8, color='gray', line=dict(width=1))),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=data_filtered['Datetime'], 
                             y=data_filtered['325 Mesh Pass Optimized'],
                             mode='lines+markers', 
                             name='325 Mesh Pass Target', 
                             line=dict(width=1, color='teal'),
                             marker=dict(symbol='circle', size=8, color='teal', line=dict(width=0))),
                  row=2, col=1)

    # Update subplot titles and axis labels
    fig.update_layout(
        title_text="",
        xaxis2=dict(title="Datetime",
                    tickformat='%B %-d'),
        yaxis1=dict(title="Compressive Strength (PSI)"),
        yaxis2=dict(title="325 Mesh Pass (%)"),
        width=1500,
        height=600,
        showlegend=True)
    return fig

