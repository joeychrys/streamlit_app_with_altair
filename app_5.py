import streamlit as st
import yfinance as yf
import altair as alt 
from ta import volume

st.set_page_config(page_title='Technical Analysis',page_icon='📈')
hide_streamlit_style = """
            <style>
            #MainMenu {

                visibility: hidden;
               
               }
            footer {

                visibility: hidden;

                }
            footer:after {

	            content:'Data Source: Yahoo Finance'; 
	            visibility: visible;
	            display: block;
	            position: relative;
	            #background-color: red;
	            padding: 5px;
	            top: 2px;

                }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

stock = st.sidebar.text_input(label="Ticker",value='AAPL')

@st.cache(allow_output_mutation=True, show_spinner=False)
def get_data(start):
    ticker = yf.Ticker(stock)
    try:
        df = ticker.history(period='max', start=start)
    except:
        pass
    return df

list_of_indicator_types = ['Volume', 'Trend']
volumn_types = ['Volume','Force Index']
trend_types = ['Simple Moving Average','RSI']

indicator_types = st.sidebar.selectbox(label='Indicator Type', options = list_of_indicator_types)

st.sidebar.success('All charts are interactive!')

if indicator_types == 'Volume':
    indicator = st.selectbox(label='Indicator', options=volumn_types)

    start = st.text_input(label='Start Year', value = '2018')
    start = f'{start}-01-01'

    df = get_data(start)
    df = df.reset_index()

    if indicator == 'Volume':
        brush = alt.selection(type='interval', encodings=['x'])
        price_base = alt.Chart(data=df).mark_line().encode(
            alt.X(
                'Date:T',
                title=None
            ), 
            alt.Y(
                'Close:Q',
                title = 'Adj Close Price'
                )
            ).properties(
                width=600,
                height=400)
        volume_graph = alt.Chart(data=df).mark_bar().encode(
                alt.X(
                    'Date:T',
                    scale = alt.Scale(domain=brush)
                ),
                alt.Y(
                    'Volume:Q',
                    axis=None
                )
                ).properties(
                    width=600,
                    height=100)
            
        price_with_selection = price_base.add_selection(brush)
        price_with_selection & volume_graph
    
    if indicator == 'Force Index':
        window_slider_expander = st.beta_expander(label='Force Index Parameters')
        window_slider = window_slider_expander.slider(label='Window', value=13, min_value=1, max_value=20)

        df['fi'] = volume.force_index(close=df['Close'],volume=df['Volume'], window=window_slider)

        brush = alt.selection(type='interval', encodings=['x'])
        price_base = alt.Chart(data=df).mark_line().encode(
            alt.X(
                'Date:T',
                title=None
            ), 
            alt.Y(
                'Close:Q',
                title = 'Adj Close Price'
                )
            ).properties(
                width=600,
                height=400)
        fi_chart_base = alt.Chart(df).mark_area().encode(
            alt.X(
                'Date:T',
                scale= alt.Scale(domain=brush)
                ),
            alt.Y(
                'fi:Q',
                axis=None,
            )
        ).properties(
            width=600,
            height=150
        )
        price_with_selection = price_base.add_selection(brush)
        price_with_selection & fi_chart_base

if indicator_types == 'Trend':
    indicator = st.selectbox(label='Indicator', options=trend_types)
    
    if indicator == 'Simple Moving Average':
        st.success('Coming Soon!')

    if indicator == 'RSI':
        st.success('Coming Soon!')
