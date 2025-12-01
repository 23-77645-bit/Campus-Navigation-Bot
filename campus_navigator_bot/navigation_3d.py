import plotly.graph_objects as go
from campus_data import get_coordinates_map, location_exists, get_location_by_name


def show_campus_3d_map(current_location: str, target_location: str):
    """
    Create and display a 3D visualization of the campus highlighting current and target locations
    Args:
        current_location: The user's current location
        target_location: The destination location
    """
    # Validate locations exist
    if not location_exists(current_location):
        raise ValueError(f"Current location '{current_location}' does not exist in the campus data.")
    
    if not location_exists(target_location):
        raise ValueError(f"Target location '{target_location}' does not exist in the campus data.")
    
    # Get all coordinates
    coordinates_map = get_coordinates_map()
    
    # Prepare data for plotting
    all_names = list(coordinates_map.keys())
    all_coords = list(coordinates_map.values())
    
    # Extract x, y, z coordinates
    x_coords = [coord[0] for coord in all_coords]
    y_coords = [coord[1] for coord in all_coords]
    z_coords = [coord[2] for coord in all_coords]
    
    # Create the 3D scatter plot
    fig = go.Figure()
    
    # Add all campus locations as regular markers
    fig.add_trace(go.Scatter3d(
        x=x_coords,
        y=y_coords,
        z=z_coords,
        mode='markers+text',
        marker=dict(
            size=8,
            color='lightblue',
            opacity=0.6
        ),
        text=all_names,
        textposition="top center",
        name='Campus Locations'
    ))
    
    # Highlight current location
    current_coords = get_coordinates_map()[current_location]
    fig.add_trace(go.Scatter3d(
        x=[current_coords[0]],
        y=[current_coords[1]],
        z=[current_coords[2]],
        mode='markers+text',
        marker=dict(
            size=15,
            color='green',
            symbol='circle'
        ),
        text=[current_location],
        textposition="middle right",
        name='Current Location'
    ))
    
    # Highlight target location
    target_coords = get_coordinates_map()[target_location]
    fig.add_trace(go.Scatter3d(
        x=[target_coords[0]],
        y=[target_coords[1]],
        z=[target_coords[2]],
        mode='markers+text',
        marker=dict(
            size=15,
            color='red',
            symbol='star'
        ),
        text=[target_location],
        textposition="middle right",
        name='Target Location'
    ))
    
    # Customize the layout
    fig.update_layout(
        title={
            'text': f'3D Campus Map: From {current_location} to {target_location}',
            'x': 0.5,
            'xanchor': 'center'
        },
        scene=dict(
            xaxis_title='X Coordinate',
            yaxis_title='Y Coordinate',
            zaxis_title='Z Coordinate',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=900,
        height=700,
        showlegend=True
    )
    
    # Show the plot in the browser
    fig.show()


if __name__ == "__main__":
    # Example usage
    print("Example 3D Campus Map Visualization")
    print("Available locations:", get_coordinates_map().keys())
    
    # Example: Show map from Ibaan Building to Sto. Tomas Building
    try:
        show_campus_3d_map("Ibaan Building", "Sto. Tomas Building")
    except ValueError as e:
        print(f"Error: {e}")