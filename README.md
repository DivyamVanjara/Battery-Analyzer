# 🔋 Battery Cell Analyzer

A simple and interactive tool to configure and analyze battery cell performance.  
Built with Python and Streamlit for rapid prototyping and real-time analysis.

---

## 👈 Get Started

Use the **sidebar** to:
- Configure your battery cells
- Select cell types (LFP or MNC)
- Input current values
- Click **"Analyze Cells"** to view real-time insights

---

## 📖 How to Use

1. **Configure Cells**  
   Use the sidebar to input cell configuration details.

2. **Select Cell Types**  
   Choose between:
   - `LFP (Lithium Iron Phosphate)`
   - `MNC (Lithium Manganese Cobalt)`

3. **Set Current Values**  
   Input the current (in Amperes) for each configured cell.

4. **Analyze**  
   Click the **"Analyze Cells"** button to process and analyze your inputs.

5. **Review Results**  
   Get real-time performance insights including:
   - Voltage
   - Temperature (if applicable)
   - Capacity calculations

---

## 🔋 Cell Type Information

### LFP (Lithium Iron Phosphate)
- **Nominal Voltage:** 3.2V  
- **Voltage Range:** 2.8V – 4.0V  
- **Characteristics:** Stable, long-lasting, safer chemistry

### MNC (Lithium Manganese Cobalt)
- **Nominal Voltage:** 3.6V  
- **Voltage Range:** 3.2V – 3.4V  
- **Characteristics:** Higher energy density, good performance

---

## 💡 Tech Stack
- **Python**
- **Streamlit** for UI & interactivity

---

## 🚀 Run Locally

Make sure you have [Streamlit](https://streamlit.io/) installed:

```bash
pip install streamlit
