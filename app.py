import streamlit as st
import pandas as pd
from modules import data_training

# Custom CSS for old money aesthetic
def apply_old_money_style():
    st.markdown("""
    <style>
        /* Base styles */
        .main, .stApp {
            background-color: #e9e5d8;
            color: #1e1e1e;
            font-family: 'Libre Baskerville', serif;
        }

        /* Headings */
        h1, h2, h3, h4, h5 {
            color: #1e1e1e;
            font-weight: 600;
        }

        /* General Text */
        p, span, div, label {
            color: #1e1e1e !important;
        }

        /* Buttons */
        .stButton>button {
            background-color: #3e3f3a;
            color: #f9f6ef;
            border-radius: 6px;
            font-family: 'Libre Baskerville', serif;
            padding: 0.5rem 1.5rem;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #5a5b54;
        }

        /* Tables */
        .stDataFrame, .stTable, table {
            background-color: #ffffff;
            color: #1e1e1e;
            border: 1px solid #cfc8b2;
            border-radius: 8px;
            padding: 1rem;
        }

        /* Sidebar */
        .sidebar .css-1d391kg, .sidebar .css-18e3th9 {
            background-color: #d7d2c0;
            color: #1e1e1e;
        }

        /* Dropdowns and inputs */
        .stSelectbox > div > div, .stMultiSelect > div > div, input {
            background-color: #ffffff;
            color: #1e1e1e;
            border: 1px solid #cfc8b2;
            border-radius: 4px;
        }

        /* Metric cards */
        .metrics-container, .brand-card {
            background-color: #fefefe;
            border: 1px solid #cfc8b2;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }

        /* Footer */
        footer {
            color: #5a5b54;
            font-size: 0.8rem;
            border-top: 1px solid #cfc8b2;
            padding-top: 1rem;
            margin-top: 2rem;
        }

        /* Optional accent */
        .accent {
            color: #395144;
        }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)


# Train the model when the app starts
model, data = data_training.run_training()

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Fashion Analytics",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom styling
    apply_old_money_style()
    
    # Two-column layout for header
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("Global Fashion Analytics")
        st.markdown("*Exclusive equity predictions for distinguished fashion houses*")
    
    # Sidebar for inputs with refined design
    with st.sidebar:
        st.markdown("### Investment Portfolio Configuration")
        st.markdown("---")
        
        # Select brand with custom styling
        st.markdown("#### Select Fashion House")
        brand_name = st.selectbox("", data['BrandName'].unique(), key="brand_selector")
        
        st.markdown("#### Select Years for Prediction")
        future_years = st.multiselect(
            "",
            options=list(range(2022, 2031)),
            default=[2022, 2023],
            key="year_selector"
        )
        
        st.markdown("---")
        predict_button = st.button("Select Years", use_container_width=True)
    
    # Main content area
    st.markdown("Brand Portfolio Analysis")
    
    # Get the selected brand's data
    brand_data = data[data['BrandName'] == brand_name].iloc[0]
    
    # Display brand information in an elegant card
    with st.container():
        st.markdown(f"""
        <div class="brand-card">
            <h3>{brand_name}</h3>
            <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                <div>
                    <p style="margin-bottom: 0.2rem; font-size: 0.9rem; color: #6b705c;">CURRENT MARKET POSITION</p>
                    <p style="font-size: 1.2rem; font-weight: bold;">{brand_data.get('MarketPosition', 'Premium')}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display predictions when button is clicked
    if predict_button and future_years:
        # Make predictions for future years
        future_equities = data_training.predict_future_equity(brand_data, future_years)
        
        # Create predictions dataframe
        predictions_df = pd.DataFrame({
            'Year': future_years,
            'Predicted Equity': future_equities
        })
        
        st.markdown(f"""
        <div class="metrics-container">
            <h3>Equity Forecast for {brand_name}</h3>
            <p style="font-style: italic; color: #6b705c; margin-bottom: 1.5rem;">
                Exclusive projections based on historical performance and market indicators
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display predictions in an elegant table
        st.markdown("### Detailed Equity Projections")
        
        # Custom styling for the table
        predictions_df['Formatted Equity'] = predictions_df['Predicted Equity'].apply(lambda x: f"${x:,.2f}")
        
        # Display only the relevant columns with proper formatting
        display_df = predictions_df[['Year', 'Formatted Equity']].rename(
            columns={'Formatted Equity': 'Projected Equity'}
        )
        
        st.table(display_df)
        
        # Key insights section
        st.markdown("### Key Insights")
        
        max_year = predictions_df.loc[predictions_df['Predicted Equity'].idxmax(), 'Year']
        max_equity = predictions_df['Predicted Equity'].max()
        
        col1, col2 = st.columns(2)
        
     
        st.markdown(f"""
        <div style="background-color: #ffffff; padding: 1.5rem; border: 1px solid #d1c9b0;">
            <p style="margin-bottom: 0.2rem; font-size: 0.9rem; color: #6b705c;">PROJECTED PEAK EQUITY</p>
            <p style="font-size: 1.4rem; font-weight: bold;">${max_equity:,.2f}</p>
            <p style="font-size: 0.9rem;">Expected in {max_year}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendations section (always visible)
    st.markdown("### Investment Recommendations")
    st.markdown("""
    <div style="background-color: #ffffff; padding: 1.5rem; border: 1px solid #d1c9b0;">
        <p>Our analysis suggests maintaining a diversified portfolio across luxury fashion houses.
        Current market conditions favor heritage brands with established market presence and sustainable practices.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <footer>
        <p>© 2025 Prestigious Investments Ltd. All rights reserved.</p>
    </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()