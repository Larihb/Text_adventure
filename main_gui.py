import PySimpleGUI as sg
from game_logic import Game


my_game = Game()
sg.theme('DarkAmber')

# --- LAYOUT ---
layout = [
    [sg.Text("The Cave Escape", font=('Helvetica', 20))],
    [sg.Push(), sg.Image(key='-IMAGE-', size=(300, 300)), sg.Push()],
    [sg.Text(size=(60, 4), key='-DESCRIPTION-', font=('Helvetica', 12))],
    [sg.HorizontalSeparator()],
    [sg.Text("Available Exits:", key='-EXITS-', font=('Helvetica', 10))],
    [sg.Button('North'), sg.Button('South'), sg.Button('East'), sg.Button('West'), sg.Button('Read Inscription')],
    [sg.HorizontalSeparator()],
    [sg.Text("Riddle Answer:")],
    [sg.Input(key='-INPUT-', size=(30, 1)), sg.Button('Submit Answer')],
    [sg.Text(size=(60, 2), key='-FEEDBACK-', text_color='yellow')],
    [sg.Button('Quit')]
]

window = sg.Window('Text Adventure Game', layout, finalize=True)


def update_display():
    """Atualiza os elementos principais da tela (descrição e saídas)."""
    room_data = my_game.get_current_room_data()
    window['-DESCRIPTION-'].update(room_data['description'])
    window['-EXITS-'].update("Available Exits: " + ", ".join(room_data['exits'].keys()))
    window['-IMAGE-'].update(filename=room_data.get('image', ''))
    window.refresh()


update_display()

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Quit':
        break
    
    if event in ['North', 'South', 'East', 'West']:
        if my_game.process_movement(event.lower()):
            update_display()
            window['-FEEDBACK-'].update('')
        else:
            window['-FEEDBACK-'].update("You can't go that way.")

    elif event == 'Read Inscription':
        feedback = my_game.process_action('read')
        window['-FEEDBACK-'].update(feedback)

    elif event == 'Submit Answer':
        answer = values['-INPUT-']
        feedback = my_game.process_action('answer', answer)
        window['-FEEDBACK-'].update(feedback)
        window['-INPUT-'].update('')
        if not my_game.is_door_locked:
            update_display()

    if my_game.current_room_key == 'cave_exit':
        window['-FEEDBACK-'].update("YOU WON THE GAME! 🎉")
        window.refresh()
        window.read(timeout=6000)
        break

window.close()