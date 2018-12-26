# Time tracker

Daemon for storing and retrieving information about personal time management.
It's intended for private usage only and requires configuring external
authorization service like Nginx HTTP basic authentication.

# Configuration

Time tracker reads configuration from environment variables:

- `DB_NAME` - name of PostgreSQL database to use
- `DB_USER` - PostgreSQL database user
- `DB_HOST` - PostgreSQL database addresss
- `DB_PORT` - PostgreSQL database port
- `DB_PASSWORD` - PostgreSQL user password
- `DB_POOL_MIN_SIZE` - lower limit on active database connections
- `DB_POOL_MAX_SIZE` - upper limit on active database connections
- `PORT` - port to listen on
- `HOST` - address to bind to
- `TZ` - timezone
