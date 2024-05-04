aixblock ml
pip install -e .
aixblock-ml init my_ml_backend
aixblock-ml start my_ml_backend
aixblock-ml start my_ml_backend -p 9091

aixblock-ml deploy gcp {ml-backend-local-dir} \
--from={model-python-script} \
--gcp-project-id {gcp-project-id} \
--aixblock-host {https://aixblock.org} \
--aixblock-api-key {YOUR-AIXBLOCK-API-KEY}