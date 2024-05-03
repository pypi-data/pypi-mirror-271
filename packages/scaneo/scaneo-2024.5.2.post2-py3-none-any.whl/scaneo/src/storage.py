import os
from minio import Minio
from glob import glob
import fnmatch
import rasterio as rio
import pandas as pd
import json
import io
import requests
from eotdl.files import list_files
from eotdl.datasets import retrieve_dataset
from eotdl.repos import FilesAPIRepo
from eotdl.auth import with_auth
import shutil


class Storage:
    def __init__(self):
        # if valid environment variables are set, use cloud storage
        url = os.getenv("URL")
        access_key = os.getenv("ACCESS_KEY")
        secret_key = os.getenv("SECRET_KEY")
        bucket = os.getenv("BUCKET")
        eotdl = os.getenv("EOTDL")
        if eotdl:
            self.storage = EOTDLStorage(eotdl)
            self.name = "eotdl/" + eotdl
            self.is_stac = False
        elif url and access_key and secret_key and bucket:
            self.storage = CloudStorage(
                url,
                access_key,
                secret_key,
                bucket,
                os.getenv("REGION", "us-east-1"),
                os.getenv("PREFIX", None),
            )
            self.name = "cloud/" + url + "/" + bucket
            self.is_stac = self.exists("catalog.json")
        # otherwise, use local storage
        else:
            path = os.getenv("DATA")
            if not path:
                raise Exception("No storage specified.")
            self.storage = LocalStorage(os.getenv("DATA"))
            self.name = "local/" + path
            self.is_stac = self.exists("catalog.json")
        self.name = self.name.replace("/", "_")

    def get_stac_catalog(self) -> dict:
        catalog_file = [f for f in self.list() if f.endswith("catalog.json")]
        if not catalog_file:
            raise Exception("No catalog file found.")
        return self.read(catalog_file[0])

    def list(self, pattern=None):
        return self.storage.list(pattern)

    def get_url(self, name):
        return self.storage.get_url(name)

    def exists(self, name):
        return self.storage.exists(name)

    def read(self, name):
        ext = name.split(".")[-1]
        if ext in ["tif", "tiff"]:
            return rio.open(self.get_url(name))
        elif ext in ["json", "geojson"]:
            # return pd.read_json(self.get_url(name)).to_json() # problem with SSL certificate
            url = self.get_url(name)
            if type(url) == io.BytesIO:
                return json.load(url)
            if url.startswith("http://") or url.startswith("https://"):
                response = requests.get(url)
                return json.loads(response.json())
            with open(url, "r") as file:
                return json.load(file)
        raise TypeError("Not a valid type")

    def save(self, name, data):
        return self.storage.save(name, data)

    def path(self):
        return str(self.storage.path)


class EOTDLStorage:
    def __init__(self, dataset):
        self.url = "https://api.eotdl.com/"
        # self.url = "http://localhost:8001/"
        os.environ["EOTDL_API_URL"] = self.url
        os.system("eotdl auth login")
        dataset = retrieve_dataset(dataset)
        self.dataset = dataset
        assert dataset["quality"] == 0, "Only Q0 datasets are supported."
        self.download_url = self.url + "datasets/" + dataset["id"] + "/download/"
        self.repo = FilesAPIRepo(self.url)

    def list(self, pattern):
        files = list_files(self.dataset["name"])
        files = [f["filename"] for f in files]
        if pattern:
            return fnmatch.filter(files, pattern)
        return files

    @with_auth
    def get_url(self, filename, user):
        # instead of a url it returns the data stream directly
        return self.repo.get_file_stream(self.dataset["id"], filename, user)

    def exists(self, name):
        return name in self.list()

    @with_auth
    def save(self, name, data, user):
        path = "/tmp/scaneo/" + name
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(json.loads(data), f)
        repo = FilesAPIRepo(self.url)
        last_version = sorted([v["version_id"] for v in self.dataset["versions"]])[-1]
        data, error = repo.ingest_file(
            path,
            self.dataset["id"],
            user,
            calculate_checksum(path),
            "datasets",
            last_version,
        )
        if error:
            raise Exception(error)
        shutil.rmtree("/tmp/scaneo")

    def path(self):
        pass


import hashlib


def calculate_checksum(file_path):
    sha1_hash = hashlib.sha1()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha1_hash.update(chunk)
    return sha1_hash.hexdigest()


class LocalStorage:
    def __init__(self, path):
        self.path = path

    def list(self, pattern):
        pattern = "**/*" if not pattern else pattern
        paths = glob(os.path.join(self.path, pattern), recursive=True)
        return [p.replace(self.path + "/", "") for p in paths]

    def get_url(self, name):
        return os.path.join(self.path, name)

    def exists(self, name):
        return os.path.exists(os.path.join(self.path, name))

    def save(self, name, data):
        with open(os.path.join(self.path, name), "w") as f:
            json.dump(json.loads(data), f)
        return self.get_url(name)

    def path(self):
        return self.path


class CloudStorage:
    def __init__(self, url, access_key, secret_key, bucket, region, prefix=None):
        self.url = url
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
        self.prefix = prefix
        self.region = region
        self.client = Minio(
            endpoint=url,
            access_key=access_key,
            secret_key=secret_key,
            secure=True,
            region=region,
        )
        if not self.client.bucket_exists(self.bucket):
            raise Exception("Bucket does not exist.")

    def list(self, pattern):
        pattern = "**/*" if not pattern else pattern
        return fnmatch.filter(
            [
                obj.object_name
                for obj in self.client.list_objects(self.bucket, recursive=True)
                # for obj in self.client.list_objects(self.bucket, prefix=self.prefix)
            ],
            pattern,
        )

    def get_name(self, name):
        return name if not self.prefix else os.path.join(self.prefix, name)

    def get_url(self, name):
        return self.client.presigned_get_object(self.bucket, self.get_name(name))

    def exists(self, name):
        try:
            return self.client.stat_object(self.bucket, self.get_name(name))
        except:
            return False

    def save(self, name, data):
        data = json.dumps(data)
        data_bytes = data.encode("utf-8")
        data_file = io.BytesIO(data_bytes)
        self.client.put_object(
            self.bucket, self.get_name(name), data_file, len(data_bytes)
        )
        return self.get_url(name)

    def path(self):
        return self.url
