import unittest
import sys
import os

# テストディレクトリをPATHに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# すべてのテストをロードして実行
if __name__ == '__main__':
    test_suite = unittest.defaultTestLoader.discover('.', pattern='test_*.py')
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # 終了コードを設定（テスト失敗時は非ゼロ）
    sys.exit(not result.wasSuccessful())
