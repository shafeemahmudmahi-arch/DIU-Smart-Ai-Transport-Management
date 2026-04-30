        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        avg_occupancy = route_buses['Current_Occupancy'].mean()
        st.metric("👥 Avg Occupancy", f"{avg_occupancy:.0f}/40")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        available_seats = (route_buses['Total_Capacity'] - route_buses['Current_Occupancy']).sum()
        st.metric("💺 Available Seats", int(available_seats))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.metric("⏱️ Next Bus ETA", f"{random.randint(3, 15)} min")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main Content
    tab1, tab2, tab3 = st.tabs(["🗺️ Live Map", "🔒 Seat Locking", "📊 My Stats"])
    
    with tab1:
        st.markdown("### 🗺️ Real-Time Bus Tracking")
        
        # Prepare data for PyDeck
        if not route_buses.empty:
            # Calculate available seats and ETA for tooltip
            route_buses['Available_Seats'] = route_buses['Total_Capacity'] - route_buses['Current_Occupancy']
            route_buses['ETA'] = route_buses.apply(lambda x: f"{random.randint(5, 20)} min", axis=1)
            
            # Create PyDeck layer with custom tooltips
            layer = pdk.Layer(
                'ScatterplotLayer',
                data=route_buses,
                get_position='[Longitude, Latitude]',
                get_color='[57, 181, 74, 200]',
                get_radius=200,
                pickable=True,
                auto_highlight=True,
            )
            
            # Add text labels
            text_layer = pdk.Layer(
                'TextLayer',
                data=route_buses,

