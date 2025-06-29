import os
from moviepy import ImageClip, AudioFileClip
from pydub import AudioSegment, silence


def combine_image_audio(image_path, audio_path, output_path):
    """Combines an image and an audio file into a video with duration of the audio."""
    audio = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path).set_duration(audio.duration)
    video = image_clip.set_audio(audio)
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")


def remove_silence(audio_path, output_path, mode='intermedio'):
    """Removes silence from an audio file with strictness levels."""
    audio = AudioSegment.from_file(audio_path)
    thresholds = {
        'estricto': -50,
        'intermedio': -40,
        'laxo': -30,
    }
    thresh = thresholds.get(mode, -40)
    silent_ranges = silence.detect_silence(audio, min_silence_len=500, silence_thresh=thresh)
    chunks = []
    prev_end = 0
    for start, end in silent_ranges:
        if start > prev_end:
            chunks.append(audio[prev_end:start])
        prev_end = end
    if prev_end < len(audio):
        chunks.append(audio[prev_end:])
    out_audio = sum(chunks)
    out_audio.export(output_path, format=os.path.splitext(output_path)[1][1:])


def autoduck(background_path, voice_path, output_path, duck_level=-20):
    """Lowers background volume when voice is present."""
    background = AudioSegment.from_file(background_path)
    voice = AudioSegment.from_file(voice_path)
    combined = background.overlay(voice, gain_during_overlay=duck_level)
    combined.export(output_path, format=os.path.splitext(output_path)[1][1:])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Editor de video con IA simple")
    subparsers = parser.add_subparsers(dest='command')

    parser_combine = subparsers.add_parser('combine')
    parser_combine.add_argument('image')
    parser_combine.add_argument('audio')
    parser_combine.add_argument('output')

    parser_silence = subparsers.add_parser('silence')
    parser_silence.add_argument('audio')
    parser_silence.add_argument('output')
    parser_silence.add_argument('--mode', choices=['estricto', 'intermedio', 'laxo'], default='intermedio')

    parser_duck = subparsers.add_parser('duck')
    parser_duck.add_argument('background')
    parser_duck.add_argument('voice')
    parser_duck.add_argument('output')
    parser_duck.add_argument('--level', type=int, default=-20)

    args = parser.parse_args()

    if args.command == 'combine':
        combine_image_audio(args.image, args.audio, args.output)
    elif args.command == 'silence':
        remove_silence(args.audio, args.output, args.mode)
    elif args.command == 'duck':
        autoduck(args.background, args.voice, args.output, args.level)
    else:
        parser.print_help()

