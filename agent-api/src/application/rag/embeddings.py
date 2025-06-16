from langchain_huggingface import HuggingFaceEmbeddings



def get_embedding_model(
        model_id : str,
        device:str = "cpu"
)-> HuggingFaceEmbeddings:
    return get_huggingface_embedding_model(model_id,device)


def get_huggingface_embedding_model(
        model_id: str,
        device:str
)-> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name = model_id,
        model_kwargs = {
            "device":device,
            "trust_remote_code":True,
        },
        encode_kwargs = {
            "normalize_embeddings":False,
        }
    )