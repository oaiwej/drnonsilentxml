import argparse
import os
import sys
from drnonsilentxml.process_media_to_xml import process_media_to_xml

def main():
    """
    Main entry point for the drnonsilentxml application.
    """
    parser = argparse.ArgumentParser(
        description="Convert audio/media file to non-silent XML segments for video editing"
    )
    parser.add_argument("-i", "--input", type=str, required=True, 
                        help="Input audio/media file path")
    parser.add_argument("-if", "--input-fps", type=float, required=True, default=60,
                        help="Input frames per second")
    parser.add_argument("-o", "--output", type=str, required=True,
                        help="Output XML file path")
    parser.add_argument("-of", "--output-fps", type=float, required=True, default=59.94,
                        help="Output frames per second")
    parser.add_argument("-t", "--threshold", type=int, default=-40,
                        help="Silence threshold in dB (default: -40)")
    parser.add_argument("-p", "--padding", type=int, default=300,
                        help="Milliseconds to extend non-silent segments (default: 300)")
    
    args = parser.parse_args()
    
    # 入力ファイルの存在確認
    input_file = args.input
    if not os.path.exists(input_file):
        print(f"エラー: 入力ファイル '{input_file}' が見つかりません。", file=sys.stderr)
        sys.exit(1)
    
    # 出力ディレクトリの存在確認
    output_dir = os.path.dirname(os.path.abspath(args.output))
    if not os.path.exists(output_dir):
        print(f"警告: 出力ディレクトリ '{output_dir}' が存在しません。作成します。", file=sys.stderr)
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            print(f"エラー: 出力ディレクトリの作成に失敗しました: {e}", file=sys.stderr)
            sys.exit(1)
    
    try:
        process_media_to_xml(
            input_file=input_file,
            output_file=args.output,
            input_fps=args.input_fps,
            output_fps=args.output_fps,
            silence_thresh=args.threshold,
            padding_ms=args.padding
        )
        print(f"完了: XMLタイムラインが '{args.output}' に生成されました。")
    except Exception as e:
        print(f"エラー: 処理中にエラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
