import argparse
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
    
    process_media_to_xml(
        input_file=args.input,
        output_file=args.output,
        input_fps=args.input_fps,
        output_fps=args.output_fps,
        silence_thresh=args.threshold,
        padding_ms=args.padding
    )

if __name__ == "__main__":
    main()
