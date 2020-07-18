### Flip book
Text file flip book using curses

Displays text files in order. This will look like a moving image

### How to use
Using a text editor write out slides in plain text and number each slide sequentially and place files in a single folder. Run flip_book and pass in the folder

### Commands
- ```q``` Quit
- ```s``` Show last line of the slide
- ```p``` Pause / play
  - ```b``` back one slide
  - ```n``` forward one slide
  - ```ctrl-b``` move back to the beginning

### Command Line
- ```directory``` path to directory or . for current directory
- ```-r``` set the frame rate (1, 2, 4, 8)
- ```-s``` Show last line of the slide
- ```-g``` goto slide number
- ```-d``` disables controls (only q to quit)
