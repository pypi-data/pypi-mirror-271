import numpy as np

def Animating(epoch, num_epochs,  max_rect=100, filled_rectangle="\u2588", nonfilled_rectangle=' '):
    perc = int(np.ceil(epoch/num_epochs * 100))
    if epoch != 0:
        print('\r' + ' ' * (max_rect + 25) + '\r', end='', flush=True)
    print(f"Training model: {filled_rectangle*(int((perc/100 * max_rect)))}{nonfilled_rectangle * (max_rect - int(perc/100 * max_rect))} / {perc}%", end='', flush=True)

def EndAnimating(max_rect=100, filled_rectangle="\u2588"):
    print('\r' + ' ' * (max_rect + 25) + '\r', end='', flush=True)
    print(f"Training model: {max_rect * filled_rectangle} / 100%", end='', flush=True)