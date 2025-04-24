from .db_config import supabase


def upload_to_store(filename, file):
    """"
    Func to upload to supabase bucket
    Args:
        filename: str = The title/video title of the pdf
        file: str = saved in .pdf format
    """
    store = supabase.storage.from_("podfiles").upload(
        f"transcripts/{filename}.pdf", file
    )
    return store


def get_file_url(filename):
    """
    Func to get the url of the transcript pdf in supabase bucket
    Args:
        filename: str = The title/video title of the pdf
    """
    file_url = supabase.storage.from_("podfiles").get_public_url(
        f"transcripts/{filename}.pdf"
    )
    return file_url
