##########################################################################################
#   天気情報を取得するAPIです。
##########################################################################################
import sys
import os
import bottle
from bottle import run


# カレントディレクトリーを変更
BASEDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASEDIR)
os.chdir(BASEDIR)

# Apache2に対応するWSGIアプリケーションを始動: "application" の名前は必須
import main
application = bottle.default_app()

if "DEBUG" in os.environ:
	run(
		host="127.0.0.1",
		port=80
	)
