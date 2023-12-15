FROM postgres:latest

# Set environment variables for PostgreSQL
ENV POSTGRES_DB=insure_cover
ENV POSTGRES_USER=ic
ENV POSTGRES_PASSWORD=ic_password

COPY init.sql /docker-entrypoint-initdb.d/


