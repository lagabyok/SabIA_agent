# Instrucciones rapidas (Backend + Frontend)

## Backend (API FastAPI)
1) Entrar a la carpeta del backend:
   ```powershell
   cd "d:\NODO CURSO\Hackathon\SabIA\backend"
   ```

2) Instalar dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

3) Crear y configurar el .env (solo la primera vez):
   ```powershell
   copy .env.example .env
   ```
   Edita .env y agrega las  keys.
   las voy a pasar x privado 
   solo usar gemini 

4) Levantar el servidor:
   ```powershell
   uvicorn app.main:app --reload --log-level info
   ```


## Frontend (Streamlit)
1) Entrar a la carpeta del frontend:
   ```powershell
   cd "d:\NODO CURSO\Hackathon\SabIA\frontend"
   ```

2) Instalar dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

3) Levantar el dashboard:
   ```powershell
   streamlit run streamlit_app.py
   ```


## Endpoints utiles
- Salud API: http://localhost:8000/health
- Ejecutar reporte: POST http://localhost:8000/run
- Ultimo reporte: http://localhost:8000/runs/latest
- Modelos Gemini: http://localhost:8000/llm/gemini/models

