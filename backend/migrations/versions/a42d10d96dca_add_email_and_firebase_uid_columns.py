"""Add email and firebase_uid columns

Revision ID: a42d10d96dca
Revises: c5c1094de9b7
Create Date: 2024-12-17 00:01:23.228916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a42d10d96dca'
down_revision = 'c5c1094de9b7'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firebase_uid', sa.String(length=120), nullable=True))
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=True))

    # After batch operation, alter the table without batch mode
    op.execute("UPDATE user SET firebase_uid = 'TEMP_UID' WHERE firebase_uid IS NULL")
    op.execute("UPDATE user SET email = 'temp@example.com' WHERE email IS NULL")

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('firebase_uid', nullable=False)
        batch_op.alter_column('email', nullable=False)
        batch_op.create_unique_constraint('uq_user_email', ['email'])
        batch_op.create_unique_constraint('uq_user_firebase_uid', ['firebase_uid'])

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint('uq_user_email', type_='unique')
        batch_op.drop_constraint('uq_user_firebase_uid', type_='unique')
        batch_op.drop_column('email')
        batch_op.drop_column('firebase_uid')

    # ### end Alembic commands ###
