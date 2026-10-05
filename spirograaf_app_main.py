from nicegui import ui
import math

# Globale variabelen voor de spirograaf instellingen
R = 120  # Straal vaste cirkel
r = 80   # Straal bewegende cirkel
d = 100  # Afstand pen tot middelpunt

svg_container = None

def update_spirograph():
    global R, r, d, svg_container
    
    # Bereken coördinaten voor de hypocykoïde (spirograaf)
    points = []
    # Bepaal het aantal stappen op basis van de grootste gemene deler om een gesloten vorm te krijgen
    steps = 1000
    max_theta = 2 * math.pi * r / math.gcd(int(R), int(r)) if r > 0 else 2 * math.pi
    
    for i in range(steps + 1):
        theta = i * max_theta / steps
        # Formule voor hypocykoïde
        x = (R - r) * math.cos(theta) + d * math.cos((R - r) * theta / r)
        y = (R - r) * math.sin(theta) - d * math.sin((R - r) * theta / r)
        
        # Centreer in het SVG canvas (uitgaande van een canvas van 400x400)
        points.append(f"{x + 200},{y + 200}")

    points_str = " ".join(points)
    
    # Vernieuw de SVG inhoud direct zonder pagina refresh
    svg_container.content = f'''
        <svg width="400" height="400" viewBox="0 0 400 400" style="background-color: #1a1a1a; border-radius: 8px;">
            <polyline points="{points_str}" fill="none" stroke="#00ffcc" stroke-width="1.5" />
        </svg>
    '''

ui.dark_mode().enable()

with ui.row().classes('w-full justify-center items-center p-4'):
    ui.label('Interactieve Spirograaf (NiceGUI)').classes('text-2xl font-bold text-cyan-400')

with ui.row().classes('w-full justify-center gap-6 p-4'):
    # Bedieningspaneel met sliders
    with ui.column().classes('w-72 gap-4'):
        ui.label('Instellingen').classes('text-lg font-semibold')
        
        ui.label('Straal vaste cirkel (R)')
        ui.slider(min=50, max=180, value=120).on('update:model-value', lambda e: [globals().update(R=e.args), update_spirograph()])
        
        ui.label('Straal bewegende cirkel (r)')
        ui.slider(min=10, max=150, value=80).on('update:model-value', lambda e: [globals().update(r=e.args), update_spirograph()])
        
        ui.label('Afstand pen (d)')
        ui.slider(min=10, max=150, value=100).on('update:model-value', lambda e: [globals().update(d=e.args), update_spirograph()])

    # Weergave van de spirograaf via een SVG element
    with ui.column().classes('items-center'):
        svg_container = ui.html()
        update_spioragraph()  # Teken direct bij het laden

# Zorg dat NiceGUI luistert naar de juiste poort voor cloud-hosting (zoals Render of Hugging Face)
ui.run(port=8080, host='0.0.0.0', title='Spirograaf App', show=False)
