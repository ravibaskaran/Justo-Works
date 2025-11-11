{
    "name"          : "Execute Query (Odoo 18)",
    "version"       : "18.0.1.0.0",
    "author"        : "Miftahussalam",
    "website"       : "https://blog.miftahussalam.com",
    "category"      : "Extra Tools",
    "license"       : "LGPL-3",
    "support"       : "me@miftahussalam.com",
    "summary"       : "Execute query from database (Migrated to Odoo 18)",
    "description"   : """
        Execute SQL Query Tool (Migrated to Odoo 18)

        Features:
        - Execute SQL queries directly from Odoo UI
        - Access via Settings > Technical
        - No need to open PostgreSQL directly

        Migrated to Odoo 18:
        - Version updated to 18.0.1.0.0
        - Python models reviewed for compatibility

        REQUIRES TESTING (HIGH PRIORITY):
        - SQL query execution
        - Security restrictions (ensure only admin/system users)
        - SQL injection prevention
        - Database connection handling
        - Query result display
        - Error handling for invalid queries

        SECURITY WARNING:
        - This module allows direct database queries
        - MUST be restricted to system administrators only
        - Test security rules thoroughly
        - Ensure proper input validation
    """,
    "depends"       : [
        "base",
        "mail",
    ],
    "data"          : [
        "views/ms_query_view.xml",
        "security/ir.model.access.csv",
    ],
    "demo"          : [],
    "test"          : [],
    "images"        : [
        "static/description/images/main_screenshot.png",
    ],
    "qweb"          : [],
    "css"           : [],
    "application"   : True,
    "installable"   : True,
    "auto_install"  : False,
}