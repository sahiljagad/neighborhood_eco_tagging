import os
import requests
import time
from pathlib import Path
from urllib.parse import urlparse

def get_taxon_id_from_name(name):
    url = "https://api.inaturalist.org/v1/search"
    params = {"q": name, "sources": "taxa"}
    time.sleep(2.0)  # be respectful to the API
    response = requests.get(url, params=params)
    response.raise_for_status()

    results = response.json().get("results", [])
    if not results:
        return None

    for result in results:
        if result["record"]["rank"] == "species":
            return {
                "common_name": result["record"].get("preferred_common_name"),
                "scientific_name": result["record"].get("name"),
                "taxon_id": result["record"].get("id")
            }

    return None


from pathlib import Path
import os
import time
import requests
from urllib.parse import urlparse

def download_images_for_taxon(taxon_id, common_name, max_images=30, out_dir="dataset", delay=4.0, max_pages=50):
    url = "https://api.inaturalist.org/v1/observations"
    params = {
        "taxon_id": taxon_id,
        "quality_grade": "research", # good quality photos
        "photos": "true",
        "per_page": 50,
        "page": 1
    }

    saved = 0
    Path(f"{out_dir}/{common_name}").mkdir(parents=True, exist_ok=True)

    pages_without_new_photos = 0

    while saved < max_images and params["page"] <= max_pages:
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {common_name}: {e}")
            break

        results = response.json().get("results", [])
        if not results:
            print("No more results. Stopping.")
            break

        images_added_this_page = 0

        for obs in results:
            for i, photo in enumerate(obs.get("photos", [])):
                img_url = photo.get("url")
                if img_url:
                    img_url = img_url.replace("square", "medium")
                    img_name = os.path.basename(urlparse(img_url).path)
                    img_path = f"{out_dir}/{common_name}/{i + images_added_this_page}_{img_name}"

                    if not os.path.exists(img_path):
                        try:
                            img_data = requests.get(img_url).content
                            with open(img_path, "wb") as f:
                                f.write(img_data)
                            saved += 1
                            images_added_this_page += 1
                        except Exception as e:
                            print(f"Failed to download {img_url}: {e}")

                    if saved >= max_images:
                        break
            if saved >= max_images:
                break

        if images_added_this_page == 0:
            pages_without_new_photos += 1
            if pages_without_new_photos >= 3:
                print(f"No new images found in last {pages_without_new_photos} pages. Stopping early.")
                break
        else:
            pages_without_new_photos = 0  # reset if new images were added

        params["page"] += 1
        time.sleep(delay)

    print(f"Downloaded {saved} images for {common_name}")

