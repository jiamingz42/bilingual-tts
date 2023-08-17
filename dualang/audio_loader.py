import tempfile
import ffmpeg

from pydub import playback
from pydub import AudioSegment  # type: ignore


def load_audio_segment(input_audio: str, verbose: bool = False) -> AudioSegment:
    """
    Converts an MKV file into an AudioSegment.

    Args:
        input_audio (str): Path to the input MKV file.

    Returns:
        AudioSegment: The audio data from the MKV file.
    """
    # Check if the input file is an MKV file
    if input_audio.endswith(".mkv"):
        # Use ffmpeg to get the number of audio tracks in the file
        probe = ffmpeg.probe(input_audio)
        audio_tracks = [
            stream for stream in probe["streams"] if stream["codec_type"] == "audio"
        ]
        if len(audio_tracks) > 1:
            selected_track = get_selected_track(audio_tracks, input_audio)
        else:
            selected_track = 0
        # Use ffmpeg to copy the selected audio track to a temporary file without re-encoding it
        codec_name = audio_tracks[selected_track]["codec_name"]
        temp_audio = tempfile.mktemp(suffix=f".{codec_name}")
        out, err = (
            ffmpeg.input(input_audio)
            .output(temp_audio, map=f"0:{selected_track}", c="copy")
            .run(capture_stdout=True, capture_stderr=True)
        )
        print(err, file=sys.stderr)
        if verbose:
            print(out)
        # Load the temporary file using AudioSegment.from_file
        input_audio = AudioSegment.from_file(temp_audio)
        print("Loaded input audio from MKV file")
    else:
        # Load the input audio file using AudioSegment.from_file
        input_audio = AudioSegment.from_file(input_audio)
        print("Loaded input audio")

    return input_audio


def get_selected_track(audio_tracks, input_audio):
    # If there is more than one audio track, ask the user to select one
    print(f"The MKV file has {len(audio_tracks)} audio tracks.")
    for i, track in enumerate(audio_tracks, start=1):
        print(
            f'{i}: {track["tags"]["language"] if "tags" in track and "language" in track["tags"] else "unknown"} (codec: {track["codec_name"]})'
        )

    listen_sample = input(
        "Do you want to listen to a sample of the audio tracks? (yes/no): "
    )
    if listen_sample.lower() == "yes":
        for i, track in enumerate(audio_tracks, start=1):
            codec_name = track["codec_name"]
            temp_audio = tempfile.mktemp(suffix=f".{codec_name}")
            out, err = (
                ffmpeg.input(input_audio)
                .output(temp_audio, map=f"0:{i-1}", c="copy")
                .run(capture_stdout=True, capture_stderr=True)
            )
            print(out, err)
            sample_audio = AudioSegment.from_file(temp_audio)[
                :30000
            ]  # Get the first 30 seconds
            print(f"Playing sample for track {i}:")
            playback.play(sample_audio)
    selected_track = int(input("Please select an audio track: ")) - 1
    return selected_track
