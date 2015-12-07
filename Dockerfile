FROM    elyase/staticpython@sha256:091ed13459547de86653fe46e768b6d274c562c0ca794749717954af8bc67efb

COPY . /src

# run the thing
CMD ["python", "/src/app.py"]