taskkill //F //IM python.exe

<!-- Run project -->
source venv/Scripts/activate && uvicorn main:app --reload
