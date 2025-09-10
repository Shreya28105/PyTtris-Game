🎮 PyTetris – Raspberry Pi + Python + USB Game Controller
A classic Tetris clone built using Python + Pygame, designed to run on Raspberry Pi with support for USB Game Controllers.
This project brings retro gaming vibes with joystick control, sound effects, and smooth gameplay.

✨ Features:
🕹️ Full USB controller support (tested on Xbox & generic USB gamepads).
🎵 Sound effects for rotation, line clear, drop, and game over.
🎶 Background music loop.
⬆️ Next-piece preview window.
🧱 Classic 7 Tetris shapes with vibrant colors.
🖥️ Runs smoothly on Raspberry Pi or any PC with Python installed.
🔁 Restart game with Start button on controller.
🎮 Keyboard fallback if no joystick is detected.

🎮 Controls:
Controller
Button	Action
A / X (Button 1)	Rotate piece
B / O (Button 2)	Hard drop
D-Pad / Left Stick	Move left / right / soft drop
Start (Button 7)	Restart (after Game Over)
Keyboard (Fallback)
Key	Action
⬅️ Left Arrow	Move left
➡️ Right Arrow	Move right
⬇️ Down Arrow	Soft drop
⬆️ Up Arrow	Rotate
Spacebar	Hard drop
R	Restart
🛠 Installation

Clone this repository:
git clone https://github.com/your-username/pytetris-rpi.git
cd pytetris-rpi

Install dependencies:
pip install pygame

Add your sound files (bgsound.mp3, explosion.mp3, clear.mp3, gameover.mp3) to the project folder.

Run the game:
python tetris.py

🔊 Sound Files:
Background music (bgsound.mp3) loops continuously.
Explosion / Drop sound plays when piece drops.
Clear sound plays when a line clears.
Game Over sound plays when board fills up.
(You can replace these with your own .mp3 files.)

⚡ Built with ❤️ by Shreya on Raspberry Pi & Python
