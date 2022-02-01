"""added constrains

Revision ID: e3b5b18317fd
Revises: d39d0345c046
Create Date: 2022-02-01 20:59:43.792142

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy.dialects import mysql

revision = 'e3b5b18317fd'
down_revision = 'd39d0345c046'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint(constraint_name="ClientRoles_ibfk_1", table_name="ClientRoles", type_="foreignkey")
    op.create_foreign_key(constraint_name='ClientRoles_ibfk_1', source_table='ClientRoles', referent_table="Clients",
                          local_cols=['clientId'], remote_cols=['clientId'], ondelete="CASCADE")
    op.drop_constraint(constraint_name="CreditCards_ibfk_1", table_name="CreditCards", type_="foreignkey")
    op.create_foreign_key(constraint_name='CreditCards_ibfk_1', source_table='CreditCards', referent_table="Clients",
                          local_cols=['clientId'], remote_cols=['clientId'], ondelete="CASCADE")
    op.drop_constraint(constraint_name="Services_ibfk_1", table_name="Services", type_="foreignkey")
    op.create_foreign_key(constraint_name='Services_ibfk_1', source_table='Services', referent_table="Cars",
                          local_cols=['carId'], remote_cols=['carId'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint(constraint_name="ClientRoles_ibfk_1", table_name="ClientRoles", type_="foreignkey")
    op.create_foreign_key(constraint_name="ClientRoles_ibfk_1", source_table='ClientRoles', referent_table="Clients",
                          local_cols=['clientId'], remote_cols=['clientId'])
    op.drop_constraint(constraint_name="CreditCards_ibfk_1", table_name="CreditCards", type_="foreignkey")
    op.create_foreign_key(constraint_name="CreditCards_ibfk_1", source_table='CreditCards', referent_table="Clients",
                          local_cols=['clientId'], remote_cols=['clientId'])
    op.drop_constraint(constraint_name="Services_ibfk_1", table_name="Services", type_="foreignkey")
    op.create_foreign_key(constraint_name="Services_ibfk_1", source_table='Services', referent_table="Cars",
                          local_cols=['carId'], remote_cols=['carId'])
    pass
