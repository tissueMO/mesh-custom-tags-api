# coding: utf-8
##########################################################################################
#   ルーティング設定とAPI処理内容を定義します。
##########################################################################################
from bottle import get, post, request
import sqlite3
import configparser

# サブモジュールを読み込み
import status.medicine
import status.has_item
