import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def main():
    st.set_page_config(page_title="Interactive Gap Analysis Tool", layout="wide")

    st.title("Interactive Gap Analysis Tool")

    st.write("""
    This tool allows you to perform a basic gap analysis for your organization. 
    Use the information provided as a guide to input your own data and visualize the gaps.
    """)

    # Sidebar with information
    st.sidebar.header("Gap Analysis Guide")
    st.sidebar.write("""
    Gap analysis involves comparing actual performance with potential or desired performance.
    It can be conducted from different perspectives:
    - Organization (e.g., Human Resources)
    - Business direction
    - Business processes
    - Information technology
    """)

    # User input for organization name
    organization_name = st.text_input("Enter your organization name:")

    # Select analysis type
    analysis_type = st.selectbox("Select the type of gap analysis:", 
                                 ["Usage Gap", "Product Gap", "Performance Gap"])

    if analysis_type == "Usage Gap":
        usage_gap_analysis()
    elif analysis_type == "Product Gap":
        product_gap_analysis()
    else:
        performance_gap_analysis()

def usage_gap_analysis():
    st.header("Usage Gap Analysis")
    st.write("""
    The usage gap is the difference between the total potential for the market and 
    actual current usage by all consumers in the market.
    """)

    market_potential = st.number_input("Enter the total market potential:", min_value=0, value=100)
    current_usage = st.number_input("Enter the current market usage:", min_value=0, value=75)

    usage_gap = market_potential - current_usage

    fig, ax = plt.subplots()
    ax.bar(["Market Potential", "Current Usage", "Usage Gap"], [market_potential, current_usage, usage_gap])
    ax.set_ylabel("Market Size")
    st.pyplot(fig)

    st.write(f"The usage gap is: {usage_gap}")
    st.write(f"This represents {usage_gap/market_potential:.2%} of the market potential.")

def product_gap_analysis():
    st.header("Product Gap Analysis")
    st.write("""
    The product gap is the part of the market an organization is excluded from due to 
    product or service characteristics.
    """)

    total_market_segments = st.number_input("Enter the total number of market segments:", min_value=1, value=5)
    covered_segments = st.number_input("Enter the number of segments your products cover:", min_value=0, max_value=total_market_segments, value=3)

    product_gap = total_market_segments - covered_segments

    fig, ax = plt.subplots()
    ax.pie([covered_segments, product_gap], labels=['Covered Segments', 'Product Gap'], autopct='%1.1f%%')
    ax.set_title("Market Segment Coverage")
    st.pyplot(fig)

    st.write(f"Your products cover {covered_segments} out of {total_market_segments} segments.")
    st.write(f"The product gap is {product_gap} segments, or {product_gap/total_market_segments:.2%} of the market.")

def performance_gap_analysis():
    st.header("Performance Gap Analysis")
    st.write("""
    Performance gap analysis compares your current performance with your desired performance 
    across various metrics.
    """)

    metrics = st.text_area("Enter performance metrics (one per line):", 
                           "Revenue\nCustomer Satisfaction\nMarket Share\nProductivity")
    metrics = metrics.split('\n')

    data = {'Metric': metrics, 'Current': [0]*len(metrics), 'Target': [0]*len(metrics)}
    df = pd.DataFrame(data)

    for i, metric in enumerate(metrics):
        col1, col2 = st.columns(2)
        with col1:
            df.loc[i, 'Current'] = st.number_input(f"Current {metric}:", key=f"current_{i}", value=50)
        with col2:
            df.loc[i, 'Target'] = st.number_input(f"Target {metric}:", key=f"target_{i}", value=75)

    df['Gap'] = df['Target'] - df['Current']

    st.write("Performance Gap Analysis:")
    st.dataframe(df)

    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(metrics))
    width = 0.35
    ax.bar([i - width/2 for i in x], df['Current'], width, label='Current')
    ax.bar([i + width/2 for i in x], df['Target'], width, label='Target')
    ax.set_ylabel('Performance')
    ax.set_title('Current vs Target Performance')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, rotation=45, ha='right')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

if __name__ == "__main__":
    main()
