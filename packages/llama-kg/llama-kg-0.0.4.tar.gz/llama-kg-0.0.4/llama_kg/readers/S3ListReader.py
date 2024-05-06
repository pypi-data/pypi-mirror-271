"""S3 file and directory reader.

A loader that fetches a file or iterates through a directory on AWS S3.
based on: https://github.com/emptycrown/llama-hub/tree/main/llama_hub/s3 
"""
import tempfile
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

from botocore.utils import fix_s3_host

from llama_index.core import download_loader
from llama_index.core.readers.base import BaseReader
from llama_index.core.readers import Document

class S3ListReader(BaseReader):
    """General reader for an S3 list of filekeyss"""
    def __init__(
        self,
        *args: Any,
        bucket: str,
        keys: List[str],
        file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = None,
        required_exts: Optional[List[str]] = None,
        filename_as_id: bool = False,
        num_files_limit: Optional[int] = None,
        file_metadata: Optional[Callable[[str], Dict]] = None,
        aws_access_id: Optional[str] = None,
        aws_access_secret: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        s3_endpoint_url: Optional[str] = "https://s3.amazonaws.com",
        **kwargs: Any,
    ) -> None:
        """Initialize S3 bucket and key, along with credentials if needed.

        Args:
        bucket (str): the name of your S3 bucket
        keys (List[str]): the names of  specific files. Must be include prefix.
        file_extractor (Optional[Dict[str, BaseReader]]): A mapping of file
            extension to a BaseReader class that specifies how to convert that file
            to text. See `SimpleDirectoryReader` for more details.
        required_exts (Optional[List[str]]): List of required extensions.
            Default is None.
        num_files_limit (Optional[int]): Maximum number of files to read.
            Default is None.
        file_metadata (Optional[Callable[str, Dict]]): A function that takes
            in a filename and returns a Dict of metadata for the Document.
            Default is None.
        aws_access_id (Optional[str]): provide AWS access key directly.
        aws_access_secret (Optional[str]): provide AWS access key directly.
        s3_endpoint_url (Optional[str]): provide S3 endpoint URL directly.
        """
        super().__init__(*args, **kwargs)

        self.bucket = bucket
        self.keys = keys

        self.file_extractor = file_extractor
        self.required_exts = required_exts
        self.filename_as_id = filename_as_id
        self.num_files_limit = num_files_limit
        self.file_metadata = file_metadata

        self.aws_access_id = aws_access_id
        self.aws_access_secret = aws_access_secret
        self.aws_session_token = aws_session_token
        self.s3_endpoint_url = s3_endpoint_url

    def load_data(self) -> List[Document]:
        """Load file(s) from S3."""
        import boto3

        s3 = boto3.resource("s3")
        s3_client = boto3.client("s3")
        if self.aws_access_id:
            session = boto3.Session(region_name='us-west-1')

            s3 = session.resource(
                "s3", 
                aws_access_key_id=self.aws_access_id,
                aws_secret_access_key=self.aws_access_secret,
                endpoint_url=self.s3_endpoint_url
            )

            s3_client = session.client(
                service_name="s3", 
                aws_access_key_id=self.aws_access_id,
                aws_secret_access_key=self.aws_access_secret,
                endpoint_url=self.s3_endpoint_url
            )

        with tempfile.TemporaryDirectory() as temp_dir:
            if False:
                suffix = Path(self.key).suffix
                filepath = f"{temp_dir}/{next(tempfile._get_candidate_names())}{suffix}"
                s3_client.download_file(self.bucket, self.key, filepath)
            else:
                bucket = s3.Bucket(self.bucket)
                for i, obj in enumerate(self.keys):
                    if self.num_files_limit is not None and i > self.num_files_limit:
                        break

                    suffix = Path(obj).suffix

                    is_dir = obj.endswith("/") # skip folders
                    is_bad_ext = (
                        self.required_exts is not None and suffix not in self.required_exts # skip other extentions
                    )

                    if is_dir or is_bad_ext:
                        continue

                    if self.filename_as_id:
                        file_name = obj.split('/')[-1]
                        filepath = (
                            f"{temp_dir}/{file_name}"
                        )
                    else:
                        filepath = (
                            f"{temp_dir}/{next(tempfile._get_candidate_names())}{suffix}"
                        )
                    s3_client.download_file(self.bucket, obj, filepath)

            try:
                from llama_index import SimpleDirectoryReader
            except ImportError:
                SimpleDirectoryReader = download_loader("SimpleDirectoryReader")

            loader = SimpleDirectoryReader(temp_dir,
                                           file_extractor=self.file_extractor,
                                           required_exts=self.required_exts,
                                           filename_as_id=self.filename_as_id,
                                           num_files_limit=self.num_files_limit,
                                           file_metadata=self.file_metadata)

            return loader.load_data()

