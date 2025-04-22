from .db_config import supabase


def upload_to_store(filename, file):
    store = supabase.storage.from_("podfiles").upload(f"transcripts/{filename}.pdf", file)
    return store


def get_file_url(filename):
    file_url = supabase.storage.from_("podfiles").get_public_url(f"transcripts/{filename}.pdf")
    return file_url