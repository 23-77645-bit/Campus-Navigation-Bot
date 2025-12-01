        # Generate bot response
        with st.spinner("Bot is thinking..."):
            response = generate_response(sanitized_input)
        
        # Check if the response is a 3D map request
        if response == "3D_MAP_REQUEST":
            # Prompt user for current and target locations
            st.session_state.waiting_for_3d_locations = True
            st.session_state.current_3d_input = sanitized_input
            response = "To create a 3D visualization, I need your current location and your destination. Please provide your current location first."
        else:
            # Add bot response to history
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Show bot response
            st.markdown(f'<div class="bot-message">Bot: {response}</div>', unsafe_allow_html=True)

        # Rerun to update the chat display
        st.rerun()