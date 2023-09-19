# makefile code:
# #########PACKAGE ACTIONS#########
# reinstall_packages:
# 	@pip uninstall -y safety_detection
# 	@pip install -e .

# # run_workflow:

run_api:
	uvicorn api.fastapi:app --reload
