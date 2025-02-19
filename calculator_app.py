import streamlit as st
import pandas as pd

# Custom Styling
st.markdown("""
    <style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .cost-table th { background-color: #f4f4f4; font-size: 18px; font-weight: bold; text-align: center; }
    .cost-table td { font-size: 16px; text-align: right; }
    </style>
""", unsafe_allow_html=True)

# Title and Header
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>📦 3PL Cost Calculator</h1>", unsafe_allow_html=True)
st.markdown("---")

# **User Inputs - Operational Metrics**
st.header("⚙️ Operational Metrics (Per Month)")

# Using Columns for Better Alignment
col1, col2 = st.columns(2)
with col1:
    orders_per_month = st.number_input("Orders Per Month", min_value=0.0, format="%.2f")
    storage_space = st.number_input("Storage Space Required (Avg per month)", min_value=0.0, format="%.2f")
    goods_in_cartons = st.number_input("Goods in per month (cartons)", min_value=0.0, format="%.2f")
    
with col2:
    units_per_order = st.number_input("Units Per Order", min_value=0.0, format="%.2f")
    goods_in_pallets = st.number_input("Goods in per month (pallets)", min_value=0.0, format="%.2f")
    kits_per_month = st.number_input("Number of kits per month", min_value=0.0, format="%.2f")

# Pricing Data
pricing = {
    "Management Fee": 250.00,
    "Pick and Pack": {
        "First Item": 1.10,
        "Additional items": 0.45,
        "Delivery Note": 0.22,
        "Pallet Pick": 5.00,
        "Carton - First Carton Pick": 1.10,
        "Carton - Additional Carton Pick": 0.40,
        "Kitting Fee (Per Kit)": 0.60
    },
    "Packaging": {
        "Paper Packaging/ Void Fill": 0.33,
        "Pallets": 7.15
    },
    "Storage": {
        "Per Pallet Per Week": 3.00
    },
    "Goods In": {
        "Per Unit": 0.20,
        "Single SKU Carton Per Carton": 1.45,
        "Single SKU Pallet Per Pallet": 4.00,
        "Courier Fee (per order based on >30KG)": 4.50
    }
}

# **Calculate Costs**
if st.button("🧮 Calculate Costs"):
    
    # Pick and Pack Costs
    pick_first_item = orders_per_month * pricing["Pick and Pack"]["First Item"]
    pick_additional_items = orders_per_month * (units_per_order - 1) * pricing["Pick and Pack"]["Additional items"]
    pallet_pick = goods_in_pallets * pricing["Pick and Pack"]["Pallet Pick"]
    carton_first_pick = goods_in_cartons * pricing["Pick and Pack"]["Carton - First Carton Pick"]
    kitting_fee = kits_per_month * pricing["Pick and Pack"]["Kitting Fee (Per Kit)"]

    pick_and_pack_total = sum([
        pick_first_item,
        pick_additional_items,
        pricing["Pick and Pack"]["Delivery Note"],
        pallet_pick,
        carton_first_pick,
        pricing["Pick and Pack"]["Carton - Additional Carton Pick"],
        kitting_fee
    ])

    # Packaging Costs
    pallets_cost = goods_in_pallets * pricing["Packaging"]["Pallets"]
    packaging_total = sum([pricing["Packaging"]["Paper Packaging/ Void Fill"], pallets_cost])

    # Storage Costs
    storage_total = storage_space * pricing["Storage"]["Per Pallet Per Week"] * 4.33  

    # Goods In Costs
    courier_fee = orders_per_month * pricing["Goods In"]["Courier Fee (per order based on >30KG)"]
    goods_in_total = sum([courier_fee])

    # **Total Cost Calculation (Including Management Fee)**
    total_3pl_cost = sum([
        pricing["Management Fee"],
        pick_and_pack_total,
        packaging_total,
        storage_total,
        goods_in_total
    ])

    # **Cost Breakdown**
    st.markdown("<h2 class='big-font'>📊 Cost Breakdown</h2>", unsafe_allow_html=True)

    cost_data = {
        "Category": ["Management Fee", "Pick and Pack", "Packaging", "Storage", "Goods In", "Total 3PL Cost"],
        "Monthly Cost (£)": [
            round(pricing["Management Fee"]),
            round(pick_and_pack_total),
            round(packaging_total),
            round(storage_total),
            round(goods_in_total),
            round(total_3pl_cost)
        ]
    }

    df = pd.DataFrame(cost_data)

    # **Styled Table**
    st.dataframe(df.style.set_properties(**{
        'background-color': '#f9f9f9', 
        'border-color': 'black',
        'text-align': 'right',
        'font-size': '16px'
    }))

    # **Final Total Cost Highlight**
    st.success(f"💰 **Total 3PL Cost: £{round(total_3pl_cost)} per month**")
