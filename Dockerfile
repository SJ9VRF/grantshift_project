FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY grantshift grantshift
COPY grantshiftbench grantshiftbench
COPY evaluation evaluation
COPY artifacts/personalized_policy.joblib artifacts/personalized_policy.joblib
COPY artifacts/personalized_policy.metadata.json artifacts/personalized_policy.metadata.json
COPY examples examples
RUN pip install --no-cache-dir .
ENTRYPOINT ["grantshift-agent"]
CMD ["--help"]
