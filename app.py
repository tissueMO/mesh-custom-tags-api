# coding: utf-8
##########################################################################################
#   WSGIアプリケーションの起動設定を行います。
##########################################################################################
import sys
import os
import bottle
from bottle import run


# カレントディレクトリーを変更
BASEDIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASEDIR)
os.chdir(BASEDIR)

# ルーティング設定を読み込み
import status.route
import holiday.route
import weather.route

# Apache2に対応するWSGIアプリケーションを始動: "application" の名前は必須
application = bottle.default_app()

if "DEBUG" in os.environ:
	run(
		host="127.0.0.1",
		port=80
	)
