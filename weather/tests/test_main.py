##########################################################################################
#    天気情報を取得するAPIのテストコードです。
##########################################################################################
import api.main as main

def test_check():
    assert main.check()["result"] in [0, 1, 2, 3, 4, 5]
