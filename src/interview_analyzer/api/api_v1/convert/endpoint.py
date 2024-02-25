from interview_analyzer.utils.files import extract_audio, cleanup_temp_file, write_bytes_file_to_temp_file


async def convert_audio_filetype(file_bytes: bytes, filename: str, output_filetype: str) -> str:
    saved_filepath = write_bytes_file_to_temp_file(file_bytes, filename, rename=False)
    output_filepath = extract_audio(input_file=saved_filepath, output_filetype=output_filetype)
    cleanup_temp_file(filepath=saved_filepath)
    return output_filepath
