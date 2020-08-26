"""empty message

Revision ID: 1f80fdc5e2e1
Revises: 4459fb95cf12
Create Date: 2020-08-24 10:51:04.213302

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1f80fdc5e2e1'
down_revision = '4459fb95cf12'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_comcode_01',
    sa.Column('GROUP_CODE', sa.String(length=30), nullable=False),
    sa.Column('CODE', sa.String(length=30), nullable=False),
    sa.Column('CODE_VALUE', sa.String(length=30), nullable=False),
    sa.Column('REGIST_DATE', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('CODE_DC', sa.String(length=1000), nullable=True),
    sa.Column('USE_AT', sa.Boolean(), nullable=False),
    sa.Column('RM_1', sa.String(length=50), nullable=True),
    sa.Column('RM_2', sa.String(length=50), nullable=True),
    sa.Column('RM_3', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('GROUP_CODE', 'CODE'),
    mysql_collate='utf8_general_ci'
    )
    op.create_index(op.f('ix_t_comcode_01_CODE'), 't_comcode_01', ['CODE'], unique=True)
    op.create_index(op.f('ix_t_comcode_01_GROUP_CODE'), 't_comcode_01', ['GROUP_CODE'], unique=False)
    op.drop_table('t_analysis_result_m01')
    op.drop_index('UC_CODE', table_name='t_comcode_m01')
    op.drop_table('t_comcode_m01')
    op.drop_table('dgrs_fclts')
    op.drop_index('ix_T_ADMIN_INFO_M01_EMAIL', table_name='T_ADMIN_INFO_M01')
    op.drop_index('ix_T_ADMIN_INFO_M01_ID', table_name='T_ADMIN_INFO_M01')
    op.drop_index('ix_T_ADMIN_INFO_M01_NM', table_name='T_ADMIN_INFO_M01')
    op.drop_table('T_ADMIN_INFO_M01')
    op.drop_index('ix_T_COMCODE_M01_CODE', table_name='T_COMCODE_M01')
    op.drop_index('ix_T_COMCODE_M01_GROUP_CODE', table_name='T_COMCODE_M01')
    op.drop_table('T_COMCODE_M01')
    op.add_column('t_admin_info_m01', sa.Column('LAST_LOGIN', sa.DateTime(), nullable=True))
    op.alter_column('t_admin_info_m01', 'AUTHOR',
               existing_type=mysql.VARCHAR(length=20),
               comment=None,
               existing_comment='권한',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'CONFM_AT',
               existing_type=mysql.VARCHAR(length=1),
               nullable=False,
               comment=None,
               existing_comment='승인 여부')
    op.alter_column('t_admin_info_m01', 'CONFM_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment=None,
               existing_comment='승인 날짜',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'CONFM_ID',
               existing_type=mysql.VARCHAR(length=30),
               comment=None,
               existing_comment='승인 ID',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'DELETE_AT',
               existing_type=mysql.VARCHAR(length=1),
               comment=None,
               existing_comment='삭제 여부',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'DELETE_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment=None,
               existing_comment='삭제 날짜',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'DELETE_ID',
               existing_type=mysql.VARCHAR(length=30),
               comment=None,
               existing_comment='삭제 ID',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'DEPT_NM',
               existing_type=mysql.VARCHAR(length=100),
               comment=None,
               existing_comment='부서 이름',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'EMAIL',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False,
               comment=None,
               existing_comment='이메일')
    op.alter_column('t_admin_info_m01', 'ID',
               existing_type=mysql.VARCHAR(length=30),
               nullable=False,
               comment=None,
               existing_comment='ID')
    op.alter_column('t_admin_info_m01', 'INSTT_NM',
               existing_type=mysql.VARCHAR(length=100),
               comment=None,
               existing_comment='기관 이름',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'JURANG',
               existing_type=mysql.VARCHAR(length=10),
               comment=None,
               existing_comment='관할구역',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'NM',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False,
               comment=None,
               existing_comment='이름')
    op.alter_column('t_admin_info_m01', 'PASSWORD',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False,
               comment=None,
               existing_comment='비밀번호')
    op.alter_column('t_admin_info_m01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment=None,
               existing_comment='등록 날짜',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'SN',
               existing_type=mysql.INTEGER(display_width=11),
               comment=None,
               existing_comment='일련번호',
               autoincrement=True)
    op.alter_column('t_admin_info_m01', 'TELNO',
               existing_type=mysql.VARCHAR(length=15),
               comment=None,
               existing_comment='전화번호',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'UPDT_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment=None,
               existing_comment='수정 날짜',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'UPDT_ID',
               existing_type=mysql.VARCHAR(length=30),
               comment=None,
               existing_comment='수정 ID',
               existing_nullable=True)
    op.create_index(op.f('ix_t_admin_info_m01_EMAIL'), 't_admin_info_m01', ['EMAIL'], unique=True)
    op.create_index(op.f('ix_t_admin_info_m01_ID'), 't_admin_info_m01', ['ID'], unique=True)
    op.create_index(op.f('ix_t_admin_info_m01_NM'), 't_admin_info_m01', ['NM'], unique=False)
    op.drop_table_comment(
        't_admin_info_m01',
        existing_comment='관리자 정보',
        schema=None
    )
    op.drop_column('t_admin_info_m01', 'LAST_LOGIN_DATE')
    op.alter_column('t_pick_place_h01', 'LA',
               existing_type=mysql.VARCHAR(length=30),
               comment=None,
               existing_comment='위도',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'LO',
               existing_type=mysql.VARCHAR(length=30),
               comment=None,
               existing_comment='경도',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'PLACE_ADRES',
               existing_type=mysql.VARCHAR(length=500),
               comment=None,
               existing_comment='장소 주소',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'PLACE_CTPRVN',
               existing_type=mysql.VARCHAR(length=10),
               comment=None,
               existing_comment='장소 시도',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'PLACE_ID',
               existing_type=mysql.VARCHAR(length=20),
               comment=None,
               existing_comment='장소 ID',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'PLACE_NM',
               existing_type=mysql.VARCHAR(length=100),
               comment=None,
               existing_comment='장소 이름',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'PLACE_RN_ADRES',
               existing_type=mysql.VARCHAR(length=500),
               comment=None,
               existing_comment='장소 도로명 주소',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'PLACE_SIGNGU',
               existing_type=mysql.VARCHAR(length=20),
               comment=None,
               existing_comment='장소 시군구',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment=None,
               existing_comment='등록 날짜',
               existing_nullable=False,
               existing_server_default=sa.text('current_timestamp()'))
    op.alter_column('t_pick_place_h01', 'SN',
               existing_type=mysql.INTEGER(display_width=11),
               comment=None,
               existing_comment='일련번호',
               autoincrement=True)
    op.drop_table_comment(
        't_pick_place_h01',
        existing_comment='사용자 선택 장소 히스토리 테이블',
        schema=None
    )
    op.alter_column('t_place_info_m01', 'LA',
               existing_type=mysql.VARCHAR(length=30),
               comment=None,
               existing_comment='위도',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'LO',
               existing_type=mysql.VARCHAR(length=30),
               comment=None,
               existing_comment='경도',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'PLACE_ADRES',
               existing_type=mysql.VARCHAR(length=500),
               comment=None,
               existing_comment='장소 주소',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'PLACE_CTPRVN',
               existing_type=mysql.VARCHAR(length=10),
               comment=None,
               existing_comment='장소 시도',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'PLACE_ID',
               existing_type=mysql.VARCHAR(length=20),
               comment=None,
               existing_comment='장소 ID')
    op.alter_column('t_place_info_m01', 'PLACE_NM',
               existing_type=mysql.VARCHAR(length=100),
               comment=None,
               existing_comment='장소 이름',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'PLACE_RN_ADRES',
               existing_type=mysql.VARCHAR(length=500),
               comment=None,
               existing_comment='장소 도로명 주소',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'PLACE_SIGNGU',
               existing_type=mysql.VARCHAR(length=20),
               comment=None,
               existing_comment='장소 시군구',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               nullable=False,
               comment=None,
               existing_comment='등록 날짜')
    op.drop_table_comment(
        't_place_info_m01',
        existing_comment='장소 정보 마스터 테이블',
        schema=None
    )
    op.alter_column('t_search_kwrd_h01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment=None,
               existing_comment='등록 날짜',
               existing_nullable=False,
               existing_server_default=sa.text('current_timestamp()'))
    op.alter_column('t_search_kwrd_h01', 'SEARCH_KWRD',
               existing_type=mysql.VARCHAR(length=100),
               comment=None,
               existing_comment='검색 키워드',
               existing_nullable=True)
    op.alter_column('t_search_kwrd_h01', 'SEARCH_TY',
               existing_type=mysql.VARCHAR(length=10),
               comment=None,
               existing_comment='검색 유형',
               existing_nullable=True)
    op.alter_column('t_search_kwrd_h01', 'SN',
               existing_type=mysql.INTEGER(display_width=11),
               comment=None,
               existing_comment='일련번호',
               autoincrement=True)
    op.drop_table_comment(
        't_search_kwrd_h01',
        existing_comment='검색 키워드 히스토리 저장 테이블',
        schema=None
    )
    op.alter_column('t_user_info_m01', 'AGRDE',
               existing_type=mysql.VARCHAR(length=10),
               comment=None,
               existing_comment='연령대',
               existing_nullable=True)
    op.alter_column('t_user_info_m01', 'DELETE_AT',
               existing_type=mysql.VARCHAR(length=1),
               nullable=True,
               comment=None,
               existing_comment='삭제 여부')
    op.alter_column('t_user_info_m01', 'EMAIL',
               existing_type=mysql.VARCHAR(length=50),
               comment=None,
               existing_comment='이메일',
               existing_nullable=True)
    op.alter_column('t_user_info_m01', 'PASSWORD',
               existing_type=mysql.VARCHAR(length=255),
               comment=None,
               existing_comment='비밀번호',
               existing_nullable=True)
    op.alter_column('t_user_info_m01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               nullable=True,
               comment=None,
               existing_comment='등록 날짜',
               existing_server_default=sa.text('current_timestamp() ON UPDATE current_timestamp()'))
    op.alter_column('t_user_info_m01', 'RESIDE_AREA',
               existing_type=mysql.VARCHAR(length=10),
               comment=None,
               existing_comment='거주 지역',
               existing_nullable=True)
    op.alter_column('t_user_info_m01', 'SEXDSTN',
               existing_type=mysql.VARCHAR(length=1),
               comment=None,
               existing_comment='성별',
               existing_nullable=True)
    op.alter_column('t_user_info_m01', 'SN',
               existing_type=mysql.INTEGER(display_width=11),
               comment=None,
               existing_comment='일련번호',
               autoincrement=True)
    op.alter_column('t_user_info_m01', 'TELNO',
               existing_type=mysql.VARCHAR(length=15),
               comment=None,
               existing_comment='전화번호',
               existing_nullable=True)
    op.drop_table_comment(
        't_user_info_m01',
        existing_comment='분석요청 동의 사용자 정보',
        schema=None
    )
    op.alter_column('t_user_location_d01', 'COURS_ORDR',
               existing_type=mysql.INTEGER(display_width=11),
               comment=None,
               existing_comment='경로 순서',
               existing_nullable=True)
    op.alter_column('t_user_location_d01', 'DE_ORDR',
               existing_type=mysql.INTEGER(display_width=11),
               comment=None,
               existing_comment='일자 순서',
               existing_nullable=True)
    op.alter_column('t_user_location_d01', 'PLACE_ID',
               existing_type=mysql.VARCHAR(length=20),
               comment=None,
               existing_comment='장소 ID',
               existing_nullable=True)
    op.alter_column('t_user_location_d01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               nullable=True,
               comment=None,
               existing_comment='등록 날짜',
               existing_server_default=sa.text('current_timestamp()'))
    op.alter_column('t_user_location_d01', 'SCHDUL_SN',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True,
               comment=None,
               existing_comment='일정 일련번호')
    op.alter_column('t_user_location_d01', 'SN',
               existing_type=mysql.INTEGER(display_width=11),
               comment=None,
               existing_comment='일련번호',
               autoincrement=True)
    op.alter_column('t_user_location_d01', 'VISIT_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment=None,
               existing_comment='방문 날짜',
               existing_nullable=True)
    op.alter_column('t_user_location_d01', 'VISIT_TIME',
               existing_type=mysql.VARCHAR(length=5),
               comment=None,
               existing_comment='방문 시간',
               existing_nullable=True)
    op.drop_constraint('FK_T_USER_LOCATION_D01_PLACE_ID_T_PLACE_INFO_M01_PLACE_ID', 't_user_location_d01', type_='foreignkey')
    op.drop_table_comment(
        't_user_location_d01',
        existing_comment='사용자 이동경로 정보',
        schema=None
    )
    op.alter_column('t_user_schdul_m01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               nullable=True,
               comment=None,
               existing_comment='등록 날짜',
               existing_server_default=sa.text("'0000-00-00 00:00:00'"))
    op.alter_column('t_user_schdul_m01', 'SN',
               existing_type=mysql.INTEGER(display_width=11),
               comment=None,
               existing_comment='일련번호',
               autoincrement=True)
    op.alter_column('t_user_schdul_m01', 'STDDE',
               existing_type=mysql.TIMESTAMP(),
               nullable=True,
               comment=None,
               existing_comment='기준일',
               existing_server_default=sa.text('current_timestamp() ON UPDATE current_timestamp()'))
    op.alter_column('t_user_schdul_m01', 'USER_SN',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True,
               comment=None,
               existing_comment='사용자 일련번호')
    op.drop_table_comment(
        't_user_schdul_m01',
        existing_comment='사용자 일정 정보',
        schema=None
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table_comment(
        't_user_schdul_m01',
        '사용자 일정 정보',
        existing_comment=None,
        schema=None
    )
    op.alter_column('t_user_schdul_m01', 'USER_SN',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False,
               comment='사용자 일련번호')
    op.alter_column('t_user_schdul_m01', 'STDDE',
               existing_type=mysql.TIMESTAMP(),
               nullable=False,
               comment='기준일',
               existing_server_default=sa.text('current_timestamp() ON UPDATE current_timestamp()'))
    op.alter_column('t_user_schdul_m01', 'SN',
               existing_type=mysql.INTEGER(display_width=11),
               comment='일련번호',
               autoincrement=True)
    op.alter_column('t_user_schdul_m01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               nullable=False,
               comment='등록 날짜',
               existing_server_default=sa.text("'0000-00-00 00:00:00'"))
    op.create_table_comment(
        't_user_location_d01',
        '사용자 이동경로 정보',
        existing_comment=None,
        schema=None
    )
    op.create_foreign_key('FK_T_USER_LOCATION_D01_PLACE_ID_T_PLACE_INFO_M01_PLACE_ID', 't_user_location_d01', 't_place_info_m01', ['PLACE_ID'], ['PLACE_ID'])
    op.alter_column('t_user_location_d01', 'VISIT_TIME',
               existing_type=mysql.VARCHAR(length=5),
               comment='방문 시간',
               existing_nullable=True)
    op.alter_column('t_user_location_d01', 'VISIT_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment='방문 날짜',
               existing_nullable=True)
    op.alter_column('t_user_location_d01', 'SN',
               existing_type=mysql.INTEGER(display_width=11),
               comment='일련번호',
               autoincrement=True)
    op.alter_column('t_user_location_d01', 'SCHDUL_SN',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False,
               comment='일정 일련번호')
    op.alter_column('t_user_location_d01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               nullable=False,
               comment='등록 날짜',
               existing_server_default=sa.text('current_timestamp()'))
    op.alter_column('t_user_location_d01', 'PLACE_ID',
               existing_type=mysql.VARCHAR(length=20),
               comment='장소 ID',
               existing_nullable=True)
    op.alter_column('t_user_location_d01', 'DE_ORDR',
               existing_type=mysql.INTEGER(display_width=11),
               comment='일자 순서',
               existing_nullable=True)
    op.alter_column('t_user_location_d01', 'COURS_ORDR',
               existing_type=mysql.INTEGER(display_width=11),
               comment='경로 순서',
               existing_nullable=True)
    op.create_table_comment(
        't_user_info_m01',
        '분석요청 동의 사용자 정보',
        existing_comment=None,
        schema=None
    )
    op.alter_column('t_user_info_m01', 'TELNO',
               existing_type=mysql.VARCHAR(length=15),
               comment='전화번호',
               existing_nullable=True)
    op.alter_column('t_user_info_m01', 'SN',
               existing_type=mysql.INTEGER(display_width=11),
               comment='일련번호',
               autoincrement=True)
    op.alter_column('t_user_info_m01', 'SEXDSTN',
               existing_type=mysql.VARCHAR(length=1),
               comment='성별',
               existing_nullable=True)
    op.alter_column('t_user_info_m01', 'RESIDE_AREA',
               existing_type=mysql.VARCHAR(length=10),
               comment='거주 지역',
               existing_nullable=True)
    op.alter_column('t_user_info_m01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               nullable=False,
               comment='등록 날짜',
               existing_server_default=sa.text('current_timestamp() ON UPDATE current_timestamp()'))
    op.alter_column('t_user_info_m01', 'PASSWORD',
               existing_type=mysql.VARCHAR(length=255),
               comment='비밀번호',
               existing_nullable=True)
    op.alter_column('t_user_info_m01', 'EMAIL',
               existing_type=mysql.VARCHAR(length=50),
               comment='이메일',
               existing_nullable=True)
    op.alter_column('t_user_info_m01', 'DELETE_AT',
               existing_type=mysql.VARCHAR(length=1),
               nullable=False,
               comment='삭제 여부')
    op.alter_column('t_user_info_m01', 'AGRDE',
               existing_type=mysql.VARCHAR(length=10),
               comment='연령대',
               existing_nullable=True)
    op.create_table_comment(
        't_search_kwrd_h01',
        '검색 키워드 히스토리 저장 테이블',
        existing_comment=None,
        schema=None
    )
    op.alter_column('t_search_kwrd_h01', 'SN',
               existing_type=mysql.INTEGER(display_width=11),
               comment='일련번호',
               autoincrement=True)
    op.alter_column('t_search_kwrd_h01', 'SEARCH_TY',
               existing_type=mysql.VARCHAR(length=10),
               comment='검색 유형',
               existing_nullable=True)
    op.alter_column('t_search_kwrd_h01', 'SEARCH_KWRD',
               existing_type=mysql.VARCHAR(length=100),
               comment='검색 키워드',
               existing_nullable=True)
    op.alter_column('t_search_kwrd_h01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment='등록 날짜',
               existing_nullable=False,
               existing_server_default=sa.text('current_timestamp()'))
    op.create_table_comment(
        't_place_info_m01',
        '장소 정보 마스터 테이블',
        existing_comment=None,
        schema=None
    )
    op.alter_column('t_place_info_m01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               nullable=True,
               comment='등록 날짜')
    op.alter_column('t_place_info_m01', 'PLACE_SIGNGU',
               existing_type=mysql.VARCHAR(length=20),
               comment='장소 시군구',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'PLACE_RN_ADRES',
               existing_type=mysql.VARCHAR(length=500),
               comment='장소 도로명 주소',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'PLACE_NM',
               existing_type=mysql.VARCHAR(length=100),
               comment='장소 이름',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'PLACE_ID',
               existing_type=mysql.VARCHAR(length=20),
               comment='장소 ID')
    op.alter_column('t_place_info_m01', 'PLACE_CTPRVN',
               existing_type=mysql.VARCHAR(length=10),
               comment='장소 시도',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'PLACE_ADRES',
               existing_type=mysql.VARCHAR(length=500),
               comment='장소 주소',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'LO',
               existing_type=mysql.VARCHAR(length=30),
               comment='경도',
               existing_nullable=True)
    op.alter_column('t_place_info_m01', 'LA',
               existing_type=mysql.VARCHAR(length=30),
               comment='위도',
               existing_nullable=True)
    op.create_table_comment(
        't_pick_place_h01',
        '사용자 선택 장소 히스토리 테이블',
        existing_comment=None,
        schema=None
    )
    op.alter_column('t_pick_place_h01', 'SN',
               existing_type=mysql.INTEGER(display_width=11),
               comment='일련번호',
               autoincrement=True)
    op.alter_column('t_pick_place_h01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment='등록 날짜',
               existing_nullable=False,
               existing_server_default=sa.text('current_timestamp()'))
    op.alter_column('t_pick_place_h01', 'PLACE_SIGNGU',
               existing_type=mysql.VARCHAR(length=20),
               comment='장소 시군구',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'PLACE_RN_ADRES',
               existing_type=mysql.VARCHAR(length=500),
               comment='장소 도로명 주소',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'PLACE_NM',
               existing_type=mysql.VARCHAR(length=100),
               comment='장소 이름',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'PLACE_ID',
               existing_type=mysql.VARCHAR(length=20),
               comment='장소 ID',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'PLACE_CTPRVN',
               existing_type=mysql.VARCHAR(length=10),
               comment='장소 시도',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'PLACE_ADRES',
               existing_type=mysql.VARCHAR(length=500),
               comment='장소 주소',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'LO',
               existing_type=mysql.VARCHAR(length=30),
               comment='경도',
               existing_nullable=True)
    op.alter_column('t_pick_place_h01', 'LA',
               existing_type=mysql.VARCHAR(length=30),
               comment='위도',
               existing_nullable=True)
    op.add_column('t_admin_info_m01', sa.Column('LAST_LOGIN_DATE', mysql.TIMESTAMP(), nullable=True, comment='마지막 로그인 날짜'))
    op.create_table_comment(
        't_admin_info_m01',
        '관리자 정보',
        existing_comment=None,
        schema=None
    )
    op.drop_index(op.f('ix_t_admin_info_m01_NM'), table_name='t_admin_info_m01')
    op.drop_index(op.f('ix_t_admin_info_m01_ID'), table_name='t_admin_info_m01')
    op.drop_index(op.f('ix_t_admin_info_m01_EMAIL'), table_name='t_admin_info_m01')
    op.alter_column('t_admin_info_m01', 'UPDT_ID',
               existing_type=mysql.VARCHAR(length=30),
               comment='수정 ID',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'UPDT_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment='수정 날짜',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'TELNO',
               existing_type=mysql.VARCHAR(length=15),
               comment='전화번호',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'SN',
               existing_type=mysql.INTEGER(display_width=11),
               comment='일련번호',
               autoincrement=True)
    op.alter_column('t_admin_info_m01', 'REGIST_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment='등록 날짜',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'PASSWORD',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True,
               comment='비밀번호')
    op.alter_column('t_admin_info_m01', 'NM',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True,
               comment='이름')
    op.alter_column('t_admin_info_m01', 'JURANG',
               existing_type=mysql.VARCHAR(length=10),
               comment='관할구역',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'INSTT_NM',
               existing_type=mysql.VARCHAR(length=100),
               comment='기관 이름',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'ID',
               existing_type=mysql.VARCHAR(length=30),
               nullable=True,
               comment='ID')
    op.alter_column('t_admin_info_m01', 'EMAIL',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True,
               comment='이메일')
    op.alter_column('t_admin_info_m01', 'DEPT_NM',
               existing_type=mysql.VARCHAR(length=100),
               comment='부서 이름',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'DELETE_ID',
               existing_type=mysql.VARCHAR(length=30),
               comment='삭제 ID',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'DELETE_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment='삭제 날짜',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'DELETE_AT',
               existing_type=mysql.VARCHAR(length=1),
               comment='삭제 여부',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'CONFM_ID',
               existing_type=mysql.VARCHAR(length=30),
               comment='승인 ID',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'CONFM_DATE',
               existing_type=mysql.TIMESTAMP(),
               comment='승인 날짜',
               existing_nullable=True)
    op.alter_column('t_admin_info_m01', 'CONFM_AT',
               existing_type=mysql.VARCHAR(length=1),
               nullable=True,
               comment='승인 여부')
    op.alter_column('t_admin_info_m01', 'AUTHOR',
               existing_type=mysql.VARCHAR(length=20),
               comment='권한',
               existing_nullable=True)
    op.drop_column('t_admin_info_m01', 'LAST_LOGIN')
    op.create_table('T_COMCODE_M01',
    sa.Column('GROUP_CODE', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('CODE', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('CODE_VALUE', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('REGIST_DATE', mysql.DATETIME(), server_default=sa.text('current_timestamp()'), nullable=False),
    sa.Column('CODE_DC', mysql.VARCHAR(length=1000), nullable=True),
    sa.Column('USE_AT', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.Column('RM_1', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('RM_2', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('RM_3', mysql.VARCHAR(length=50), nullable=True),
    sa.CheckConstraint('`USE_AT` in (0,1)', name='CONSTRAINT_1'),
    sa.PrimaryKeyConstraint('GROUP_CODE', 'CODE'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_T_COMCODE_M01_GROUP_CODE', 'T_COMCODE_M01', ['GROUP_CODE'], unique=False)
    op.create_index('ix_T_COMCODE_M01_CODE', 'T_COMCODE_M01', ['CODE'], unique=True)
    op.create_table('T_ADMIN_INFO_M01',
    sa.Column('SN', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('ID', mysql.VARCHAR(length=30), nullable=False),
    sa.Column('NM', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('PASSWORD', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('TELNO', mysql.VARCHAR(length=15), nullable=True),
    sa.Column('CONFM_AT', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.Column('CONFM_ID', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('CONFM_DATE', mysql.DATETIME(), nullable=True),
    sa.Column('REGIST_DATE', mysql.DATETIME(), server_default=sa.text('current_timestamp()'), nullable=True),
    sa.Column('UPDT_ID', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('UPDT_DATE', mysql.DATETIME(), server_default=sa.text('current_timestamp()'), nullable=True),
    sa.Column('DELETE_AT', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.Column('DELETE_ID', mysql.VARCHAR(length=30), nullable=True),
    sa.Column('DELETE_DATE', mysql.DATETIME(), nullable=True),
    sa.Column('LAST_LOGIN', mysql.DATETIME(), nullable=True),
    sa.Column('AUTHOR', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('JURANG', mysql.VARCHAR(length=20), nullable=True),
    sa.Column('EMAIL', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('INSTT_NM', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('DEPT_NM', mysql.VARCHAR(length=100), nullable=True),
    sa.CheckConstraint('`CONFM_AT` in (0,1)', name='CONSTRAINT_1'),
    sa.CheckConstraint('`DELETE_AT` in (0,1)', name='CONSTRAINT_2'),
    sa.PrimaryKeyConstraint('SN'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_T_ADMIN_INFO_M01_NM', 'T_ADMIN_INFO_M01', ['NM'], unique=False)
    op.create_index('ix_T_ADMIN_INFO_M01_ID', 'T_ADMIN_INFO_M01', ['ID'], unique=True)
    op.create_index('ix_T_ADMIN_INFO_M01_EMAIL', 'T_ADMIN_INFO_M01', ['EMAIL'], unique=True)
    op.create_table('dgrs_fclts',
    sa.Column('address_name', mysql.VARCHAR(length=1000), nullable=True),
    sa.Column('category_group_code', mysql.VARCHAR(length=1000), nullable=True),
    sa.Column('category_group_name', mysql.VARCHAR(length=1000), nullable=True),
    sa.Column('category_name', mysql.VARCHAR(length=1000), nullable=True),
    sa.Column('distance', mysql.VARCHAR(length=1000), nullable=True),
    sa.Column('id', mysql.VARCHAR(length=1000), nullable=True),
    sa.Column('phone', mysql.VARCHAR(length=1000), nullable=True),
    sa.Column('place_name', mysql.VARCHAR(length=1000), nullable=True),
    sa.Column('place_url', mysql.VARCHAR(length=1000), nullable=True),
    sa.Column('road_address_name', mysql.VARCHAR(length=1000), nullable=True),
    sa.Column('x', mysql.VARCHAR(length=1000), nullable=True),
    sa.Column('y', mysql.VARCHAR(length=1000), nullable=True),
    mysql_default_charset='utf8',
    mysql_engine='CONNECT'
    )
    op.create_table('t_comcode_m01',
    sa.Column('GROUP_CODE', mysql.VARCHAR(length=30), nullable=False, comment='그룹 코드'),
    sa.Column('CODE', mysql.VARCHAR(length=30), nullable=False, comment='코드'),
    sa.Column('CODE_VALUE', mysql.VARCHAR(length=30), nullable=False, comment='코드 값'),
    sa.Column('REGIST_DATE', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp() ON UPDATE current_timestamp()'), nullable=False, comment='등록 날짜'),
    sa.Column('CODE_DC', mysql.VARCHAR(length=1000), nullable=True, comment='코드 설명'),
    sa.Column('USE_AT', mysql.VARCHAR(length=1), nullable=False, comment='사용 여부'),
    sa.Column('RM_1', mysql.VARCHAR(length=50), nullable=True, comment='비고 1'),
    sa.Column('RM_2', mysql.VARCHAR(length=50), nullable=True, comment='비고 2'),
    sa.Column('RM_3', mysql.VARCHAR(length=50), nullable=True, comment='비고 3'),
    sa.PrimaryKeyConstraint('GROUP_CODE', 'CODE'),
    comment='공통코드',
    mysql_comment='공통코드',
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('UC_CODE', 't_comcode_m01', ['CODE'], unique=True)
    op.create_table('t_analysis_result_m01',
    sa.Column('SN', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False, comment='일련번호'),
    sa.Column('USER_SN', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True, comment='사용자 일련번호'),
    sa.Column('REGIST_DATE', mysql.TIMESTAMP(), nullable=True, comment='등록 날짜'),
    sa.Column('RISK_GRAD', mysql.VARCHAR(length=10), nullable=True, comment='위험 등급'),
    sa.ForeignKeyConstraint(['USER_SN'], ['t_user_info_m01.SN'], name='FK_T_ANALYSIS_RESULT_M01_USER_SN_T_USER_INFO_M01_SN'),
    sa.PrimaryKeyConstraint('SN'),
    comment='분석결과 정보',
    mysql_comment='분석결과 정보',
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_index(op.f('ix_t_comcode_01_GROUP_CODE'), table_name='t_comcode_01')
    op.drop_index(op.f('ix_t_comcode_01_CODE'), table_name='t_comcode_01')
    op.drop_table('t_comcode_01')
    # ### end Alembic commands ###