from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter

def get_spliter(chunk_size:int)->splitter:
    chunk_overlap = int(0.15*chunk_size)

    return RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )

