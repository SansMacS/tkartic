# Python GUI App

This project is a graphical user interface (GUI) application built using Python's Tkinter library. The application allows users to manage rooms, providing functionalities to enter and create rooms.

## Project Structure

```
python-gui-app
├── src
│   ├── main.py               # Entry point of the application
│   ├── gui
│   │   └── window.py         # GUI setup and user interaction
│   ├── controllers
│   │   └── room_controller.py # Logic for room management
│   └── models
│       └── room.py           # Room object definition
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd python-gui-app
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Execute the main script:
   ```
   python src/main.py
   ```

## Usage Guidelines

- Upon launching the application, you will see buttons for "Enter Room" and "Create Room."
- Click "Enter Room" to access an existing room or "Create Room" to set up a new room.
- Follow the prompts to manage your rooms effectively.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.