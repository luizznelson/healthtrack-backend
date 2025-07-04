"""initial migration

Revision ID: f9e286924ff4
Revises: 
Create Date: 2025-07-02 23:33:27.694361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9e286924ff4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questionnaire_templates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questionnaire_templates_id'), 'questionnaire_templates', ['id'], unique=False)
    op.create_index(op.f('ix_questionnaire_templates_title'), 'questionnaire_templates', ['title'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('paciente', 'nutricionista', name='userrole'), nullable=True),
    sa.Column('nutricionista_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['nutricionista_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('question_templates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('template_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['template_id'], ['questionnaire_templates.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_question_templates_id'), 'question_templates', ['id'], unique=False)
    op.create_table('questionarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('respostas', sa.Text(), nullable=True),
    sa.Column('data', sa.DateTime(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questionarios_id'), 'questionarios', ['id'], unique=False)
    op.create_table('questionnaire_responses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('template_id', sa.Integer(), nullable=False),
    sa.Column('paciente_id', sa.Integer(), nullable=False),
    sa.Column('total_score', sa.Integer(), nullable=False),
    sa.Column('interpretation', sa.Text(), nullable=False),
    sa.Column('data_resposta', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['paciente_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['template_id'], ['questionnaire_templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questionnaire_responses_id'), 'questionnaire_responses', ['id'], unique=False)
    op.create_table('relatorios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conteudo', sa.Text(), nullable=True),
    sa.Column('paciente_id', sa.Integer(), nullable=False),
    sa.Column('nutricionista_id', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['nutricionista_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['paciente_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_relatorios_id'), 'relatorios', ['id'], unique=False)
    op.create_table('option_templates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('is_default', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question_templates.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_option_templates_id'), 'option_templates', ['id'], unique=False)
    op.create_table('questionnaire_answers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('response_id', sa.Integer(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('selected_option_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question_templates.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['response_id'], ['questionnaire_responses.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['selected_option_id'], ['option_templates.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questionnaire_answers_id'), 'questionnaire_answers', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_questionnaire_answers_id'), table_name='questionnaire_answers')
    op.drop_table('questionnaire_answers')
    op.drop_index(op.f('ix_option_templates_id'), table_name='option_templates')
    op.drop_table('option_templates')
    op.drop_index(op.f('ix_relatorios_id'), table_name='relatorios')
    op.drop_table('relatorios')
    op.drop_index(op.f('ix_questionnaire_responses_id'), table_name='questionnaire_responses')
    op.drop_table('questionnaire_responses')
    op.drop_index(op.f('ix_questionarios_id'), table_name='questionarios')
    op.drop_table('questionarios')
    op.drop_index(op.f('ix_question_templates_id'), table_name='question_templates')
    op.drop_table('question_templates')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_questionnaire_templates_title'), table_name='questionnaire_templates')
    op.drop_index(op.f('ix_questionnaire_templates_id'), table_name='questionnaire_templates')
    op.drop_table('questionnaire_templates')
    # ### end Alembic commands ###
