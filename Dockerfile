FROM    python@sha256:ad39551743b356efda7c61f46019b97d49d1aab01b97f0e6d87c9b34326f3bfe

COPY . /src

# run the thing
CMD ["python", "/src/app.py"]