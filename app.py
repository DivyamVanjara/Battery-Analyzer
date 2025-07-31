import streamlit as st
import random
import pandas as pd
from typing import Dict, List, Tuple

st.set_page_config(
    page_title="Battery Cell Analyzer",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .cell-result {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    
    .cell-result.mnc {
        border-left-color: #dc3545;
    }
    
    .stSelectbox > div > div {
        background-color: #f8f9fa;
    }
    
    .stNumberInput > div > div {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

def calculate_cell_parameters(cell_type: str, current: float) -> Dict:
    """Calculate battery cell parameters based on type and current"""
    
    # Voltage based on cell type
    if cell_type.upper() == "LFP":
        voltage = 3.2
        max_voltage = 4.0
        min_voltage = 2.8
    else:  # MNC
        voltage = 3.6
        max_voltage = 3.4
        min_voltage = 3.2
    
    temperature = round(random.uniform(25, 40), 1)
    
    capacity = round(voltage * current, 2)
    
    if max_voltage > min_voltage:
        voltage_range_percent = round(((voltage - min_voltage) / (max_voltage - min_voltage)) * 100, 1)
    else:
        voltage_range_percent = 50.0 
    
    return {
        "voltage": voltage,
        "current": current,
        "temperature": temperature,
        "capacity": capacity,
        "max_voltage": max_voltage,
        "min_voltage": min_voltage,
        "voltage_range_percent": voltage_range_percent
    }

def display_cell_result(cell_id: int, cell_type: str, params: Dict):
    """Display individual cell results in a styled card"""
    
    css_class = "mnc" if cell_type.upper() == "MNC" else ""
    
    st.markdown(f"""
    <div class="cell-result {css_class}">
        <h4>🔋 Cell {cell_id} ({cell_type})</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Voltage", f"{params['voltage']}V")
        
    with col2:
        st.metric("Current", f"{params['current']}A")
        
    with col3:
        st.metric("Temperature", f"{params['temperature']}°C")
        
    with col4:
        st.metric("Capacity", f"{params['capacity']} Wh")
    

    st.write("**Voltage Range:**")
    progress_value = max(0.0, min(1.0, params['voltage_range_percent'] / 100))
    st.progress(progress_value)
    st.write(f"Range: {params['min_voltage']}V - {params['max_voltage']}V (Current: {params['voltage']}V)")

def main():

    st.markdown("""
    <div class="main-header">
        <h1>🔋 Battery Cell Analyzer</h1>
        <p>Configure your battery cells and analyze their performance</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.header("⚙️ Cell Configuration")
    st.sidebar.write("Configure up to 8 battery cells for analysis")
    
    num_cells = st.sidebar.slider("Number of cells to analyze", 1, 8, 3)
    
    cells_data = []
    
    st.sidebar.subheader("Cell Settings")
    
    for i in range(num_cells):
        st.sidebar.write(f"**Cell {i+1}**")
        
        cell_type = st.sidebar.selectbox(
            f"Cell {i+1} Type",
            ["LFP", "MNC"],
            key=f"type_{i}",
            help="LFP: Lithium Iron Phosphate, MNC: Lithium Manganese Cobalt"
        )
        
        current = round(st.sidebar.number_input(
            f"Cell {i+1} Current (A)",
            min_value=0.1,
            max_value=10.0,
            value=2.0,
            step=0.1,
            key=f"current_{i}"
        ),2)
        
        cells_data.append({
            "id": i + 1,
            "type": cell_type,
            "current": current
        })
        
        st.sidebar.write("---")
    
    if st.sidebar.button("🔍 Analyze Cells", type="primary"):
        st.session_state.analyze = True
    
    if hasattr(st.session_state, 'analyze') and st.session_state.analyze:
        
        results = []
        for cell in cells_data:
            params = calculate_cell_parameters(cell["type"], cell["current"])
            results.append({
                "id": cell["id"],
                "type": cell["type"],
                **params
            })
        
        st.header("📊 Analysis Summary")
        
        total_capacity = sum(result["capacity"] for result in results)
        avg_temperature = round(sum(result["temperature"] for result in results) / len(results), 1)
        peak_voltage = max(result["voltage"] for result in results)
        cell_count = len(results)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Capacity", f"{total_capacity} Wh")
            
        with col2:
            st.metric("Avg Temperature", f"{avg_temperature}°C")
            
        with col3:
            st.metric("Peak Voltage", f"{peak_voltage}V")
            
        with col4:
            st.metric("Cell Count", f"{cell_count}")
        
        st.write("---")
        
        st.header("🔋 Individual Cell Results")
        
        for result in results:
            display_cell_result(result["id"], result["type"], result)
            st.write("")
        
        st.header("📋 Data Table")
        
        df_data = []
        for result in results:
            df_data.append({
                "Cell ID": result["id"],
                "Type": result["type"],
                "Voltage (V)": result["voltage"],
                "Current (A)": result["current"],
                "Temperature (°C)": result["temperature"],
                "Capacity (Wh)": result["capacity"],
                "Min Voltage (V)": result["min_voltage"],
                "Max Voltage (V)": result["max_voltage"]
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="battery_cell_analysis.csv",
            mime="text/csv"
        )
        
        st.header("📈 Cell Type Distribution")
        
        type_counts = df["Type"].value_counts()
        st.bar_chart(type_counts)
        
        st.header("⚡ Capacity Comparison")
        
        capacity_data = df.set_index("Cell ID")["Capacity (Wh)"]
        st.bar_chart(capacity_data)
        
    else:
        st.info("👈 Configure your battery cells in the sidebar and click 'Analyze Cells' to get started!")
        
        st.header("📖 How to Use")
        
        st.write("""
        1. **Configure Cells**: Use the sidebar to set up your battery cells
        2. **Select Cell Types**: Choose between LFP (Lithium Iron Phosphate) and MNC (Lithium Manganese Cobalt)
        3. **Set Current Values**: Enter the current for each cell in Amperes
        4. **Analyze**: Click the 'Analyze Cells' button to process your data
        5. **Review Results**: View detailed analysis including voltage, temperature, and capacity calculations
        """)
        
        st.header("🔋 Cell Type Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("LFP (Lithium Iron Phosphate)")
            st.write("""
            - **Nominal Voltage**: 3.2V
            - **Voltage Range**: 2.8V - 4.0V
            - **Characteristics**: Stable, long-lasting, safer chemistry
            """)
            
        with col2:
            st.subheader("MNC (Lithium Manganese Cobalt)")
            st.write("""
            - **Nominal Voltage**: 3.6V
            - **Voltage Range**: 3.2V - 3.4V
            - **Characteristics**: Higher energy density, good performance
            """)

if __name__ == "__main__":
    main()

