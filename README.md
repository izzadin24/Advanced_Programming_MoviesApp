# Movie Analytics System: Data Science & Desktop Engineering 🎬

A comparative project implementing **Data Science (Python)** and **Software Engineering (Java)** approaches to analyze the "TMDB Top Rated Movies" dataset.

**Project Type:** Final Project (Tugas Besar Pemrograman Lanjut)  
**Team:** Musmid
**Dataset Source:** Kaggle (TMDB Top Rated Movies)

---

## 📂 Project Structure

This repository is divided into two main modules:

1.  **`python_app/`**: A Rapid Prototyping module using **Streamlit**. Focuses on data cleaning, exploration, and interactive visualization.
2.  **`java_app/`**: A Robust Desktop Application using **JavaFX**. Focuses on Object-Oriented Programming (OOP), manual data parsing (Regex), and modular architecture.

```text
TUBES_PL/
├── data/
│   └── raw/
│       └── Top_Rated_Movies.csv  <-- The Dataset
├── python_app/
│   ├── app.py                    <-- Main Streamlit Code
│   ├── requirements.txt          <-- Library Dependencies
│   └── start_app.bat             <-- One-Click Launcher
└── java_app/
    ├── src/
    │   └── com/example/tubes/app/
    │       ├── Main.java         <-- JavaFX Entry Point
    │       ├── Film.java         <-- Data Model (OOP)
    │       └── DataProcessor.java<-- Custom Regex Parser
    └── lib/                      <-- JavaFX SDK Libraries

```

## 🚀 How to Run (Quick Start)
1. Cloning the Repository
First, download this project to your local machine:

```
git clone [https://github.com/username/repo-name.git](https://github.com/username/repo-name.git)
cd TUBES_PL
```

2. Running the Python Dashboard (Automatic Setup)
We have provided a smart batch script that automatically creates a Virtual Environment (venv), installs dependencies, and launches the app.

1Navigate to the python_app folder.
1) Navigate to the python_app folder.
2) Double-click the start_app.bat file.
3) Wait a moment for the setup to complete. The dashboard will open automatically in your browser.
4) Note: Requires Python 3.x installed and added to PATH.
5) Running the Java Desktop App
   
The Java application is built using JavaFX 17 and requires an IDE (IntelliJ IDEA recommended) to run.

1) Open IntelliJ IDEA.
2) Open the TUBES_PL folder as a project.
3) Ensure Project Structure is set to Java 17+.
4) Important: Configure the VM Options in your Run Configuration to point to the JavaFX SDK:
```
--module-path "\path\to\your\javafx-sdk-17\lib" --add-modules javafx.controls,javafx.fxml,javafx.graphics
```
5) Run the Main class.


