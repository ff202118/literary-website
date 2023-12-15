from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = 'l%3ya7fn3moipdpcltj(tdfcv5^@lj=t5d&72levvls+y*@_4^'

SQLALCHEMY_DATABASE_URI = 'mysql://root:fjq159357@127.0.0.1:3306/Web_DB'

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
