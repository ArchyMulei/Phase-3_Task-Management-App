"""populate_book_customer_association

Revision ID: 7c74f447b337
Revises: 01d85a2b5c36
Create Date: 2023-10-05 16:36:31.916582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c74f447b337'
down_revision = '01d85a2b5c36'
branch_labels = None
depends_on = None

def upgrade():
    # Insert data into the book_customer_association table
    op.execute("INSERT INTO book_customer_association (book_id, customer_id) VALUES (1, 1), (2, 1), (2, 2)")

def downgrade():
    # Define the downgrade code here if needed
    pass

