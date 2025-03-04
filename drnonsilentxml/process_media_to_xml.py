import os
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, indent, ElementTree
from typing import List, Dict, Optional
from pydub import AudioSegment, silence
from drnonsilentxml.utils.ipcn_enumerate import ipcn_enumerate
from drnonsilentxml.utils.to_xml import to_xml
from drnonsilentxml.utils.frames import frames


IN = 0
OUT = 1

def process_media_to_xml(input_file: str, output_file: str, 
                         input_fps: float, output_fps: float, 
                         silence_thresh: int = -40,
                         padding_ms: int = 300) -> None:
    """
    Process an audio/media file, detect non-silent segments, and generate XML for video editing.
    
    Args:
        input_file: Path to the audio/media input file
        output_file: Path for XML output file
        input_fps: Input frames per second
        output_fps: Output frames per second
        silence_thresh: Threshold for silence detection in dB (default: -40)
        padding_ms: Milliseconds to add as padding to non-silent segments (default: 300)
    """
    filename = input_file
    i_fps = input_fps
    o_fps = output_fps

    root = Element('xmeml', {'version': '5'})
    sound = AudioSegment.from_file(filename)


    start_ms = 0
    vclipitems = []
    aclipitems = []
    for i, pre, chunk, nex in ipcn_enumerate(silence.detect_nonsilent(sound, silence_thresh=silence_thresh)):
        # padding_ms適用
        if pre is not None:
            chunk[IN] = max(0, pre[OUT], chunk[IN]-padding_ms)
        else:
            chunk[IN] = max(0, chunk[IN]-padding_ms)
        # padding_ms適用
        if nex is not None:
            chunk[OUT] = min(len(sound), nex[IN], chunk[OUT]+padding_ms)
        else:
            chunk[OUT] = min(len(sound), chunk[OUT]+padding_ms)
        
        vclipItemId = '{:s} {:d}'.format(os.path.basename(filename), i)
        aclipItemId = '{:s} {:d}'.format(os.path.basename(filename), 10000+i)
        vclipitems.append(
            ('clipitem', [
                ('name', os.path.basename(filename)),
                ('duration', frames(len(sound), i_fps, o_fps)),
                ('rate', [
                    ('timebase', i_fps),
                    ('ntsc', 'TRUE'),
                ]), 
                ('start', frames(start_ms, i_fps, o_fps)),
                ('end',   frames(start_ms + chunk[OUT] - chunk[IN], i_fps, o_fps)),
                ('enabled', 'TRUE'),
                ('in',  frames(chunk[IN], i_fps, o_fps)),
                ('out', frames(chunk[OUT], i_fps, o_fps)),
                ('file', [
                    ('duration', frames(len(sound), i_fps, o_fps)),
                    ('rate', [
                        ('timebase', i_fps),
                        ('ntsc', 'TRUE'),
                    ]), 
                    ('name', 'Slug'),
                    ('timecode', [
                        ('string',  '00:00:00:00'),
                        ('displayformat',   'NDF'),
                        ('rate',     [
                            ('timebase', i_fps),
                            ('ntsc', 'TRUE'),
                        ]), 
                    ]), 
                    ('media', [
                        ('video', [
                            ('samplecharacteristics', [
                                ('width', '2560'),
                                ('height', '1440')
                            ]) 
                        ]), 
                        ('audio', [
                            ('channelcount', '2')
                        ]), 
                    ]), 
                    ('mediaSource', 'Slug'),
                ] if i == 0 else '', {'id': '{:s} {:s}'.format(os.path.basename(filename), '-1')}), 
                ('compositemode', 'normal'),
                ('link', [
                    ('linkclipref', vclipItemId)
                ]), 
                ('link', [
                    ('linkclipref', aclipItemId)
                ]), 
                ('comments', ''),
            ], {'id': vclipItemId})
        )
        aclipitems.append(
            ('clipitem', [
                ('name', os.path.basename(filename)),
                ('duration', frames(len(sound), i_fps, o_fps)),
                ('rate', [
                    ('timebase', i_fps),
                    ('ntsc', 'TRUE'),
                ]), 
                ('start', frames(start_ms, i_fps, o_fps)),
                ('end',   frames(start_ms + chunk[OUT] - chunk[IN], i_fps, o_fps)),
                ('enabled', 'TRUE'),
                ('in',  frames(chunk[IN], i_fps, o_fps)),
                ('out', frames(chunk[OUT], i_fps, o_fps)),
                ('file', '', {'id': '{:s} {:s}'.format(os.path.basename(filename), '-1')}), 
                ('sourcetrack', [
                    ('mediatype', 'audio'),
                    ('trackindex', '1'),
                ]), 
                ('link', [
                    ('linkclipref', vclipItemId),
                    ('mediatype', 'video'),
                ]), 
                ('link', [
                    ('linkclipref', aclipItemId),
                ]), 
                ('comments', ''),
            ], {'id': aclipItemId})
        )
        start_ms += chunk[OUT] - chunk[IN]


    to_xml(root, [
        ('sequence', [
            ('name', os.path.splitext(os.path.basename(filename))[0]),
            ('duration', frames(start_ms, i_fps, o_fps)),
            ('rate', [
                ('timebase', i_fps),
                ('ntsc', 'TRUE'),
            ]), 
            ('in',  '-1'),
            ('out', '-1'),
            ('timecode', [
                ('string',  '01:00:00:00'),
                ('frame',   str(i_fps * 3600)),
                ('displayformat',   'NDF'),
                ('rate',     [
                    ('timebase', i_fps),
                    ('ntsc', 'TRUE'),
                ]), 
            ]), 
            ('media', [
                ('video', [
                    ('track',  vclipitems),
                    ('format', [
                        ('samplecharacteristics', [
                            ('width', '2560'),
                            ('height', '1440'),
                            ('pixelaspectratio', 'square'),
                            ('rate',     [
                                ('timebase', i_fps),
                                ('ntsc', 'TRUE'),
                            ]), 
                            ('codec',     [
                                ('appspecificdata', [
                                    ('appname', 'Final Cut Pro'),
                                    ('appmanufacturer', 'Apple Inc.'),
                                    ('data', [
                                        ('qtcodec', '')
                                    ]), 
                                ]), 
                            ]), 
                        ]) 
                    ]), 
                ]), 
                ('audio', [
                    ('track',  aclipitems),
                    ('enabled', 'TRUE'),
                    ('locked',  'FALSE'),
                ]), 
            ]), 
        ])
    ])
    indent(root, space="\t", level=0)
    # print(tostring(root))
    
    # ファイルに書き込み
    tree = ElementTree(root)
    with open(output_file, mode='wb') as f:
        f.write(("\n".join([
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<!DOCTYPE xmeml>',
            '',
        ])).encode('utf8'))
        tree.write(f, encoding="utf-8")

