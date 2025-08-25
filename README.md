# ♟️ Chess Game in Python

A fully functional **Python Chess Game** that supports both **Player vs Player (PvP)** and **Player vs AI** modes.  
The project is modular, separating the game board, pieces, AI logic, and UI for maintainability and extension.

---

## 🚀 Features

- **Two game modes**:
  - Player vs Player (local multiplayer)
  - Player vs AI (basic computer opponent)
- **Move validation**: ensures only legal chess moves are allowed
- **Game rules**: supports check, checkmate, stalemate, promotion, and castling
- **User Interface**:
  - Simple click-based move input
  - Information panels for game state
- **Opening Book**: basic move suggestions from `book.py`
- **Clean Architecture**: UML diagram included for better understanding

---

## 📂 Project Structure

- Chess/
  -  AI.py                 # Chess AI logic (computer opponent)
  -  UI.py                 # User interface rendering
  -  board.py              # Board representation and state management
  -  piece.py              # Piece classes and movement rules
  -  node.py               # Game tree node representation (for AI search)
  -  book.py               # Opening book / predefined moves
  -  click.py              # Handle user input (mouse clicks, PvP mode)
  -  panel.py              # Side panel for game info
  -  constaints.py         # Game constants (board size, colors, etc.)
  -  main.py               # Entry point to start the game
  -  UML.jpg               # UML class diagram
  -  Image/                # Assets (piece images, icons, etc.)
  -  pycache/              # Auto-generated cache
