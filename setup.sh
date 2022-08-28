mkdir -p ~/.streamlit
mkdir data

echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml