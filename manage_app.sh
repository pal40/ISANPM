#!/bin/bash

# Configuration
PID_FILE="streamlit_app.pid"
APP_SCRIPT="app.py"
VENV_DIR="venv"

function start_app() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo "Application is already running (PID: $PID)."
            exit 1
        else
            echo "Found stale PID file. Cleaning up..."
            rm "$PID_FILE"
        fi
    fi

    echo "Starting the Portfolio Manager application..."
    # Activate virtual environment and start streamlit in the background
    source "$VENV_DIR/bin/activate"
    nohup streamlit run "$APP_SCRIPT" > streamlit.log 2>&1 &
    
    # Capture the Process ID of the background job
    NEW_PID=$!
    echo $NEW_PID > "$PID_FILE"
    echo "Application started successfully! (PID: $NEW_PID)"
    echo "You can check the logs in streamlit.log"
}

function stop_app() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo "Stopping the application (PID: $PID)..."
            kill "$PID"
            rm "$PID_FILE"
            echo "Application stopped successfully."
        else
            echo "Application is not running. Cleaning up stale PID file."
            rm "$PID_FILE"
        fi
    else
        echo "Application is not currently running (no PID file found)."
    fi
}

function status_app() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo "Application is running (PID: $PID)."
        else
            echo "Application is NOT running, but PID file exists."
        fi
    else
        echo "Application is NOT running."
    fi
}

case "$1" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    status)
        status_app
        ;;
    restart)
        stop_app
        sleep 2
        start_app
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
esac
