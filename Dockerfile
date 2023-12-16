FROM postgres:latest

# Set environment variables for PostgreSQL
ENV POSTGRES_DB=insure_cover
ENV POSTGRES_USER=ic
ENV POSTGRES_PASSWORD=ic_password
# PostgreSQL default port
EXPOSE 5432

COPY init.sql /docker-entrypoint-initdb.d/


