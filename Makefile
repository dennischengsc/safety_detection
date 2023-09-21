run_api:
	uvicorn docker.fastapi:app --reload

run_streamlit:
	streamlit run app2.py
